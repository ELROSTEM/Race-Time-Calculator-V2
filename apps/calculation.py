from time import sleep

import numpy as np
import pandas as pd
import streamlit as st


def cal_drag_f(area, drag_mu, velocity, fluid_density=1.225):
    """Calculates Drag Force"""
    """The ISA or International Standard Atmosphere states the density of air is 1.225 kg/m3 at sea level and 15 degrees C."""
    Df = area*drag_mu*0.5*fluid_density*(velocity**2)
    return Df

def cal_friction_f(total_mass, friction_mu):
    """Calculates Friction Force"""
    Ff = total_mass/1000*9.81*friction_mu
    return Ff

def app():
    """
    This is the main app function
    """
    #Constant
    interval = 0.0017

    ##############################################################################################
    """Get Data"""
    #Form
    form_dva = st.empty()
    with form_dva.container():
        with st.form(key='form_dva'):
            #Drag
            area = st.number_input("Car Front area (m^2)")
            drag_mu = st.number_input("Drag Coefficient")

            #DVA
            car_mass = st.number_input("Car Mass (g)")
            friction_mu = st.number_input("Friction Coefficient")

            submit = st.form_submit_button(label='Submit')

    try:
        if submit == True:

            #Values can not be zero
            assert(car_mass !=0 and friction_mu !=0), "Can the values be zero 🤔? no."

            #Clear Form
            form_dva.empty()

            with st.spinner('Wait for it...'):
                """Executing code"""
                sleep(1)

                data = {'time(s)': np.arange(0, 2, interval, dtype=float)}
                df = pd.DataFrame(data)

                #Load in datasets
                F_thrust = 'https://raw.githubusercontent.com/Roosevelt-Racers/Race-Time-Calculator-V2/main/data/F-thurst(v1).csv'
                F_thrust = pd.read_csv(F_thrust)

                Co2_mass = 'https://raw.githubusercontent.com/Roosevelt-Racers/Race-Time-Calculator-V2/main/data/Co2-mass(v1).csv'
                Co2_mass = pd.read_csv(Co2_mass)
                
                #Create one dataframe
                df_loaded = pd.merge(F_thrust, Co2_mass , on='time(s)')
                df_loaded = df_loaded.drop(columns="time(s)")
                df = pd.concat([df, df_loaded.reindex(df.index)], axis=1)
                
                #Create total mass as mass
                Co2_empty = Co2_mass['Co2-mass(g)'].iloc[-1] + car_mass
                df['Co2-mass(g)'] = Co2_mass['Co2-mass(g)'] + car_mass
                df = df.rename(columns={"Co2-mass(g)": "mass(g)"})

                #Fill Nan values
                df['mass(g)'] = df['mass(g)'].fillna(Co2_empty)
                df['F-thrust(N)'] = df['F-thrust(N)'].fillna(0)

                #Calculate Friction Force
                df['F-friction(N)'] = [cal_friction_f(total_mass=row,friction_mu=friction_mu) for row in df['mass(g)']]


            ############################################################3
            #Calculate DVA
            
                # #Create the Dataframe
                df_dva = pd.DataFrame(columns=('time(s)', 'F-thrust(N)', 'mass(g)', 'F-friction(N)', 'F-drag(N)', 'F-net(N)', 'acceleration(m/s^2)', 'delta-v(m/s)', 'velocity(m/s)', 'delta-d(m)', 'distance(m)'))
                df_dva.loc[0] = [df.loc[0, 'time(s)'], df.loc[0, 'F-thrust(N)'], df.loc[0, 'mass(g)'], df.loc[0, 'F-friction(N)'], 0, 0, 0, 0, 0, 0, 0]

                index = 1
                while df_dva['distance(m)'].values[-1] < 20:
                    """While the distance is not greater than 20 continue calculating"""

                    # Append the known values
                    df_dva = pd.concat([df_dva, pd.DataFrame({
                        'time(s)': [df.loc[index, 'time(s)']],
                        'F-thrust(N)': [df.loc[index, 'F-thrust(N)']],
                        'mass(g)': [df.loc[index, 'mass(g)']],
                        'F-friction(N)': [df.loc[index, 'F-friction(N)']]
                    })], ignore_index=True)

                    # Read the Drag based off the previous velocity
                    """The problem is here the list is here right beneath the word here """
                    df_dva.loc[index, 'F-drag(N)'] = cal_drag_f(area=area, drag_mu=drag_mu, velocity=df_dva.loc[index-1, 'velocity(m/s)'])

                    # Calculate the Fnet
                    df_dva.loc[index, 'F-net(N)'] = (df_dva.loc[index, 'F-thrust(N)'] - df_dva.loc[index, 'F-friction(N)'] - df_dva.loc[index, 'F-drag(N)'])

                    # Calculate the acceleration
                    df_dva.loc[index, 'acceleration(m/s^2)'] = (df_dva.loc[index, 'F-net(N)'] / df_dva.loc[index, 'mass(g)'] * 1000)

                    # Calculate the delta-velocity
                    df_dva.loc[index, 'delta-v(m/s)'] = (interval * (df_dva.loc[index-1, 'acceleration(m/s^2)'] + df_dva.loc[index, 'acceleration(m/s^2)']) / 2)

                    # Calculate the velocity
                    df_dva.loc[index, 'velocity(m/s)'] = (df_dva.loc[index-1, 'velocity(m/s)'] + df_dva.loc[index, 'delta-v(m/s)'])

                    # Calculate the delta-distance
                    df_dva.loc[index, 'delta-d(m)'] = (interval * (df_dva.loc[index-1, 'velocity(m/s)'] + df_dva.loc[index, 'velocity(m/s)']) / 2)

                    # Calculate the distance
                    df_dva.loc[index, 'distance(m)'] = (df_dva.loc[index-1, 'distance(m)'] + df_dva.loc[index, 'delta-d(m)'])

                    index += 1

            st.success('Done!')


        #---------------------------------------
        # Metric

            top_speed = (df_dva['velocity(m/s)'].max())*(18/5)
            end_time = df_dva['time(s)'].values[-1]

            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Top Speed (km/hr)", round(top_speed, 4))
            metric_col2.metric("End time (sec)", round(end_time, 4))
            # metric_col3.metric("Efficiency", "86%", "4%")

        #---------------------------------------
        #Graphs

            #Acceleration Graph
            acc_dataframe = df_dva[['time(s)', 'acceleration(m/s^2)']]
            st.header('Acceleration Over Time')
            acc_col1, acc_col2 = st.columns([3, 1])
            acc_col1.subheader('Acceleration Over Time Chart')
            acc_col1.line_chart(acc_dataframe.rename(columns={'time(s)':'index'}).set_index('index'))
            acc_col2.subheader('Acceleration DataFrame')
            acc_col2.write(acc_dataframe)
            #Acceleration Expander
            acc_expander = st.expander('What did we do?')
            acc_expander.write("We did these calculation:")
            acc_expander.latex(r'''F_{net} = F_{CO2} – F_{D} – F{f} = (m_{car} + m_{CO2}) a''')

            #Velocity Graph
            v_dataframe = df_dva[['time(s)', 'velocity(m/s)']]
            st.header('Velocity Over Time')
            v_col1, v_col2 = st.columns([3, 1])
            v_col1.subheader('Velocity Over Time Chart')
            v_col1.line_chart(v_dataframe.rename(columns={'time(s)':'index'}).set_index('index'))
            v_col2.subheader('Velocity DataFrame')
            v_col2.write(v_dataframe)
            #Velocity Expander
            v_expander = st.expander('What did we do?')
            v_expander.write("We did these calculation:")
            v_expander.latex(r'''
                v_{n}=\sum_{0}^{n} \frac{\left[a\left(t_{n}\right)+a\left(t_{n+1}\right)\right]}{2} \bullet\left(t_{n+1}-t_{n}\right)
            ''')
            
            #Distance Graph
            d_dataframe = df_dva[['time(s)', 'distance(m)']]
            st.header('Distance Over Time')
            d_col1, d_col2 = st.columns([3, 1])
            d_col1.subheader('Distance Over Time Chart')
            d_col1.line_chart(d_dataframe.rename(columns={'time(s)':'index'}).set_index('index'))
            d_col2.subheader('Distance DataFrame')
            d_col2.write(d_dataframe)
            #Distance Expander
            d_expander = st.expander('What did we do?')
            d_expander.write("We did these calculation:")
            d_expander.latex(r'''
                d_{n}=\sum_{0}^{n} \frac{\left[v\left(t_{n}\right)+v\left(t_{n+1}\right)\right]}{2} \bullet\left(t_{n+1}-t_{n}\right)
            ''')


            st.header("The full data table:")
            st.write(df_dva)

            dva_csv = df_dva.to_csv().encode('utf-8')
            st.download_button(
                label="Download DVA data as CSV",
                data=dva_csv,
                file_name='dva_data.csv',
                mime='text/csv',)



    except Exception as e:
        st.warning(e)


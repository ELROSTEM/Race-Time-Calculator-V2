from time import sleep

import pandas as pd
import streamlit as st

# import calculation_functions as cf


#Friciton Force (Ff)
def cal_friction_f(total_mass, friction_mu):
    """Calculates Friction Force"""
    Ff = total_mass/1000*9.81*friction_mu
    return Ff

#Time generator
def total_time_gen(interval=0.0017):
    """
    Generator that yields number all the way till 2 based on the interval provided

    This generator is used to extend the time(s) in the dataframe so furture calculations
    could be done until the car reaches the finish line.
    """
    time = 0
    while time < 2:
        yield time
        time += interval


def app():


##############################################################################################
    """Calculate Drag"""

    #Form
    form_drag = st.empty()
    with form_drag.container():
        with st.form(key='form_drag'):
            area = st.number_input("Car Front area")
            drag_mu = st.number_input("Drag Coeffecient")
            submit = st.form_submit_button(label='Submit')

    try:
        if submit == True:

            #Values can not be zero
            assert(area !=0 and drag_mu !=0), "The input values can not be zero! 😤"

            #Clear Form
            form_drag.empty()


            # for i in range(101):
            #     st.progress(i)
            #     #Excuting code          #Another way of doing progress
            #     sleep(0.5)
            # st.write("Done")
            with st.spinner('Wait for it...'):
                """Executing code"""
                sleep(1)
                st.write("HOLA")
            
    except Exception as e:
        st.warning(e)
        


##############################################################################################
    """Calculate DVA"""

    #Form
    form_dva = st.empty()
    with form_dva.container():
        with st.form(key='form_dva'):
            car_mass = st.number_input("CarMas")
            friction_mu = st.number_input("Friction Mu")
            submit = st.form_submit_button(label='Submit')

    try:
        if submit == True:

            #Values can not be zero
            assert(car_mass !=0 and friction_mu !=0), "Can the values be zero 🤔? no."

            #Clear Form
            form_dva.empty()


            # for i in range(101):
            #     st.progress(i)
            #     #Excuting code          #Another way of doing progress
            #     sleep(0.5)
            # st.write("Done")
            with st.spinner('Wait for it...'):
                """Executing code"""
                sleep(1)

                data = {'time(s)': list(total_time_gen())}
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

            st.success('Done!')
            st.write(Co2_empty)
            st.write(df)
            st.write(car_mass,friction_mu)

            # df2 = pd.concat([pd.DataFrame([i], columns=['time(s)']) for i in range(5)],
            #   ignore_index=True)


            # df["test"] = total_time_gen()

            # st.write(df)
    except Exception as e:
        st.warning(e)


#     ###############################################################################
#     # Sidebar

#     #Header
#     st.sidebar.header('Race Time Calculator')

#     #---------------------------------------
#     #File upload

#     help_input_csv = """Please upload a CSV File with the required parameters"""

#     #Upload CSV File
#     uploaded_file = st.sidebar.file_uploader(
#         label='Upload Race Time Data', help=help_input_csv)

#     #---------------------------------------
#     #Given inputs

#     #car_mass
#     car_mass = st.sidebar.number_input(
#         label='Car Mass', help="The Car Mass should be the weight of the car in grams")

#     #friction_u or friction coeffe (subject to change as experiments improve)
#     friction_u = st.sidebar.number_input(
#         label='Friction Coeff', help="The friction Coeffecient should be Kinetic")

#     ###############################################################################
#     # Main body

#     st.title("Calculations")

#     #---------------------------------------
#     # Calculations
#     dataframe = pd.read_csv(uploaded_file)

#     #Talkes in all the data and outputs only Time, Total Mass, and Fnet
#     dva_dataframe = cf.dataframe_to_dva(dataframe, car_mass, friction_u)

#     #Calculate accerlation (here cause it can be done in one line)
#     dva_dataframe['Acceleration (a)'] = (dva_dataframe['Fnet']/dva_dataframe['Total Mass'])*1000

#     #Find Continuous
#     dva_dataframe = cf.find_continuous_time(dva_dataframe)

#     #Calculate speed change
#     dva_dataframe = cf.cal_speed_change(dva_dataframe)

#     #Caluculate speed
#     dva_dataframe = cf.cal_speed(dva_dataframe)

#     #Calculate distance change
#     dva_dataframe = cf.cal_distance_change(dva_dataframe)

#     #Caluculate distance
#     dva_dataframe = cf.cal_distance(dva_dataframe)

#     #DVA Columns Only 
#     dva_dataframe = dva_dataframe[['Continuous Time', 'Acceleration (a)', 'Speed (v)', 'Distance (d)']]
#     #Calculating End Time
#     dva_dataframe = dva_dataframe[dva_dataframe['Distance (d)'] <= 20]  

# #---------------------------------------
# # Metric

#     top_speed = (dva_dataframe['Speed (v)'].max())*(18/5)
#     end_time = dva_dataframe['Continuous Time'].values[-1]

#     metric_col1, metric_col2 = st.columns(2)
#     metric_col1.metric("Top Speed (km/hr)", round(top_speed, 4))
#     metric_col2.metric("End time (sec)", round(end_time, 4))
#     # metric_col3.metric("Efficiency", "86%", "4%")

# #---------------------------------------
# #Graphs

#     #Acceleration Graph
#     acc_dataframe = dva_dataframe[['Continuous Time', 'Acceleration (a)']]
#     st.header('Acceleration Over Time')
#     acc_col1, acc_col2 = st.columns([3, 1])
#     acc_col1.subheader('Acceleration Over Time Chart')
#     acc_col1.line_chart(acc_dataframe.rename(columns={'Continuous Time':'index'}).set_index('index'))
#     acc_col2.subheader('Acceleration DataFrame')
#     acc_col2.write(acc_dataframe)

#     #Acceleration Expander
#     acc_expander = st.expander('What did we do?')
#     acc_expander.write("We did these calculation:")
#     acc_expander.latex(r'''F_{net} = F_{CO2} – F_{D} – F{f} = (m_{car} + m_{CO2}) a''')

#     #Velocity Graph
#     v_dataframe = dva_dataframe[['Continuous Time', 'Speed (v)']]
#     st.header('Velocity Over Time')
#     v_col1, v_col2 = st.columns([3, 1])
#     v_col1.subheader('Velocity Over Time Chart')
#     v_col1.line_chart(v_dataframe.rename(columns={'Continuous Time':'index'}).set_index('index'))
#     v_col2.subheader('Velocity DataFrame')
#     v_col2.write(v_dataframe)

#     #Velocity Expander
#     v_expander = st.expander('What did we do?')
#     v_expander.write("We did these calculation:")
#     v_expander.latex(r'''
#         v_{n}=\sum_{0}^{n} \frac{\left[a\left(t_{n}\right)+a\left(t_{n+1}\right)\right]}{2} \bullet\left(t_{n+1}-t_{n}\right)
#     ''')
    
#     #Distance Graph
#     d_dataframe = dva_dataframe[['Continuous Time', 'Distance (d)']]
#     st.header('Distance Over Time')
#     d_col1, d_col2 = st.columns([3, 1])
#     d_col1.subheader('Distance Over Time Chart')
#     d_col1.line_chart(d_dataframe.rename(columns={'Continuous Time':'index'}).set_index('index'))
#     d_col2.subheader('Distance DataFrame')
#     d_col2.write(d_dataframe)

#     d_expander = st.expander('What did we do?')
#     d_expander.write("We did these calculation:")
#     d_expander.latex(r'''
#         d_{n}=\sum_{0}^{n} \frac{\left[v\left(t_{n}\right)+v\left(t_{n+1}\right)\right]}{2} \bullet\left(t_{n+1}-t_{n}\right)
#     ''')


#     dva_dataframe

#     dva_csv = dva_dataframe.to_csv().encode('utf-8')
#     st.download_button(
#         label="Download DVA data as CSV",
#         data=dva_csv,
#         file_name='dva_data.csv',
#         mime='text/csv',)

from time import sleep

import pandas as pd
import streamlit as st

import apps.calculation_functions as cf

# import calculation_functions as cf


def app():

    #Form
    form = st.empty()
    with form.container():
        with st.form(key='my_form'):
            car_mass = st.number_input("CarMas")
            friction_u = st.number_input("Friction U")
            submit = st.form_submit_button(label='Submit')

    if submit:
        form.empty()
        # for i in range(101):
        #     st.progress(i)
        #     #Excuting code          #Another way of doing progress
        #     sleep(0.5)
        # st.write("Done")
        with st.spinner('Wait for it...'):

            """Executing code"""
            sleep(2)

            #Load in datasets
            F_thrust = 'https://raw.githubusercontent.com/Roosevelt-Racers/Race-Time-Calculator-V2/main/data/F-thurst(v1).csv'
            F_thrust = pd.read_csv(F_thrust)

            Co2_mass = 'https://raw.githubusercontent.com/Roosevelt-Racers/Race-Time-Calculator-V2/main/data/Co2-mass(v1).csv'
            Co2_mass = pd.read_csv(Co2_mass)
            
            #Create one dataframe
            df = pd.merge(F_thrust, Co2_mass , on='time(s)')

            #Create total mass as mass
            df['Co2-mass(g)'] = Co2_mass['Co2-mass(g)'] + car_mass
            df = df.rename(columns={"Co2-mass(g)": "mass(g)"})

            #Calculate Friction Force
            df['F-friction(N)'] = [cf.cal_friction_f(total_mass=row,friction_u=friction_u) for row in df['mass(g)']]

        st.success('Done!')
        st.write(df)   
        st.write(car_mass,friction_u)





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

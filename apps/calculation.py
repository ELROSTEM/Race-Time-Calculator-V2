import pandas as pd
import streamlit as st

# import calculation_functions as cf


def app():

    # df = pd.read_csv(r"/data/F-thrust(v1).csv")
    

    # st.write(df)




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

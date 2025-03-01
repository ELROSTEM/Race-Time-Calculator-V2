from time import sleep

import numpy as np
import streamlit as st
import pandas as pd
from scipy.integrate import odeint

"""
All variables are in expressed in SI base units.
"""

def drag(area, drag_mu, velocity, fluid_density  = 1.225):
    """
    The ISA or International Standard Atmosphere states the density of air is 1.225 kg/m3 at sea level and 15 degrees C.
    """
    Df = area*drag_mu*0.5*fluid_density*(velocity**2)
    return Df

def friction(total_mass, friction_mu):
    Ff = total_mass*9.81*friction_mu
    return Ff

def pressure(cartridge_mass, model = 'van der waals'):
    if model == "ideal":
        factor = 3.90e9
        P = factor*cartridge_mass 
    if model == "van der waals":
        # CO2 van der waals constants
        a = 0.364
        b = 0.00004267
        v_m = 1.14e-5*0.04401
        P = -a*((cartridge_mass/v_m)**2)+2436.1485*cartridge_mass/(v_m-b*cartridge_mass)
    else:
        raise Exception("Invalid pressure model.") 
    return P

def thrust(t):
    """
    The equation for thrust is based on experiments where the acceleration of a CO2-canister powered cart was measured. 
    A logistic regression model is applied to velocity data, and the derivative of the model is calculated to produce a thrust curve.
    """
    m_test = 0.561718
    # regression constants
    a = 2.17606
    b = 27.883
    c = -5.03262
    F_t = m_test*(a*b*np.exp(-b*t-c))/(np.exp(-b*t-c)+1)**2
    return F_t

def ssqrt(x):
    return np.sign(x)*np.sqrt(abs(x))

def app():

    form_dva = st.empty()
    with form_dva.container():
        with st.form(key='form_dva'):

            """
            default values based on base car for nationals
                mass = 0.058
                c_d = 0.72936
                frontal_area = 2*0.00112714

            """

            frontal_area = st.number_input(label="Car frontal area (m^2)",min_value=0.,value=2*0.00112714,format='%.8f')
            drag_coeff = st.number_input(label="Drag coefficient",min_value=0.,value=0.72936,format='%.3f')
            car_mass = 0.001*st.number_input(label="Car mass (g)",min_value=0.,value=58.)

            with st.expander('Advanced Options'):
                friction_mu = st.number_input(label="Friction Coefficient", min_value=0.,value=0.)
                radius = st.number_input(label="CO2 exit radius (mm)", min_value=0.7)
                
                st.write("Solver options")
                dt = st.number_input(label="dt",value=0.001,format='%.4f')
                max_time = st.number_input(label="Maximum Time (s)",value=1.5)
                max_distance = st.number_input(label="Maximum Distance (m)",value=20.)
                pressure_model = st.selectbox("Pressure model",("van der waals","ideal"),0)

            submit = st.form_submit_button(label='Submit')

    try:
        if submit == True:
            #Clear Form
            form_dva.empty()

            with st.spinner('Wait for it...'):
                #Executing code
                sleep(1)

                #constants
                v_e = 267. 
                P_a = 101325.
                radius = 0.7
                A_e = np.pi*(radius*0.001)**2

                #kinematic equations
                def car(y, t, c_d, A_f, m_0):
                    mass, xdot, x = y
                    rhoc = (mass - m_0 + 0.008)/1.14e-5
                    ydot = [-A_e*rhoc*min(v_e,ssqrt(2*(pressure(mass - m_0 + 0.008, pressure_model)-P_a)/rhoc)), 
                            (1/mass)*(thrust(t) - drag(frontal_area, c_d, xdot) - friction(mass, friction_mu)), 
                            xdot
                            ]
                    return ydot
                
                #intialize and generate solution
                
                y_0 = [car_mass, 0., 0.]
                time = np.arange(0.,max_time,dt)

                solution = odeint(car, y_0, time, args = (drag_coeff, frontal_area, car_mass))
                
                msol = solution[:, 0]
                vsol = solution[:, 1]
                xsol = solution[:, 2]


                #calculated values
                Fsol = (thrust(time) - drag(frontal_area, drag_coeff, vsol) - friction(msol, friction_mu))
                asol = Fsol/msol

            st.success('Done!')


        #---------------------------------------
        # Metrics

            top_speed = (vsol.max())

            for i, x in enumerate(xsol):
                end_time = time[i]
                if x >= max_distance:
                    break

            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Top Speed (m/s)", round(top_speed, 4))
            metric_col2.metric("Predicted Race time (s)", round(end_time, 4))
            # metric_col3.metric("Efficiency", "86%", "4%")

        #---------------------------------------
        #Graphs
            
            def display_graph(data, label:str, unit:str):
                dataframe = pd.DataFrame(data, index = time, columns=[label+" "+unit])
                st.header(label)
                col1,col2 = st.columns([3,1])
                col1.subheader(label+" Graph")
                col1.line_chart(dataframe, x_label='time (s)', y_label=label+" "+unit)
                col2.subheader(label+" Data")
                col2.write(dataframe)

            display_graph(asol, "Acceleration", "(m/s^2)")
            display_graph(vsol, "Velocity", "(m/s)")
            display_graph(xsol, "Distance", "(m)")
            display_graph(msol, "Mass", "(kg)")
            display_graph(Fsol, "Net Force", "(N)")

            st.header("The full data table:")
            full_table = pd.DataFrame(data={'time (s)':time, 
                                            'distance (m)':xsol,
                                            'velocity (m/s)':vsol,
                                            'acceleration (m/s^2)':asol,
                                            'force (N)':Fsol,
                                            'mass (kg)':msol})
            st.write(full_table)

            dva_csv = full_table.to_csv().encode('utf-8')
            st.download_button(
                label="Download DVA data as CSV",
                data=dva_csv,
                file_name='data.csv',
                mime='text/csv',)



    except Exception as exception:
        st.warning(exception)


from time import sleep

import numpy as np
import streamlit as st
import pandas as pd
import scipy

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
    Ff = total_mass/1000*9.81*friction_mu
    return Ff

def pressure(cartridge_mass, model = 'van_der_waals'):
    if model == "ideal":
        factor = 3.90e9
        P = factor*cartridge_mass 
    if model == "van_der_waals":
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
    """
    This is the main app function
    """
    #Constant
    dt = 0.001

    ##############################################################################################
    """Get Data"""
    #Form
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

            # for now, friction is zero until an Advanced Options tab is implemented
            # friction_mu = st.number_input("Friction Mu")
            friction_mu = 0.

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
                    ydot = [-A_e*rhoc*min(v_e,ssqrt(2*(pressure(mass - m_0 + 0.008)-P_a)/rhoc)), 
                            (1/mass)*(thrust(t) - drag(frontal_area, c_d, xdot) - friction(mass, friction_mu)), 
                            xdot
                            ]
                    return ydot
                
                #intialize and generate solution
                
                y_0 = [car_mass, 0., 0.]
                time = np.arange(0.,1.5,0.001)

                solution = scipy.integrate.odeint(car, y_0, time, args = (drag_coeff, frontal_area, car_mass))
                
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
                if x >= 20:
                    break

            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Top Speed (m/s)", round(top_speed, 4))
            metric_col2.metric("Predicted Race time (s)", round(end_time, 4))
            # metric_col3.metric("Efficiency", "86%", "4%")

        #---------------------------------------
        #Graphs
            
            acc_dataframe = pd.DataFrame(asol, index = time, columns=['acceleration (m/s^2)'])
            v_dataframe = pd.DataFrame(vsol, index = time, columns=['velocity (m/s)'])
            d_dataframe = pd.DataFrame(xsol, index = time, columns=['distance (m)'])

            #Acceleration Graph
            st.header('Acceleration')
            acc_col1, acc_col2 = st.columns([3, 1])

            acc_col1.subheader('a-t Graph')
            acc_col1.line_chart(acc_dataframe, x_label='time (s)', y_label="acceleration (m/s^2)")
            acc_col2.subheader('Acceleration Data')
            acc_col2.write(acc_dataframe)

            #Velocity Graph
            st.header('Velocity')
            v_col1, v_col2 = st.columns([3, 1])

            v_col1.subheader('v-t Graph')
            v_col1.line_chart(v_dataframe, x_label='time (s)', y_label="velocity (m/s)")
            v_col2.subheader('Velocity Data')
            v_col2.write(v_dataframe)
            
            #Distance Graph
            st.header('Distance')
            d_col1, d_col2 = st.columns([3, 1])

            d_col1.subheader('d-t Graph')
            d_col1.line_chart(d_dataframe, x_label='time (s)', y_label="distance (m)")
            d_col2.subheader('Distance Data')
            d_col2.write(d_dataframe)

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


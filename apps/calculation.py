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
    Ff = total_mass/1000*9.81*friction_mu
    return Ff

def pressure(cartridge_mass, model = 'van_der_waals'):
    if model == "ideal":
        factor = 3.90e9
        P = factor*cartridge_mass 
    if model == "van_der_waals":
        canister_vol = 1.14e-5
        # CO2 van der waals constants
        a = 0.364
        b = 0.00004267
        v_m = canister_vol*0.04401/cartridge_mass
        P = (-a/(v_m**2)+2436.1485/(v_m-b))
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
                c_d = 0.7457
                frontal_area = 2*0.001119287

            """

            frontal_area = st.number_input("Car frontal area (m^2)")
            drag_coeff = st.number_input("Drag coefficient")
            car_mass = 0.001*st.number_input("Car mass (g)")

            # for now, friction is zero until an Advanced Options tab is implemented
            # friction_mu = st.number_input("Friction Mu")
            car_mass = 0.058
            drag_coeff = 0.7457
            frontal_area = 2*0.001119287
            friction_mu = 0.

            submit = st.form_submit_button(label='Submit')

    try:
        if submit == True:

            #Values can not be zero
            assert(car_mass !=0), "Can the values be zero 🤔? no."

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
                    ydot = [-(1/v_e)*(thrust(t)+A_e*(pressure(mass - car_mass + 0.008) - P_a)), 
                            (1/mass)*(thrust(t) - drag(frontal_area, c_d, xdot) - friction(mass, friction_mu)), 
                            xdot
                            ]
                    return ydot
                
                #intialize and generate solution
                
                y_0 = [car_mass, 0., 0.]
                time = np.arange(0.,1.5,0.001)

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
                if x >= 20:
                    break

            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Top Speed (m/s)", round(top_speed, 4))
            metric_col2.metric("Race time (sec)", round(end_time, 4))
            # metric_col3.metric("Efficiency", "86%", "4%")

        #---------------------------------------
        #Graphs

            #Acceleration Graph
            acc_dataframe = pd.Series(asol, index = time)
            st.header('Acceleration Over Time')
            acc_col1, acc_col2 = st.columns([3, 1])
            acc_col1.subheader('Acceleration Over Time Chart')
            acc_col1.line_chart(acc_dataframe)
            acc_col2.subheader('Acceleration DataFrame')
            acc_col2.write(acc_dataframe)

            #Acceleration Expander
            acc_expander = st.expander('What did we do?')
            acc_expander.write("We did these calculation:")
            acc_expander.latex(r'''F_{net} = F_{CO2} - F_{D} - F{f} = (m_{car} + m_{CO2}) a''')

            #Velocity Graph
            v_dataframe = vsol
            st.header('Velocity Over Time')
            v_col1, v_col2 = st.columns([3, 1])
            v_col1.subheader('Velocity Over Time Chart')
            v_col1.line_chart(v_dataframe)
            v_col2.subheader('Velocity DataFrame')
            v_col2.write(v_dataframe)

            #Velocity Expander
            v_expander = st.expander('What did we do?')
            v_expander.write("We did these calculation:")
            v_expander.latex(r'''
                v_{n}=\sum_{0}^{n} \frac{\left[a\left(t_{n}\right)+a\left(t_{n+1}\right)\right]}{2} \bullet\left(t_{n+1}-t_{n}\right)
            ''')
            
            #Distance Graph
            d_dataframe = xsol
            st.header('Distance Over Time')
            d_col1, d_col2 = st.columns([3, 1])
            d_col1.subheader('Distance Over Time Chart')
            d_col1.line_chart(d_dataframe)
            d_col2.subheader('Distance DataFrame')
            d_col2.write(d_dataframe)

            #Distance Expander
            d_expander = st.expander('What did we do?')
            d_expander.write("We did these calculation:")
            d_expander.latex(r'''
                d_{n}=\sum_{0}^{n} \frac{\left[v\left(t_{n}\right)+v\left(t_{n+1}\right)\right]}{2} \bullet\left(t_{n+1}-t_{n}\right)
            ''')

            st.header("The full data table:")
            st.write(solution)

            # st.download_button(
            #     label="Download DVA data as CSV",
            #     data=np.array2string(solution),
            #     file_name='data.csv',
            #     mime='text/csv',)



    except Exception as exception:
        st.warning(exception)


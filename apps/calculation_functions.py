import numpy as np
import pandas as pd
from streamlit import cache

###############################################################################
# ^Python standard line length



###############################################################################

#Friciton Force (Ff)
@cache
def cal_friction_f(total_mass, friction_mu):
    """Calculates Friction Force"""
    Ff = total_mass/1000*9.81*friction_mu
    return Ff

###############################################################################

#Net force (Fnet)
@cache
def force_net(force, friction_force, drag_force):
    Fnet = force - friction_force - drag_force
    return Fnet

###############################################################################

#CO2 Mass [will be added to car mass which is give to us]
@cache
def co2_mass(co2_mass):
    return co2_mass

###############################################################################

#Dataframe to Dva Dataframe
@cache(allow_output_mutation=True)# <-- idk why I need to put this do more research
def dataframe_to_dva(dataframe, car_mass, friction_u):
    """Returns a dva_dataframe ready for the dva to be calculated. It takes in all the
    data from the inputed CSV file and outputs only Time, total mass, and Fnet over time
    """
    
    #Get Total Mass
    dataframe["Total Mass"] = dataframe["CO2 Mass (Mco2)"] + car_mass
    
    #Get Friction_u (subject to change cause friction coeffe changes)
    dataframe["Friction Coeffe (u)"] = friction_u

    #Get Friction Force (Ff)
    dataframe["Friction Force (Ff)"] = friction_f(dataframe["Total Mass"], dataframe["Friction Coeffe (u)"])

    #Get Force net (Fnet)
    dataframe["Fnet"] = force_net(dataframe["Force (N)"], dataframe["Friction Force (Ff)"], dataframe["Drag (FD)"])

    #---------------------------------------
    #dva Calculationsi

    #Create DataFrame
    dva_dataframe = dataframe[["Time (s)", "Total Mass", "Fnet"]]

    #Replace all negative with 0 (for covinence at this moment)
    dva_dataframe[dva_dataframe < 0] = 0

    # Find where to start
    for index,row in dva_dataframe.iterrows():
        if row['Fnet'] > 0:
            # row_above = dva_dataframe.iloc[[index-1]]
            # row_above_diff = 0-row_above['Fnet']
            # row_diff = 0-row['Fnet']
            # if abs(row_above_diff) < abs(row_diff):
            #     dva_dataframe = dva_dataframe.iloc[index-1:]
            #     break
            dva_dataframe = dva_dataframe.iloc[index:]
            break
    dva_dataframe = dva_dataframe.reset_index(drop=True)

    return dva_dataframe


###############################################################################
#Calculate Continuous Time
@cache
def find_continuous_time(dva_dataframe):
    
    sec = []
    for index,row in dva_dataframe.iterrows(): # <- index is not being used which makes it waste memory but if remove index variable row is not created
        first_row = dva_dataframe.iloc[[0]]
        sec.append(row['Time (s)'] - first_row['Time (s)'])
    df = pd.concat(sec).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    # dva_dataframe = dva_dataframe.iloc[: , 1:]
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Continuous Time'], axis=1, inplace=False)
    return dva_dataframe

###############################################################################
#Acceleration (a)

#---------------------------------------
#Speed Change (delta v)  [Calculated using acceleration]
@cache
def cal_speed_change(dva_dataframe):
    ser = pd.Series({0:0}, name='Speed Change (delta v)')
    delta_v = []
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        if index == 0:
            row_above['Acceleration (a)'] = 0
        delta_v.append((row['Time (s)'] - row_above['Time (s)'])*(row_above['Acceleration (a)']+row['Acceleration (a)'])/2)
    delta_v[0] = ser
    df = pd.concat(delta_v).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Speed Change (delta v)'], axis=1, inplace=False)
    # dva_dataframe = dva_dataframe[:-1]
    return dva_dataframe

###############################################################################

#Speed (v)   [Calculated using delta v]
@cache
def cal_speed(dva_dataframe):
    ser = pd.Series({0:0}, name='Speed (v)')
    v = [ser]
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        v.append(v[-1]+row['Speed Change (delta v)'])
    del v[0]
    df = pd.concat(v).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Speed (v)'], axis=1, inplace=False)
    return dva_dataframe
#---------------------------------------
#distance change (delta d) [calculated using speed]
@cache
def cal_distance_change(dva_dataframe):
    ser = pd.Series({0:0}, name='Distance Change (delta d)')
    delta_d = []
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        delta_d.append((row['Time (s)'] - row_above['Time (s)'])*(row_above['Speed (v)']+row['Speed (v)'])/2)
    delta_d[0] = ser
    df = pd.concat(delta_d).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Distance Change (delta d)'], axis=1, inplace=False)
    return dva_dataframe

###############################################################################

#distance (d)  [calculated using delta d]
@cache
def cal_distance(dva_dataframe):
    ser = pd.Series({0:0}, name='Distance (d)')
    d = [ser]
    for index, row in dva_dataframe.iterrows():
        row_above = dva_dataframe.iloc[[index-1]]
        d.append(d[-1]+row['Distance Change (delta d)'])
    del d[0]
    df = pd.concat(d).reset_index(drop=True)
    dva_dataframe = pd.concat([dva_dataframe, df], axis=1)
    dva_dataframe = dva_dataframe.set_axis([*dva_dataframe.columns[:-1], 'Distance (d)'], axis=1, inplace=False)
    return dva_dataframe


###############################################################################



#d-t, v-t, a-t calculator
def calculate_dva_t(dataframe):
    """This function calculates the v-t and a-t using the d-t table"""
    # get differences for time values
    count_t_vals = dataframe['time'].values
    diffs_t = count_t_vals[:-1] - count_t_vals[1:]

    # get differences for displacement values
    count_d_vals = dataframe['displacement'].values
    diffs_d = count_d_vals[:-1] - count_d_vals[1:] 

    # create velocity column and calculte it
    velocity = diffs_d / diffs_t
    dataframe['velocity']= np.insert(velocity,0,0)

    # calculate difference in velocity
    count_v_vals = dataframe['velocity'].values
    diffs_v = count_v_vals[:-1] - count_v_vals[1:]
    diffs_v=np.round(diffs_v,1)

    # calculate accelertaion
    accel= diffs_v / diffs_t
    dataframe['acceleration']=np.append(accel,0)
    return dataframe


###############################################################################


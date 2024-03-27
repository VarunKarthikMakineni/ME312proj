import math
import csv
import pyomo.environ as pyo
import numpy as np

G = 6.67e-11
M = 5.97e24

# DELTA-V REQUIRED TO CHANGE THE ORBIT OF SATELLITE IN TWO BURNS
def deltav_radius_change( initial_radius , final_radius ):

    delta_v1 = math.sqrt( G * M / initial_radius )*(math.sqrt( 2 * final_radius / ( initial_radius + final_radius )) - 1 )
    delta_v2 = math.sqrt( G * M / final_radius )*( 1 - math.sqrt( 2 * initial_radius / ( initial_radius + final_radius )))

    deltav_total = abs(delta_v1) + abs(delta_v2)

    return deltav_total

# DELTA-V REQUIRED TO CHANGE THE INCLINATION OF A CIRCULAR ORBIT
def deltav_inclination_change( initial_inclination , final_inclination , orbtital_radius):

    orbital_velocity =  math.sqrt( G * M / orbtital_radius )

    deltav_total = 2 * orbital_velocity * math.sin( abs( initial_inclination - final_inclination ) / 2)

    return deltav_total

# DELTA-V REQUIRED FOR HOHHMAN TRANSFER TO FIRST CHANGE INCLINATION, THEN CHANGE RADIUS
def hohhman_transfer( initial_radius , initial_inclination , final_radius , final_inclination ):

    deltav_inclin = deltav_inclination_change( initial_inclination , final_inclination , initial_radius )
    deltav_rad = deltav_radius_change( initial_radius , final_radius )

    deltav_total = deltav_inclin + deltav_rad

    return deltav_total

# GENERATES A LOOK UP TABLE THAT CONTAINS THE DELTA V REQUIRED TO MANEUVER BETWEEN ORBITS OF DIFFERENT SATELLITES
def deltav_lut( input_dict ):
    
    payloads = list(input_dict.keys())
    num_payloads = len(payloads)
    deltav_lookup_table = {}

    for i in range(num_payloads):
        for j in range(i,num_payloads):

            
            deltav_lookup_table[(payloads[i],payloads[j])] = \
                deltav_lookup_table[(payloads[j],payloads[i])] = hohhman_transfer(input_dict[payloads[i]]["radius"], 
                                                                         input_dict[payloads[i]]["inclination"],
                                                                         input_dict[payloads[j]]["radius"],
                                                                         input_dict[payloads[j]]["inclination"])
            
    return deltav_lookup_table

# LOADS THE DATA ABOUT PAYLOADS FROM A CSV FILE
def load_input_file(filename):

    with open(filename,"r") as f:

        csv_reader = csv.reader(f)

        # DROP THE HEADER LINE
        for row in csv_reader:
            break

        # CREATE LIST TO STORE DATA AND ADD INITIAL ORBIT
        payloads = {}
        initial_orbit = { "initial_orbit" : { "mass" : 0 , "radius" : (6371e3+50e3) , "inclination" : 0 } }
        
        # READ DATA INTO THE LIST
        for row in csv_reader:

            pid = row[0]
            mass = float(row[1])
            orbit_radius = float(row[2])
            orbit_inclination = float(row[3])
            
            payloads[pid] = { "mass" : mass , "radius" : orbit_radius , "inclination" : orbit_inclination }

            # yield tuples
            # yield pyo.Set.End
        return initial_orbit , payloads

# LOADS THE DATA ABOUT LAUNCH VEHICLES FROM A CSV FILE
def load_lvs(filename):

    with open(filename,"r") as f:

        csv_reader = csv.reader(f)

        # DROP THE HEADER LINE
        for row in csv_reader:
            break

        # CREATE LIST TO STORE DATA AND ADD INITIAL ORBIT
        lvs = {}
        
        # READ DATA INTO THE LIST
        for row in csv_reader:

            num = row[0]
            mass_limit = float(row[1])
            deltav_limit = float(row[2])
            cost_to_launch = float(row[3])
            
            lvs[num] = { "mass_limit" : mass_limit , "deltav_limit" : deltav_limit , "cost_to_launch" : cost_to_launch }

        return lvs

def zero(*args):
    return 0

def dezero( x ):

    new = []

    for i in x:
        if i != 0:
            new.append(i)

    return new
import pyomo.environ as pyo
import tools,constraints,results
import time

model = pyo.ConcreteModel()

input_file_name = "randinp.csv"
lv_file_name = "lvs.csv"

# READ THE INPUT FROM FILE
# THE INPUT DATA CONTAINS THE ID, MASS, ORBITAL RADIUS AND INCLINATION FOR EACH PAYLOAD
model.initial_orbits , model.input = tools.load_input_file(input_file_name)
model.available_lvs = tools.load_lvs(lv_file_name)

model.payloads = pyo.Set(initialize=model.input.keys()) #LIST OF PAYLOAD IDs FOR INDEXING
model.launch_vehicles = pyo.RangeSet(1,len(model.input)) # LIST OF LAUNCH VEHCILE NUMBERS FOR INDEXING
model.deltav_matrix = tools.deltav_lut(model.input | model.initial_orbits)   # GET CALCULATED DELTA-V FOR THE INPUT
model.delta_v_limit = 15000 # m/s
model.mass_limit = 500 # kg


######################## VARIABLES ########################
model.is_lv_active = pyo.Var( model.launch_vehicles , domain=pyo.Binary ) # BINARY, 1 IF LV IS BEING USED
model.lv_type = pyo.Var( model.launch_vehicles , domain = pyo.PositiveIntegers , bounds = (0,len(model.available_lvs)) )
model.launch_order = pyo.Var( model.launch_vehicles , model.payloads , model.payloads , domain = pyo.Binary ) # i,j,k. 1 if j launches after k on i
model.initial_payload = pyo.Var( model.launch_vehicles , model.payloads , domain = pyo.Binary ) # 1 IF PAYLOAD IS THE FIRST SATELLITE AFTER INITIAL ORBIT
model.payload_hierarchy = pyo.Var( model.payloads , domain=pyo.RangeSet(1,len(model.input)) )


######################## OBJECTIVE ########################

# MINIMISE THE NUMBER OF ACTIVE LVs
model.obj = pyo.Objective( expr = sum( [model.is_lv_active[lv] for lv in model.launch_vehicles] ) , sense=pyo.minimize )

####################### CONSTRAINTS #######################

# EACH PAYLOAD SHOULD BE IN EXACTLY ONE LAUNCH VEHICLE, AFTER ONE OTHER PAYLOAD OR IN THE INITIAL POSITION
model.cons1 = pyo.Constraint( model.payloads , rule = constraints.cons1 )

# A PAYLOAD CAN BE FOLLOWED BY ONLY ONE PAYLOAD
model.cons2 = pyo.Constraint( model.launch_vehicles , model.payloads , rule = constraints.cons2 )

# A PAYLOAD CAN'T BE LAUNCHED AFTER ITSELF
model.cons3 = pyo.Constraint( model.payloads , rule = constraints.cons3 )

# IF A PAYLOAD IS BEING LAUNCHED AFTER ANOTHER PAYLOAD, THE OTHER PAYLOAD SHOULD BE ON THE SAME VEHICLE
model.cons4 = pyo.Constraint( model.launch_vehicles , model.payloads , model.payloads , rule = constraints.cons4 )

# ONLY ONE PAYLOAD AFTER INTIAL ORBIT IF LV IS ACTIVE
model.cons5 = pyo.Constraint( model.launch_vehicles , rule=constraints.cons5 )

# ONLY ACTIVE LAUNCH VEHICLES CAN HAVE PAYLOAD
model.cons6 = pyo.Constraint( model.launch_vehicles , rule=constraints.cons6 )

# "SUBTOUR" ELIMINATION FOR THE PAYLOADS
model.cons7 = pyo.Constraint( model.launch_vehicles , model.payloads , model.payloads , rule = constraints.cons7 )

# TOTAL DELTA-V SHOULD'NT EXCEED LIMITATION
model.cons8 = pyo.Constraint( model.launch_vehicles , rule = constraints.cons8 )

# TOTAL MASS SHOULD'NT EXCEED LIMITATION
model.cons9 = pyo.Constraint( model.launch_vehicles , rule = constraints.cons9 )

# model.pprint()


# SOLVE THE PROBLEM USING CBC

# solver = pyo.SolverFactory("cbc", executable = "D:\\Coursework\\ME312\\Cbc-releases.2.10.11-w64-msvc17-md\\bin\\cbc.exe")
solver = pyo.SolverFactory("cbc")

print("\nSolving the model....\n")
start_time = time.time()
result = solver.solve(model)
end_time = time.time()
# print(result)

# model.launch_order.pprint()
# model.initial_payload.pprint()
# model.payload_hierarchy.pprint()

active_lvs = results.active_lvs( model , disp = True )

for l in active_lvs:
    _ = results.stacking_sequence(model,l,disp=True)

print("Solution Time: "+str(end_time-start_time))
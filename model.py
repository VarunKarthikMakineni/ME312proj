import pyomo.environ as pyo
import tools,constraints

model = pyo.ConcreteModel()

input_file_name = "inp.csv"

# READ THE INPUT FROM FILE
# THE INPUT DATA CONTAINS THE ID, MASS, ORBITAL RADIUS AND INCLINATION FOR EACH PAYLOAD
model.initial_orbits , model.input = tools.load_input_file(input_file_name)


model.payloads = pyo.Set(initialize=model.input.keys()) #LIST OF PAYLOAD IDs FOR INDEXING
model.launch_vehicles = pyo.RangeSet(1,len(model.input)) # LIST OF LAUNCH VEHCILE NUMBERS FOR INDEXING
model.deltav_matrix = tools.deltav_lut(model.input | model.initial_orbits)   # GET CALCULATED DELTA-V FOR THE INPUT


######################## VARIABLES ########################
model.is_lv_active = pyo.Var( model.launch_vehicles , domain=pyo.Binary ) # BINARY, 1 IF LV IS BEING USED
model.launch_order = pyo.Var( model.launch_vehicles , model.payloads , model.payloads , domain = pyo.Binary ) # i,j,k. 1 if j launches after k on i
model.initial_payload = pyo.Var( model.launch_vehicles , model.payloads , domain = pyo.Binary ) # 1 IF PAYLOAD IS THE FIRST SATELLITE AFTER INITIAL ORBIT


######################## OBJECTIVE ########################

# MINIMISE THE NUMBER OF ACTIVE LVs
model.obj = pyo.Objective( expr = sum( [model.is_lv_active[lv] for lv in model.launch_vehicles] ) , sense=pyo.minimize )

####################### CONSTRAINTS #######################

# EACH PAYLOAD SHOULD BE IN EXACTLY ONE LAUNCH VEHICLE, AFTER ONE OTHER PAYLOAD OR IN THE INITIAL POSITION
model.cons1 = pyo.Constraint( model.payloads , rule = constraints.cons1 )

# A PAYLOAD CAN'T BE LAUNCHED AFTER ITSELF
model.cons2 = pyo.Constraint( model.payloads , rule = constraints.cons2 )

# IF A PAYLOAD IS BEING LAUNCHED AFTER ANOTHER PAYLOAD, THE OTHER PAYLOAD SHOULD BE ON THE SAME VEHICLE
model.cons3 = pyo.Constraint( model.launch_vehicles , model.payloads , model.payloads , rule = constraints.cons3 )

# ONLY ONE PAYLOAD AFTER INTIAL ORBIT IF LV IS ACTIVE
model.cons4 = pyo.Constraint( model.launch_vehicles , rule=constraints.cons4 )

# ONLY ACTIVE LAUNCH VEHICLES CAN HAVE PAYLOAD
model.cons5 = pyo.Constraint( model.launch_vehicles , rule=constraints.cons5 )

# TOTAL DELTA-V SHOULD'NT EXCEED LIMITATION

model.pprint()


# SOLVE THE PROBLEM USING CBC

solver = pyo.SolverFactory("cbc", executable = "D:\\Coursework\\ME312\\Cbc-releases.2.10.11-w64-msvc17-md\\bin\\cbc.exe")
result = solver.solve(model)
print(result)

model.launch_order.pprint()
model.initial_payload.pprint()
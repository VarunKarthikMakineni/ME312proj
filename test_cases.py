import pyomo.environ as pyo
import constraints

model = pyo.ConcreteModel()

model.payloads = ["101","102","103"]
model.launch_vehicles = ["1","2","3"]

model.is_lv_active = {}
model.launch_order = {}
model.initial_payload = {}

for lv in model.launch_vehicles:
    for pd1 in model.payloads:
        for pd2 in model.payloads:
            model.launch_order[(lv,pd1,pd2)] = 0
        model.initial_payload[(lv,pd1)] = 0

model.is_lv_active["1"] = 1
model.launch_order[("1","101","102")] = 1
model.launch_order[("1","102","103")] = 1
model.initial_payload[("1","103")] = 1

# c1 = c2 = c3 = c4 = c5 = False

for lv in model.launch_vehicles:
    for pd1 in model.payloads:
        for pd2 in model.payloads:
            pass
        model.initial_payload[(lv,pd1)] = 0
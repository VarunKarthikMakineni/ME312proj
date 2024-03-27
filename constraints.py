import pyomo.environ as pyo

M = 100  ## WARNING!!!!! MAKE THIS NUMBER BIGGER THAN NUMBER OF SATELLITES INPUT

def cons1( model , pd ):

    num_follow_deploys = sum( [ model.launch_order[lv,pd,x] for x in model.payloads for lv in model.launch_vehicles] )
    num_initial_deploys = sum( [ model.initial_payload[lv,pd] for lv in model.launch_vehicles ] )

    return ( num_follow_deploys + num_initial_deploys ) == 1

def cons2( model , lv , pd ):

    return sum( [ model.launch_order[lv,pd_it,pd] for pd_it in model.payloads ] ) <= 1
    
def cons3( model , pd ):

    return sum( [ model.launch_order[lv,pd,pd] for lv in model.launch_vehicles] ) <= 0

def cons4( model , lv , pd_following , pd ):

    num_launches_pd = sum( [ model.launch_order[lv,pd,prev_payload] for prev_payload in model.payloads ] ) \
                                 + sum( [ model.initial_payload[lv,pd] ] )
    
    pd_following_after_pd = sum( [ model.launch_order[lv,pd_following,pd] ])
    
    return pd_following_after_pd <= num_launches_pd

def cons5( model , lv ):

    return sum( [ model.initial_payload[lv,pd] for pd in model.payloads ] ) == sum( [ model.is_lv_active[lv] ] )

def cons6( model , lv ):

    num_launches_on_lv =  sum( [ model.launch_order[lv,pd1,pd2] for pd1 in model.payloads for pd2 in model.payloads ] \
              + [ model.initial_payload[lv,pd] for pd in model.payloads ] )
    
    lv_active = sum( [ model.is_lv_active[lv] ] )      # EITHER 1 OR 0

    return num_launches_on_lv <= lv_active * M

def cons7( model , lv , pd1 , pd2 ):

    return model.payload_hierarchy[pd1] - model.payload_hierarchy[pd2] >= 1 - M*(1-model.launch_order[lv,pd1,pd2])

def cons8( model , lv ):

    total_dv = 0

    for pd1 in model.payloads:
        for pd2 in model.payloads:

            total_dv = total_dv + model.launch_order[lv,pd1,pd2] * model.deltav_matrix[pd2,pd1]

        total_dv = total_dv + model.initial_payload[lv,pd1]*model.deltav_matrix["initial_orbit",pd1]
    
    return total_dv <= model.delta_v_limit

def cons9( model , lv ):

    total_mass = 0

    for pd1 in model.payloads:
        for pd2 in model.payloads:

            total_mass = total_mass + model.launch_order[lv,pd1,pd2] * model.input[pd1]["mass"]

        total_mass = total_mass + model.initial_payload[lv,pd1] * model.input[pd1]["mass"]
    # print(total_dv)
    return total_mass <= model.mass_limit

def is_subtour( model , pd ):
    
    pass
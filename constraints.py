import pyomo.environ as pyo

def cons1( model , pd ):

    num_follow_deploys = sum( [ model.launch_order[lv,pd,x] for x in model.payloads for lv in model.launch_vehicles] )
    num_initial_deploys = sum( [ model.initial_payload[lv,pd] for lv in model.launch_vehicles ] )

    return ( num_follow_deploys + num_initial_deploys ) == 1
    
def cons2( model , pd ):

    return sum( [ model.launch_order[lv,pd,pd] for lv in model.launch_vehicles] ) <= 0

def cons3( model , lv , pd_following , pd ):

    num_launches_pd = sum( [ model.launch_order[lv,pd,prev_payload] for prev_payload in model.payloads ] ) \
                                 + sum( [ model.initial_payload[lv,pd] ] )
    
    pd_following_after_pd = sum( [ model.launch_order[lv,pd_following,pd] ])
    
    return pd_following_after_pd <= num_launches_pd

def cons4( model , lv ):

    return sum( [ model.initial_payload[lv,pd] for pd in model.payloads ] ) == sum( [ model.is_lv_active[lv] ] )

def cons5( model , lv ):

    return sum( [ model.launch_order[lv,pd1,pd2] for pd1 in model.payloads for pd2 in model.payloads ] \
              + [ model.initial_payload[lv,pd] for pd in model.payloads ] ) <= sum( [ model.is_lv_active[lv] ] ) 
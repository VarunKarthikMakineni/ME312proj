import tools

def active_lvs( model , disp = False ):

    if disp:
        print("The following launch vehicles are being used")

    active = []
    for lv in model.launch_vehicles:
        if model.is_lv_active[lv].value:
            active.append(lv)
            if disp:
                print(lv)
    
    return active

def stacking_sequence( model , lv , disp = False):

    if disp:
        print("Stacking sequence on vehicle "+str(lv))

    seq = [0]*len(model.payloads)
    intl_pd = 0

    for i in model.payloads:
        for j in model.payloads:
            if model.launch_order[lv,i,j].value:
                seq[int(model.payload_hierarchy[j].value)] = i

        if model.initial_payload[lv,i].value:
            intl_pd = i
    
    seq = [intl_pd]+seq
    seq = tools.dezero(seq)

    if disp:
        for pd in seq:
            print(pd)

    return seq
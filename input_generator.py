import random
import csv

FILENAME = "randinp.csv"

RAD_RANGE = (6371000+70000,6371000+250000)
INCL_RANGE = (0*3.1415/180,90*3.1415/180)

MASS_RANGE = (20,300)

NUM_PAYLOADS = 8

print("\nGenerating random paylaods....")

payloads = []
for i in range(NUM_PAYLOADS):

    pid = str(101+i)
    mass = random.randint(*MASS_RANGE)
    rad = random.randint(*RAD_RANGE)
    incl = random.random()*(INCL_RANGE[1]-INCL_RANGE[0])+INCL_RANGE[0]
    payloads.append((pid,mass,rad,incl))

with open(FILENAME,"w") as inp_file:
    
    print("\n Writing to "+FILENAME+".....")
    writer = csv.writer(inp_file)
    writer.writerow(("Payload ID","Mass","Target_radius","Target_inclination"))

    for pd in payloads:
        writer.writerow(pd)

print("\nInput file generated.")
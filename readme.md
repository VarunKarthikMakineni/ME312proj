# Week 1

This code is a basic model of the problem with suggestions from Prof. Avinash about linearisation.
Features are listed below.

## On the problem 
1. This is probably a mixture of a **Bin Packing Problem** and a **Multiple Travelling Salesmen Problem**.

2. Bin Packing Problem involves using the least number of bins to pack items. This problem is similar because we have to use the least number of launch vehicles required. However in a bin packing problem, the size or 'cost' of each of the items is fixed. Here, it depends on the order in which they are launched on the same launch vehicle.

3. Multiple Travelling Salesmen Problem involves having multiple salesmen cover each node in a graph. This problem is similar because the order in which they cover the graph decides the total distance travelled, but we have to minimise the number of 'salesmen' and each of them has a limit on how much they can travel

## Approaches Tried
1. One of the first approaches was to try it to solve like a bin packing problem by assigning payloads to each launch vehicle. But in that case, the order in which they are launched on that vehicle was not known, so the total propellant required could not be calculated.

## Current Approach
1. Try to solve it like the bin packing problem, but add a third dimension which is the order in which they are launched.

2. The number of launch vehicles taken is equal to the number of payloads because that may be the worst case possible scenario. If we need less launch vehicles we can simply not use some of them. This is worse (?) than the previous approach because it uses more variables but it will enable us to track the payloads going on each of the vehicles individually.

3. A condition is that all launch vehicles put them in the same initial orbit, and the payloads are carried from there for deployment.

## Variables Used
1. A variable to keep track of which launch vehicles are being used. This can be used to formulate the objective function.

2. A variable that keeps track of the order in which payloads are being launched.

3. A variable that keeps track of which payload is being deployed after the initial orbit. This is because in the current approach, this payload won't fit into the above variable because this is not being deployed *after* another payload

4. A matrix that is a look-up table for finding the delta-V to go between any two orbits. This is to linearise the problem and not bring the non-linear equations into the problem.

5. Sets containing names of payloads and launch vehicles that are required for indexing while applying constraints.

## Objective Function

1. Use the variable that keeps track of active launch vehicles, an minimise it

## Constraints

1. Each payload should be in only one launch vehicle, and should be deployed after one other payload (or) it should be the first payload to be deployed on that vehicle

2. A payload can't be launched after itself

3. If a payload is being launched after another payload, the other payload should also be on this vehicle

4. Only one payload has to be deployed after the initial orbit, if the launch vehicle is active

5. Only active launch vehicles can have a payload. Without this constraints, we can use 0 launch vehicles to launch all payloads.

6. Total delta-V required should be within the capability of the launch vehicle. THIS HAS NOT BEEN IMPLEMENTED IN CODE YET because the solution obtained right now should be that all payloads can be launched on the same launch vehcile. Once this desired solution is obtained, we can start adding other constraints regarding mass, propellant, etc.
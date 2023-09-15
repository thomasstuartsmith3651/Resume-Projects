Thermodynamics Snookered Guide

ballGeneration.py:
-generates balls at random positions and velocities anywhere in the container
- by typing desired initial values of speed, ball radius and number of balls into 
the __init__ function this variables in the simulation can be changed freely
- in order to ensure smooth running of the simulation:
any velocity can be used but the ball radius for 20 particles is limited at 1/25 the container
radius to ensure all collisions are recorded

containerGeneration.py:
-generates container of fixed position
-radius of container can be varied in __init__

Simulation.py:
-number of collisions can be varied by changing noCollisions in __init__ function
-typically 100 collisions does not take too long but 1000 collisions does take minutes
 and was used for the majority of plots
-runs simulation and collects data necessary for the analysis

plots.py:
-where the code will be run
-contains data analysis functions - well labelled in order of tasks
-as data analysis functions are not contained in a class the functions have to be run at the bottom of the plots.py file
-to run the simulation type run(1) as initialisation is already prepared

testingCode.py
-tests initialisation of particles, timeTocollision function, collide function and nextColllision function.
-all functions can be run at the bottom of the file

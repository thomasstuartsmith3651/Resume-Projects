CHARGED PARTICLE SIMULATION GUIDE

HOW THE CODE WORKS
    ballGeneration.py
    -generates balls used in the simulation in random positions within the container (contains Particles class)
    -here the desired number of balls, ball charges, ball velocity distributions can be changed and initialised

    containerGeneration.py
    -contains Container class which generates container of specified radius (mass is irrelevant but set to high number to show immovability)

    ball.py
    -contains the class ball which has the functions move, collide and electrostatic
    -these functions are all called in the simulation
    - works on object classes (Particles and Container)

    Simulation.py
    - contains simulation class which runs simuilation
    - creates a list of particles and components that can then be called to run ball functions when necessary
    - the main operative function is the intervalRunning function that uses a while loop to move simulation forward an interval at a time
    - during each interval components are check to be overlapping or about to overlap in the next interval and collided.
    - the electrostatic function is run between each particle and each particle is then moved according to the move function
    - the run function then generates the figure using the central position of each particle found during intervalRunning


RUNNING THE CODE
    run.py
    - by running run.py the simulation is executed
    - the positive charges are blue with '+' hatching and the negative charges are red with '-' hatching
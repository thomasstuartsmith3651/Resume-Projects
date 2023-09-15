from ball import ball
from containerGeneration import Container
from ballGeneration import Particles
from Simulation import Simulation
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy.optimize import curve_fit
import scipy.stats as stats


''' 
RUNNING SIMULATION
-generates particles and adds them to the simulation
-adds container
-runs the simulation
'''
''' 
run plots below, initialisation and running kept separate and not run as one function for flexibility
'''
def runCode():

        parts = Particles()
        con = Container()
        parts.randomPositions()
        parts.randomVelocities()
        parts.chargeDist()
        sim = Simulation()
        sim.addParticles()
        sim.addContainer()
        sim.run(1)

runCode()
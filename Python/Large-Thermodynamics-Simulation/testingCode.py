import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from ballGeneration import Particles
from containerGeneration import Container
from Simulation import Simulation
from ball import ball



'''
Checking Initial Position Generation
'''

def positionAnimate():
    ''' 
    Able to generate 45 balls of radius 1 in container radius 10 consistently in under 8s
    '''

    parts = Particles()
    
    f = pl.figure()
    
    containerPatch = pl.Circle([0., 0.], 10, ec='g', fill=False, ls='solid')
    ax = pl.axes(xlim=(-10, 10), ylim=(-10, 10))
    ax.add_patch(containerPatch)
                
    for i in range(parts.count):
        
        ballPatch = pl.Circle((parts.positions[i]), parts.radius, ec='g', fill=True, ls='solid')
        ax.add_patch(ballPatch)
    pl.show()
    
'''
Checking Initial Velocity Distribution
'''

def initialVelocitydistributionForgaussian():
    parts = Particles()
    plt.hist(parts.xVelocities,bins = 20)
    plt.hist(parts.yVelocities,bins = 20)
    plt.xlabel('Velocity')
    plt.ylabel('Number')
    plt.show()

''' 
Checking timeTocollision function by comparing output with paper calculation
'''

def timeTocollisionTest():
    #ballcollisions
    con = Container()
    ball1 = ball(1,1,(-1,0),(1,0))
    ball2 = ball(1,1,(5,0),(0.5,0))
    ball1.timeTocollision(ball2)
    print(ball1.timeTocollision(ball2))
    #containercollisions
    ball2.timeTocollision(con)
    print(ball1.timeTocollision(con))


def collideCheck():
    con = Container()
    ball1 = ball(1,1,(9,0),(5,1))
    ball2 = ball(1,1,(5,0),(3,2))
    ball1.collide(ball2)
    print(ball1.velocity,ball2.velocity)
    ball1.collide(con)
    print(ball1.velocity)


def testNextcollision():
    sim = Simulation()
    parts = Particles()
    parts.randomPositions()
    parts.randomVelocities()

    sim.addParticles()
    sim.addContainer()

    sim.nextCollision()
    
    plt.hist(sim.posMagnitude,bins=15)
    plt.show()
    plt.hist(sim.separationMagnitude,bins=15)
    plt.show()
    #check updated simulation arrays
    print('time',sim.time,'plottime',sim.plotTime,
    'totalmomentum',sim.totalMomentum,'totalKE',sim.totalKE,'currentpressure',sim.pressurePlot,'velocitiesmagnitudes',sim.velocityMagnitudes)




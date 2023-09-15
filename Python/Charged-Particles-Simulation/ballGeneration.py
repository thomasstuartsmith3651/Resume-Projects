import numpy as np 
import scipy as sp
import pylab as pl
from scipy.stats import rayleigh
import random as rand
from containerGeneration import Container

class Particles():
    ''' 
    produces particles of variable number, speed and radius

    '''

    def __init__(self,radius = 1, mass=1, vMu=0,number=3):
        self.radius = radius
        self.count = number
        self.vMu = vMu
        self.vStd = vMu/(5.0)
        self.balls = []
        
        self.mass = mass

        self.positions = self.randomPositions()
        self.velocities = self.randomVelocities()
        self.charges = self.chargeDist()
        
    ''' 
    PARTICLE CLASS INFORMATION
    '''    
    
    def __repr__(self):
        return ('radius={self.radius},number={self.count},velocity={self.vMu},velocitystDev = {self.vStd},positions={self.positions},velocities={self.velocities}')

    def __str__(self):
        return ('r={self.radius},n={self.count},v={self.vMu},dev = {self.vStd},p={self.positions},v={self.velocities}')

    def chargeDist(self):
        charges = []
        for i in range(self.count):
            charge = rand.choice([-1.6e-19,1.6e-19])
            charges.append(charge)
        
        return charges
            

    def randomPositions(self):
        con = Container()
        positions = []
        for i in range(self.count):
            #generate five random tuples
            position = (np.random.uniform(-con.radius,con.radius),np.random.uniform(-con.radius,con.radius))           
            positions.append(position)
        ''' 
        testing to see if balls overlap and if so replacing overlapping
        ball until it no longer overlaps

        also testing to see if ball is outside container

        runs a while loop that delets an overlapping particle and produces another
        randomly positioned particle until the are the specified number of not 
        overlapping particles

        '''
        
        deleted = 1
        while deleted > 0:
            deleted = 0
            for i in range(self.count):
                for j in range(i+1,self.count):
                    
                    
                    pi = positions[i]
                    pj = positions[j]
                    dx = pi[0]-pj[0]
                    dy = pi[1]-pj[1]
                    magPI = np.sqrt((pi[0]**2
                                     +pi[1]**2))
                    magPJ = np.sqrt((pj[0]**2
                                     +pj[1]**2))
                    drSq = (dx**2
                            +dy**2)
                    if drSq < 4.2*self.radius**2:
                        
                        positions[j] = (np.random.uniform(-con.radius,con.radius),np.random.uniform(-con.radius,con.radius))
                        
                        deleted = deleted+1
                    elif magPI > con.radius -self.radius:
                        positions[i] = (np.random.uniform(-con.radius,con.radius),np.random.uniform(-con.radius,con.radius))
                        deleted = deleted+1
                    elif magPJ > con.radius - self.radius:
                        positions[j] = (np.random.uniform(-con.radius,con.radius),np.random.uniform(-con.radius,con.radius))
                        deleted = deleted+1
            
        return positions

    def randomVelocities(self):
        ''' 
        random speeds(Rayleigh distribution is a 2d Maxwell-Boltzmann distribution) and angles  
        speed = np.random.rayleigh(scale=self.v,size=self.count)

        phi = np.random.random(size=self.count)*2*np.pi
        velocities = []
        for i in range(self.count):
            velocities.append(np.array([np.cos(phi[i]), np.sin(phi[i])]) * speed[i])
        n.b. requires addition of scale number in init
        '''
        ''' 
        generating speeds using gaussian distribution in x and y values

        '''
        '''
        self.xVelocities = []
        self.yVelocities = []
        
        for i in range(int(self.count/2)):
            self.xVelocities.append(rand.gauss(self.vMu,self.vStd))
            self.xVelocities.append(rand.gauss(-self.vMu,self.vStd))
            
        
        for j in range(int(self.count/2)):
            self.yVelocities.append(rand.gauss(self.vMu,self.vStd))
            self.yVelocities.append(rand.gauss(-self.vMu,self.vStd))

        velocities = []
        for k in range(self.count):
            velocities.append((float(self.xVelocities[k]),float(self.yVelocities[k])))
        '''

        ''' 
        To reduce error in relationship graphs the particles will all be generated at the same speed
        and to prevent the
        average velocity not being equal to zero their angle will be calculated as a fraction of 2pi
        '''
        phi = []
        for i in range(self.count):
            phi.append(2*np.pi*i
                       /self.count)

        velocities = []
        for j in range(self.count):
            velocities.append(np.array([np.cos(phi[j]), np.sin(phi[j])]) * self.vMu)
        
        return velocities




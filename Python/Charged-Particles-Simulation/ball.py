import numpy as np
import scipy as sp
import pylab as pl
from ballGeneration import Particles
from containerGeneration import Container


class ball(object):
    balls = {}
    def __init__(self, mass, radius, position, velocity, charge):
        """

        initialises mass,radius,position and velocity such that positions and velocities can be produced by Particles class

        """
        parts = Particles()
        con = Container()
        radius = parts.radius
        
        self.position = np.array(position,dtype = np.float64)
        self.velocity = np.array(velocity,dtype = np.float64)
        self.charge = np.array(charge,dtype = np.float64)


        self.dt = 0.05 
        self.mass = float(parts.mass)
        self.radius = float(np.abs(radius))
        self.centres = np.array(self.position)
        

    ''' 
    BALL CLASS INFORMATION 
    -formal and informal
    - __repr__ and __str__ 
    '''
    def __repr__(self):
        return ('mass = ',self.mass, 'radius = ',self.radius, 'position =' ,self.position, 'velocity = ',self.velocity, 'dt =' ,self.dt) 
                
    def __str__(self):
        return ('mass = ',self.mass, 'radius = ',self.radius, 'position =' ,self.position, 'velocity = ',self.velocity, 'dt =' ,self.dt)

    ''' 
    patch() and move() functions

    patch function: produces filled blue circle of radius self.radius to represent the 'ball' in this simulation.
    The initial positon of the centre of which is found using the particle generating
    class and then developed acording to the simulation.

    move function: ensures container does not move and develops position self.dt in time 

    '''
    
    def move(self):
        con = Container
        if isinstance(self,con):
            self.position = self.position
        
        else:
            self.position = (self.position + self.dt*self.velocity)
        return self.position
        

    def collide(self,other):

        ''' 
        For collisions with the container the perpendicular velocity of the particle to the container is reversed
        and done in the reference frame of the container.

        For collisions between particles conservation of momentum in the centre of mass frame was used to find the 
        resulting velocities 

        '''
        con = Container
        if isinstance(other,con):
            '''
            perpendicular velocity is found using dot product of particle velocity and position and 
            then reversed and parallel velocity is unchanged and added to find the new velocity
            '''
            velNorm = np.sqrt((self.velocity[0])**2+self.velocity[1]**2)
            posNorm = np.sqrt((self.position[0])**2+self.position[1]**2)
            selfVelperpendicular = (np.dot(self.position,self.velocity))*self.position/(posNorm*posNorm)
            selfVelparallel = self.velocity - selfVelperpendicular
            
            selfVelnew = -selfVelperpendicular + selfVelparallel
            otherVelnew = 0

        else:
            ''' 
            done in reference frame of other to simplify  (of) stands for other frame)
            reference velocity found and velocities converted to reference frame velocities
            '''
            ofVelocity = self.velocity - other.velocity
            #velocity parallel component found using dot product with the separation of the centres of the particles
            centreSeparation = self.position - other.position
            normCentreseparation = centreSeparation/(np.sqrt(centreSeparation.dot(centreSeparation)))
            OfselfSpeedparallel = np.dot(ofVelocity,normCentreseparation)
            OfselfVelocityperpendicular = ofVelocity - OfselfSpeedparallel*normCentreseparation
           
            #magnitudes of parallel speeds found using conservation of momentum calculation
            ofOtherspeedNewparallel = 2 * self.mass * OfselfSpeedparallel / (self.mass + other.mass)
            ofSelfspeedNewparallel = OfselfSpeedparallel * (self.mass - other.mass) / (self.mass + other.mass)
            #parallel speeds converted into velocities using normalised vector betwen the particle centres
            ofSelfvelocityNewparallel = normCentreseparation * ofSelfspeedNewparallel
            ofOthervelocityNewparallel = normCentreseparation * ofOtherspeedNewparallel


            '''
            new reference velocities found summing new parallel velocity with constant perpendicular velocity
            rf velocities converted into lab frame velocities by adding the reference velocity

            '''
            otherVelnew = other.velocity + ofOthervelocityNewparallel
            selfVelnew = other.velocity + ofSelfvelocityNewparallel + OfselfVelocityperpendicular

        self.velocity = selfVelnew
        other.velocity = otherVelnew


    def electrostatic(self,other):

        k = 8.99e37
        parts = Particles
        r = self.position-other.position
        
        magr = np.sqrt(np.abs(r[0]**2+r[1]**2))
        rnorm = r/magr
       
        magAcceleration = k*self.charge*other.charge/(magr)
        acceleration = magAcceleration*rnorm
        
        
        self.velocity[0] = self.velocity[0]+acceleration[0]*self.dt
        self.velocity[1] = self.velocity[1]+acceleration[1]*self.dt

        
        
        
      
        



        






            




        





        

            



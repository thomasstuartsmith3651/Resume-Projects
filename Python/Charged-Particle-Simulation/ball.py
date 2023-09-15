import numpy as np 
import scipy as sp
import pylab as pl
from ballGeneration import Particles
from containerGeneration import Container


class ball(object):
    balls = {}
    def __init__(self, mass, radius, position, velocity):
        """

        initialises mass,radius,position and velocity such that positions and velocities can be produced by Particles class

        """
        parts = Particles()
        mass = 1
        radius = parts.radius
        
        self.position = np.array(position,dtype = np.float64)
        self.velocity = np.array(velocity,dtype = np.float64)

        
        self.dt = 0.15/parts.vMu 
        self.mass = float(np.abs(mass))
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
    def patch(self):
        ballPatch = pl.Circle(self.position,self.radius,fill=True)
        return ballPatch
    
    def move(self):
        con = Container
        if isinstance(self,con):
            self.position = self.position
        
        else:
            self.position = (self.position + self.dt*self.velocity)
        return self.position
        
        
    def timeTocollision(self, other):
        """
        time to collision between 2 balls
        returns None if:  there is no collision between those two balls
                          the balls are already overlapping


        Uses differential equation in 'Thermodynamics Snookered' worksheet to find the time to the next collision
        The equation outputs up to two values of dt and the smallest positive value of dt is appended to the list 
        of possible collisions in the simulation class
        """
        
        con = Container 
        # finding the different variables in the equation
        # dr and dv are the distance between the particles and their differences in velocity respectivelt
        dr = (self.position - other.position)
        dv = self.velocity - other.velocity

        # produces dv**2 which is labelled as a to clarify the discriminant calculation
        a = np.dot(dv,dv)

        # finds the square of the differences in radius of the colliding objects as this value is the (square of the) distance at which the collision will happen
        if isinstance(other,con):
            Rsq = (self.radius - other.radius)**2
        else:
            Rsq = (self.radius + other.radius)**2
        
        # square of the distances between the colliding objects
        drSq = dr.dot(dr)
    
        #iscriminant calculation to determine if equation produces imaginary solutions
        c = drSq-Rsq
        b = 2*dv.dot(dr)
        discriminant = b**2 - 4*a*c
        
        # a negative discriminant will result in an imaginary dt
        if discriminant < 0:
            '''
            Testing Code to check if dt was properly translated to simulation 
            print(100,'negDisc')
            '''
            return 100.0
        #simplifies dt calculation in event discriminant is 0
        elif discriminant == 0:
            dt = -b/(2*a)
            '''
            Testing Code to check if dt was properly translated to simulation           
            print(100,'disc=0')
            '''
            return 100.0
            
        elif discriminant > 0:
            
            dt1 = (-b + np.sqrt(discriminant))/(2*a)
            dt2 = (-b - np.sqrt(discriminant))/(2*a)
            if dt1 <0 and dt2 < 0:
                #print(-1,'dt1neg')
                return -1
            elif dt1 < 0 and dt2 >=0:
                #print(dt2,'dt2')
                return dt2
            elif dt2 < 0 and dt1 >=0 :
                #print(dt1,'dt1')
                return dt1
            elif dt1>0 and dt2 > 0:
                #print(dt1,dt2,'dt1,dt2')
                return np.amin(np.array([dt1,dt2]))
     
        

    def collide(self,other):

        ''' 
        For collisions with the container the perpendicular velocity of the particle to the container is reversed
        and done in the reference frame of the container.

        For collisions between particles conservation of momentum in the centre of mass frame was used to find the 
        resulting velocities 

        '''
        
        mass1 = self.mass
        mass2 = other.mass
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
            

            
            ''' 
            Note when collision with container occurs
            print('container')
            '''

            

       
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



        






            




        





        

            



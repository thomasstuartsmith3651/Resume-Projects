from ball import ball
from containerGeneration import Container
from ballGeneration import Particles
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import scipy.constants as const
from scipy.optimize import curve_fit

class Simulation(object):
    ''' 
    Contains functions to initialise and run simulation of balls with variable radii and intial velocities and positions
    in a container of variable radius.

    '''
    
    parts = Particles()
    con = Container()
    def __init__(self, particles=(), bRadius=parts.radius, cRadius = con.radius, noCollisions=10000000000000):
        
        #initialise particles with radius and determine number of collisions
        parts = Particles()
        bal = ball(parts.mass,parts.radius,parts.positions,parts.velocities,parts.charges)
        self.bRadius = bRadius
        self.noCollisions = noCollisions
        #generates necessary arrays and initial values to calculate different quantities that need to be
        #calculated over the entire simulation
        self.components = []
        self.particles = []
       
        self.interval = bal.dt #optimal speed for best running of simulation
        self.time = 0 #total time passed
        self.plotTime=[] #array of cumulative time to collision

        #task9 checks of code quality
        self.posMagnitude = []   #used to produce displacement from centre histogram, appended to during check to see if overlapping with container
        self.separationMagnitude = [] #used to produce separation histogram, appended to during particle overlapping code
        
        #gas properties
        self.totalMomentum = [] 
        self.totalKE = []
        self.pressurePlot = []
        self.velocityMagnitudes = []




    def addParticles(self):

        """
        Adding particles produced by Particles() class
        """
        parts = Particles()
        
        for i in range(parts.count):
            bal = (ball(1,parts.radius,parts.positions[i],parts.velocities[i],parts.charges[i]))
            self.particles.append(bal)
        
        return self.particles

    def addContainer(self):
        ''' 
        adding container produced by Container() class
        '''
        self.components=[]
        con = Container()
        self.components.append(con)
        for particle in self.particles:
            
            self.components.append(particle)
        
        return self.components

    
    def intervalRunning(self):
        """ 
        - runs timeTocollision and collide functions in tandem with an animation function to simulate multiple ball
        collisions within a fixed container
        -contains an additional code to collide any particles that overlap incase timeTocollision application is unsuccsessful
        this does however introduce a limitation to the number of simultaneous collisions the simulation can run
        - collects the velocity,momentum and position of each particle after each set of collisions
        -then calcultes the total kinetic energy and momentum 
        -calculates pressure on walls of container by recording velocity before and after each particle-container collision
        """



        ''' 
        Determining time to the next collision:

        produces an array of all the dt values between all of the particles
        finds the smallest positive dt value but also appends any dt values that occur within the
        time interval of the smallest dt value 
        runs the move function for the duration of the dt 
        whilst checking that if any collisions are missed,they occur by checking to see if the 
        particles overlap with each other and are not about to collide and rerunning the collide function
        '''

        #arrays that are hidden in function
        timesTocollisions = []
        positiveTimes = []
        n=0
        possTimecollision= []
        centres = []
        parts = Particles()
        kineticEnergy = []
        containerCollisions = []
        duration = 1
        
        selfParticles = []                       
        others = []                              
        
        


        while duration  > 0:
            selfNo=[]
            otherNo=[]
            
            for i in range(len(self.particles)):
                 for j in range(len(self.particles)):
                    if i != j:
                        self.particles[i].electrostatic(self.particles[j])
                        self.particles[j].electrostatic(self.particles[i])            
            
            

            ''' 
            CONTAINER COLLISION
            Checking to see if there is a missed container collision:
            Finds the magnitude of the distance from the centre of the circle in order to determine
            if there is unexpected overlap
            This is done by producing a list of (particle number,magnitude) arrays 
        '''
            con = Container()
            steps =0
            amount = 0
            mag = []
            colliders = []
            for z in range(parts.count):
                    nextPos = self.particles[z].position+self.particles[z].velocity*self.interval
                    displacementMagnitude = np.sqrt((nextPos[0])**2 + (nextPos[1])**2)
                    mag.append(displacementMagnitude)
                    
                    #self.posMagnitude.append(displacementMagnitude) # collecting for histogram
                    amount += 1
                    
            for i in range(len(mag)):
                
                if mag[i] > con.radius - parts.radius:
                    selfNo.append(i+1)
                    otherNo.append(0)
                
    
            ''' 
                PARTICLE COLLISION
                runs in same manner to container variant except it needs to keep track of 
                both particle numbers


            '''
            num = 0            
            bouncers = []                
            separationMag = []
            nextseparationMag = []
                
            for a in range(parts.count):          
                    for s in range(a+1,parts.count):
                        separation = (self.particles[a].position 
                                    - self.particles[s].position)
                        separationMag.append(a)
                        separationMag.append(s)
                        separationMag.append(np.sqrt(separation[0]**2
                                                    +separation[1]**2))
                        self.separationMagnitude.append(np.sqrt(separation[0]**2
                                                        +separation[1]**2))
                        
                        
                        num += 1

                    for s in range(a+1,parts.count):
                        nextPosa = self.particles[a].position + self.particles[a].velocity*self.interval
                        nextPoss = self.particles[s].position + self.particles[s].velocity*self.interval
                        nextseparation = (nextPosa 
                                    - nextPoss)
                        nextseparationMag.append(a)
                        nextseparationMag.append(s)
                        nextseparationMag.append(np.sqrt(nextseparation[0]**2
                                                    +nextseparation[1]**2))
                        


                        
                        
                                #referenceDirection = self.particles[a].velocity.dot(self.particles[s].velocity)
                         
            separationMagreshape = np.reshape(separationMag,(num,3)) 
            nextseparationMagreshape = np.reshape(nextseparationMag,(num,3)) 
            number = 0
            #print(separationMagreshape)
            #print(nextseparationMagreshape)
            
            
            for k in range(num) : 
                
                if nextseparationMagreshape[k,2] < 2*self.bRadius:
                                
                                bouncers.append(separationMagreshape[k,0]) #a
                                selfNo.append(separationMagreshape[k,0]+1)
                                bouncers.append(separationMagreshape[k,1]) #s
                                otherNo.append(separationMagreshape[k,1]+1)
                                bouncers.append(separationMagreshape[k,2]) #separationMag
                                number += 1

            for k in range(len(selfNo)):
                selfParticles.append(self.components[int(selfNo[k])])
                others.append(self.components[int(otherNo[k])])   

            if len(selfNo) >0:
                for a in range(len(selfNo)):      
                    selfParticles[a].collide(others[a]) 


                    
            #moves all particles according to their velocities and updates circle centres
            n = n+1       
            for i in range(parts.count):
                    self.particles[i].move()
                    centres.append(self.particles[i].position)
            m = parts.count*2    
            patchPositions = np.reshape(centres,(n,m))
            
            steps+=1


            
            
            
            return patchPositions
        
        
       
        
        

            
        


        '''
        Velocity Magnitude collection
        '''
        for partic in self.particles:
            velocityMagnitude= np.sqrt(partic.velocity[0]**2
                                       +partic.velocity[1]**2)
            self.velocityMagnitudes.append(velocityMagnitude)

            


        ''' 
        KINETIC ENERGY CALCULATION
        checks that kinetic energy is constant by summing all kinetic energies of the particles after
        every set of collisions

        '''

        for particle in self.particles:
                KE = 0.5*1*particle.velocity.dot(particle.velocity)
                kineticEnergy.append(KE)

        totalKE = 0
        for q in kineticEnergy:
            totalKE = totalKE+q

        self.totalKE.append(totalKE)


        ''' 
        tracks momentum (not conserved)
        '''
        momentum = []
        for particle in self.particles:
            momentum.append(1*particle.velocity)    
        totalMomentum = (0,0)
        for m in momentum:   
            totalMomentum += m
        totalMomentummag = np.sqrt(totalMomentum[0]**2
                                   +totalMomentum[1]**2)
        self.totalMomentum.append(totalMomentummag)
        

        #self.time +=(time) #total time
        #self.plotTime.append(self.time)  # produces an time array where the times increase by the next time to collision


        
            
    def run(self, num_frames, animate=True):
        ''' 
        Animates all of the balls. 
        Every interval the ball patches are removed and replaced by ball patches with updated centres
        '''
        if animate:
            #producing figure with fixed axes and container representation
            f = pl.figure()
            con = Container()
            containerPatch = pl.Circle([0., 0.], con.radius, ec='g', fill=False, ls='solid')
            ax = pl.axes(xlim=(-con.radius, con.radius), ylim=(-con.radius, con.radius))
            ax.add_patch(containerPatch)
            
            
        #range = number of sets of collisions
        for frame in range(self.noCollisions):
            parts = Particles()
            bal = ball(parts.mass,parts.radius,parts.positions,parts.velocities,parts.charges)
            ''' 
            self.nextCollision returnes the new patch positions in an array of size twice the number of particles
            as the position x and y values are appended individually and so code adds the positions 'in twos'
            '''
            for q in self.intervalRunning():
                instBallpatches = []
                for no in range(parts.count):
                    r = 2*no
                    if self.particles[no].charge < 0:
                        colour = 'r'
                        label = '-'
                    else:
                        colour = 'b'
                        label = '+'
                        
                    ballPatch = pl.Circle((q[r],q[r+1]), parts.radius, hatch = label, color = colour, fill=False, ls='solid')
                    instBallpatches.append(ballPatch)
                    ax.add_patch(ballPatch)
                    
                    #print(r)
                    #print(ballPatch.center)
                pl.pause(0.001)
                for c in range(parts.count):
                    instBallpatches[c].remove()
        pl.show()


              
                
                
      
               
      

            
                            
         






                    














                
         







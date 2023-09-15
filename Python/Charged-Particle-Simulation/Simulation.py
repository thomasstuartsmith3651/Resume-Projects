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
    def __init__(self, particles=(), bRadius=parts.radius, noCollisions=100):
        
        #initialise particles with radius and determine number of collisions
        parts = Particles()
        self.bRadius = bRadius
        self.noCollisions = noCollisions
        #generates necessary arrays and initial values to calculate different quantities that need to be
        #calculated over the entire simulation
        self.components = []
        self.particles = []
       
        self.interval = 0.15/parts.vMu #optimal speed for best running of simulation
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
            bal = (ball(1,parts.radius,parts.positions[i],parts.velocities[i]))
            self.particles.append(bal)
        #print(self.particles)
        return self.particles

    def addContainer(self):
        ''' 
        adding container produced by Container() class
        '''
        self.components=[]
        con = Container()
        
        for particle in self.particles:
            self.components.append(particle)
        self.components.append(con)
        return self.components

    
    def nextCollision(self):
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
        

        for i in range(parts.count):          
            for j in range(i+1,parts.count+1):
                #timeTocollision between every object
                possTimecollision=(self.particles[i].timeTocollision(self.components[j]))
                '''
                enable check of all dts produced in ball class
                '''
                timesTocollisions.append(possTimecollision)
                
                
                
                #append all positive dts that aren't given error value of 100 or -1
                #if possTimecollision > self.interval and possTimecollision < 100 and possTimecollision > -0.1:
                if possTimecollision < 100 and possTimecollision > -0.1:
                    positiveTimes.append(i)
                    positiveTimes.append(j)
                    positiveTimes.append(possTimecollision)
                    n = n+1
                ''' 
                reordering into columns of i,j and timeTocollision
                ''' 
        posTimecolumns = np.reshape(positiveTimes,(n,3))
                
        time = 1000
        #finding smallest dt
        for p in range(n):
                    if posTimecolumns[p,2] < time:
                        time = posTimecolumns[p,2]
        nom = 0
        selfNo = []
        otherNo = []
        times = []
        #adding all dts within interval of smallest dt
        for g in range(n):
                    if posTimecolumns[g,2] < time+self.interval:
                        selfNo.append(int(posTimecolumns[g,0]))
                        otherNo.append(int(posTimecolumns[g,1]))
                        times.append(posTimecolumns[g,2])
        
                
                
        #print(times,'times')        

        #finding collisions with container in order to calculate pressure
        x =0        
        for on in range(len(otherNo)):
            if otherNo[on] == parts.count:
                containerCollisions.append(selfNo[on])
                containerCollisions.append(self.particles[int(selfNo[on])].velocity)
                x+=1

                            
                

        # producing arrays of the colliding particles in the same array position as the particle that they are colliding with  
        selfParticles = []                       
        others = []                              
        
        for k in range(len(selfNo)):
            selfParticles.append(self.components[int(selfNo[k])])
            others.append(self.components[int(otherNo[k])])
        duration = float(time)
        con = Container()
        n = 0
        
        # running move function with checks until the next collision
        while duration  > 0.0+self.interval:
            
            
           #moves all particles according to their velocities and updates circle centres
            n = n+1       
            for i in range(parts.count):
                self.particles[i].move()
                centres.append(self.particles[i].position)
            m = parts.count*2    
            patchPositions = np.reshape(centres,(n,m))
            duration -= self.interval
            #print(duration)
        for i in range(len(self.particles)):
            if (self.particles[i].position[0])**2 + (self.particles[i].position[1])**2 >101:
                print('container fail')
                print((self.particles[i].position,self.particles[i].mass,duration))

            
        

        ''' 
        COLLIDES ALL STIPULATED PARTICLES

        '''
        m = parts.count*2 
        patchPositions = np.reshape(centres,(n,m))
        for a in range(len(selfNo)):
            
            #print(selfParticles[a].velocity)
            selfParticles[a].collide(others[a])
            

            '''
            checks all particles are being collided
            if len(selfParticles) > 2:
                print(selfParticles[a])
                print(times,'times')
                print(selfParticles[a].velocity,'after')
            '''

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
        

        self.time +=(time) #total time
        self.plotTime.append(self.time)  # produces an time array where the times increase by the next time to collision


        ''' 
        takes all of the recorded velocities just before conatiner collisions
        and uses position in self.particles array to match the before and after collision
        velocities
        then finds the change in velocities and adds them all together

        '''
        #produces matrix with first column containing particles num 
        #in the first column and its velocitiy before colliding with the container in the second column
        conDV = []
        containerCollisionsreshape = np.reshape(containerCollisions,(x,2)) 
        velChange = []
        DVs = 0
        for y in range(x):
            #calculates change in velocity for each particle colliding with the container
            velChange = (containerCollisionsreshape[y,1]
                         - self.particles[int(containerCollisionsreshape[y,0])].velocity) 
            conDV.append(velChange)
            DVs += 1
        
        totalDV = 0
        conDVreshape = np.reshape(conDV,(DVs,2))
        for dv in range(DVs):

            totalDV += np.sqrt((conDVreshape[dv][0])**2
                                +(conDVreshape[dv][1])**2) #magnitude of change in velocity for each particle

        totalPressure = totalDV/time #total pressure during time to collision
        self.pressurePlot.append(totalPressure)

        return patchPositions
            
            
            
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
            ''' 
            self.nextCollision returnes the new patch positions in an array of size twice the number of particles
            as the position x and y values are appended individually and so code adds the positions 'in twos'
            '''
            for q in self.nextCollision():
                instBallpatches = []
                for no in range(parts.count):
                    r = 2*no
                    
                    ballPatch = pl.Circle((q[r],q[r+1]), parts.radius, ec='g', fill=True, ls='solid')
                    instBallpatches.append(ballPatch)
                    ax.add_patch(ballPatch)
                    #print(r)
                    #print(ballPatch.center)
                pl.pause(0.001)
                for c in range(parts.count):
                    instBallpatches[c].remove()
        pl.show()


              
                
                
      
               
      
''' 
            MISSED CONTAINER COLLISION
            Checking to see if there is a missed container collision:
            Finds the magnitude of the distance from the centre of the circle in order to determine
            if there is unexpected overlap
            This is done by producing a list of (particle number,magnitude) arrays 
            '''
            # amount = 0
            # mag = []
            # colliders = []
            # for z in range(parts.count):
            #     mag.append(z)
            #     displacementMagnitude = np.sqrt((self.particles[z].position[0])**2 + (self.particles[z].position[1])**2)
            #     mag.append(displacementMagnitude)
                
            #     self.posMagnitude.append(displacementMagnitude) # collecting for histogram
            #     amount += 1
                

            # magReshape = np.reshape(mag,(amount,2))
            # #first checks to see if particle is already set to collide with the container (up to four particles)
            # for mags in range(amount) :   
            #     if len(selfNo) == 1:
            #         if magReshape[mags,1] > (con.radius - self.bRadius) and magReshape[mags,0] != selfNo[0] and magReshape[mags,0] != otherNo[0]:
            #             colliders.append(magReshape[mags,0])#z
            #     if len(selfNo) == 2:
            #         if magReshape[mags,1] > (con.radius - self.bRadius) and magReshape[mags,0] != selfNo[0]  and magReshape[mags,0] != otherNo[0]and magReshape[mags,0] != selfNo[1]and magReshape[mags,0] != otherNo[1]:
            #             colliders.append(magReshape[mags,0])#z
            #     if len(selfNo) == 3:
            #         if magReshape[mags,1] > (con.radius - self.bRadius) and magReshape[mags,0] != selfNo[0] and magReshape[mags,0] != otherNo[0]and magReshape[mags,0] != otherNo[1]and magReshape[mags,0] != otherNo[1]and magReshape[mags,0] != otherNo[2]and magReshape[mags,0] != otherNo[2]:
            #             colliders.append(magReshape[mags,0])#z
            # #collides all particles with specified magnitude if displacement
            # for z in colliders:
            #     containerCollisions.append(z)
            #     containerCollisions.append(self.particles[int(z)].velocity)
            #     self.particles[int(z)].collide(con)  
            #     x+=1
            #     self.particles[int(z)].move()  
            # ''' 
            # MISSED PARTICLE COLLISION
            # runs in same manner to container variant except it needs to keep track of 
            # both particle numbers


            # '''
            # num = 0            
            # bouncers = []                
            # separationMag = []
            
            # for a in range(parts.count):          
            #     for s in range(a+1,parts.count):
            #         separation = (self.particles[a].position 
            #                       - self.particles[s].position)
            #         separationMag.append(a)
            #         separationMag.append(s)
            #         separationMag.append(np.sqrt(separation[0]**2
            #                                      +separation[1]**2))
            #         self.separationMagnitude.append(np.sqrt(separation[0]**2
            #                                         +separation[1]**2))
            #         num += 1
            #                 #referenceDirection = self.particles[a].velocity.dot(self.particles[s].velocity)
                        
            # separationMagreshape = np.reshape(separationMag,(num,3)) 
            # number = 0
            # for k in range(num) : 
            #     if len(selfNo) == 1: 
            #         if separationMagreshape[k,2] < 2*self.bRadius  and separationMagreshape[k,0] != selfNo[0] and separationMagreshape[k,0] != otherNo[0]:
            #             bouncers.append(separationMagreshape[k,0]) #a
            #             bouncers.append(separationMagreshape[k,1]) #s
            #             bouncers.append(separationMagreshape[k,2]) #separationMag
            #             number += 1
            #     if len(selfNo) == 2:
            #         if separationMagreshape[k,2] < 2*self.bRadius  and separationMagreshape[k,0] != selfNo[0]  and separationMagreshape[k,0] != otherNo[0]and separationMagreshape[k,0] != selfNo[1]and separationMagreshape[k,0] != otherNo[1]:
            #             bouncers.append(separationMagreshape[k,0]) #a
            #             bouncers.append(separationMagreshape[k,1]) #s
            #             bouncers.append(separationMagreshape[k,2]) #separationMag
            #             number += 1
            #     if len(selfNo) == 3:
            #         if separationMagreshape[k,2] < 2*self.bRadius and separationMagreshape[k,0] != selfNo[0] and separationMagreshape[k,0] != otherNo[0]and separationMagreshape[k,0] != selfNo[1]and separationMagreshape[k,0] != otherNo[1]and separationMagreshape[k,0] != selfNo[2]and separationMagreshape[k,0] != otherNo[2]:
            #             bouncers.append(separationMagreshape[k,0]) #a
            #             bouncers.append(separationMagreshape[k,1]) #s]#
            #             bouncers.append(separationMagreshape[k,2]) #separationMag
            #             number += 1

            #     if len(selfNo) == 4:
            #         if separationMagreshape[k,2] < 2*self.bRadius and separationMagreshape[k,0] != selfNo[0] and separationMagreshape[k,0] != otherNo[0]and separationMagreshape[k,0] != selfNo[1]and separationMagreshape[k,0] != otherNo[1]and separationMagreshape[k,0] != selfNo[2]and separationMagreshape[k,0] != otherNo[2] and separationMagreshape[k,0] != selfNo[3]and separationMagreshape[k,0] != otherNo[3]:
            #             bouncers.append(separationMagreshape[k,0]) #a
            #             bouncers.append(separationMagreshape[k,1]) #s]#
            #             bouncers.append(separationMagreshape[k,2]) #separationMag
            #             number += 1
            #             #print(bouncers)
            # bouncersReshape = np.reshape(bouncers,(number,3))
            # for o in range(number):
            #             #print(bouncersReshape[o][0])
            #     self.particles[int(bouncersReshape[o][0])].collide(self.particles[int(bouncersReshape[o][1])])
                
            #     self.particles[int(bouncersReshape[o][0])].move()
            #     self.particles[int(bouncersReshape[o][1])].move()
            
                            
            # #enables while loop to function by developing time by how much time has been multiplied by the velocities of the particles
            # duration = duration - self.interval






                    














                
         







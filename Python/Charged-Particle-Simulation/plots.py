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
TASK 9 
For 10000 collisions Momentum and Pressure were plotted against time
with 20 balls of radius 0.2 in a container, radius 10. The balls were 
initialised with speeds of 22.0
'''

def histogramDisplacement():
        plt.hist(sim.posMagnitude,bins=15)  #histogram of distance from the centre of the container
        plt.xlabel('Displacement From Centre Magnitude')
        plt.ylabel('Number')
        plt.title('Distances From Container Centre')
        plt.savefig('Displacement.png')
        plt.show()

def histogramSeparation():
        plt.hist(sim.separationMagnitude,bins=15)  #histogram of ball separation
        plt.xlabel('Displacement Magnitude')
        plt.ylabel('Number')
        plt.title('Distances Between Particles')
        plt.savefig('Separation.png')
        plt.show()

''' 
TASK 9
The shape of the distributions were as expected with the number increasing linearly with
distance from the centre with a reduced muber in the final bin as the ball centre did not
extend all the way to the container radius due to the radius of the ball

There was no exact predicted form for the separation of the balls but as expected there 
was a maximum close to the width of the container with a form that is inconclusive to any easily
identifiable distribution
'''

'''
TASK 10

In an ideal gas kinetic energy is proportional to temperature
-in two dimensions Average Energy = boltzmann constant x Temperature
and although this simulation is not quite of an ideal gas as the
volume of balls is not negligible this relationship should hold as
there are no long range forces between the particles 'no potential energies'

Momentum is not conserved as the collisions with the container do not conerve momentum
Only KE is conserved

If the velocities are all doubles the temperature will increase to the power 4
Pressure will double as the momentum change when colliding with the container will double
There will be more overlapping of the balls as the simulation will effectively check positions 
half as often
'''

''' 
TASK 11
-testing conservation of system kinetic energy, momentum and pressure
-calculations for average temperature and pressure
-plots testing Boyle's law, Gay-Lussac's law and Number of Partcles - Pressure proportionality
'''

#plot of kinetic energy with time
def totalKEplot():
        plt.plot(sim.plotTime,sim.totalKE) # kinetic energy constant as expected
        plt.xlabel('Time')
        plt.ylabel('Total Kinetic Energy')
        plt.title('Total KE with Time')
        plt.savefig('KineticEnergy.png')
        plt.show()


''' 
Momentum and Pressure Time Plots

- varies greatly from time interval to time interval
-average momentum and pressure depraciates with time as a rate of -0.67456255
 due to momentum not being conserved in collisions with
 the container

'''
#plot of total momentum of all the particles against time
def totalMomentumplot():
        plt.plot(sim.plotTime,sim.totalMomentum)
        plt.xlabel('Time')
        plt.ylabel('Total Total Momentum')
        plt.title('Total Momentum with Time')
        
        poly_con, cov_poly_con = np.polyfit(sim.plotTime,sim.totalMomentum,1,cov=True)
        m = np.poly1d(poly_con)
        plt.plot(sim.plotTime,m(sim.plotTime),'g--',label = 'Average Momentum')
        plt.savefig('MomentumTime.png')
        print(m[1],'mgtraph')
        plt.show()

#plot of gas pressure against time
def plotIntervalPressure():
        plt.plot(sim.plotTime,sim.pressurePlot)
        plt.xlabel('Time')
        plt.ylabel('Pressure')
        plt.title('Pressure')
        poly_con, cov_poly_con = np.polyfit(sim.plotTime,sim.pressurePlot,1,cov=True)
        m = np.poly1d(poly_con)
        plt.plot(sim.plotTime,m(sim.plotTime),'g--',label='Average Pressure')
        
        plt.savefig('PressureTime.png')
        print(m[1],'pgraph')
        plt.show()

#calculates the average pressure throughout whole simulation
def averagePressure():
        totalPressure = 0
        for i in sim.pressurePlot:
            totalPressure += i*sim.interval
        averagePressure = totalPressure/sim.time
        print(averagePressure)

#calculates average temperature throughout whole simulation
def averageTemperature():
        averageKE = 0
        for j in sim.totalKE:
            averageKE += j/(len(sim.totalKE))
        averageTemperature = averageKE/const.k 
        print(averageTemperature)
        return averageTemperature
        
    



''' 
Pressure Vs Temperature
-20 Particles
-bRadius = 0.2
-cRadius = 10
-varied by changing velocity
'''
def gayLussac():
    Pressure02 = [20.04998126,78.52332902,192.3115829,277.349493,478.3696854,773.3801195, 534.5293833]
    Temperature02 = [1.81E+25,7.24E+25,1.63E+26,2.90E+26,4.53E+26,6.52E+26,5.28E+26]

    plt.plot(Temperature02,Pressure02,'x')
    poly_con, cov_poly_con = np.polyfit(Temperature02,Pressure02,1,cov=True)
    m = np.poly1d(poly_con)
    plt.plot(Temperature02,m(Temperature02)) 
    plt.xlabel('Temperature')
    plt.ylabel('Pressure')
    plt.title('Gay-Lussac Law')
    plt.legend()
    plt.savefig('GayLussac.png')
    plt.show()

''' 
Pressure against Volume
number of balls  = 20
velocity = 30
radius = 0.2
changed radius of the container
'''
def boyle():
    Pressure = sorted([758.2342095,393.965628,278.0303872,169.1684094,342.4013019,549.7118397,1088.389553,126.8306879,145.6614943,171.486])
    Volume = sorted([314.1592654,615.7521601,1017.87602,1256.637061,804.2477193,452.3893421,201.0619298,2123.716634,1809.557368,1520.530844],reverse = True)
    
    plt.plot(Volume,Pressure,'x')
    def func(x,a):
        return (a/x)
    initial = [16570]
    params,params_cov = curve_fit(func,Volume,Pressure,initial,maxfev=100000) 
    plt.plot(Volume,func(Volume,params),'')
    exp = []
    for i in Volume:
        exp.append(func(i,params))
    

    #chi-squared test of 1/x fit
    chiSquared = 0
    for i in range(len(Volume)):
            chi = (Pressure[i]-exp[i])**2/(exp[i])
            chiSquared += chi
            print(chi)
    print(chiSquared,'chi')
    plt.title('Boyle\'s Law')
    plt.xlabel('Volume')
    plt.ylabel('Pressure')
    #plt.savefig('boyle.png')
    plt.show()

''' 
Number vs Pressure
v = 30
r = 0.2
cR = 10
varied initial number of balls
not included in report
'''
def numberPressure():
    Number = [10,14,18,22,8,12,16,20]
    Pressure = [189.2702877,368.1769169,597.2084395,912.5655313,114.1525404,304.0914841,491.190749,779.862632]
    plt.plot(Number,Pressure,'x')
    poly_con, cov_poly_con = np.polyfit(Number,Pressure,1,cov=True)
    m = np.poly1d(poly_con)
    plt.plot(Number,m(Number))
    exp = []
    for i in Number:
        exp.append(m(i))
    

''' 
TASK 12
Test how PT constancy is affected as the volume of the balls becomes a bigger fraction of the container
Pressure Vs Temperature for particles of radius 0.01,0.2,0.4
- n=20 container radius =10
- straight line of best fit for 0.01 and 0.2 (plot points for 0.01 omitted to avoid crowding)
- form of 0.04 radius points unclear so points were joined for clarity
-each pressure,temperature pair was from a 10000 collision 

'''
def task12():
    #100 sets of collisions run for each pressure,temperature pair
    Pressure001 = [540.1812072,428.8112043,292.9031994,126.2860893,59.34550344,12.41724896]
    Temperature001 = [6.52E+26,4.53E+26,2.90E+26,1.63E+26,7.24E+25,1.81E+25]
    Pressure02 = [20.04998126,78.52332902,192.3115829,277.349493,478.3696854,673.3801195, 534.5293833]
    Temperature02 = [1.81E+25,7.24E+25,1.63E+26,2.90E+26,4.53E+26,6.52E+26,5.28E+26]
    Pressure04=sorted([1054.905489,35.39936642,104.00362,194.5955416,349.6985795,651.9660935,790.7878697,871.231327,944.8709097,450.5513026])
    Temperature04=sorted([6.52E+26,1.81E+25,7.24E+25,1.63E+26,2.90E+26,4.53E+26,5.28E+26,5.68E+26,6.09E+26,3.51E+26])
 
    #plotting 0.2 and 0.4 radius points
    plt.plot(Temperature02,Pressure02,'xg',label='0.2')
    plt.plot(Temperature04,Pressure04,'xy',label='0.4')
    

    #fitting straight line to 0.4, 0.2 and 0.01 radius plots
    poly_con, cov_poly_con = np.polyfit(Temperature001,Pressure001,1,cov=True)
    m001 = np.poly1d(poly_con)
    plt.plot(Temperature001,m001(Temperature001),'b',label='0.01') 

    poly_con, cov_poly_con = np.polyfit(Temperature02,Pressure02,1,cov=True)
    m02 = np.poly1d(poly_con)
    plt.plot(Temperature02,m02(Temperature02),'g',label='0.2') 

    plt.plot(Temperature04,Pressure04,'xy')
    poly_con, cov_poly_con = np.polyfit(Temperature04,Pressure04,1,cov=True)
    m04 = np.poly1d(poly_con)
    plt.plot(Temperature04,m04(Temperature04),'y',label='0.4') 

    #chi squared test of straight line fits

    0.01
    exp = []
    for i in Temperature001:
        exp.append(m001(i))
    
    chiSquared = 0
    for i in range(len(Temperature001)):
            chi = (Pressure001[i]-exp[i])**2/(exp[i])
            chiSquared += chi
           
    print(chiSquared,'chi')
    

    exp = []
    for i in Temperature02:
        exp.append(m02(i))
    
    chiSquared = 0
    for i in range(len(Temperature02)):
            chi = (Pressure02[i]-exp[i])**2/(exp[i])
            chiSquared += chi
            
    print(chiSquared,'chi')
    exp = []
    for i in Temperature04:
        exp.append(m04(i))
    
    chiSquared = 0
    for i in range(len(Temperature04)):
            chi = (Pressure04[i]-exp[i])**2/(np.abs(exp[i]))
            chiSquared += chi
            
    print(chiSquared,'chi')

    plt.title('Ideal Gas Test')
    plt.xlabel('Temperature')
    plt.ylabel('Pressure')
    plt.legend()
    plt.savefig('idealgas.png')
    plt.show()


''' 
TASK 14

runnig 2000 collisions and removed first half collisions to allow for enough collisions to make sure all particles
have taken Maxwell-Boltzmann form from initialised velocity (if that is the natural distribution)

fitted distribution with variable scaling and temperature to produce new average temperature value
returned temperature: 8.291618096909064e+23

chi-squared test to determine goodness of fit

'''
        


def velocitiesDistribution():
        
        
        y, binEdges = np.histogram(sim.velocityMagnitudes[1000:], bins=25)
        bincentres = 0.5*(binEdges[1:]+binEdges[:-1])
        plt.bar(bincentres, y , width=0.51, color = "y")
        
        #plt.plot(bincentres,y,'x')
        def maxBolt(x,a,T):
            xSq = []
            for i in range(len(x)):
                xSq.append(x[i]**2)
            ax = []
            for j in range(len(x)):
                ax.append(a*x[j])
            return ax*np.exp((xSq)/(-2*const.k*T))
        initial = [200,1.81074262900998e+25]
        params,params_cov = curve_fit(maxBolt,bincentres,y,initial) 
        plt.plot(bincentres,maxBolt(bincentres,params[0],params[1]),'r')
        plt.xlabel('Velocity')
        plt.ylabel('Number')
        plt.title('Velocity Distribution')
        print(params[1],'temperature')
        
        '''  
        Chi-Squared Test
        Find number value at same velocity value at bin centres
        23 degrees of freedom
        '''
        expected = []
        for i in range(len(bincentres)):
            expected.append(params[0]*bincentres[i]*np.exp((bincentres[i])**2/(-2*const.k*params[1])))
        
        #normalising expected

        sumObs = 0
        for i in y:
            sumObs +=i
        sumExp = 0
        for j in expected:
            sumExp +=j

        normExp = [] 
        for k in expected:
            normExp.append(k*sumObs/sumExp)
        test = np.ones(25)
        norm = [] 
        for k in test:
            norm.append(k*sumObs/25)

        plt.plot(bincentres,normExp,'m')
        plt.savefig('MaxwellBoltzmann.png')
        plt.show()
        
        #chi squared equation
        chiSquared = 0
        for i in range(len(bincentres)):
            chi = (y[i]-normExp[i])**2/normExp[i]
            chiSquared += chi
            #print(chi)
        print(chiSquared)
        ''' 
        Produced chi squared value of 36.462209925860144 which means that the fit is 0.96302 likely to be correct
        '''





'''   
Task 14
a = 0 as ther are no intermolecular forces and so b can be simply found using the gradient of P and T at constant number=20
and volume = 100pi


rearranging P(V-Nb) = NkT

'''
def vanDerwaals():
    Pressure001 = sorted([540.1812072,428.8112043,292.9031994,126.2860893,59.34550344,12.41724896])
    Temperature001 = sorted([6.52E+26,4.53E+26,2.90E+26,1.63E+26,7.24E+25,1.81E+25])
    Pressure01 = sorted([14.69127978,76.28893617,168.9550201,299.9243754,432.3580024,579.7411642])
    Temperature01 = sorted([1.81E+25,7.24E+25,1.63E+26,2.90E+26,4.53E+26,6.52E+26])
    Pressure02 = sorted([20.04998126,78.52332902,192.3115829,277.349493,468.3696854,653.3801195, 518.5293833])
    Temperature02 = sorted([1.81E+25,7.24E+25,1.63E+26,2.90E+26,4.53E+26,6.52E+26,5.28E+26])
    Pressure03 = sorted([22.91222527,87.2805147,219.0781878,365.9550612,452.4357566,783.4192922])
    Temperature03 = sorted([1.81E+25,7.24E+25,2.190781878E+26,2.90E+26,4.53E+26,6.52E+26])
    Pressure04=sorted([1054.905489,35.39936642,104.00362,194.5955416,349.6985795,651.9660935,790.7878697,871.231327,944.8709097,450.5513026])
    Temperature04=sorted([6.52E+26,1.81E+25,7.24E+25,1.63E+26,2.90E+26,4.53E+26,5.28E+26,5.68E+26,6.09E+26,3.51E+26])
 

    #finding the gradient of every Pressure-Time graph
    gradients = []
   
    poly_con, cov_poly_con = np.polyfit(Temperature001,Pressure001,1,cov=True)
    m,c = np.poly1d(poly_con)
    gradients.append(m)

    poly_con1, cov_poly_con1 = np.polyfit(Temperature01,Pressure01,1,cov=True)
    m1,c1 = np.poly1d(poly_con1)
    gradients.append(m1)

    poly_con2, cov_poly_con2 = np.polyfit(Temperature02,Pressure02,1,cov=True)
    m2,c2 = np.poly1d(poly_con2)
    gradients.append(m2)
    poly_con3, cov_poly_con3 = np.polyfit(Temperature03,Pressure03,1,cov=True)
    m3,c3 = np.poly1d(poly_con3)
    gradients.append(m3)
    
    poly_con4, cov_poly_con4 = np.polyfit(Temperature04,Pressure04,1,cov=True)
    m4,c4 = np.poly1d(poly_con4)
    gradients.append(m4)

    #finding b values for every radius
    allb=[]
    for i in gradients:
        b = (100*np.pi/20)-const.k/i
        allb.append(b)

    radius = [0.01,0.1,0.2,0.3,0.4]
    plt.plot(radius,allb,'x')
    def squared(x,a,b):
        return a*np.square(x) + b
    initial = [10,-0.1]
    params,params_cov = curve_fit(squared,radius,allb,initial,maxfev=100000) 
    x = np.linspace(0,0.4,20)
    plt.plot(x,squared(x,params[0],params[1]),'')
    #plt.plot(Temperature001,m(Temperature001),'b',label='a=0,b=15.7079,ballRadius=0.01,averageSpeed=30') 
    plt.xlabel('Radius')
    plt.ylabel('Gas Constant, b')
    plt.title('Van Der Waals')
    plt.legend()
    plt.savefig('VanDerWaals.png')

    plt.show()

''' 
RUNNING SIMULATION
-generates particles and adds them to the simulation
-adds container
-runs the simulation
'''
''' 
run plots below, initialisation and running kept separate and not run as one function for flexibility
'''
sim = Simulation()
sim = Simulation()
parts = Particles()
con = Container()
parts.randomPositions()
parts.randomVelocities()
sim.addParticles()
sim.addContainer()
sim.run(1)
#comment out above to run ideal gas and maxwell plots
averagePressure()
averageTemperature()

numberPressure()

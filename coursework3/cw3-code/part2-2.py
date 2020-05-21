import numpy as np
import matplotlib.pyplot as plot
import decimal 
import random as rnd 

# Useful scaling tools 
ms = 0.001
mV = 0.001 
bigMOhm = 1000000
nA = 0.000000001
nS = 0.000000001

# Parameters in the integrate and fire model 
membraneTimeConstant = 10*ms 
leakyReversalPotential = -65*mV
resetPotential = leakyReversalPotential
membraneResistance = 100*bigMOhm
electrodeInputCurrent = 0*nA
thresholdPotential = -50*mV
averageFiringRate = 15

rmie = membraneResistance*electrodeInputCurrent

# Synapse parameters
gs = 4*nS
maxs = 0.5
synapseTimeConstant = 2*ms 
synapseReversalPotential = 0*mV
nrIncomingSynapses = 40

# STDP parameters 
STDP = True 
aplus = 0.2*nS
aminus = 0.25*nS 
plusTimeConstant = 20*ms
minusTimeConstant = 20*ms 

def synapsecurrent(v):
    output =  0
    for i in range(nrIncomingSynapses):
        rmgspsves = gsynapses[i]*synapses[i]*membraneResistance*(v-synapseReversalPotential)
        output += rmgspsves
    return output

def f(v):
    return (leakyReversalPotential-v-synapsecurrent(v)+rmie)/membraneTimeConstant

def p(ps):
    return -ps/synapseTimeConstant

## The initial condition 
v0 = resetPotential

## Timestep and total time 
dt = 0.25*ms
T = 1
t = np.linspace(0, T, int(T/dt)+1)
spike_train = np.zeros(len(t))
synapses = np.zeros(nrIncomingSynapses)
presynapseSpikeTime = np.zeros(nrIncomingSynapses)
postsynapseSpikeTime = -1

# np.random.seed(1)
randomnumbers = np.random.random([len(t),40])

def stdp(t):
    if t > 0:
        return aplus*np.exp(-np.abs(t)/plusTimeConstant)
    else:
        return -aminus*np.exp(-np.abs(t)/minusTimeConstant)

gsynapses = [gs]*nrIncomingSynapses
spike_train[0] = v0
gsynapsesChanges = np.zeros([40,len(t)])

for i in range(1, len(t)):
    # For each synapse, see if it fired an action potential in this time slice 
    for j in range(nrIncomingSynapses):
        if randomnumbers[i-1,j] < averageFiringRate*dt:
            presynapseSpikeTime[j] = (i-1)*dt
            synapses[j] += maxs
        else:
            synapses[j] = synapses[j]+p(synapses[j])*dt 

    if STDP:
        for j in range(nrIncomingSynapses):
            gsynapses[j] += stdp(postsynapseSpikeTime-presynapseSpikeTime[j])
            if gsynapses[j] > 4*nS:
                gsynapses[j] = 4*nS
            elif gsynapses[j] < 0:
                gsynapses[j] = 0
            gsynapsesChanges[j,i-1] = gsynapses[j]

    if spike_train[i-1] > thresholdPotential:
        postsynapseSpikeTime = (i-1)*dt
        spike_train[i-1] = 0*mV
        spike_train[i] = resetPotential
    else:
        spike_train[i] = spike_train[i-1]+f(spike_train[i-1])*dt    


for i in range(nrIncomingSynapses):
    plot.plot(t,gsynapsesChanges[i])
np.savetxt('gsynapses.csv',gsynapsesChanges,delimiter=',')
plot.plot(t,spike_train)
plot.show()

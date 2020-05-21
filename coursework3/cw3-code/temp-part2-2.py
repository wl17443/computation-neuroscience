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

## The initial condition 
v0 = resetPotential

## Parameters to simulate postsynapse voltage 
dt = 0.25*ms
T = 300
t = np.linspace(0, T, int(T/dt)+1)
spike_train = np.zeros(len(t))
spike_train2 = np.zeros(len(t))
# Simulate 40 spike trains due to poisson process 
randomnumbers = np.random.random([len(t),40])
presynapseSpikeTrains = np.zeros([len(t),40])
for i in range(len(t)):
    for j in range(40):
        if randomnumbers[i,j] < dt*averageFiringRate:
            presynapseSpikeTrains[i,j] = 1

presynapsestats = np.zeros([40,3])
for i in range(40):
    presynapsestats[i,0] = gs

postsynapseSpikeTime = -1000*ms

def synapsecurrent(v):
    output =  0
    for i in range(nrIncomingSynapses):
        rmgspsves = presynapsestats[i,0]*presynapsestats[i,1]*membraneResistance*(v-synapseReversalPotential)
        output += rmgspsves
    return output

def f(v):
    return (leakyReversalPotential-v-synapsecurrent(v)+rmie)/membraneTimeConstant

def p(ps):
    return -ps/synapseTimeConstant

def stdp(t):
    if t > 0:
        return aplus*np.exp(-np.abs(t)/plusTimeConstant)
    else:
        return -aminus*np.exp(-np.abs(t)/minusTimeConstant)

for i in range(1, len(t)):
    for j in range(40):
        if presynapseSpikeTrains[i-1,j] == 1:
            presynapsestats[j,2] = (i-1)*dt
            presynapsestats[j,1] += maxs 
            if STDP:
                presynapsestats[j,0] += stdp(postsynapseSpikeTime-(i-1)*dt)
                if presynapsestats[j,0] > 4*nS:
                    presynapsestats[j,0] = 4*nS
                elif presynapsestats[j,0] < 0:
                    presynapsestats[j,0] = 0 
        else:
            presynapsestats[j,1] = presynapsestats[j,1] + p(presynapsestats[j,1])*dt 

    if spike_train[i-1] > thresholdPotential:
        postsynapseSpikeTime = (i-1)*dt
        spike_train[i-1] = 0*mV
        spike_train[i] = resetPotential
        spike_train2[i-1] = 1
        if STDP and presynapseSpikeTrains[i-1,j] == 0:
            for j in range(40):
                presynapsestats[j,0] += stdp(postsynapseSpikeTime-presynapsestats[j,2])
                if presynapsestats[j,0] > 4*nS:
                    presynapsestats[j,0] = 4*nS
                elif presynapsestats[j,0] < 0:
                    presynapsestats[j,0] = 0 
    else:
        spike_train[i] = spike_train[i-1]+f(spike_train[i-1])*dt   

    for x in range(40):
        presynapseSpikeTrains[i-1,x] = presynapsestats[x,0] 

np.savetxt('spike_train.csv',spike_train2,delimiter=', ')
presynapseSpikeTrains = presynapseSpikeTrains.T
np.savetxt('gsynapses.csv',presynapseSpikeTrains,delimiter=', ')
# for i in range(40):
#     plot.plot(t,presynapseSpikeTrains[i])
# plot.show()
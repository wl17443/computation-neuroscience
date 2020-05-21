import numpy as np
import matplotlib.pyplot as plot
import decimal 

# Useful scaling tools 
ms = 0.001
mV = 0.001 
bigMOhm = 1000000
nA = 0.000000001

# Parameters in the integrate and fire model 
membraneTimeConstant = 10*ms 
leakyReversalPotential = -70*mV
resetPotential = leakyReversalPotential
membraneResistance = 10*bigMOhm
electrodeInputCurrent = (3.1)*nA
thresholdPotential = -40*mV

# range function but with floats 
def drange(x, y, jump):
  while x < y:
    yield float(x)
    x += decimal.Decimal(jump)


# Using euler's method to approximate spike-train 

def f(v):
    return (leakyReversalPotential-v+rmie)/membraneTimeConstant

## The initial condition 
v0 = resetPotential

## Timestep and total time 
dt = 0.25*ms
T = 1
t = np.linspace(0, T, int(T/dt)+1)
spike_train = np.zeros(len(t))
di = 0.1
currents = np.linspace(2, 5, int((5-2)/di)+1)
numberofspikes = np.zeros(len(currents))

for j in range(len(currents)):
    electrodeInputCurrent = currents[j]*nA
    rmie = membraneResistance*electrodeInputCurrent
    spike_train[0] = v0
    for i in range(1, len(t)):
        spike_train[i] = spike_train[i-1]+f(spike_train[i-1])*dt
        # if spike_train[i] >= thresholdPotential:
        #     spike_train[i] = resetPotential 

    total = 0 
    for i in range(len(spike_train)):
        if spike_train[i] >= thresholdPotential:
            total += 1
    numberofspikes[j] = total 

print(numberofspikes)
plot.figure ()
plot.plot(currents,numberofspikes)
plot.title("Firing Rate as the Function of the Input Current")
plot.xlabel("Input Current (nA)")
plot.ylabel("Firing Rate")
plot.show()
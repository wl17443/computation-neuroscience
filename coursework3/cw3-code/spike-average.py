import numpy as np 
import csv
import matplotlib.pyplot as plot 

ms=0.001
## Parameters to simulate postsynapse voltage 
dt = 0.25*ms
T = 300
t = np.linspace(0, T, int(T/dt)+1)

firingtimes = []
with open('spike_train.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        firingtimes.append(float(row[0]))

binsize = 10 
result = np.zeros(31)
for i in range(len(firingtimes)):
    if firingtimes[i] == 1:
        index = i*dt/10
        result[int(index)] += 1
result[30] = result[29]
print(result)
for i in range(len(result)):
    result[i] = result[i]/10
plot.plot(range(0,310,10),result)
plot.title('Average Firing Rate of the Postsynaptic Neuron as a Function of Time')
plot.xlabel('Time (s)')
plot.ylabel('Average Firing Rate (Hz)')
plot.show()
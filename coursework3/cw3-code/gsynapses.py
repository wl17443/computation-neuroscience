import numpy as np 
import matplotlib.pyplot as plot 

ms=0.001
## Parameters to simulate postsynapse voltage 
dt = 0.25*ms
T = 300
t = np.linspace(0, T, int(T/dt)+1)

gsynapses = np.genfromtxt('gsynapses.csv', delimiter=", ")
steady_gsynapses = [[] for i in range(40)]
# for i in range(len(t)):
#     for j in range(40):
#         if  steady_gsynapses[j] == []:
#             steady_gsynapses[j].append(gsynapses[j,i])
#         elif gsynapses[j,i] != steady_gsynapses[j][-1]:
#             steady_gsynapses[j].append(gsynapses[j,i])

# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plot.hist(x=gsynapses, bins='auto',
                            alpha=0.7, rwidth=0.85)
plot.grid(axis='y', alpha=0.75)
plot.xlabel('Weight')
plot.ylabel('Frequency')
plot.title('Histogram of the Steady-State Synaptic Weights After One Run of the Simulation')
plot.text(23, 45, r'$\mu=15, b=3$')
maxfreq = n.max()
# Set a clean upper y-axis limit.
plot.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)




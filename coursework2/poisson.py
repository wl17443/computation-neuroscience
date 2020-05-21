import random as rnd
import numpy as np
from load import load_data 
import matplotlib.pyplot as plot

def get_spike_train(rate,big_t,tau_ref):

    if 1<=rate*tau_ref:
        print("firing rate not possible given refractory period f/p")
        return []

    exp_rate=rate/(1-tau_ref*rate)

    spike_train=[]

    t=rnd.expovariate(exp_rate)

    while t< big_t:
        spike_train.append(t)
        t+=tau_ref+rnd.expovariate(exp_rate)

    return spike_train

def fano_factor(spike_train,interval,big_t):
    totalSpikes = len(spike_train)
    spikesInInterval = [0] * (int) (big_t/interval)
    for i in range(totalSpikes):
        index = int(np.floor(spike_train[i]/interval))
        spikesInInterval[index] += 1
    average = sum(spikesInInterval)/len(spikesInInterval)
    for i in range(len(spikesInInterval)):
        spikesInInterval[i] = (spikesInInterval[i] - average) ** 2
    variance = sum(spikesInInterval)/len(spikesInInterval)
    fano = variance/average 
    return fano 

def data2TimedSpikes(spikes,interval):
    spike_train = []
    for i in range(len(spikes)):
        if spikes[i] == 1:
            spike_train.append(i*interval)
    return spike_train

def coefficientOfVariation(spike_train):
    isi = []
    totalSpikes = len(spike_train)
    for i in range(totalSpikes-1):
        isi.append(spike_train[i+1]-spike_train[i])
    average = sum(isi)/len(isi)
    for i in range(len(isi)):
        isi[i] = (isi[i] - average) ** 2
    cov = np.sqrt(sum(isi)/len(isi))/average 
    return cov

# def autocorrelate(spike_train,data):
#     for i in range(3000):
#         for j in range(3000):
#             difference = spike_train[i] - spike_train[j]
#             index = int(np.round(difference/ms+100))
#             if index < 200 and index >= 0:
#                 data[index] += 1
#     for i in range(len(data)):
#         data[i] = data[i]/3000

def autocorrelate(spike_train):
    output = []
    for i in range(3000):
        for j in range(3000):
            difference = (spike_train[i] - spike_train[j]) / ms
            if difference >= -100 and difference <= 100:
                output.append(difference)
    return output

def spike_trig_average(spike_train, stimulus):
    output = [0] * 50
    spikes = 0
    for i in range(len(spike_train)):
        if spike_train[i] == 1:
            spikes += 1
            index = i 
            while index >= 0 and i-index <= 50:
                output[49-(i-index)] = output[49-(i-index)] + stimulus[index]
                index -= 1
    for i in range(len(output)):
        output[i] = output[i]/spikes
    return output

Hz=1.0
sec=1.0
ms=0.001

rate=35.0*Hz
tau_ref=0*ms

big_t=1000*sec
interval = 10*ms

spike_data = load_data("rho.dat",int)
stimulus_data = load_data("stim.dat",float)
spike_train = data2TimedSpikes(spike_data,2*ms)

hist_data = autocorrelate(spike_train)
plot.hist(hist_data,bins=range(-100,100),normed=1)
plot.xlabel('Offset (ms)')
plot.ylabel('Spikes')
plot.title(r'Autocorrelogram')
plot.show()

spike_trig = spike_trig_average(spike_data, stimulus_data)
plot.plot(range(-100,0,2),spike_trig)
plot.xlabel('τ (ms)')
plot.ylabel('Spike Triggered Average C(τ)')
plot.title(r'The Spike Triggered Average')
plot.show()
import os

import numpy as np
import matplotlib.pyplot as plt

analysis_portion = 0.2

reference = {}
with open('data/reference.dat','r') as f:
    for line in f:
        if line.startswith('#'):
            continue
        else:
            name, experiment, simulation = line.split()
            experiment = float(experiment)
            simulation = float(simulation)
            #print(name, experiment, simulation)
            reference[name] = (experiment, simulation)

# Load VLMP values
for name in reference:
    resultsFolder = 'results/results/'
    # Create empty numpy array, just one row
    data = np.empty((1))
    # Iterate over all folders in resultsFolder that start with name
    for folder in os.listdir(resultsFolder):
        if folder.startswith(name):
            dataLocal = np.loadtxt(resultsFolder +'/'+ folder + '/gyrationRadius.dat')

            # Extract the last analysis_portion% of the data
            dataLocal = dataLocal[int(len(dataLocal)*(1-analysis_portion)):][:,1]
            data = np.append(data, dataLocal)

    mean = np.mean(data)
    error  = np.std(data)/np.sqrt(len(data))
    reference[name] = (reference[name][0], reference[name][1], mean, error)

plt.figure(figsize=(10,10))
plt.title('Comparison of experimental, reference simulation and VLMP')

# X axis, experiment names
# experiment black dots
# simulation green pentagons
# vlmp red triangles

x = np.arange(len(reference))
plt.xticks(x, reference.keys(), rotation=90)

# Plot the experimental values
y = [reference[name][0] for name in reference]
plt.plot(x, y, 'k-o', label='Experiment', linewidth=2, markersize=10)

# Plot the reference simulation values
y = [reference[name][1] for name in reference]
plt.plot(x, y, 'g-p', label='Reference simulation', linewidth=2, markersize=10)

# Plot the VLMP values, with error bars
y = [reference[name][2] for name in reference]
yerr = [reference[name][3] for name in reference]
plt.errorbar(x, y, yerr=yerr, fmt='r-^', label='VLMP', linewidth=2, markersize=10)

plt.ylim(0.0, 100.0)

# Add grid
plt.grid(True)

plt.legend()
plt.show()


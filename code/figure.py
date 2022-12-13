import matplotlib.pyplot as plt
import numpy as np
import sys


if len(sys.argv) != 3:
    print("Usage: python3 figure.py <results.csv> <figure.png>")
    sys.exit(1)

# Get results from csv
results = np.genfromtxt(sys.argv[1], delimiter=',')

# Plot results
fig, axs = plt.subplots(3, figsize=(10, 8))
axs[0].plot(results[:, 0], results[:, 1], label="Quality")
axs[0].plot(results[:, 0], results[:, 2], label="Sharpen")
axs[0].plot(results[:, 0], results[:, 3], label="Noise")
axs[0].set_ylabel("Actuator value")
axs[0].legend()
axs[1].plot(results[:, 0], results[:, 4], label="Similarity")
axs[1].set_ylabel("Similarity")
axs[2].plot(results[:, 0], results[:, 5], label="Size")
axs[2].set_ylabel("Size")

# Save figure
plt.savefig(sys.argv[2])

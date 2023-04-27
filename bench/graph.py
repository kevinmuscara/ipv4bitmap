import matplotlib.pyplot as plt
import numpy as np

# Data for the benchmarks
addresses = [6561]
time_seconds = [533.64]
network_bytes = [1108992]
network_mb = [1.11]
memory_bytes = [39305216]
memory_mb = [39.31]

# Plotting the benchmarks
labels = [f'{addr}' for addr in addresses]
x = np.arange(len(labels))
width = 0.4

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting time in seconds
ax.bar(x - width/2, time_seconds, width, label='Time (seconds)')

# Plotting network in MB
ax.bar(x, network_mb, width, label='Network (MB)', color='orange')

# Plotting memory in MB
ax.bar(x + width/2, memory_mb, width, label='Memory (MB)', color='green')

# Adjusting axes labels and ticks
ax.set_xlabel('Addresses')
ax.set_ylabel('Time (seconds) / Network (MB) / Memory (MB)')
ax.set_title('Benchmarks')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Displaying the plot
plt.tight_layout()
plt.show()

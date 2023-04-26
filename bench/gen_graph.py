import matplotlib.pyplot as plt
import numpy as np

# Data for the benchmarks
worker_threads = [16, 32, 16, 32]
addresses = [625, 625, 10000, 10000]
time_seconds = [9.61, 5.20, 156.98, 79.83]
memory_bytes = [33701888, 25329664, 88342528, 26001408]
memory_mb = [33.7, 25.33, 88.34, 26.00]

# Plotting the benchmarks
labels = ['16 (625)', '32 (625)', '16 (10,000)', '32 (10,000)']
x = np.arange(len(labels))
width = 0.4

fig, ax = plt.subplots(figsize=(10, 6))

# Plotting time in seconds
ax.bar(x - width/2, time_seconds, width, label='Time (seconds)')

# Plotting memory in MB
ax.bar(x + width/2, memory_mb, width, label='Memory (MB)', color='green')

# Adjusting axes labels and ticks
ax.set_xlabel('Worker Threads (Addresses)')
ax.set_ylabel('Time (seconds) / Memory (MB)')
ax.set_title('Benchmarks')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

# Displaying the plot
plt.tight_layout()
plt.show()

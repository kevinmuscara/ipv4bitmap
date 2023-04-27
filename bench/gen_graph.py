import matplotlib.pyplot as plt
import numpy as np

# Data for the benchmarks
worker_threads = [16, 32, 64, 128, 256, 512, 16, 32, 64, 128, 256, 512]
addresses = [625, 625, 625, 625, 625, 625, 10000, 10000, 10000, 10000, 10000, 10000]
time_seconds = [9.61, 5.20, 3.21, 2.25, 1.91, 6.00, 156.98, 79.83, 43.43, 26.94, 50.62, 62.11]
network_bytes = [125952, 121856, 116736, 117760, 104448, 86016, 2307072, 2224128, 2124800, 2105344, 2228224, 1292288]
network_mb = [0.13, 0.12, 0.12, 0.12, 0.1, 0.08, 2.31, 2.22, 2.12, 2.10, 2.22, 1.29]
memory_bytes = [33701888, 25329664, 37863424, 39043072, 63193088, 37027840, 88342528, 26001408, 47087616, 73465856, 31391744, 142639104]
memory_mb = [33.7, 25.33, 37.86, 39.04, 63.19, 37.02, 88.34, 26.00, 47.08, 73.46, 31.39, 142.63]

# Plotting the benchmarks
labels = [f'{wt} ({addr})' for wt, addr in zip(worker_threads, addresses)]
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
ax.set_xlabel('Worker Threads (Addresses)')
ax.set_ylabel('Time (seconds) / Network (MB) / Memory (MB)')
ax.set_title('Benchmarks')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90)
ax.legend()

# Displaying the plot
plt.tight_layout()
plt.show()

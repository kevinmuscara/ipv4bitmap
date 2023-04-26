# Pinging the internet
Inspired by [Tom7's Harder Drive](http://tom7.org/harder/) project, this repo provides the utilities to ping every IP address in the IPv4 address space.

## Create IP List
There are 2^32 possible IP addresses, or around 4.2 billion addresses. The output list will be stored in `ip_list.txt`.

### Exponential Range
To skip addresses and create a list within a range of `range^4`, use the `generate_ip_list.py` script:

```shell
sudo python3 generate_ip_list.py <range>
```

Provide a 0-256 range value.
**NOTE: This script requires elevated privilages to write to the output file**

Example Usage:
```shell
sudo python3 generate_ip_list.py 1
```

Output:
```
0.0.0.0
```

### Ordered Range
To create an IP list between a defined IP range, use the `generate_ip_range.py` script:

```shell
sudo python3 generate_ip_range.py <start_range> <end_range>
```

Provide a start and end range between `0.0.0.0` to `255.255.255.255`.

Example Usage:
```shell
sudo python3 generate_ip_range.py 0.0.0.0 0.0.0.5
```

Output:
```
0.0.0.0
0.0.0.1
0.0.0.2
0.0.0.3
0.0.0.4
0.0.0.5
```

## Pinging IPs
There are three scripts for pinging the IPs from the `ip_list.txt`. See below:
**NOTE: Sending ICMP echo requires elevated permissions, use sudo for all scripts below**

All scripts will output to `icmp_responses.txt`. See the sample output below:

`1` is alive, `0` is dead.

```
0.0.0.0,0
0.0.0.1,0
0.0.1.0,0
0.0.1.1,0
0.1.0.0,0
0.1.0.1,0
0.1.1.0,0
0.1.1.1,0
1.0.0.0,0
1.0.0.1,1
1.0.1.0,0
1.0.1.1,0
1.1.0.0,0
1.1.0.1,0
1.1.1.0,1
1.1.1.1,1
```

### No delay 
Use the no delay script for smaller amounts (>625) of IPs. To send ICMP echos without a delay, run the `ping_no_delay.py` script:

```shell
sudo python3 ping_no_delay.py
```

### Chunk/Delay
Use the chunk delay script for large amounts (>2000) of IPs. ICMP echo utilizes a lot of bandwidth, therefore we need to limit the requests sent out into chunks. run the `ping_delay.py` script:

```shell
sudo python3 ping_delay.py
```

You can modify the `chunk_size` and `delay_between_chunks` variables to increase the amount of data sent. The larger the chunk size, the larger the delay should be.

```python
chunk_size = 300 # Amount sent in each batch
delay_between_chunks = 10 # Seconds idle between each sent batch

for i in range(0, len(ip_addresses), chunk_size):
    chunk = ip_addresses[i:i + chunk_size]
    chunk_results = await asyncio.gather(*[check_ip(ip) for ip in chunk])
    results.extend(chunk_results)

    if i + chunk_size < len(ip_addresses):
        await asyncio.sleep(delay_between_chunks)
```

### Worker threads
Use the worker thread script for extremely large amounts (>10000) of IPs. Use the [benchmarks](#benchmarks) below to get an idea of how many threads to use for your batch size. run the `ping_worker.py` script:

```shell
sudo python3 ping_worker.py
```

You can modify the `NUM_THREADS` variable to use more or less threads.

```python
NUM_THREADS = 128

# Add tasks to the queue
for i in range(0, len(ip_addresses), chunk_size):
    chunk = ip_addresses[i:i + chunk_size]
    for ip in chunk:
        task_queue.put(ip)

# Create a pool of worker threads
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)
``` 

## Image Output
To view the results as a bitmap image with black pixels representing dead hosts, and white pixels representing alive hosts, we can use the `create_map.py` script:

**NOTE: If you run this with elevated privilages, you will get permission issues viewing the image.**

```shell
python3 create_map.py
```

View the sample outputs below:

### 10,000 Addresses
![10,000 Addresses](10k.png "10,000 Addresses")

### 50,000 Addresses
![50,000 Addresses](50k.png "50,000 Addresses")

### 100,000 Addresses
![100,000 Addresses](104k.png "100,000 Addresses")

## Benchmarks
Benchmarks using [worker thread](#worker-threads) system.

### 16 worker threads (625 addresses): 

- 9.61 seconds
- 125952 bytes (network) 0.13 MB
- 33701888 bytes (memory) 33.7 MB

### 32 worker threads (625 addresses):

- 5.20 seconds
- 121856 bytes (network) 0.12 MB
- 25329664 bytes (memory) 25.33 MB

### 16 worker threads (10,000 addresses): 

- 156.98 seconds
- 2307072 bytes (network) 2.31 MB
- 88342528 bytes (memory) 88.34 MB

### 32 worker threads (10,000 addresses):

- 79.83 seconds
- 2224128 bytes (network) 2.22 MB
- memory unmeasured
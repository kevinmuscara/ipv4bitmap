## Creating all possible IPs
There are 2^32 possible IP addresses, or around 4.2 billion.

In `generate_ip_list.py`, modify loop range to create more or less IPs:
```python
for a in range(<number>):
  for b in range(<number>):
      for c in range(<number>):
          for d in range(<number>):
```

Ideally for each octect, your range will be the same number. This equates to number^4 IP addresses created. If your range is 10, the script will create the first 10,000 possible IP Addresses.

This will output a list of IPs into `ip_list.txt`.

**NOTE: I would not recommend going above 100 unless you have a lot of RAM.**

## Pinging IPs
To ping the IPs from the `ip_list.txt` file run the `ping_ip_list.py` script.

**NOTE: Sending ICMP echo requires elevated permissions**
```shell
sudo python3 ping_ip_list.py
```

This will output all ICMP requests as a 0 if it is dead, or 1 if it is alive.

Sample output:
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

## Network Limitations
Sending large amounts of ICMP echo requests requires sending a lot of data out, therefore we need to add a wait between a certain batch size. Use the `ping_with_delay.py` file to send large amounts of ICMP pings.

Modify the `chunk_size` and `delay_between_chunks` variables to increase the amount of data sent. The larger the chunk size, the larger the delay should be.
```python
chunk_size = 300
delay_between_chunks = 10

for i in range(0, len(ip_addresses), chunk_size):
    chunk = ip_addresses[i:i + chunk_size]
    chunk_results = await asyncio.gather(*[check_ip(ip) for ip in chunk])
    results.extend(chunk_results)

    if i + chunk_size < len(ip_addresses):
        await asyncio.sleep(delay_between_chunks)
```

## Queue with Worker Threads
For better performance, we can use worker threads. Use the `ping_worker.py` file to send large amounts of ICMP pings using thread workers.

Modify the `NUM_THREADS` variable to use more or less threads.
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

## Worker Thread Benchmarks
Benchmarks for ICMP echos using thread system.

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
- memory unmeasurable
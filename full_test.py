import argparse
import asyncio
import aioping
import psutil
import time
import queue
import threading
import sys

# Create a task queue
task_queue = queue.Queue()

async def check_ip(ip):
    try:
        delay = await aioping.ping(ip, timeout=0.25)
        print(f"{ip} is alive ({delay} ms)")
        return f"{ip},1"
    except TimeoutError:
        print(f"{ip} is dead")
        return f"{ip},0"
    except Exception as e:
        return f"Error checking {ip}: {e}"

def worker():
    while True:
        # Get a task from the queue
        try:
            task = task_queue.get(block=False)
        except queue.Empty:
            # If the queue is empty, exit the thread
            return

        # Execute the task
        result = asyncio.run(check_ip(task))

        # Add the result to the list
        results.append(result)

def generate_ip_range(start_ip, end_ip):
    def ip_to_int(ip):
        octets = ip.split('.')
        return int(octets[0]) * 256**3 + int(octets[1]) * 256**2 + int(octets[2]) * 256 + int(octets[3])

    def int_to_ip(num):
        octet_d = num % 256
        num //= 256
        octet_c = num % 256
        num //= 256
        octet_b = num % 256
        num //= 256
        octet_a = num
        return f"{octet_a}.{octet_b}.{octet_c}.{octet_d}"

    start_int = ip_to_int(start_ip)
    end_int = ip_to_int(end_ip)

    ip_addresses = []
    for i in range(start_int, end_int + 1):
        ip = int_to_ip(i)
        ip_addresses.append(ip)

    return ip_addresses

def check_ips(ip_addresses, num_threads):
    print(f"Checking {len(ip_addresses)} IP addresses...")

    chunk_size = 300
    delay_between_chunks = 5  # Adjust this value to set the wait time between chunks

    global results
    results = []

    # Add tasks to the queue
    for i in range(0, len(ip_addresses), chunk_size):
        chunk = ip_addresses[i:i + chunk_size]
        for ip in chunk:
            task_queue.put(ip)

    # Create a pool of worker threads
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    # Wait for all worker threads to finish
    for t in threads:
        t.join()

    return results

def get_network_usage():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.used, memory.total

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ping a range of IP addresses.')
    parser.add_argument('start_ip', type=str, help='Start IP address')
    parser.add_argument('end_ip', type=str, help='End IP address')
    parser.add_argument('--threads', type=int, default=32, help='Number of worker threads to use.')
    args = parser.parse_args()

    try:
        start_time = time.time()
        start_sent, start_recv = get_network_usage()
        start_used_mem, total_mem = get_memory_usage()

        # Generate IP range
        ip_addresses = generate_ip_range(args.start_ip, args.end_ip)

        # Check IPs using ping worker
        results = check_ips(ip_addresses, args.threads)

        # Write results to file
        with open("icmp_responses.txt", "w") as f:
            for result in results:
                f.write(result + "\n")

        end_time = time.time()
        end_sent, end_recv = get_network_usage()
        end_used_mem, _ = get_memory_usage()

        execution_time = end_time - start_time
        sent_data = end_sent - start_sent
        recv_data = end_recv - start_recv
        used_mem_diff = end_used_mem - start_used_mem

        print(f"Execution time: {execution_time:.2f} seconds")
        print(f"Network usage: sent {sent_data} bytes, received {recv_data} bytes")
        print(f"Memory usage: used {used_mem_diff} bytes out of {total_mem} bytes")

    except Exception as e:
        print(f"Error: {e}")
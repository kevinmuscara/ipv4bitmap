import argparse
import asyncio
import aioping
import psutil
import time
import queue
import threading

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

def check_ips(ip_list_file, output_file, num_threads):
    with open(ip_list_file, 'r') as f:
        ip_addresses = f.read().splitlines()

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

    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + "\n")

    print(f"Finished. {len(results)} IP addresses checked.")

def get_network_usage():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.used, memory.total

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ping a list of IP addresses.')
    parser.add_argument('--threads', type=int, default=32, help='Number of worker threads to use.')
    args = parser.parse_args()

    try:
        start_time = time.time()
        start_sent, start_recv = get_network_usage()
        start_used_mem, total_mem = get_memory_usage()

        check_ips("ip_list.txt", "icmp_responses.txt", args.threads)

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

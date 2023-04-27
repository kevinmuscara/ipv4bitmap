import argparse
import psutil
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor

def check_ip(ip):
    try:
        ping_command = ["ping", "-c", "1", "-W", "1.5", ip]
        ping_process = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = ping_process.communicate()

        if ping_process.returncode == 0:
            print(f"{ip} is alive")
            return f"{ip},1"
        else:
            print(f"{ip} is dead")
            return f"{ip},0"
    except Exception as e:
        return f"Error checking {ip}: {e}"

def check_ips(ip_list_file, output_file):
    with open(ip_list_file, 'r') as f:
        ip_addresses = f.read().splitlines()

    print(f"Checking {len(ip_addresses)} IP addresses...")

    results = []

    with ThreadPoolExecutor() as executor:
        ping_futures = [executor.submit(check_ip, ip) for ip in ip_addresses]

        for future in ping_futures:
            result = future.result()
            results.append(result)

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
    args = parser.parse_args()

    try:
        start_time = time.time()
        start_sent, start_recv = get_network_usage()
        start_used_mem, total_mem = get_memory_usage()

        check_ips("ip_list.txt", "icmp_responses.txt")

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

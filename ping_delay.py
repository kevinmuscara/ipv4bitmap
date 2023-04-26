import asyncio
import aioping
import psutil
import time
import argparse

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


async def check_ips(ip_list_file, output_file, chunk_size, delay_between_chunks):
    with open(ip_list_file, 'r') as f:
        ip_addresses = f.read().splitlines()

    print(f"Checking {len(ip_addresses)} IP addresses...")

    results = []

    for i in range(0, len(ip_addresses), chunk_size):
        chunk = ip_addresses[i:i + chunk_size]
        chunk_results = await asyncio.gather(*[check_ip(ip) for ip in chunk])
        results.extend(chunk_results)

        if i + chunk_size < len(ip_addresses):
            await asyncio.sleep(delay_between_chunks)

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


def parse_arguments():
    parser = argparse.ArgumentParser(description='IP Address Checker')
    parser.add_argument('--chunk', type=int, default=300, help='Number of IP addresses to process in each chunk')
    parser.add_argument('--delay', type=int, default=5, help='Time delay between processing each chunk')

    return parser.parse_args()


if __name__ == '__main__':
    try:
        start_time = time.time()
        start_sent, start_recv = get_network_usage()
        start_used_mem, total_mem = get_memory_usage()

        args = parse_arguments()
        asyncio.run(
            check_ips("ip_list.txt", "icmp_responses.txt", args.chunk, args.delay)
        )

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

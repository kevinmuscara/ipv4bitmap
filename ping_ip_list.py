import asyncio
import aioping

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

async def check_ips(ip_list_file, output_file):
    with open(ip_list_file, 'r') as f:
        ip_addresses = f.read().splitlines()

    print(f"Checking {len(ip_addresses)} IP addresses...")

    results = await asyncio.gather(*[check_ip(ip) for ip in ip_addresses])

    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + "\n")

    print(f"Finished. {len(results)} IP addresses checked.")

try:
    asyncio.run(check_ips("ip_list.txt", "icmp_responses.txt"))
except Exception as e:
    print(f"Error: {e}")

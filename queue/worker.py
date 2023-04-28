import argparse
import subprocess
import multiprocessing
import pika
import time
import psutil

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


def callback(ch, method, properties, body):
    ip = body.decode()
    response = check_ip(ip)
    with open("ping_results.txt", "a") as file:
        file.write(f"{response}\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def run_worker():
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='ip_queue')

    # Set the number of concurrent workers
    channel.basic_qos(prefetch_count=100)

    # Infinite loop to listen for messages
    while True:
        method_frame, header_frame, body = channel.basic_get(queue='ip_queue', auto_ack=False)
        if method_frame:
            # A message was retrieved
            callback(channel, method_frame, header_frame, body)
        else:
            # The queue is empty
            break

    # Close the connection
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run multiple worker processes')
    parser.add_argument('num_workers', type=int, help='number of worker processes to run')

    args = parser.parse_args()
    num_workers = args.num_workers

    start_time = time.time()

    # Run the specified number of worker processes
    processes = []
    for _ in range(num_workers):
        process = multiprocessing.Process(target=run_worker)
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print runtime statistics
    print(f"Runtime: {elapsed_time:.2f} seconds")

    # Print network usage
    net_usage = psutil.net_io_counters()
    print(f"Network Usage:\n"
          f" - Bytes Sent: {net_usage.bytes_sent}\n"
          f" - Bytes Received: {net_usage.bytes_recv}")

    # Print memory usage
    mem_usage = psutil.virtual_memory()
    print(f"Memory Usage:\n"
          f" - Total Memory: {mem_usage.total}\n"
          f" - Available Memory: {mem_usage.available}\n"
          f" - Used Memory: {mem_usage.used}\n"
          f" - Memory Usage Percentage: {mem_usage.percent}%")

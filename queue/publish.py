import pika
import sys

start_ip = sys.argv[1]
end_ip = sys.argv[2]

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

# Establish a connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='ip_queue')

for i in range(start_int, end_int + 1):
    ip = int_to_ip(i)
    channel.basic_publish(exchange='', routing_key='ip_queue', body=ip)

print("Complete.")

# Close the connection
connection.close()
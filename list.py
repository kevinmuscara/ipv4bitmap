import sys

if len(sys.argv) != 2:
    print("Usage: sudo python3 list.py <range>")
    print("Please provide a single integer range.")
    sys.exit(1)

try:
    range_value = int(sys.argv[1])
    if range_value < 1 or range_value > 256:
        print("Range value should be between 1 and 256.")
        sys.exit(1)
except ValueError:
    print("Invalid range value. Please provide a single integer.")
    sys.exit(1)

filename = "ip_list.txt"

with open(filename, "w") as f:
    for a in range(range_value):
        for b in range(range_value):
            for c in range(range_value):
                for d in range(range_value):
                    ip = f"{a}.{b}.{c}.{d}"
                    f.write(ip + "\n")

print("Complete.")

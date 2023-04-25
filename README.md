# internet
Inspired by tom7

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
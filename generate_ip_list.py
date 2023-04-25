with open("ip_list.txt", "w") as f:
    for a in range(10):
        for b in range(10):
            for c in range(10):
                for d in range(10):
                    ip = f"{a}.{b}.{c}.{d}"
                    f.write(ip + "\n")


print("complete.")
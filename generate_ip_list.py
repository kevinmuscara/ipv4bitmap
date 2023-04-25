with open("ip_list.txt", "w") as f:
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    ip = f"{a}.{b}.{c}.{d}"
                    f.write(ip + "\n")


print("complete.")
with open("ip_list.txt", "w") as f:
    for a in range(5):
        for b in range(5):
            for c in range(5):
                for d in range(5):
                    ip = f"{a}.{b}.{c}.{d}"
                    f.write(ip + "\n")


print("complete.")
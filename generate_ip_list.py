with open("ip_list.txt", "w") as f:
    for a in range(15):
        for b in range(15):
            for c in range(15):
                for d in range(15):
                    ip = f"{a}.{b}.{c}.{d}"
                    f.write(ip + "\n")


print("complete.")
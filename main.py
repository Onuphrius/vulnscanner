import json
import masscan
import os
from colorama import init, Fore

import binmaster as config
# Variables
start_at = 42
init()

ip_ranges = []
for range in config.range:
    try:
        new_range = open(f"./ipranges/{range}", "r").readlines()
        clean_new_range = list(map(str.strip, new_range))
        ip_ranges = ip_ranges + clean_new_range
    except Exception as e:
        print(e)
if not os.path.exists(f"{config.name}.result"):
    open(f"{config.name}.result", "w").write("")

done = 1

if start_at != 0:
    ip_ranges = ip_ranges[start_at:]
    done = start_at +1 

for ip_range in ip_ranges:
    try:
        num = 0
        ip_range = ip_range.strip()
        mas = masscan.PortScanner()
        mas.scan(ip_range, ports=config.ports, arguments=config.param)
        scan_result = json.loads(mas.scan_result)
        for ip in scan_result["scan"]:
            connections = scan_result['scan'][ip]
            for con in connections:
                data = con
                data["ip"] = ip
                result = config.execute(ip)
                if result:
                    num = num + 1
                    open(f"{config.name}.result", "a").write(f"{data}\n")
                    print(f"{Fore.GREEN}{data}{Fore.RESET}")
                else:
                    print(f"{Fore.RED}{data}{Fore.RESET}")
        if num == 0:
            print(f"{Fore.BLUE}[{done}/{len(ip_ranges)}] No Ips detected on Ip Range {ip_range}{Fore.RESET}")
        else:
            print(f"{Fore.BLUE}[{done}/{len(ip_ranges)}] {num} Ips detected on Ip Range {ip_range}{Fore.RESET}")
    except Exception as e:
        print(e)
    done = done + 1
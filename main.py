import json
import masscan
import os
from colorama import init, Fore
import scan_all as config
import time

# Variables
start_at = 220
init()
ip_ranges = []
global_start = time.time()
for range in config.range:
    try:
        new_range = open(f"./ipranges/{range}", "r").readlines()
        clean_new_range = list(map(str.strip, new_range))
        ip_ranges = ip_ranges + clean_new_range
    except Exception as e:
        print(e)
if not os.path.exists(f"{config.name}.result"):
    open(f"{config.name}.result", "w").write("")
if not os.path.exists(f"{config.name}.long"):
    open(f"{config.name}.long", "w").write("")
done = 1

if start_at != 0:
    ip_ranges = ip_ranges[start_at:]
    done = start_at +1 

for ip_range in ip_ranges:
    try:
        print(f"{Fore.BLUE}[{done}/{len(ip_ranges)}] Started scanning {ip_range}{Fore.RESET}")
        num = 0
        start_time = time.time()
        ip_range = ip_range.strip()
        mas = masscan.PortScanner()
        mas.scan(ip_range, ports=config.ports, arguments=config.param)
        scan_result = json.loads(mas.scan_result)
        if len(scan_result["scan"]) < config.max_result:
            for ip in scan_result["scan"]:
                connections = scan_result['scan'][ip]
                for con in connections:
                    num = num + 1
                    data = con
                    data["ip"] = ip
                    open(f"{config.name}.result", "a").write(f"{data}\n")
            end_time = time.time()
            diff_time = round(end_time - start_time)
            global_start = global_start + diff_time
            total_time = round((global_start / (done - start_at)) * (len(ip_ranges) - done))
            prnt = f'''
            Count: [{done}/{len(ip_ranges)}]
            Range: {ip_range}
            Ips: {num}
            Time: {diff_time}s
            Scan completed: {total_time}
            '''
            print(f"{Fore.BLUE}{prnt}{Fore.RESET}")
        else:
            open(f"{config.name}.long", "a").write(f"{ip_range}\n")
            print(f"{Fore.BLUE}[{done}/{len(ip_ranges)}]To many Ips detected on Ip Range {ip_range}{Fore.RESET}")

    except Exception as e:
        input(e)
    done = done + 1
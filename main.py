import json
import masscan
from colorama import init, Fore
import scan_all
import time
from pymongo import MongoClient

def readjson():
    with open("config.json", "r") as file:
        return json.load(file)
def savejson(config):
    with open("config.json", "w") as file:
        json.dump(config, file)

# Setup
init()
ip_ranges = []
global_start = time.time()
config = readjson()

for range in config["range"]:
    try:
        new_range = open(f"./ipranges/{range}", "r").readlines()
        clean_new_range = list(map(str.strip, new_range))
        ip_ranges = ip_ranges + clean_new_range
    except Exception as e:
        print(e)
        
mongodb = MongoClient(config["mongodb"])
db = mongodb[config["db"]]
collection = db[config["collection"]]

start_at = config["start"]
if start_at != 0:
    ip_ranges = ip_ranges[start_at:]
    
for ip_range in ip_ranges:
    try:
        print(f"{Fore.BLUE}[{start_at}/{len(ip_ranges)}] Started scanning {ip_range}{Fore.RESET}")
        num = 0
        start_time = time.time()
        ip_range = ip_range.strip()
        mas = masscan.PortScanner()
        mas.scan(ip_range, ports=config["ports"], arguments=config["param"])
        scan_result = json.loads(mas.scan_result)
        scan = scan_result["scan"]
        data_all = []
        for ip in scan:
            connections = scan[ip]
            for con in connections:
                num = num + 1
                data = con
                data["ip"] = ip
                data_all.append(data)
        data_all_web = scan_all.execute(data_all)
        if data_all_web != []:
            collection.insert_many(data_all_web)
        end_time = time.time()
        diff_time = round(end_time - start_time)
        global_start = global_start + diff_time
        total_time = round((global_start / (start_at + 1)) * (len(ip_ranges) - start_at))
        prnt = f'''
                Count: [{start_at}/{len(ip_ranges)}]
                Range: {ip_range}
                Ips: {num}
                Time: {diff_time}s
                Scan completed: {total_time}
        '''
        print(f"{Fore.BLUE}{prnt}{Fore.RESET}")


    except Exception as e:
        input(e)
    start_at = start_at + 1
    config["start"] = start_at
    savejson(config)
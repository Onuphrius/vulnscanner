import time
import json
import masscan
import scan_all
from colorama import init, Fore
from pymongo import MongoClient

def read_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file)

def load_ip_ranges(config):
    ip_ranges = []
    for range_file in config["range"]:
        try:
            with open(f"./ipranges/{range_file}", "r") as file:
                clean_new_range = [line.strip() for line in file.readlines()]
                ip_ranges.extend(clean_new_range)
        except Exception as e:
            print(e)
    return ip_ranges

def main():
    init()
    config = read_json("config.json")
    ip_ranges = load_ip_ranges(config)

    mongodb = MongoClient(config["mongodb"])
    db = mongodb[config["db"]]
    collection = db[config["collection"]]

    start_at = config["start"]
    global_start = time.time()

    for start_at, ip_range in enumerate(ip_ranges[start_at:], start_at):
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
                    num += 1
                    data = con
                    data["ip"] = ip
                    data_all.append(data)

            data_all_web = scan_all.execute(data_all)

            if data_all_web:
                collection.insert_many(data_all_web)

            end_time = time.time()
            diff_time = round(end_time - start_time)
            global_start += diff_time
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

        start_at += 1
        config["start"] = start_at
        save_json("config.json", config)

if __name__ == "__main__":
    main()

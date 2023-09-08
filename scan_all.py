import os
import time
import random
import requests
import concurrent.futures
from colorama import Fore
from bs4 import BeautifulSoup

# Variabels
name = "scan-all-top-20"
ports = "20,21-23,25,53,80,110-111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080"
range = ["all"]
param = "--max-rate 1310720 --banners --sendq"
max_result = 99999999
def execute(data_all):
    clean_data = []
    random.shuffle(data_all)
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for data in data_all:
            futures.append(executor.submit(getdata, data))
        for future in concurrent.futures.as_completed(futures):
            clean_data.append(future.result())
    return clean_data

def getdata(data):
    try:
        ip = data["ip"]
        port = data["port"]
        data["time"] = round(time.time())
        print(f"{Fore.LIGHTBLACK_EX}Scanning Webpage of {ip}{Fore.RESET}")
        headers = {
            "User-Agent": "Bigschniff Internet Scanner Contact: tf@maill.com"
        }
        r = requests.get(f"http://{ip}:{port}", headers=headers, timeout=5)
        r.raise_for_status()
        data["headers"] = r.headers
        data["url"] = r.url
        soup = BeautifulSoup(r.text, 'html.parser')
        data["title"] = soup.find('title').text
        links = []
        links_a = soup.find_all('a')
        for link in links_a:
            href = link.get('href')
            if href:
                links.append(href)
        data["links"] = links
    except:
        pass
    return data
import os
import time
import random
import requests
from colorama import Fore
from alive_progress import alive_bar
import concurrent.futures
from bs4 import BeautifulSoup
def execute(data_all):
    clean_data = []
    random.shuffle(data_all)
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        futures = []
        for data in data_all:
            futures.append(executor.submit(getdata, data))
        with alive_bar(len(data_all), title=f"{Fore.BLUE}") as bar:
            for future in concurrent.futures.as_completed(futures):
                clean_data.append(future.result())
                bar()
    return clean_data

def getdata(data):
    try:
        ip = data["ip"]
        port = data["port"]
        data["time"] = round(time.time())
        headers = {
            "User-Agent": "Bigschniff Internet Scanner Contact: tf@maill.com"
        }
        r = requests.get(f"http://{ip}:{port}", headers=headers, timeout=5, verify=False)
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
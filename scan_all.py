import requests
from colorama import Fore
from bs4 import BeautifulSoup

# Variabels
name = "scan-all-top-20"
ports = "20,21-23,25,53,80,110-111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080"
range = ["all"]
param = "--max-rate 1310720 --banners --sendq"
max_result = 99999999

def execute(data):
    try:
        ip = data["ip"]
        port = data["port"]
        print(f"{Fore.LIGHTBLACK_EX}Scanning Webpage of {ip}{Fore.RESET}")
        headers = {
            "User-Agent": "Bigschniff Internet Scanner Contact: tf@maill.com"
        }
        r = requests.get(f"http://{ip}:{port}", headers=headers, timeout=5)
        r.raise_for_status()
        data["headers"] = r.headers
        data["url"] = r.url
        soup = BeautifulSoup(r.text, 'html.parser')
        data["title"] = soup.find('title')
        links = []
        links_a = soup.find_all('a')
        for link in links_a:
            href = link.get('href')
            if href:
                links.append(href)
        data["links"] = links
        return data
    except:
        return False
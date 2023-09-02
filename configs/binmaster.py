import requests
from colorama import init, Fore
# Variabels
name = "binmaster"
ports = "6969"
range = ["google_cloud_all"]
param = "--max-rate 1000000 --banners"


def execute(result):
    try:
        print(result)
        ip = result
        print(f"{Fore.LIGHTWHITE_EX}Scanning Webpage of {ip}{Fore.RESET}")
        headers = {
            "User-Agent": "Bigschniff Internet Scanner Contact: tf@maill.com"
        }
        
        r = requests.get(f"http://{ip}:6969", headers=headers, timeout=5)
        r.raise_for_status()
        if "BinMaster" in r.text:
            return True
        return False
    except:
        return False
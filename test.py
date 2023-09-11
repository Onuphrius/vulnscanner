import requests
headers = {
    "user": "bigschniff",
    "type": "get"
}
r = requests.get("http://127.0.0.1:5000/api", headers=headers)
print(r.json())
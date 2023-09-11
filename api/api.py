import json
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

with open(f"range", "r") as file:
    ranges = [line.strip() for line in file.readlines()]
with open(f"users.txt", "r") as file:
    users = [line.strip() for line in file.readlines()]
active_ranges = []

def save_range():
    with open(f"range", "w") as file:
        for range in ranges:
            file.write(f"{range}\n")

actions = ["get", "return", "fail"]
@app.route("/api")
def get_range():
    user = request.headers.get("user")
    type_action = request.headers.get("type")
    if user not in users:
        return Response(json.dumps({"success": False, "error": "false_user"}), status=400)
    if type_action not in actions:
        return Response(json.dumps({"success": False, "error": "false_type"}), status=400)
    if type_action == "get":
        response_range = ranges[0]
        ranges.pop(0)
        save_range()
        active_ranges.append(response_range)
        return Response(json.dumps({"success": True, "range": f"{response_range}"}), status=200)
    
    return Response("", status=200)
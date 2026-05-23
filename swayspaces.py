#!/usr/bin/env python3

import subprocess
import json
import sys

data = {}

def get_workspaces():
    output = subprocess.check_output(["swaymsg", "-t", "get_workspaces", "--raw"])
    raw = output.decode("utf-8")
    return generate_workspace_data(raw)

def handle_init(change):
    name = change["current"].get("name")
    if name and name not in data:
        data[name] = {
            "name": name,
            "output": change["current"].get("output", "best"),
            "focused": change["current"].get("focused", False),
        }

def handle_empty(change):
    data.pop(change["current"]["name"], None)

def handle_focus(change):
    cur = change.get("current")
    if cur is not None and cur["name"] in data:
        data[cur["name"]]["output"] = cur["output"]
        data[cur["name"]]["focused"] = (cur.get("focused") or
                                        any(n.get("focused") for n in
                                            cur.get("nodes", [])))
    old = change.get("old")
    if old is not None and old.get("name") in data:
        name = old["name"]
        data[name]["output"] = old["output"]
        data[name]["focused"] = (old.get("focused") or
                                 any(n.get("focused") for n in
                                     old.get("nodes", [])))

def handle_change(change):
    match change["change"]:
        case "focus":
            return handle_focus(change)
        case "init":
            return handle_init(change)
        case "empty":
            return handle_empty(change)
        case _:
            print(change["change"], file=sys.stderr)



def parse(line) -> dict:
    workspaces = json.loads(line)
    if isinstance(workspaces, dict):
        return handle_change(workspaces)
    for wsp in workspaces:
        name = wsp.get("name")
        if name:
            data[name] = {
                "name": name,
                "output": wsp.get("output", "best"),
                "focused": wsp.get("focused", False),
            }

def generate_workspace_data(line) -> dict:
    parse(line)
    items = sorted(data.values(), key=lambda x: x["name"])
    return json.dumps(items)

if __name__ == "__main__":
    process = subprocess.Popen(
        ["swaymsg", "-t", "subscribe", "-m", '["workspace"]', "--raw"],
        stdout=subprocess.PIPE,
    )
    if process.stdout is None:
        print("Error: could not subscribe to sway events")
        exit(1)
    print(get_workspaces(), flush=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.decode("utf-8")
        print(generate_workspace_data(line), flush=True)

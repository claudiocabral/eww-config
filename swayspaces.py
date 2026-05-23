#!/usr/bin/env python3

import subprocess
import json
import sys

data = []

def get_workspaces():
    output = subprocess.check_output(["swaymsg", "-t", "get_workspaces", "--raw"])
    raw = output.decode("utf-8")
    return generate_workspace_data(raw)

def handle_init(change):
    if not any(item["name"] == change["current"].get("name") for item in data):
        data.append({
            "name": change["current"].get("name", "test"),
            "output": change["current"].get("output", "best"),
            "focused": change["current"].get("focused", False),
        });

def handle_empty(change):
    for item in data:
        if item["name"] == change["current"]["name"]:
            data.remove(item)

def handle_focus(change):
    for item in data:
        if ("current" in change
            and change["current"] is not None
            and item["name"] == change["current"]["name"]):
            item["output"] =  change["current"]["output"]
            item["focused"] = change["current"]["focused"]
            item["focused"] = (change["current"]["focused"] or
                               any(node.get("focused") for node in
                                   change["current"]["nodes"]))
        if ("old" in change
            and change["old"] is not None
            and item["name"] == change["old"].get("name", "")):
                item["output"] =  change["old"]["output"]
                item["focused"] = (change["old"]["focused"] or
                                   any(node.get("focused") for node in
                                       change["old"]["nodes"]))

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
        data.append({
            "name": wsp.get("name", "test"),
            "output": wsp.get("output", "best"),
            "focused": wsp.get("focused", False),
        })

def generate_workspace_data(line) -> dict:
    parse(line)
    data.sort(key=lambda item: item["name"])
    return json.dumps(data)

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
        line = process.stdout.readline().decode("utf-8")
        #if line == "":
        #    break
        print(generate_workspace_data(line), flush=True)

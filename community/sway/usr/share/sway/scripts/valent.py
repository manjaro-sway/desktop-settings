#!/usr/bin/env python3
import dbus
import json
import math

CONNECTIVITY_STRENGTH_SYMBOL = {
    0: "󰞃",
    1: "󰢼",
    2: "󰢽",
    3: "󰢾",
}

BATTERY_PERCENTAGE_SYMBOL = {
    0: "",
    1: "",
    2: "",
    3: "",
    4: ""
}

bus = dbus.SessionBus()
valent_object = bus.get_object("ca.andyholmes.Valent", "/ca/andyholmes/Valent")
valent_interface = dbus.Interface(valent_object, "org.freedesktop.DBus.ObjectManager")
managed_objects = valent_interface.GetManagedObjects()

dangerously_empty=False
connected=False
no_connectivity=False

devices = []

for path in managed_objects:
    device = {}
    device["state"] = "connected" if managed_objects[path].get("ca.andyholmes.Valent.Device", {}).get("State", 0) == 3 else "disconnected"
    device["id"] = managed_objects[path].get("ca.andyholmes.Valent.Device", {}).get("Id", 0)
    device["name"] = managed_objects[path].get("ca.andyholmes.Valent.Device", {}).get("Name", 0)

    device_obj = bus.get_object("ca.andyholmes.Valent", path)
    device_action_interface = dbus.Interface(device_obj, "org.gtk.Actions")

    battery_state = device_action_interface.Describe("battery.state")[2][0]
    device["battery_percentage"] = battery_state["percentage"]
    device["battery_status"] = "discharging" if battery_state["charging"] == 0 else "charging"

    connectivity_state = device_action_interface.Describe("connectivity_report.state")[2][0]["signal-strengths"]["1"]
    device["connectivity_strength"] = connectivity_state["signal-strength"]

    if device["state"] == "connected":
        connected = True
    
    if device["connectivity_strength"] <= 1:
        no_connectivity = True

    if device["battery_percentage"] <= 15 and device["battery_status"] == "discharging":
        dangerously_empty = True

    devices.append(device)

data = {}
data["alt"] = "no-devices" if len(devices) == 0 else "dangerously-empty" if dangerously_empty else "no-signal" if no_connectivity else "connected" if connected else "disconnected"
data["class"] = data["alt"]
data["tooltip"] = ""
for device in devices:
    battery_symbol = 0 if device['battery_percentage'] < 20 else 1 if device['battery_percentage'] < 40 else 2 if device['battery_percentage'] < 60 else 3 if device['battery_percentage'] < 80 else 4
    details = f"{CONNECTIVITY_STRENGTH_SYMBOL[device['connectivity_strength']]} {BATTERY_PERCENTAGE_SYMBOL[battery_symbol]}  {device['battery_percentage']}% ({device['battery_status']})" if device['state'] == "connected" else ""
    data['tooltip'] += f"{device['name']} ({device['state']})\t  \n"

print(json.dumps(data))

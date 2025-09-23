import PySimpleGUI as sg
import os
import GPUtil
import platform

def run1():
    script_path = r"restartgpu.py"
    os.system(f'start cmd /k python "{script_path}"')

# Get GPU info
gpus = GPUtil.getGPUs()
gpu_name = gpus[0].name if gpus else "No GPU detected"

info = f"""System: {platform.system()}
User Name: {platform.node()}
Release: {platform.release()}
Version: {platform.version()}
Machine: {platform.machine()}
Processor: {platform.processor()}
Python Version: {platform.python_version()}
GPU: {gpu_name}
PID: {os.getpid()}
"""

# Define the layout
layout = [
    [sg.Text(info, font=("Helvetica", 14), size=(60, None))],
    [sg.Button("Restart GPU", size=(20, 2))]
]

# Create the window
window = sg.Window("DeviceManager", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Restart GPU":
        run1()

window.close()

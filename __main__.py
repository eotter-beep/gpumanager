import tkinter as tk
import os
import GPUtil
import platform

def run1():
    script_path = r"restartgpu.py"
    os.system(f'start cmd /k python "{script_path}"')

root = tk.Tk()
root.title("DeviceManager")

# get GPU info
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
"""

label = tk.Label(root, text=info, font=("Helvetica", 14), justify="left")
label.pack(pady=20)

button = tk.Button(root, text="Restart GPU", command=run1, height=2, width=20)
button.pack(padx=20, pady=20)

root.mainloop()

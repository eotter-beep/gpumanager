import tkinter as tk
import os
import GPUtil
import platform

def run1():
    script_path = r"restartgpu.py"
    os.system(f'start cmd /k python "{script_path}"')

root = tk.Tk()
root.title("GPUManager")
info = f"System: {platform.system()}\n \
User Name: {platform.node()}\n \
Release: {platform.release()}\n \
Version: {platform.version()}\n \
Machine: {platform.machine()}\n \
Processor: {platform.processor()}\n \
Python Version: {platform.python_version()}\n \
GPU: {gpus[0].name}\n \
"
Label(root, text=info, font=("Helvetica", 14))
button = tk.Button(root, text="Restart GPU", command=run1, height=2, width=20)
button.pack(padx=20, pady=20)

root.mainloop()

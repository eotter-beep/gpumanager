import customtkinter as ctk
import os
import GPUtil
import platform

# Function to run the restart GPU script
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

# Set theme
ctk.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

# Create window
root = ctk.CTk()
root.title("DeviceManager")
root.geometry("600x400")

# Label for info
label = ctk.CTkLabel(root, text=info, justify="left", font=("Helvetica", 14))
label.pack(pady=20, padx=20)

# Button to restart GPU
button = ctk.CTkButton(root, text="Restart GPU", command=run1, height=40, width=200)
button.pack(pady=20)

root.mainloop()

import customtkinter as ctk
import os
import GPUtil
import platform
import time
import threading
from tkinter import Toplevel, Label

# Function to run the restart GPU script
def run1():
    script_path = r"restartgpu.py"
    os.system(f'start cmd /k python "{script_path}"')

# Global variable to track FPS window state
fps_window = None
fps_running = False

def show_fps():
    global fps_window, fps_running
    
    if fps_running:
        # If FPS is already running, stop it
        fps_running = False
        if fps_window and fps_window.winfo_exists():
            fps_window.destroy()
        return
    
    # Create transparent overlay window
    fps_window = Toplevel(root)
    fps_window.title("FPS Monitor")
    fps_window.geometry("150x60+100+100")  # Position at top-left corner
    fps_window.overrideredirect(True)  # Remove window decorations
    fps_window.attributes('-topmost', True)  # Always on top
    fps_window.attributes('-alpha', 0.8)  # Semi-transparent
    fps_window.configure(bg='black')
    
    # FPS label
    fps_label = Label(fps_window, text="FPS: --", font=("Arial", 16, "bold"), 
                     fg="white", bg="black")
    fps_label.pack(expand=True, fill='both')
    
    fps_running = True
    button_fps.configure(text="Hide FPS")
    
    # Function to update FPS in a separate thread
    def update_fps():
        frame_count = 0
        last_time = time.time()
        
        while fps_running and fps_window.winfo_exists():
            # Simulate FPS calculation (you can replace this with actual FPS measurement)
            current_time = time.time()
            frame_count += 1
            
            if current_time - last_time >= 1.0:  # Update every second
                fps = frame_count / (current_time - last_time)
                fps_label.config(text=f"FPS: {fps:.1f}")
                frame_count = 0
                last_time = current_time
            
            time.sleep(0.01)  # Small delay to prevent high CPU usage
    
    # Start FPS update in a separate thread
    fps_thread = threading.Thread(target=update_fps, daemon=True)
    fps_thread.start()
    
    # Make the window draggable
    def start_drag(event):
        fps_window.x = event.x
        fps_window.y = event.y
    
    def do_drag(event):
        deltax = event.x - fps_window.x
        deltay = event.y - fps_window.y
        x = fps_window.winfo_x() + deltax
        y = fps_window.winfo_y() + deltay
        fps_window.geometry(f"+{x}+{y}")
    
    fps_label.bind("<Button-1>", start_drag)
    fps_label.bind("<B1-Motion>", do_drag)
    
    # Close handling
    def on_close():
        global fps_running
        fps_running = False
        button_fps.configure(text="Show FPS")
    
    fps_window.protocol("WM_DELETE_WINDOW", on_close)

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
button.pack(pady=10)

# Button to show FPS
button_fps = ctk.CTkButton(root, text="Show FPS", command=show_fps, height=40, width=200)
button_fps.pack(pady=10)

root.mainloop()

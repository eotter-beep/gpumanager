import customtkinter as ctk
import os
import platform
import subprocess
import sys
import time
import threading
from pathlib import Path
from tkinter import Toplevel, Label

import GPUtil
import psutil
from PIL import ImageGrab, Image
import numpy as np

# ----------------- GPU Restart -----------------
def _run_in_terminal(command):
    """Best-effort attempt to launch a command in a detached terminal."""
    system = platform.system()
    if system == "Windows":
        os.system(f'start "" cmd /k {command}')
        return True

    # Try common Linux terminals
    if system == "Linux":
        terminals = [
            os.environ.get("TERMINAL"),
            "x-terminal-emulator",
            "gnome-terminal",
            "konsole",
            "xfce4-terminal",
            "lxterminal",
            "xterm",
        ]
        for term in filter(None, terminals):
            try:
                subprocess.Popen([term, "-e", "bash", "-lc", command])
                return True
            except FileNotFoundError:
                continue
            except Exception as exc:
                print(f"Failed to launch {term}: {exc}")
        print("No compatible terminal emulator found; running in background instead.")
    return False


def run1():
    script_path = Path("restartgpu.py")
    if not script_path.exists():
        print("restartgpu.py not found!")
        return

    command = f'"{sys.executable}" "{script_path}"'
    if not _run_in_terminal(command):
        try:
            subprocess.Popen([sys.executable, str(script_path)])
        except Exception as exc:
            print(f"Failed to launch restartgpu.py: {exc}")


def run2():
    script_path = Path("optimizer.cmd")
    system = platform.system()

    if system == "Windows" and script_path.exists():
        _run_in_terminal(f'"{script_path}"')
        return

    if system != "Windows":
        alt_script = script_path.with_suffix(".sh")
        if alt_script.exists():
            if not _run_in_terminal(f'"{alt_script}"'):
                try:
                    subprocess.Popen(["bash", str(alt_script)])
                except Exception as exc:
                    print(f"Failed to launch {alt_script}: {exc}")
        else:
            print("Optimizer script not available on this platform.")
        return

    print("Cannot run the optimizer")

# ----------------- FPS Measurement -----------------
fps_window = None
fps_running = False

def get_screen_fps(exclude_window=None, interval=0.2):
    """Estimates FPS by comparing consecutive screen captures while ignoring DeviceManager window."""
    last_frame = None
    frame_changes = 0
    start_time = time.time()

    while time.time() - start_time < 1.0:  # measure for 1 second
        screen = ImageGrab.grab()
        if exclude_window:
            x, y, w, h = exclude_window
            black_box = Image.new("RGB", (w, h), (0, 0, 0))
            screen.paste(black_box, (x, y))

        frame = np.array(screen.convert("L"))  # grayscale

        if last_frame is not None:
            diff = np.abs(frame.astype(np.int16) - last_frame.astype(np.int16))
            if diff.mean() > 5:  # threshold for frame change
                frame_changes += 1

        last_frame = frame
        time.sleep(interval)

    fps = frame_changes / (time.time() - start_time)
    return fps

def show_fps():
    global fps_window, fps_running
    if fps_running:
        fps_running = False
        if fps_window and fps_window.winfo_exists():
            fps_window.destroy()
        button_fps.configure(text="Show FPS")
        return

    fps_window = Toplevel(root)
    fps_window.title("FPS Monitor")
    fps_window.geometry("220x100+100+100")
    fps_window.overrideredirect(True)
    fps_window.attributes('-topmost', True)
    fps_window.attributes('-alpha', 0.85)
    fps_window.configure(bg='#1a1a1a')

    fps_label = Label(fps_window, text="FPS being used: Measuring...", font=("Arial", 14, "bold"), fg="#00ff00", bg='#1a1a1a')
    fps_label.pack(expand=True, fill='both', padx=10, pady=5)

    info_label = Label(fps_window, text="", font=("Arial", 10), fg="#cccccc", bg='#1a1a1a')
    info_label.pack(expand=True, fill='both', padx=10, pady=5)

    fps_running = True
    button_fps.configure(text="Hide FPS")

    def update_fps():
        while fps_running and fps_window.winfo_exists():
            # Get DeviceManager window area to ignore
            x, y = root.winfo_x(), root.winfo_y()
            w, h = root.winfo_width(), root.winfo_height()
            exclude_area = (x, y, w, h)

            fps = get_screen_fps(exclude_window=exclude_area, interval=0.1)

            try:
                cpu_percent = psutil.cpu_percent()
                ram_percent = psutil.virtual_memory().percent
                info_text = f"CPU: {cpu_percent:.0f}% | RAM: {ram_percent:.0f}%"
            except:
                info_text = "System stats unavailable"

            # Update labels safely in main thread
            fps_window.after(0, lambda f=fps, i=info_text: (fps_label.config(text=f"FPS: {f:.1f}"), info_label.config(text=i)))

    threading.Thread(target=update_fps, daemon=True).start()

    # Make overlay draggable
    def start_drag(event):
        fps_window.x = event.x
        fps_window.y = event.y
    def do_drag(event):
        x = fps_window.winfo_x() + event.x - fps_window.x
        y = fps_window.winfo_y() + event.y - fps_window.y
        fps_window.geometry(f"+{x}+{y}")

    fps_label.bind("<Button-1>", start_drag)
    fps_label.bind("<B1-Motion>", do_drag)
    info_label.bind("<Button-1>", start_drag)
    info_label.bind("<B1-Motion>", do_drag)

    fps_window.protocol("WM_DELETE_WINDOW", lambda: close_fps())

def close_fps():
    global fps_running
    fps_running = False
    if fps_window and fps_window.winfo_exists():
        fps_window.destroy()
    button_fps.configure(text="Show FPS")

# ----------------- System Info -----------------
try:
    gpus = GPUtil.getGPUs()
    gpu_name = gpus[0].name if gpus else "No GPU detected"
except Exception:
    gpu_name = "GPU info unavailable"

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

# ----------------- UI Setup -----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("DeviceManager")
root.geometry("600x400")

label = ctk.CTkLabel(root, text=info, justify="left", font=("Helvetica", 14))
label.pack(pady=20, padx=20)

button = ctk.CTkButton(root, text="Restart GPU", command=run1, height=40, width=200)
button.pack(pady=10)

button_fps = ctk.CTkButton(root, text="Show FPS", command=show_fps, height=40, width=200)
button_fps.pack(pady=10)

button = ctk.CTkButton(root, text="Run the Optimizer", command=run2, height=40, width=200)
button.pack(pady=10)

root.mainloop()

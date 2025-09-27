import os
import platform
import subprocess
import sys
import tkinter as tk

def _append_status(line):
    """Helper to append a line to the status textbox."""
    status.configure(state="normal")
    status.insert(tk.END, line + "\n")
    status.see(tk.END)
    status.configure(state="disabled")
    root.update_idletasks()


def startinstall():
    packages = [
        "customtkinter",
        "GPUtil",
        "numpy",
        "Pillow",
        "psutil",
    ]

    status.configure(state="normal")
    status.delete("1.0", tk.END)
    status.configure(state="disabled")

    for package in packages:
        _append_status(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            _append_status(f"✔ Installed {package}")
        except subprocess.CalledProcessError as exc:
            _append_status(f"✖ Failed to install {package}: {exc}")

    if platform.system() == "Windows":
        os.system("echo Installation complete")


def startinstall():
    packages = ["GPUtil", "customtkinter"]
    output_lines = []

    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            output_lines.append(f"Installed {package}")
        except subprocess.CalledProcessError as exc:
            output_lines.append(f"Failed to install {package}: {exc}")

    skip_message = "Skipping the other libraries because they are included in the official Python base"
    output_lines.append(skip_message)

    message = "\n".join(output_lines)
    status.configure(state="normal")
    status.delete("1.0", tk.END)
    status.insert(tk.END, message)
    status.configure(state="disabled")

    if platform.system() == "Windows":
        os.system(f'echo {skip_message}')

root = tk.Tk()
root.title("DeviceManager")

# Label
label = tk.Label(root, text="Easily manage your devices!", font=("Helvetica", 14))
label.pack(pady=20)

# Button
button = tk.Button(root, text="Start the installer", command=startinstall)
button.pack(pady=10)

status = tk.Text(root, width=50, height=6, state="disabled")
status.pack(padx=20, pady=10)

root.mainloop()

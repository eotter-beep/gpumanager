import tkinter as tk
import os

def run1():
    script_path = r"restartgpu.py"
    os.system(f'start cmd /k python "{script_path}"')

root = tk.Tk()
root.title("GPUManager")

button = tk.Button(root, text="Restart GPU", command=run1, height=2, width=20)
button.pack(padx=20, pady=20)

root.mainloop()

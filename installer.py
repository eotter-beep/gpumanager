import tkinter as tk
import os

def startinstall():
    os.system('start cmd /k "pip install GPUtil"')
    os.system('start cmd /k "echo Skipping the other libraries because they are included in the official Python base"')

root = tk.Tk()
root.title("DeviceManager")

# Label
label = tk.Label(root, text="Easily manage your devices!", font=("Helvetica", 14))
label.pack(pady=20)

# Button
button = tk.Button(root, text="Start the installer", command=startinstall)
button.pack(pady=20)

root.mainloop()

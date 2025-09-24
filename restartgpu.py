import os
import keyboard
import time
print("GPUManager")
print("----------------------------------------------------------------------")
print("Restart the terminal to avoid terminal messups when restarting the GPU (takes 5 seconds)")
time.sleep(5)
os.system('cls')
time.sleep(5)
print("Restart GPU")
def resgpu():
  keyboard.send("windows+ctrl+shift+b")
resgpu()

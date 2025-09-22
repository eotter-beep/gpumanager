import os
import keyboard
import time
print("GPUManager")
print("----------------------------------------------------------------------")
print("Restart the terminal to avoid terminal messups when restarting the GPU")
time.sleep(10)
os.system('cls')
time.sleep(10)
print("Restart GPU")
def resgpu():
  keyboard.send("windows+ctrl+shift+b")
resgpu()

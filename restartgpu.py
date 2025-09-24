import os
import keyboard
import time
import sys

print("GPUManager")
print("----------------------------------------------------------------------")
print("Restart the terminal to avoid terminal messups when restarting the GPU (takes 5 seconds)")
time.sleep(5)
os.system('cls')

def print_progress_bar(seconds):
    for i in range(seconds):
        # Calculate percentage
        progress = (i + 1) / seconds
        bar_length = 30
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Print progress bar
        sys.stdout.write(f'\rRestarting GPU in {seconds-i} seconds... [{bar}] {progress*100:.1f}%')
        sys.stdout.flush()
        time.sleep(1)
    
    # Clear the line after completion
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

def resgpu():
    keyboard.send("windows+ctrl+shift+b")

# Show progress bar for 5 seconds before restarting GPU
print_progress_bar(5)
resgpu()
print("GPU restart signal sent!")

import os
import platform
import sys
import time

try:
    import keyboard
except ImportError:
    keyboard = None

print("GPUManager")
print("----------------------------------------------------------------------")
print("Restart the terminal to avoid terminal messups when restarting the GPU (takes 5 seconds)")
time.sleep(5)
os.system('cls' if os.name == 'nt' else 'clear')

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
    if platform.system() != "Windows":
        print("GPU restart shortcut is only available on Windows.")
        return

    if keyboard is None:
        print("The 'keyboard' module is not installed; cannot send the restart shortcut.")
        return

    keyboard.send("windows+ctrl+shift+b")

# Show progress bar for 5 seconds before restarting GPU
print_progress_bar(5)
resgpu()
print("GPU restart signal sent! (will take a few seconds to flick on and off the black screen, that means it restarted)")

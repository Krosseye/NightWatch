"""
This script handles the actions to perform at end of the countdown timer.
"""

import logging
import os
import platform
from tkinter import messagebox

import pyautogui


def get_os():
    """Determines the name of the operating system."""
    os_name = platform.system()
    return os_name


def pause_media():
    """Pauses the media playback using pyautogui to simulate the play/pause button press."""
    pyautogui.press("playpause")
    logging.info("Pausing media...")
    messagebox.showinfo("NightWatch", "Media has been paused.")


def sleep_system(self):
    """Puts the system to sleep based on the operating system."""
    current_os = get_os()
    logging.info("Going to sleep...")
    if current_os == "Windows":
        os.system(
            'powershell.exe Write-Host "Putting the computer to sleep..." && rundll32.exe powrprof.dll,SetSuspendState 0,1,0'
        )
    elif current_os == "Darwin":
        os.system("pmset sleepnow")
    elif current_os == "Linux":
        os.system("systemctl suspend")
    else:
        self.show_error("Unable to suspend, unkown operating system.")


def shutdown_system(self):
    """Shuts down the system based on the operating system."""
    current_os = get_os()
    logging.info("Shutting down...")
    if current_os == "Windows":
        os.system("shutdown /s /t 0")
    elif current_os == "Darwin":
        os.system("sudo shutdown -h now")
    elif current_os == "Linux":
        os.system("sudo shutdown -h now")
    else:
        self.show_error("Unable to shutdown, unkown operating system.")

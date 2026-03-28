import subprocess
import os
import webbrowser
import pyautogui
from datetime import datetime
from utils import logger

class BasicPCControl:
    """Basic PC control for JARVIS"""
    
    def __init__(self):
        self.apps = {
            "notepad": "gedit",
            "calculator": "gnome-calculator",
            "browser": "firefox",
            "terminal": "gnome-terminal",
            "files": "nautilus",
        }
    
    def execute(self, command):
        """Execute a basic PC command"""
        cmd = command.lower().strip()
        
        # Open application
        if cmd.startswith("open "):
            app = cmd.replace("open ", "").strip()
            if app in self.apps:
                try:
                    subprocess.Popen([self.apps[app]])
                    return f"Opening {app}, sir."
                except:
                    return f"Could not open {app}, sir."
            return None
        
        # Type text
        if cmd.startswith("type ") or cmd.startswith("write "):
            text = cmd.replace("type ", "").replace("write ", "").strip()
            try:
                pyautogui.write(text, interval=0.03)
                return f"Typed: {text}"
            except:
                return "Could not type text, sir."
        
        # Screenshot
        if cmd == "screenshot":
            try:
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = os.path.join(desktop, filename)
                pyautogui.screenshot().save(filepath)
                return f"Screenshot saved to desktop, sir."
            except:
                return "Could not take screenshot, sir."
        
        return None

pc_control = BasicPCControl()
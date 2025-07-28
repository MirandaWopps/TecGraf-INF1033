#Theme.py
#responsible for the theme of the application: dark or bright

#These 2 imports will find the OS and the system theme, so we can set Dark Mode or Light Mode.
import subprocess #acess to terminal
import os #discover the operational system

import sys

#Discovering the operational system
def getOS(): 
    if sys.platform.startswith('win'):
        return 'Windows'
    elif sys.platform.startswith('linux'):
        return 'Linux'
    elif sys.platform.startswith('darwin'):
        return 'macOS'
    else:
        return 'Unknown'
    

#Detecting the system theme
def is_system_dark(os_name):
    if os_name == 'Windows':
        import ctypes
        import winreg
        try:
            # Method 1: System color check
            if ctypes.windll.user32.GetSysColor(15) < 128:  # COLOR_WINDOW = 15
                return True
            
            # Method 2: Registry check (more reliable)
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as key:
                apps_use_light = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
                return apps_use_light == 0
        except Exception as e:
            print(f"Error checking dark mode: {e}")
            return False

    #Linux detection algorithm using a subprocess: a terminal command    
    elif os_name == 'Linux':
        try:
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True,
                text=True
                    )
            output = result.stdout.strip()
            if 'prefer-dark' in output:
                return True
        except Exception as e:
            print(f"Erro ao detectar tema do sistema: {e}")
            return False


#Apply theme
def apply_theme(widget, dark_mode):
    """Aplica o tema escuro ou claro a um QWidget (como MainWindow)"""
    if dark_mode:
        widget.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #3A3A3A;
                border: 1px solid #555;
                padding: 8px;
                min-width: 120px;
                border-radius: 8px;  /* 👈 mais arredondado */
            }
            QPushButton:hover {
                background-color: #2A2A2A;
            }
            QLabel {
                background-color: #2D2D2D;
                border: 1px solid #555;
            }
        """)
    else:
        widget.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                color: #000000;
            }
            QPushButton {
                background-color: #E0E0E0;
                border: 1px solid #AAA;
                padding: 8px;
                min-width: 120px;
                border-radius: 8px;
            }
            QLabel {
                border: 1px solid #AAA;
            }
        """)


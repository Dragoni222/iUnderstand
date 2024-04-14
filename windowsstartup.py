# Python code to add current script to the registry

# Thank you to hitesh_kumar_kushwaha on Geeks for Geeks for the automated startup code

# module to edit the windows registry 


import ctypes
import getpass
import os

USER_NAME = getpass.getuser()


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path += "\main.py"
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)
        
        
#thanks to RDCH106 on github for admin-check code
def is_admin():
    is_admin = False
    is_win = False
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        is_win = True

    print("Admin privileges: {}".format(is_admin))
    return is_admin, is_win

"""
This file is responsible for the UI and functioning of MUPPET.
To start the program, call main_menu().

-RF
"""

import questionary
import configparser
import os

# questionary print styles
MUPPET_COLOR = "fg:lime"
MUPPET_ERROR = "fg:red"
MUPPET_CAUTION = "fg:black bg:orange"
MUPPET_INFO = "fg:blue italic"

USER_CONFIG_PATH = "user_config.ini"

def main_menu():
    questionary.print("\t- Main Menu -", style=MUPPET_COLOR)
    mm_option = questionary.select(
        "What do you want to do?",
        choices=[
            "MUPPET Setup",
            "Batch VMDL Maker",
            "Close MUPPET."
        ]
    ).ask()

    match mm_option:
        case "MUPPET Setup":
            menu_setup()
        case "Batch VMDL Maker":
            questionary.print("This has not been implemented yet.", style=MUPPET_CAUTION)
        case "Close MUPPET.":
            questionary.print("\tBye!", style=MUPPET_COLOR)
            return() # ends program

# settings menu
def menu_setup():
    questionary.print("\t- Settings -", style=MUPPET_COLOR)
    setup_option = questionary.select(
        ">",
        choices = [
            "Set dmxconvert.exe location",
            "Set resourcecompiler.exe location",
            "Back to Main Menu",
        ]
    ).ask()

    match setup_option:
        case "Set dmxconvert.exe location":
            config_dmxconvert_location()
        case "Set resourcecompiler.exe location":
            config_compiler_location()
        case "Back to Main Menu":
            main_menu()

# requests the location to dmxconvert.exe
def config_dmxconvert_location():
    questionary.print("dmxconvert.exe is found in this folder:\nsteamapps/common/Half-Life Alyx/game/bin/win64/dmxconvert.exe\nType 'back' to go back to menu!", style=(MUPPET_INFO))
    exe_path: str = questionary.path("dmxconvert.exe file path: ").ask()
    if exe_path.lower() == "back":
        menu_setup()
    else:
        exe_path = os.path.normpath(exe_path) # normalizes path
        if os.path.isfile(exe_path): # if path is direct to file
            if os.path.basename(exe_path) == "dmxconvert.exe":
                update_config('path_dmxconvert', exe_path)
        elif os.path.isdir(exe_path) and "dmxconvert.exe" in os.listdir(exe_path): # check if path is folder containing dmxconvert.exe
            #append to end of path
            if exe_path[-1] == "/":
                exe_path = exe_path + "dmxconvert.exe"
            else:
                exe_path = exe_path + "/dmxconvert.exe"
            update_config('path_dmxconvert', exe_path)
        else: # path is wrong invalid.
            questionary.print("Path is invalid, 'dmxconvert.exe' could not be found.", style=MUPPET_ERROR)
            questionary.press_any_key_to_continue().ask()
            menu_setup()

# requests the location to resourcecompiler.exe
def config_compiler_location():
    questionary.print("resourcecompiler.exe is found in this folder: \nsteamapps/common/Half-Life Alyx/game/bin/win64/resourcecompiler.exe \nType 'back' to go back to menu!", style=(MUPPET_INFO))
    exe_path: str = questionary.path("dmxconvert.exe file path: ").ask()
    if exe_path.lower() == "back":
        menu_setup()
    else:
        exe_path = os.path.normpath(exe_path) # normalizes path
        if os.path.isfile(exe_path): # if path is direct to file
            if os.path.basename(exe_path) == "resourcecompiler.exe":
                update_config('path_compiler', exe_path)
        elif os.path.isdir(exe_path) and "resourcecompiler.exe" in os.listdir(exe_path): # check if path is folder containing resourcecompiler.exe
            #append to end of path
            if exe_path[-1] == "/":
                exe_path = exe_path + "resourcecompiler.exe"
            else:
                exe_path = exe_path + "/resourcecompiler.exe"
            update_config('path_compiler', exe_path)
        else: # path is wrong invalid.
            questionary.print("Path is invalid, 'resourcecompiler.exe' could not be found.", style=MUPPET_ERROR)
            questionary.press_any_key_to_continue().ask()
            menu_setup()

# checks if user config file exists, if not, create
def first_time_check():
    if not os.path.exists(USER_CONFIG_PATH):
        create_config()

# creates config for the first time, initializes as false. during runtime, check if config_get() returns false, direct user to settings.
def create_config(): 
    config = configparser.ConfigParser()
    config['Paths'] = {
        'path_dmxconvert' : False,
        'path_compiler' : False,
        }
    with open(USER_CONFIG_PATH, 'w') as cfg:
        config.write(cfg)

# updates config
def update_config(variable, argument): 
    questionary.print(f"Updated config, {variable} to {argument}", style=MUPPET_INFO)
    config = configparser.ConfigParser()
    with open(USER_CONFIG_PATH, 'r+') as cfg:
        config.read(USER_CONFIG_PATH)
        config.set('Paths', variable, argument)
        config.write(cfg)

# returns value from config
def config_get(option): 
    config = configparser.ConfigParser()
    config.read(USER_CONFIG_PATH)
    return(config.get(option))

#TODO this is not used yet.
# verifies if the mod path is valid.
def verify_mod_path(mod_path: str) -> bool:
    mod_path = os.path.normpath(mod_path)
    mod_path = mod_path.lower()
    HLA_PATH = "half-life alyx/content/hlvr_addons"
    if HLA_PATH in mod_path:
        return True
    else:
        return False

# Starting Point
questionary.print("-== Welcome to MUPPET ==-", style=MUPPET_COLOR)
first_time_check() # check if config file has been made, if not, make config
main_menu()

import time
import pyautogui
import keyboard
from colorama import Fore, Style
import platform


def perform_click(inventory_keybind, game_version):
    coordinates = get_mouse_coordinates(game_version);
    pyautogui.hotkey(inventory_keybind)
    time.sleep(0.2)
    pyautogui.click(x=420, y=360, button='right')
    pyautogui.click(x=420, y=410)
    pyautogui.hotkey('esc')


def get_mouse_coordinates(game_version):
    resolution = pyautogui.size()

    coordinates = []

    return coordinates


def get_operating_system():
    system = platform.system()
    if system == 'Windows':
        version = platform.win32_ver()
        if version[0] == '10':
            return 'Windows 10'
        elif version[0] == '11':
            return 'Windows 11'
    elif system == 'Linux':
        return 'Linux'
    else:
        return 'Unbekannt'


def create_intro_output():
    app_version = "v0.2.1-beta (23.03.24)"
    app_name = "     QuickArmorChange " + app_version
    created_by = "     © 2024 by AEYCEN / 2_L_8"

    if get_operating_system() == 'Windows 11' or 'Linux':
        index_app = app_name.find("QuickArmorChange")
        index_aeycen = created_by.find("AEYCEN")
        index_2l8 = created_by.find("2_L_8")

        app_name = (
            f"{Fore.MAGENTA}{app_name[:index_app]}"
            f"{app_name[index_app:index_app + len('QuickArmorChange')]}{Style.RESET_ALL}"
            f"{app_name[index_app + len('QuickArmorChange'):]}"
        )

        created_by = (
            f"{created_by[:index_aeycen]}{Fore.CYAN}"
            f"{created_by[index_aeycen:index_aeycen + len('AEYCEN')]}{Style.RESET_ALL}"
            f"{created_by[index_aeycen + len('AEYCEN'):index_2l8]}{Fore.YELLOW}"
            f"{created_by[index_2l8:index_2l8 + len('2_L_8')]}{Style.RESET_ALL}"
            f"{created_by[index_2l8 + len('2_L_8'):]}"
        )

    print("")
    print(app_name)
    print(created_by)
    print("")
    print(f"     OS: {get_operating_system()} / Resolution: {pyautogui.size().width}x{pyautogui.size().height}px")


def create_response_output(hotkey_string):
    hotkey_input_response = "     QuickArmorChange is now RUNNING with the hotkey '" + hotkey_string + "'"

    if get_operating_system() == 'Windows 11' or 'Linux':
        index_running = hotkey_input_response.find("RUNNING")
        index_hotkey = hotkey_input_response.find(hotkey_string)

        hotkey_input_response = (
            f"{hotkey_input_response[:index_running]}{Fore.GREEN}"
            f"{hotkey_input_response[index_running:index_running + len('RUNNING')]}{Style.RESET_ALL}"
            f"{hotkey_input_response[index_running + len('RUNNING'):index_hotkey]}{Fore.MAGENTA}"
            f"{hotkey_input_response[index_hotkey:index_hotkey + len(hotkey_string)]}{Style.RESET_ALL}"
            f"{hotkey_input_response[index_hotkey + len(hotkey_string):]}"
        )

    print("")
    print(hotkey_input_response)


def create_outro_output():
    exit_hint = "     > Enter 'Shift' into console to deactivate QuickArmorChange <"

    if get_operating_system() == 'Windows 11' or 'Linux':
        index_open_bracket = exit_hint.find(">")
        index_close_bracket = exit_hint.find("<")

        exit_hint = (
            f"{exit_hint[:index_open_bracket]}{Fore.RED}"
            f"{exit_hint[index_open_bracket:index_open_bracket + len('>')]}{Style.RESET_ALL}"
            f"{exit_hint[index_open_bracket + len('>'):index_close_bracket]}{Fore.RED}"
            f"{exit_hint[index_close_bracket:index_close_bracket + len('<')]}{Style.RESET_ALL}"
            f"{exit_hint[index_close_bracket + len('<'):]}"
        )

    print(exit_hint)
    keyboard.wait('shift')


# # # App process # # #

create_intro_output()

game_version = input("     Enter your ARK Version. Survival Evolved [se] or Survival Ascended [sa]: ")
inventory_keybind = input("     Enter configured inventory keybind (e.g. 'i' or 'tab'): ")
hotkey = input("     Enter your preferred hotkey for the macro (e.g. 'l' or 'alt+l'): ")
keyboard.add_hotkey(hotkey, perform_click(inventory_keybind, game_version))

create_response_output(hotkey)

create_outro_output()

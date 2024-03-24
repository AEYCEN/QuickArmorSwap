import time
import pyautogui
import keyboard
from colorama import Fore, Style
import platform
import configparser
import os

settings_file = 'settings.txt'
app_version = "v0.3-beta (25.03.24)"


class Error(Exception):
    pass


def save_parameters_to_file(i_parameters_to_write):
    if not os.path.exists(settings_file):
        with open(settings_file, 'w') as file:
            file.write('')

    existing_parameters = load_all_parameters_from_file()

    existing_parameters.update(i_parameters_to_write)

    with open(settings_file, 'w') as file:
        for key, value in existing_parameters.items():
            file.write(f"{key}={value}\n")


def load_all_parameters_from_file():
    parameters = {}
    with open(settings_file, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            parameters[key] = value
    return parameters


def load_parameter_from_file(i_key):
    with open(settings_file, 'r') as file:
        for line in file:
            line_key, line_value = line.strip().split('=')
            if line_key == i_key:
                return line_value
    return 'Key not found'


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
        raise Error('Unknown OS (Mac is not supported)')


def read_game_ui_scaling(i_game_path, i_game_version):
    # try:
    #     config = configparser.ConfigParser(strict=False, allow_no_value=True)
    #     if i_game_version == 'ase':
    #         file_path = i_game_path + '/ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini'
    #     else:
    #         file_path = i_game_path + '/ShooterGame/Saved/Config/Windows/GameUserSettings.ini'
    #
    #     config.read(file_path)
    #
    #     if 'UIScaling' in config['/Script/ShooterGame.ShooterGameUserSettings']:
    #         return config['/Script/ShooterGame.ShooterGameUserSettings']['UIScaling']
    #     else:
    #         raise Error('ARK is not Installed')
    # except FileNotFoundError:
    #     raise Error('ARK is not Installed')

    return 1.0000


def read_game_inventory_keybind(i_game_path, i_game_version):
    # try:
    #     config = configparser.ConfigParser(strict=False)
    #     file_path = i_game_path + '/ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini'
    #     config.read(file_path)
    #
    #     if 'VoiceAudioVolume' in config['/Script/ShooterGame.ShooterGameUserSettings']:
    #         return config['/Script/ShooterGame.ShooterGameUserSettings']['UIScaling']
    #     else:
    #         return "Key not found"
    # except FileNotFoundError:
    return "i"


def get_mouse_coordinates(i_game_path, i_game_version):
    ui_scaling = read_game_ui_scaling(i_game_path, i_game_version)
    screen_width = pyautogui.size().width
    screen_height = pyautogui.size().height

    print(ui_scaling)

    coordinates = []

    if i_game_version == 'ase':
        # Diese ermittlung der Koordinaten erstellen bitte :)
        coordinates.append([420, 360])  # Koordinaten für den ersten Klick
        coordinates.append([420, 410])  # Koordinaten für den zweiten Klick

    else:
        coordinates.append([420, 360])
        coordinates.append([420, 410])

    return coordinates


def create_intro_output():
    app_name = "     QuickArmorSwap " + app_version
    created_by = "     © 2024 by AEYCEN / 2_L_8"

    if get_operating_system() == 'Windows 11' or 'Linux':
        index_app = app_name.find("QuickArmorSwap")
        index_aeycen = created_by.find("AEYCEN")
        index_2l8 = created_by.find("2_L_8")

        app_name = (
            f"{Fore.MAGENTA}{app_name[:index_app]}"
            f"{app_name[index_app:index_app + len('QuickArmorSwap')]}{Style.RESET_ALL}"
            f"{app_name[index_app + len('QuickArmorSwap'):]}"
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
    print(f'     [OS: {get_operating_system()} / Resolution: {pyautogui.size().width}x{pyautogui.size().height}px]')


def create_response_output(i_hotkey_string):
    hotkey_input_response = "     QuickArmorSwap is now RUNNING with the hotkey '" + i_hotkey_string + "'"

    if get_operating_system() == 'Windows 11' or 'Linux':
        index_running = hotkey_input_response.find("RUNNING")
        index_hotkey = hotkey_input_response.find("'" + i_hotkey_string + "'")
        hotkey_length = len(i_hotkey_string)

        hotkey_input_response = (
            f"{hotkey_input_response[:index_running]}{Fore.GREEN}"
            f"{hotkey_input_response[index_running:index_running + len('RUNNING')]}{Style.RESET_ALL}"
            f"{hotkey_input_response[index_running + len('RUNNING'):index_hotkey + 1]}{Fore.MAGENTA}"
            f"{hotkey_input_response[index_hotkey + 1:index_hotkey + 1 + hotkey_length]}{Style.RESET_ALL}"
            f"{hotkey_input_response[index_hotkey + 1 + hotkey_length:]}"
        )

    print("")
    print(hotkey_input_response)


def create_outro_output():
    exit_hint = "     > Hit 'SHIFT' into console to deactivate QuickArmorSwap <"

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

saved_parameters = load_all_parameters_from_file()

if 'game_version' not in saved_parameters or 'game_path' not in saved_parameters or 'hotkey' not in saved_parameters:
    print("")
    print("     - Setting up QuickArmorSwap -")

if 'game_version' not in saved_parameters:
    while True:
        game_version = input("     Enter your ARK Version. Survival Evolved [ase] or Survival Ascended [asa]: ")
        if game_version.lower() in ['ase', 'asa']:
            break
        else:
            print('     Invalid input. Please enter "ase" or "asa".')
    input_game_version = {'game_version': game_version}
    save_parameters_to_file(input_game_version)
else:
    game_version = load_parameter_from_file('game_version')

if 'game_path' not in saved_parameters:
    while True:
        if game_version == 'ase':
            game_path = input('     Enter your path to the "ASKSurvivalEvolved" game folder: ')
        else:
            game_path = input('     Enter your path to the "Ark Survival Ascended" game folder: ')
        if os.path.isdir(game_path) and ((game_version == 'ase' and game_path.endswith('ARKSurvivalEvolved')) or (game_version == 'asa' and game_path.endswith('Ark Survival Ascended'))):
            break
        else:
            if game_version == 'ase':
                game_path = input('     Invalid input. Please enter the whole folder path to the "ASKSurvivalEvolved" game folder: ')
            else:
                game_path = input('     Invalid input. Please enter the whole folder path to the "Ark Survival Ascended" game folder: ')
    input_game_path = {'game_path': game_path}
    save_parameters_to_file(input_game_path)
else:
    game_path = load_parameter_from_file('game_path')

if 'hotkey' not in saved_parameters:
    hotkey = input("     Enter your preferred hotkey for the macro (e.g. 'l' or 'alt+l'): ")
    input_hotkey = {'hotkey': hotkey}
    save_parameters_to_file(input_hotkey)
else:
    hotkey = load_parameter_from_file('hotkey')


def perform_macro():
    coordinates = get_mouse_coordinates(game_path, game_version)
    inventory_keybind = read_game_inventory_keybind(game_path, game_version)

    pyautogui.hotkey(inventory_keybind)
    time.sleep(0.2)
    pyautogui.click(x=coordinates[0][0], y=coordinates[0][1], button='right')
    pyautogui.click(x=coordinates[1][0], y=coordinates[1][1])
    pyautogui.hotkey('esc')


try:
    keyboard.add_hotkey(hotkey, perform_macro)
except Error as e:
    print("ERROR:", e)

create_response_output(hotkey)

create_outro_output()

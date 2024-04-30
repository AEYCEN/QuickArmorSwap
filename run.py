import time
import pyautogui
import keyboard
from colorama import Fore, Style
import platform
import configparser
import os
import tkinter

settings_file = 'settings.txt'
app_version = "v0.4-beta (30.04.24)"


class Error(Exception):
    pass


def save_parameters_to_file(i_parameters_to_write):
    if not os.path.exists(settings_file):
        raise Error('Settings file not found! Please create a file "settings.txt" in the QuickArmorSwap folder')

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
    try:
        config = configparser.ConfigParser(strict=False)
        if i_game_version == 'ase':
            file_path = i_game_path + '/ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini'
        else:
            file_path = i_game_path + '/ShooterGame/Saved/Config/Windows/GameUserSettings.ini'

        with open(file_path, 'r', encoding='utf-16') as file:
            config.read_file(file)

        section_name = '/Script/ShooterGame.ShooterGameUserSettings'

        if 'UIScaling' in config[section_name]:
            return config[section_name]['UIScaling']
        else:
            raise Error('ARK is not Installed')
    except FileNotFoundError:
        raise Error('ARK is not Installed')


def read_game_resolution(i_game_path, i_game_version):
    try:
        config = configparser.ConfigParser(strict=False)
        if i_game_version == 'ase':
            file_path = i_game_path + '/ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini'
        else:
            file_path = i_game_path + '/ShooterGame/Saved/Config/Windows/GameUserSettings.ini'

        with open(file_path, 'r', encoding='utf-16') as file:
            config.read_file(file)

        section_name = '/Script/ShooterGame.ShooterGameUserSettings'

        return [int(config[section_name]['ResolutionSizeX']), int(config[section_name]['ResolutionSizeY'])]
    except FileNotFoundError:
        raise Error('ARK is not Installed')


# def read_game_inventory_keybind(i_game_path, i_game_version):
#     try:
#         config = configparser.ConfigParser(strict=False)
#         file_path = i_game_path + '/ShooterGame/Saved/Config/WindowsNoEditor/GameUserSettings.ini'
#         config.read(file_path)
#
#         if 'VoiceAudioVolume' in config['/Script/ShooterGame.ShooterGameUserSettings']:
#             return config['/Script/ShooterGame.ShooterGameUserSettings']['UIScaling']
#         else:
#             return "Key not found"
#     except FileNotFoundError:
#     return "i"


def get_mouse_coordinates(i_game_path, i_game_version):
    # global ui_scaling
    # global resolution
    # screen_width = resolution[0]
    # screen_height = resolution[1]
    #
    coordinates = []
    #
    # if i_game_version == 'ase':
    #     # Diese ermittlung der Koordinaten erstellen bitte :)
    #     coordinates.append([400, 660])  # Koordinaten für den ersten Klick
    #     coordinates.append([400, 710])  # Koordinaten für den zweiten Klick
    #
    # else:
    #     coordinates.append([420, 360])
    #     coordinates.append([420, 410])

    fc_string = load_parameter_from_file('first_click_coordinates')
    fc_parts = fc_string.split(',')
    first_coordinates = [int(part) for part in fc_parts]

    sc_string = load_parameter_from_file('second_click_coordinates')
    sc_parts = sc_string.split(',')
    second_coordinates = [int(part) for part in sc_parts]

    coordinates.append(first_coordinates)
    coordinates.append(second_coordinates)

    return coordinates


def create_intro_output():
    global coloring
    app_name = "     QuickArmorSwap " + app_version
    created_by = "     © 2024 by AEYCEN / 2_L_8"

    if coloring:
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
    global coloring
    hotkey_input_response = "     QuickArmorSwap is now RUNNING with the hotkey '" + i_hotkey_string + "'"

    if coloring:
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
    global coloring
    exit_hint = "     > Press '#' to deactivate QuickArmorSwap <"

    if coloring:
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
    keyboard.wait('#')


def hide_label(i_label):
    time.sleep(2)
    i_label.master.destroy()


def update_lower_set_count():
    global set_count
    set_count -= 1
    displayText('Amor sets left: ' + str(set_count))


def update_upper_set_count():
    global set_count
    set_count += 1
    displayText('Amor sets left: ' + str(set_count))


def perform_macro():
    global game_path
    global game_version
    global inventory_keybind
    global set_count
    set_count -= 1
    coordinates = get_mouse_coordinates(game_path, game_version)

    pyautogui.hotkey(inventory_keybind)
    time.sleep(0.2)
    pyautogui.click(x=coordinates[0][0], y=coordinates[0][1], button='right')
    pyautogui.click(x=coordinates[1][0], y=coordinates[1][1])
    pyautogui.hotkey('esc')
    if set_count > 0:
        displayText('Armor sets left: ' + str(set_count))


def displayText(i_text):
    font_size = '32'
    label = tkinter.Label(text=i_text, font=('OCR A Extended', font_size), fg='white', bg='black')
    label.master.overrideredirect(True)
    x = pyautogui.size().width / 2
    label.master.geometry(f"+{round(x)}+{font_size}")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "black")
    label.pack()
    label.update()
    hide_label(label)


# - # - # - # - App process - # - # - # - #

coloring = False
operating_system = get_operating_system()
if operating_system == 'Windows 11' or operating_system == 'Linux':
    coloring = True

create_intro_output()

if not os.path.exists(settings_file):
    raise Error('Settings file not found! Please create a file "settings.txt" in the QuickArmorSwap folder.')

saved_parameters = load_all_parameters_from_file()

# COORDINATE CALC FEATURE
if 'first_click_coordinates' not in saved_parameters or 'second_click_coordinates' not in saved_parameters:
    raise Error('The keys "first_click_coordinates" and "second_click_coordinates" need to have saved comma seperated numbers in the settings.txt file.')

# ASA FEATURE
if load_parameter_from_file('game_version') == 'asa':
    raise Error('Unfortunately, the development of the feature for Ark: Survival Ascended is not yet complete. Please remove the content of the settings.txt file completely.')

if 'game_version' not in saved_parameters or 'hotkey' not in saved_parameters:
    print("")
    print("     - Setting up QuickArmorSwap -")

if 'game_version' not in saved_parameters:
    # while True:
    #     game_version = input("     Enter your ARK Version. Survival Evolved [ase] or Survival Ascended [asa]: ")
    #     if game_version.lower() in ['ase', 'asa']:
    #         break
    #     else:
    #         print('     Invalid input. Please enter "ase" or "asa".')
    #
    #     if game_version == 'asa':
    #         print()
    #         print(
    #             '     Unfortunately, the development of the feature for ASA is not yet complete. The program will now end')
    #         exit(1)
    game_version = 'ase'

    input_game_version = {'game_version': game_version}
    save_parameters_to_file(input_game_version)
else:
    game_version = load_parameter_from_file('game_version')

# if 'game_path' not in saved_parameters:
#     if game_version == 'ase':
#         game_path = input('     Enter your path to the "ARKSurvivalEvolved" game folder: ')
#     else:
#         game_path = input('     Enter your path to the "Ark Survival Ascended" game folder: ')
#
#     i = 0
#     while True:
#         if os.path.isdir(game_path) and ((game_version == 'ase' and game_path.endswith('ARKSurvivalEvolved')) or (
#                 game_version == 'asa' and game_path.endswith('Ark Survival Ascended'))):
#             break
#         else:
#             i = i + 1
#
#             if game_version == 'ase':
#                 if i >= 3:
#                     print(
#                         '     Input still invalid. Check out the instructions on our Github page under "Using QuickArmorSwap->In the Terminal"')
#                     game_path = input(
#                         '     Try again and enter the whole folder pathto the "ASKSurvivalEvolved" game folder: ')
#
#                 game_path = input(
#                     '     Invalid input. Enter the whole folder path to the "ASKSurvivalEvolved" game folder: ')
#             else:
#                 if i >= 3:
#                     print(
#                         '     Input still invalid. Check out the instructions on our Github page under "Using QuickArmorSwap->In the Terminal"')
#                     game_path = input(
#                         '     Try again and enter the whole folder pathto the "Ark Survival Ascended" game folder: ')
#
#                 game_path = input(
#                     '     Invalid input. Enter the whole folder path to the "Ark Survival Ascended" game folder: ')
#
#     input_game_path = {'game_path': game_path}
#     save_parameters_to_file(input_game_path)
# else:
game_path = load_parameter_from_file('game_path')

if 'hotkey' not in saved_parameters:
    hotkey = input("     Enter your preferred hotkey for the macro (e.g. 'l' or 'alt+l'): ")
    # COORDINATE CALC FEATURE
    print('     Dont forget do adjust the coordinate values in the settings.txt file before the first use. Further instructions are on our GitHub page.')

    input_hotkey = {'hotkey': hotkey}
    save_parameters_to_file(input_hotkey)
else:
    hotkey = load_parameter_from_file('hotkey')

# - - - - - - - - - Reading game files  - - - - - - - - - - - #
# ui_scaling = read_game_ui_scaling(game_path, game_version)
# resolution = read_game_resolution(game_path, game_version)
# inventory_keybind = read_game_inventory_keybind(game_path, game_version)
inventory_keybind = 'i'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

print('')
while True:
    set_count = input("     Enter your count of Amor sets(e.g. '5' or '10'): ")
    if set_count.isdigit():
        set_count = int(set_count)
        break
    else:
        print('     Invalid input. Please enter an integer number.')

try:
    keyboard.add_hotkey(hotkey, perform_macro)
    keyboard.add_hotkey('alt+1', update_lower_set_count)
    keyboard.add_hotkey('alt+2', update_upper_set_count)
except Error as e:
    print("ERROR:", e)

create_response_output(hotkey)

create_outro_output()

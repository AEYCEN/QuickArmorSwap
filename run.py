import time
import pyautogui
import keyboard
from colorama import Fore, Style
import platform
import configparser
import os
import tkinter
import threading

settings_file = 'settings.txt'
app_version = "v0.5-beta.dev3 (10.01.25)"


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
            line = line.strip()
            if '=' not in line or line == '':  # FIX: Leere Zeilen und Zeilen ohne '=' abfangen
                continue
            key, value = line.split('=', 1)  # FIX: maxsplit=1, falls der Wert ein '=' enthält
            parameters[key] = value
    return parameters


def load_parameter_from_file(i_key):
    with open(settings_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' not in line or line == '':  # FIX: Leere Zeilen abfangen
                continue
            line_key, line_value = line.split('=', 1)  # FIX: maxsplit=1
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


def get_mouse_coordinates():  # FIX: Unnötige Parameter entfernt
    coordinates = []

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


def create_response_output(i_hotkey):
    global coloring
    hotkey_input_response = "     QuickArmorSwap is now RUNNING with the hotkey '" + i_hotkey + "'"

    if coloring:
        index_running = hotkey_input_response.find("RUNNING")
        index_hotkey = hotkey_input_response.find("'" + i_hotkey + "'")
        hotkey_length = len(i_hotkey)

        hotkey_input_response = (
            f"{hotkey_input_response[:index_running]}{Fore.GREEN}"
            f"{hotkey_input_response[index_running:index_running + len('RUNNING')]}{Style.RESET_ALL}"
            f"{hotkey_input_response[index_running + len('RUNNING'):index_hotkey + 1]}{Fore.MAGENTA}"
            f"{hotkey_input_response[index_hotkey + 1:index_hotkey + 1 + hotkey_length]}{Style.RESET_ALL}"
            f"{hotkey_input_response[index_hotkey + 1 + hotkey_length:]}"
        )

    print("")
    print(hotkey_input_response)


def create_outro_output(i_deactivation_hotkey):
    global coloring
    exit_hint = "     > Press '" + i_deactivation_hotkey + "' to deactivate QuickArmorSwap <"

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
    keyboard.wait(i_deactivation_hotkey)



def update_lower_set_count():
    global set_count
    if set_count > 0:  # FIX: Nicht unter 0 gehen
        set_count -= 1
    displayText('Armor sets left: ' + str(set_count))  # FIX: "Amor" -> "Armor"


def update_upper_set_count():
    global set_count
    set_count += 1
    displayText('Armor sets left: ' + str(set_count))  # FIX: "Amor" -> "Armor"


def perform_macro():
    global game_version
    global inventory_keybind
    global set_count

    if set_count <= 0:  # FIX: Prüfen ob noch Sets vorhanden sind
        displayText('No armor sets left!')
        return

    set_count -= 1
    coordinates = get_mouse_coordinates()  # FIX: Keine unnötigen Parameter mehr

    pyautogui.hotkey(inventory_keybind)
    time.sleep(0.2)
    pyautogui.click(x=coordinates[0][0], y=coordinates[0][1], button='right')
    pyautogui.click(x=coordinates[1][0], y=coordinates[1][1])
    pyautogui.hotkey('esc')
    displayText('Armor sets left: ' + str(set_count))  # FIX: Immer anzeigen, nicht nur wenn > 0


def displayText(i_text):
    """Zeigt ein Overlay-Label für 2 Sekunden an.
    Alle Tkinter-Operationen laufen in einem eigenen Thread,
    damit der Hauptthread nicht blockiert wird und kein Thread-Konflikt entsteht."""

    def _run_overlay():
        try:
            font_size = 32
            root = tkinter.Tk()
            root.overrideredirect(True)
            root.configure(bg='black')

            label = tkinter.Label(root, text=i_text, font=('OCR A Extended', font_size), fg='white', bg='black')
            label.pack()

            # Fenster-Position berechnen (horizontal zentriert)
            root.update_idletasks()
            window_width = label.winfo_reqwidth()
            screen_width = pyautogui.size().width
            x = (screen_width - window_width) // 2
            root.geometry(f"+{x}+{font_size}")

            root.lift()
            root.wm_attributes("-topmost", True)
            root.wm_attributes("-disabled", True)
            root.wm_attributes("-transparentcolor", "black")

            # Nach 2 Sekunden schließen — via root.after(), bleibt im selben Thread
            root.after(2000, root.destroy)
            root.mainloop()

        except Exception as e:
            print(f"     Display overlay error: {e}")

    t = threading.Thread(target=_run_overlay, daemon=True)
    t.start()


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
    raise Error('The keys "first_click_coordinates" and "second_click_coordinates" need to have saved comma separated numbers in the settings.txt file.')

# ASA FEATURE
if load_parameter_from_file('game_version') == 'asa':
    raise Error('Unfortunately, the development of the feature for Ark: Survival Ascended is not yet complete. Please remove the content of the settings.txt file completely.')

if 'game_version' not in saved_parameters or 'hotkey' not in saved_parameters:
    print("")
    print("     - Setting up QuickArmorSwap -")

if 'game_version' not in saved_parameters:
    while True:
        game_version = input("     Enter your ARK Version. Survival Evolved [ase] or Survival Ascended [asa]: ")
        if game_version.lower() in ['ase', 'asa']:
            break
        else:
            print('     Invalid input. Please enter "ase" or "asa".')

        if game_version == 'asa':
            print()
            print(
                '     Unfortunately, the development of the feature for ASA is not yet complete. The program will now end')
            exit(1)
    game_version = 'ase'

    input_game_version = {'game_version': game_version}
    save_parameters_to_file(input_game_version)
else:
    game_version = load_parameter_from_file('game_version')

if 'hotkey' not in saved_parameters:
    hotkey = input("     Enter your preferred hotkey to execute the macro (e.g. 'l' or 'alt+l'): ")
    input_hotkey = {'hotkey': hotkey}
    save_parameters_to_file(input_hotkey)
else:
    hotkey = load_parameter_from_file('hotkey')

if 'deactivation_hotkey' not in saved_parameters:
    deactivation_hotkey = input("     Enter your preferred hotkey to deactivate the macro (e.g. '#'): ")
    print('')
    print('     Dont forget to adjust the coordinate values in the settings.txt file before the first use. Further instructions are on our GitHub page.')

    input_deactivation_hotkey = {'deactivation_hotkey': deactivation_hotkey}
    save_parameters_to_file(input_deactivation_hotkey)
else:
    deactivation_hotkey = load_parameter_from_file('deactivation_hotkey')

# - - - - - - - - - Reading game files  - - - - - - - - - - - #
inventory_keybind = 'i'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

print('')
while True:
    set_count = input("     Enter your count of Armor sets (e.g. '5' or '10'): ")  # FIX: "Amor" -> "Armor"
    if set_count.isdigit() and int(set_count) > 0:  # FIX: Auch 0 abfangen
        set_count = int(set_count)
        break
    else:
        print('     Invalid input. Please enter a positive integer number.')

try:
    keyboard.add_hotkey(hotkey, perform_macro)
    keyboard.add_hotkey('alt+1', update_lower_set_count)
    keyboard.add_hotkey('alt+2', update_upper_set_count)
except Exception as e:  # FIX: Exception statt Error, um auch keyboard-Fehlöiier abzufangen
    print("ERROR:", e)

create_response_output(hotkey)

create_outro_output(deactivation_hotkey)
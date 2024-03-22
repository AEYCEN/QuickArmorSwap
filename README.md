<p align="center">
  <picture>
    <source
      width="256px"
      media="(prefers-color-scheme: dark)"
    >
    <img 
      src="app/static/img/quickArmorChange-full.png"
    >
  </picture>
  <br><br>
  <b style="font-size: 16px">© 2024 by AEYCEN / 2_L_8</b>
   <br>
   Exploit the full potential and take the advantage.
</p>

# ARK:SE QuickArmorChange

<p style="font-size: 17px">Instant player armor swap macro for Ark: Survival Evolved.</p>

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ReVanced/revanced-patches/release.yml)
![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)


## 💪🏼 Features

Some of the features the macro provides are:

* ⏱️ **In-game armor swap in just 1 second**: One pressing your configured macro hotkey, all the armor pieces currently worn by the player will be swapped with a new set prepared in the inventory within one second
* ⌨️ **Customizable hotkey**: After launching the application, you can define your own key or key combination for the hotkey to activate the macro
* 🪶 **Lightweight application**: The application is very lightweight and takes up almost no storage space


## 🛠️ Installation

QuickArmorChange does require [Python](https://www.python.org/downloads/) >= 3.10 on the machine in order to run.
After downloading the .zip file, extract the files and copy the root folder to a desired location (e.g. Desktop).


### 🪟 Installation for Windows

After that, right-click the folder and select `Open in Terminal`. 
Then, try creating the virtual environment with the following command. 
If it fails because of restricting windows policies, you may activate the slider `Change execution policy` in the Windows-Settings under `System > For developers`, shown in the screenshot below:

    py -3 -m venv venv

![PowerShellSlider](img/settings_powerShellSlider.png)

After executing the last command you shouldn't get a response. Now you can activate the virtual environment with the following command:

    venv\Scripts\activate

A green command line prefix saying `(venv)` should appear. If so, install all the required dependencies:

    pip install -r requirements.txt


### 🐧 Installation for Linux

Right-click the root folder and select `Open in Terminal`.
If you are using Ubuntu Linux, you need to install the python virtual environment library first:

    sudo apt install python3-venv

Then create the virtual environment with the following command:

    python3 -m venv venv

After executing the last command you shouldn't get a response. Now you can activate the virtual environment with the following command:

    . venv/bin/activate

A command line prefix saying `(venv)` should appear. If so, install all the required dependencies:

    pip install -r requirements.txt


## 🚀 Usage

### 🦖 In-Game preparations
<a name="in-game-preparations"></a>

1. In order for QuickArmorChange to be able to change the armor, a folder with any name must be created in the player's inventory (however, "Armor" is recommended). 

2. For the following step, it is recommended to activate the folder view in the inventory, the button for switching is located in the upper right corner of the inventory next to the "Toggle tooltip" button.

3. Either one or more complete armor sets of any type (flak, leather, etc.) must be moved into the folder.

QuickArmorChange always replaces exactly one entire armor set.
The more sets there are in the folder, the more often the macro can be used to replace defective parts.


### ♻️ Launching QuickArmorSwap

#### 🪟 Launching on Windows

To start QuickArmorChange, open the terminal in the QuickArmorChange folder like described in the installation guide and always activate the environment with `venv\Scripts\activate` before you run the application with the following command:

    py run.py

ℹ️ If you want to stop the running environment (venv) after using the application, just type `deactivate`.


#### 🐧 Launching on Linux

To start QuickArmorChange, open the terminal in the QuickArmorChange folder like described in the installation guide and execute the following commands:

    . venv/Scripts/activate
    sudo su
    xhost +
    python run.py

ℹ️ If you want to stop the running environment (venv) after using the application, just type `deactivate`. Additionally, you can enable the access control again with `xhost -`.


### 🏂 Using QuickArmorSwap

#### 🖥️ In the terminal

First, the program will ask you which hotkey you would like to define to activate the macro.
You can define both individual keys on the keyboard and key combinations.
In the latter case, a `+` must be added to separate the keys for input.

> Examples:
> 
> Define the `L` key as a hotkey -> Enter: `l`
> 
> Define the key combination `ALT+L` as a hotkey -> Enter: `alt+l`

The following inputs are possible and with a `+` combinable for key combinations:
 
> ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright'

Once the hotkey has been successfully defined, the application confirms that it is active with the defined hotkey.

ℹ️ To deactivate the application and thus the macro, focus on the terminal and press `SHIFT` once.


#### 🦖 In-game

Once QuickArmorSwap has been successfully started, go into the game and into an active session (single player or multiplayer).
If you did the inventory preparations described in [In-Game preparations](#-in-game-preparations) you can now hit your hotkey and enjoy the magic.

❕ As soon as the macro has been started, there must be no strong mouse movement during the process, otherwise the macro cannot be executed correctly.

## 🔰 Version

> This README file is associated with QuickArmorSwap `v0.2-beta`


## 📖 Imprint

**Development, Conception & Support**
- [AEYCEN](https://github.com/AEYCEN) (Discord: aeycen)
- [2_L_8](https://github.com/2-L-8) (Discord: 2_l_8)

Create an issue ticket on GitHub for bug reports and feature requests or join our [Discord server](https://discord.gg/N55gSQcVEC) for individual support.


## 📜 Licence

QuickArmorChange is licensed under the GPLv3 licence. Please see the [licence file](LICENSE) for more information.
[tl;dr](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3) you may copy, distribute and modify QuickArmorChange as long as you track changes/dates in source files.
Any modifications to QuickArmorChange must also be made available under the GPL along with build & install instructions.

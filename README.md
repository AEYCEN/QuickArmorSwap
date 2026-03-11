<p align="center">
    <picture>
        <source
          width="200px"
          media="(prefers-color-scheme: dark)"
        >
        <img 
          src="img/qas.png"
        >
    </picture>
    <br>
    <b style="font-size: 16px">© 2024-2026 by AEYCEN / 2_L_8</b>
    <br>
    Exploit the full potential and take the advantage.
    <br>
</p>

---

<p style="font-size: 17px">Instant player armor swap macro for Ark: Survival Evolved.</p>

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ReVanced/revanced-patches/release.yml)
![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)

> NOTE: Ark: Survival Ascended is not supported yet

## 💪🏼 Features

* ⚡ **Instant armor swap in ~0.5 seconds** — Press your configured hotkey and QuickArmorSwap will open your inventory, right-click the armor folder, and equip a fresh set — all within half a second
* ⌨️ **Fully customizable hotkeys** — Choose any key or key combination for both the macro trigger and the deactivation key
* 🔢 **On-screen armor set counter** — A color-coded HUD overlay shows how many sets remain (cyan → amber → red) with a smooth fade-out animation
* 🔍 **Automatic game detection** — Reads your ARK installation folder to auto-detect your inventory keybind, UI scaling, resolution, and required settings
* 🎯 **Guided coordinate calibration** — An interactive overlay lets you position two crosshair markers directly on the correct inventory slots.
* 📐 **UIScaling change detection** — If you change your in-game UI scaling, the calibration wizard automatically re-triggers on next launch
* 🪶 **Lightweight** — Single Python script, minimal dependencies, almost no storage footprint


## 📋 Requirements

* **Windows 10 or Windows 11**
* **[Python 3.10+](https://www.python.org/downloads/)** — Make sure to check **"Tcl/Tk and IDLE"** during installation (it is checked by default)
* **ARK: Survival Evolved** — Must be installed and launched at least once so the config files exist


## 🛠️ Installation

### Step 1 — Download and extract

Download the latest QuickArmorSwap `.zip` file from GitHub. Extract it and copy the folder to a location of your choice (e.g. your Desktop).

### Step 2 — Open a Command Prompt in the folder

Open the QuickArmorSwap folder in File Explorer. Click the address bar at the top, type `cmd`, and press Enter. A Command Prompt window will open, already set to the correct folder.

<!-- 📸 SCREENSHOT: File Explorer address bar with "cmd" typed in, and the resulting CMD window -->

### Step 3 — Create a virtual environment

Run the following command to create an isolated Python environment:

```
py -3 -m venv venv
```

You should not see any output — that means it worked.

### Step 4 — Activate the virtual environment

```
venv\Scripts\activate
```

You should see a `(venv)` prefix appear before the command prompt.

<!-- 📸 SCREENSHOT: CMD window showing (venv) prefix -->

### Step 5 — Install dependencies

With the virtual environment active (you see `(venv)` in your prompt), run:

```
pip install -r requirements.txt
```

Wait for the installation to complete. You're ready to go.


## 🦖 In-Game Preparations

Before using QuickArmorSwap, you need to set up your ARK inventory:

### 1. Set windowed mode

The game **must** run in **Windowed** or **Windowed Fullscreen** mode. Native fullscreen is not supported and will cause the screen to turn black when the overlay appears.

<!-- 📸 SCREENSHOT: ARK display settings showing windowed/windowed fullscreen option -->

### 2. Enable "Disable Menu Transitions"

This is **required**. Without it, the inventory animation delay will cause the macro to click in the wrong places.

1. Open ARK
2. Go to **Options → Advanced**
3. Check **"Disable Menu Transitions"**
4. Click **Apply** and **Save**

<!-- 📸 SCREENSHOT: ARK advanced settings with "Disable Menu Transitions" checked -->

> QuickArmorSwap checks this setting automatically on launch and will tell you if it's not enabled.

### 3. Create an armor folder in your inventory

1. Open your inventory
2. Create a new folder (the name doesn't matter, but "Armor" is recommended)
3. It is recommended to enable **folder view** in the inventory — the toggle button is in the upper-right corner of the inventory, next to the "Toggle tooltip" button

<!-- 📸 SCREENSHOT: ARK inventory with folder view enabled and an "Armor" folder visible -->

### 4. Fill the folder with armor sets

Move one or more **complete** armor sets (helmet, chest, gloves, legs, boots) of any type into the folder. Each set equals one macro use. The more sets you have, the more often you can swap before needing to restock.

<!-- 📸 SCREENSHOT: Inside the armor folder showing multiple complete armor sets -->


## 🚀 Launching QuickArmorSwap

Every time you want to use QuickArmorSwap:

1. Open a terminal in the QuickArmorSwap folder (see [Installation Step 2](#step-2--open-a-terminal-in-the-folder))
2. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
3. Run the application:
   ```
   py run.py
   ```

> To stop the virtual environment after you're done, type `deactivate`.


## ✨ First-Time Setup

When you launch QuickArmorSwap for the first time, a guided setup wizard walks you through the configuration. All your settings are saved in `settings.txt` and remembered for future launches.

<!-- 📸 SCREENSHOT: Terminal showing the QuickArmorSwap banner and first-time setup panel -->

### 1. ARK version

You'll be asked which ARK version you're using. Currently only **ASE** (Ark: Survival Evolved) is fully supported. Type `ase` and press Enter.

### 2. Game folder path

Enter the **full path** to your `ARKSurvivalEvolved` game folder. This is typically something like:

```
C:\Program Files (x86)\Steam\steamapps\common\ARKSurvivalEvolved
```

**How to find this path on Steam:**
1. Open Steam
2. Right-click **ARK: Survival Evolved** in your library
3. Select **Manage → Browse local files**
4. Copy the path from the File Explorer address bar

<!-- 📸 SCREENSHOT: Steam "Browse local files" option and the resulting Explorer window with the path highlighted -->

> QuickArmorSwap uses this path to automatically detect your **inventory keybind** from `Input.ini`. If you use a custom key to open your inventory (e.g. Tab instead of I), it will be detected and used. If the file isn't found, the default key `I` is used.

### 3. Macro hotkey

Enter the key or key combination you want to use to trigger the armor swap. Examples:

| Input          | Meaning                     |
|----------------|-----------------------------|
| `l`            | Press the L key             |
| `+`            | Press the + key             |
| `alt+l`        | Hold Alt and press L        |
| `ctrl+shift+l` | Hold Ctrl+Shift and press L |

Choose a key that doesn't conflict with any ARK keybinds.

### 4. Deactivation hotkey

Enter the key you want to use to stop QuickArmorSwap. For example `#` or `esc`. This is the key you press when you're done playing and want to shut down the macro, it works in-game too.

### 5. Coordinate calibration

This is the most important step. QuickArmorSwap needs to know exactly where on your screen the armor folder and the equip button are located.

An overlay with **two crosshair markers** will appear on top of your screen:

| Marker | Color | What to place it on |
|--------|-------|---------------------|
| **1st marker** | 🟢 Green | The **armor folder** in your inventory (right-click target) |
| **2nd marker** | 🟠 Orange | The **"Equip Items" option** in the dropdown menu that appears after right-clicking the folder |

<!-- 📸 SCREENSHOT: Calibration overlay showing both crosshair markers positioned on the inventory -->

**Controls during calibration** (these work globally — even when ARK has focus):

| Key | Action |
|-----|--------|
| `Arrow keys` | Move the active marker by 1 pixel |
| `Shift + Arrow keys` | Move the active marker by 10 pixels |
| `Enter` | Confirm the current marker position |
| `Esc` | Cancel calibration |

**How to calibrate:**

1. When asked "Press Enter to start calibration", open ARK and go into a session
2. Open your inventory so the armor folder is visible
3. Press **Enter** (works even while ARK has focus)
4. Position the **green marker** directly on your armor folder and press **Enter**
5. Right-click the folder so the dropdown menu appears
6. Position the **orange marker** on the "Equip Items" option and press **Enter**
7. Done! The coordinates are saved automatically

> **Tip:** Use `Shift + Arrow keys` for big adjustments, then fine-tune with regular arrow keys.

### 6. Armor set count

Enter how many armor sets are currently in your folder. This number is shown on the in-game overlay and decremented each time you use the macro.

After this, QuickArmorSwap is fully configured and running:

<!-- 📸 SCREENSHOT: Terminal showing the status table with all settings, the green "RUNNING" indicator, and the exit hint -->


## 🎮 Using QuickArmorSwap In-Game

Once you see **● RUNNING** in the terminal, the macro is active. Switch to ARK and play.

### Swapping armor

Press your **macro hotkey**. QuickArmorSwap will:

1. Open your inventory (using your detected keybind)
2. Right-click the armor folder
3. Click the equip option
4. Close the inventory

All of this happens within roughly 0.5 seconds. A HUD overlay at the top of the screen briefly shows how many sets you have left.

<!-- 📸 SCREENSHOT: In-game HUD overlay showing "4 sets left" in cyan -->

> **⚠️ Important:** Do not move your mouse while the macro is running. The process is very fast, but any strong mouse movement during the ~0.5 seconds will cause misclicks.

### Armor set counter

The overlay changes color to indicate urgency:

| Color | Meaning |
|-------|---------|
| 🔵 Cyan | Normal — plenty of sets left |
| 🟡 Amber | Warning — 2 or fewer sets remaining |
| 🔴 Red | Empty — no sets left (shows "Restock!") |

### Adjusting the count

| Hotkey | Action |
|--------|--------|
| `Alt+1` | Decrease count by 1 |
| `Alt+2` | Increase count by 1 |

Use `Alt+2` after you've refilled your armor folder to update the counter without restarting.

### Stopping QuickArmorSwap

Press your **deactivation hotkey** (e.g. `#`). The program will shut down cleanly.


## ⚙️ Configuration

All settings are stored in `settings.txt` in the QuickArmorSwap folder. This file is created automatically after first-time setup. A typical file looks like this:

```
game_version=ase
game_path=C:\Program Files (x86)\Steam\steamapps\common\ARKSurvivalEvolved
hotkey=+
deactivation_hotkey=#
first_click_coordinates=320,580
second_click_coordinates=330,670
inventory_keybind=tab
saved_ui_scaling=1.000000
```

### Resetting a specific setting

If you want to change any setting, simply **delete the corresponding line** from `settings.txt`, save the file, and restart QuickArmorSwap. The setup wizard will ask you for that value again.

For example, to change your hotkey, delete the `hotkey=...` line and restart.

### When re-calibration happens automatically

QuickArmorSwap saves the `UIScaling` value from your ARK settings alongside your calibrated coordinates. If you change your in-game UI scaling, the calibration wizard will automatically trigger again on the next launch so your click positions stay accurate.


## 🪲 Troubleshooting

### The screen turns black and the game minimizes after pressing the hotkey

Your game is running in native fullscreen. Switch to **Windowed** or **Windowed Fullscreen** mode in ARK's display settings.

### "Required ARK setting not enabled!" error on launch

You need to enable **"Disable Menu Transitions"** in ARK under **Options → Advanced**. See [In-Game Preparations](#2-enable-disable-menu-transitions).

### "GameUserSettings.ini not found" error

Make sure you've launched ARK at least once so the config files are created, and that your game path in `settings.txt` points to the correct `ARKSurvivalEvolved` folder.

### The macro clicks in the wrong places

Re-run the calibration by deleting the lines `first_click_coordinates`, `second_click_coordinates`, and `saved_ui_scaling` from `settings.txt`, then restart QuickArmorSwap.

### I want to change my hotkey

Delete the `hotkey=...` line from `settings.txt`, save, and restart. You'll be asked to enter a new one.

### I changed my inventory keybind in ARK

Delete the `inventory_keybind=...` line from `settings.txt` and restart. QuickArmorSwap will re-read your keybind from ARK's `Input.ini`.

### The counter shows the wrong number after restocking

Use `Alt+2` to increment the count for each set you added back to the folder. Use `Alt+1` if you went one too high.

### The set count drops to 0 and shows "Restock!" after pressing `Alt+1` or `Alt+2`

You probably installed Python without enabling the **"Tcl/Tk and IDLE"** option. Reinstall Python and make sure this option is checked during installation.

<!-- 📸 SCREENSHOT: Python installer with "tcl/tk and IDLE" checkbox highlighted -->


## 🔰 Version

This README is associated with **QuickArmorSwap v1.0-beta1 (11.03.26)**.

### Upgrading to a new version

1. Delete the old QuickArmorSwap folder
2. Extract the new version
3. Copy your old `settings.txt` into the new folder to keep your settings

> If the new version introduces changes to settings format, you may need to delete `settings.txt` and go through the setup again.


## 💫 Contact

**Development, Conception & Support**
- [AEYCEN](https://github.com/AEYCEN) (Discord: aeycen)
- [2_L_8](https://github.com/2-L-8) (Discord: 2_l_8)

Create an issue ticket on GitHub for bug reports and feature requests, or join our [Discord server](https://discord.gg/N55gSQcVEC) for individual support.
 git fetch origin
  git branch -u origin/reimplementation reimplementation
  git remote set-head origin -a

## 📜 License

QuickArmorSwap is licensed under the **GPLv3 license**. See the [LICENSE](LICENSE) file for details.

[tl;dr](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3) — You may copy, distribute, and modify QuickArmorSwap as long as you track changes/dates in source files. Any modifications must also be made available under the GPL along with build & install instructions.
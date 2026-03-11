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
    Exploit the full potential and take the advantage
    <br>
</p>

---

<p style="font-size: 17px">Instant player armor swap macro for Ark: Survival Evolved (ASE) and Ark: Survival Ascended (ASA)</p>

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/ReVanced/revanced-patches/release.yml)
![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)


## 💪🏼 Features

* ⚡ **Instant armor swap in ~0.5 seconds** — Press your configured hotkey and QuickArmorSwap will open your inventory, right-click the armor folder, and equip a fresh set — all within half a second
* 🦖 **Supports both ASE and ASA** — Switch between Ark: Survival Evolved and Ark: Survival Ascended at any time. Game paths, calibration, and keybinds are stored separately per version
* 🔍 **Automatic game settings sync** — Reads your ARK config files to detect your inventory keybind, UI scaling, and resolution. Changes to your in-game settings are picked up automatically
* 🎯 **Guided coordinate calibration** — An interactive overlay lets you position two crosshair markers directly on the correct inventory slots — no manual pixel guessing
* ⌨️ **Fully customizable hotkeys** — Choose any key or key combination for both the macro trigger and the deactivation key
* 🔢 **On-screen armor set counter** — A color-coded HUD overlay shows how many sets remain to change
* 📐 **UIScaling change detection** — If you change your in-game UI scaling, the calibration wizard automatically re-triggers on next launch
* 🪶 **Lightweight** — Single Python script, minimal dependencies, almost no storage footprint


## 📋 Requirements

* **Windows 10 or Windows 11**
* **[Python 3.10+](https://www.python.org/downloads/)** — Make sure to check **"Tcl/Tk and IDLE"** during installation (it is checked by default)
* **ARK: Survival Evolved** and/or **ARK: Survival Ascended** — Must be installed and launched at least once so the config files exist


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

Before using QuickArmorSwap, you need to prepare a few things inside ARK. These steps apply to both ASE and ASA unless noted otherwise.

### 1. Set windowed mode

The game **must** run in **Windowed** or **Windowed Fullscreen** mode. Native fullscreen is not supported and will cause the screen to turn black when the overlay appears.

<!-- 📸 SCREENSHOT: ARK display settings showing windowed/windowed fullscreen option -->

### 2. Enable "Disable Menu Transitions"

This is **required**. Without it, the inventory animation delay will cause the macro to click in the wrong places.

1. Open ARK
2. Navigate to the setting:
   - **ASE:** Options → Advanced
   - **ASA:** Settings → General → UI
3. Check **"Disable Menu Transitions"**
4. Click **Apply** and **Save**

<!-- 📸 SCREENSHOT: ARK advanced settings with "Disable Menu Transitions" checked -->

> QuickArmorSwap checks this setting automatically on launch and will show an error with step-by-step instructions if it's not enabled.

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

1. Open a Command Prompt in the QuickArmorSwap folder (open the folder in File Explorer, click the address bar, type `cmd`, press Enter)
2. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
3. Run the application:
   ```
   py run.py
   ```
You can interrupt the application at any point with pressing `CTRL+C` inside the terminal.

> (Optional) To stop the virtual environment after you're done, type `deactivate`.


## ✨ First-Time Setup

When you launch QuickArmorSwap for the first time, a guided setup wizard walks you through the configuration. All your settings are saved in `settings.txt` and remembered for future launches.

<!-- 📸 SCREENSHOT: Terminal showing the QuickArmorSwap banner and first-time setup panel -->

### 1. ARK version

You'll be asked which ARK version you're using:

| Input | Game |
|-------|------|
| `ase` | Ark: Survival Evolved |
| `asa` | Ark: Survival Ascended |

After choosing, you'll be asked: **"Ask for game version on every start?"**

- **Yes** — Every time you launch QuickArmorSwap, you can choose between ASE and ASA. Your last selection is the default (just press Enter to keep it). This is ideal if you play both games.
- **No** — The version you chose is used on every start without asking. You can always change this later in `settings.txt`.

> Game paths, calibrated coordinates, and UI scaling are stored **separately** for each version. Switching between ASE and ASA does not lose any settings — everything is remembered independently.

### 2. Game folder path

Enter the **full path** to your game's root folder:

| Version | Expected folder name | Example path                                                                          |
|---------|---------------------|---------------------------------------------------------------------------------------|
| **ASE** | `ARKSurvivalEvolved` | `C:\Program Files\Epic Games\ARKSurvivalEvolved` (Epic Games example)                 |
| **ASA** | `Ark Survival Ascended` | `C:\Program Files (x86)\Steam\steamapps\common\Ark Survival Ascended` (Steam example) |

**How to find this path on Steam:**
1. Open Steam
2. Right-click the game in your library
3. Select **Manage → Browse local files**
4. Copy the path from the File Explorer address bar

<!-- 📸 SCREENSHOT: Steam "Browse local files" option and the resulting Explorer window with the path highlighted -->

Each version's path is only asked once. If you later switch to the other version (e.g. from ASE to ASA), you'll be asked for that version's path on first use.

> **What gets synced from the game folder:**
>
> QuickArmorSwap reads the following from your game's config files on every launch:
>
> | Setting | Source file | Fallback if not found |
> |---------|-----------|----------------------|
> | Inventory keybind | `Input.ini` | Default key `I` |
> | UI scaling | `GameUserSettings.ini` | Default `1.0` |
> | Resolution | `GameUserSettings.ini` | Current screen resolution |
>
> The config files are located at:
> - **ASE:** `<game folder>\ShooterGame\Saved\Config\WindowsNoEditor\`
> - **ASA:** `<game folder>\ShooterGame\Saved\Config\Windows\`
>
> These values are **never saved** to `settings.txt` — they are re-read from the game files every time. If you change your inventory keybind or UI scaling in ARK, QuickArmorSwap picks it up automatically on the next launch.

### 3. Macro hotkey

Enter the key or key combination you want to use to trigger the armor swap. Examples:

| Input | Meaning |
|-------|---------|
| `l` | Press the L key |
| `+` | Press the + key |
| `alt+l` | Hold Alt and press L |
| `ctrl+shift+l` | Hold Ctrl+Shift and press L |

Choose a key that doesn't conflict with any ARK keybinds.

### 4. Deactivation hotkey

Enter the key you want to use to stop QuickArmorSwap. For example `#` or `esc`. This key works globally — even while ARK has focus.

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

> **Note:** Coordinates are stored separately per game version. If you switch from ASE to ASA (or vice versa) and haven't calibrated for that version yet, the calibration wizard will run again.

### 6. Armor set count

Enter how many armor sets are currently in your folder. This number is shown on the in-game overlay and decremented each time you use the macro.

After this, QuickArmorSwap is fully configured and running:

<!-- 📸 SCREENSHOT: Terminal showing the status table with all settings, the green "RUNNING" indicator, and the exit hint -->


## 🎮 Using QuickArmorSwap In-Game

Once you see <span style="color: lime">**● RUNNING**</span> in the terminal, the macro is active. Switch to ARK and play.

### Swapping armor

1. Don't be in any menu screen. The macro will not function if you activate it while you are in an open menu.
2. Press your **macro hotkey**. 

QuickArmorSwap will:

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

When the macro is ● RUNNING, press your **deactivation hotkey** (e.g. `#`). The program will shut down cleanly. This is even possible while tabbed into the game.

Otherwise press `CTRL+C` at any point inside the terminal to force interrupt the application.


## ⚙️ Configuration

All settings are stored in `settings.txt` in the QuickArmorSwap folder. This file is created automatically after first-time setup. A typical file for a user who plays both ASE and ASA looks like this:

```
last_selected_game_version=ase
hotkey=+
deactivation_hotkey=#
ask_version_on_start=True
ase_game_path=C:\Program Files (x86)\Steam\steamapps\common\ARKSurvivalEvolved
asa_game_path=D:\SteamLibrary\steamapps\common\Ark Survival Ascended
ase_first_click_coords=320,580
ase_second_click_coords=330,670
ase_saved_ui_scaling=1.000000
asa_first_click_coords=415,600
asa_second_click_coords=425,690
asa_saved_ui_scaling=0.850000
```

Note that **inventory keybind**, **resolution**, and **UI scaling** are _not_ stored here — they are re-read from your game files on every launch.

### Resetting a specific setting

If you want to change any setting, simply **delete the corresponding line** from `settings.txt`, save the file, and restart QuickArmorSwap. The setup wizard will ask you for that value again.

For example, to change your hotkey, delete the `hotkey=...` line and restart.

### Switching between ASE and ASA

If `ask_version_on_start` is set to `True`, you'll be asked which version to use on every launch. Your last choice is the default — just press Enter to keep it.

If you set it to `False` during first-time setup and want to change it later, either:
- Edit `settings.txt` and change `ask_version_on_start=True`
- Or delete the `ask_version_on_start` and `last_selected_game_version` lines to re-trigger the setup

### When re-calibration happens automatically

QuickArmorSwap saves the `UIScaling` value alongside the calibrated coordinates for each version. If you change your in-game UI scaling, the calibration wizard will automatically trigger on the next launch for that version.


## 🪲 Troubleshooting

### The screen turns black and the game minimizes after pressing the hotkey

Your game is running in native fullscreen. Switch to **Windowed** or **Windowed Fullscreen** mode in ARK's display settings.

### "Required ARK setting not enabled!" error on launch

You need to enable **"Disable Menu Transitions"** in ARK:
- **ASE:** Options → Advanced
- **ASA:** Settings → General → UI

See [In-Game Preparations](#2-enable-disable-menu-transitions).

### "GameUserSettings.ini not found" error

Make sure you've launched ARK at least once so the config files are created, and that the game path in `settings.txt` points to the correct folder.

### The macro clicks in the wrong places

Re-run the calibration by deleting the coordinate and scaling lines for your version from `settings.txt`. For example, for ASE delete:
```
ase_first_click_coords=...
ase_second_click_coords=...
ase_saved_ui_scaling=...
```
Then restart QuickArmorSwap.

### I want to change my hotkey

Delete the `hotkey=...` line from `settings.txt`, save, and restart. You'll be asked to enter a new one.

### The inventory keybind shows "(default)" but I have a custom keybind in ARK

QuickArmorSwap reads the keybind from `Input.ini` in your game's config folder on every launch. If it shows "(default)", the file either doesn't exist or doesn't contain a `ShowMyInventory` entry. Make sure you've customized the keybind _inside ARK_ (not just in an external config editor) and that the game has been launched at least once since.

### The counter shows the wrong number after restocking

Use `Alt+2` to increment the count for each set you added back to the folder. Use `Alt+1` if you went one too high.

### The set count overlay crashes or doesn't appear

You probably installed Python without enabling the **"Tcl/Tk and IDLE"** option. Reinstall Python and make sure this option is checked during installation.

<!-- 📸 SCREENSHOT: Python installer with "tcl/tk and IDLE" checkbox highlighted -->


## 🔰 Version

This README is associated with **QuickArmorSwap v1.0-beta2 (12.03.26)**.

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

> ⭐ If you like this project, support us by giving it a Star on [GitHub](https://github.com/AEYCEN/QuickArmorSwap) :)

## 📜 License

QuickArmorSwap is licensed under the **GPLv3 license**. See the [LICENSE](LICENSE) file for details.

[tl;dr](https://www.tldrlegal.com/license/gnu-general-public-license-v3-gpl-3) — You may copy, distribute, and modify QuickArmorSwap as long as you track changes/dates in source files. Any modifications must also be made available under the GPL along with build & install instructions.
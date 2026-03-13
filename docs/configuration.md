# ⚙️ Configuration

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

## Resetting a specific setting

If you want to change any setting, simply **delete the corresponding line** from `settings.txt`, save the file, and restart QuickArmorSwap. The setup wizard will ask you for that value again.

For example, to change your hotkey, delete the `hotkey=...` line and restart.

## Switching between ASE and ASA

If `ask_version_on_start` is set to `True`, you'll be asked which version to use on every launch. Your last choice is the default — just press Enter to keep it.

If you set it to `False` during first-time setup and want to change it later, either:
- Edit `settings.txt` and change `ask_version_on_start=True`
- Or delete the `ask_version_on_start` and `last_selected_game_version` lines to re-trigger the setup

## When re-calibration happens automatically

QuickArmorSwap saves the `UIScaling` value alongside the calibrated coordinates for each version. If you change your in-game UI scaling, the calibration wizard will automatically trigger on the next launch for that version.

## ⏭️ Next steps

**Continue with [❔ Troubleshooting](troubleshooting.md)**


*Or go back to*:
  - [🎮 Using QuickArmorSwap In-Game](usage.md)
  - [Startpage](https://github.com/AEYCEN/QuickArmorSwap)
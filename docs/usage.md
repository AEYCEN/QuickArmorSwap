# 🎮 Using QuickArmorSwap In-Game

Once you see <span style="color: #85FF00">**● RUNNING**</span> in the terminal, the macro is active. Switch to ARK and play.

## Swapping armor

1. Don't be in any menu screen. The macro will not function if you activate it while you are in an open menu.
2. Press your **macro hotkey**. 

QuickArmorSwap will:

1. Open your inventory (using your detected keybind)
2. Right-click the armor folder
3. Click the equip option
4. Close the inventory

All of this happens within roughly 0.5 seconds. A HUD overlay at the top of the screen briefly shows how many sets you have left.

<img src="../img/screenshot/ase-armor-counter.png" style="width: 100%" alt="SCREENSHOT: In-game HUD overlay showing '4 sets left' in cyan">


> **⚠️ Important:** Do not move your mouse while the macro is running. The process is very fast, but any strong mouse movement during the ~0.5 seconds will cause misclicks.

## Armor set counter

The overlay changes color to indicate urgency:

| Color | Meaning |
|-------|---------|
| 🔵 Cyan | Normal — plenty of sets left |
| 🟡 Amber | Warning — 2 or fewer sets remaining |
| 🔴 Red | Empty — no sets left (shows "Restock!") |

## Adjusting the count

| Hotkey | Action |
|--------|--------|
| `Alt+1` | Decrease count by 1 |
| `Alt+2` | Increase count by 1 |

Use `Alt+2` after you've refilled your armor folder to update the counter without restarting.

## Stopping QuickArmorSwap

When the macro is ● RUNNING, press your **deactivation hotkey** (e.g. `#`). The program will shut down cleanly. This is even possible while tabbed into the game.

Otherwise press `CTRL+C` at any point inside the terminal to force interrupt the application.

## ⏭️ Next steps

**Continue with [⚙️ Configuration](configuration.md)**


*Or go back to*:
  - [✨ First-Time Setup](first-time-setup.md)
  - [Startpage](https://github.com/AEYCEN/QuickArmorSwap)
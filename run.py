"""
QuickArmorSwap — Ark: Survival Ascended and Ark: Survival Evolved Macro Tool
Quickly swap armor sets in-game with a single hotkey press.

© 2024-2026 by AEYCEN / 2_L_8
"""

from __future__ import annotations

import os
import platform
import queue
import re
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import keyboard
import pyautogui

# ─── Rich Console Setup ────────────────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, IntPrompt
    from rich.table import Table
    from rich.text import Text
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

APP_VERSION = "v1.0 (16.03.26)"
SETTINGS_FILE = Path("settings.txt")

console = Console() if HAS_RICH else None


# ═══════════════════════════════════════════════════════════════════════════════
#  Exceptions
# ═══════════════════════════════════════════════════════════════════════════════

class QuickArmorSwapError(Exception):
    """Base exception for all app-specific errors."""


class SettingsError(QuickArmorSwapError):
    """Raised when the settings file is missing or malformed."""


class PlatformError(QuickArmorSwapError):
    """Raised on unsupported operating systems."""


# ═══════════════════════════════════════════════════════════════════════════════
#  Settings (dataclass-based, replaces loose file helpers)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Coordinates:
    x: int
    y: int

    @classmethod
    def from_string(cls, raw: str) -> Coordinates:
        """Parse '420,360' → Coordinates(420, 360)."""
        parts = [p.strip() for p in raw.split(",")]
        if len(parts) != 2 or not all(p.lstrip("-").isdigit() for p in parts):
            raise SettingsError(f"Invalid coordinate format: '{raw}'. Expected 'x,y' (e.g. '420,360').")
        return cls(x=int(parts[0]), y=int(parts[1]))

    def __str__(self) -> str:
        return f"{self.x},{self.y}"


@dataclass
class Settings:
    """Holds every persisted user preference.

    Version-dependent fields (game path, keybind, coordinates, UIScaling)
    are stored separately per game version (_ase / _asa suffixes).
    Property accessors route to the correct field based on the currently
    selected ``last_selected_game_version``.
    """

    # ── Global settings ──────────────────────────────────────────────────────
    last_selected_game_version: Optional[str] = None
    hotkey: Optional[str] = None
    deactivation_hotkey: Optional[str] = None
    ask_version_on_start: Optional[bool] = None

    # ── Per-version settings ─────────────────────────────────────────────────
    ase_game_path: Optional[str] = None
    asa_game_path: Optional[str] = None
    ase_inventory_keybind: str = ""   # runtime only — always re-read from game files
    asa_inventory_keybind: str = ""
    _keybind_from_file: bool = False  # True = read from Input.ini, False = fallback "i"
    _ui_scaling_from_file: bool = False  # True = read from GameUserSettings.ini
    _res_x: int = 0       # runtime only — game resolution
    _res_y: int = 0
    _resolution_from_file: bool = False  # True = from GameUserSettings.ini, False = screen max
    first_click_ase: Optional[Coordinates] = None
    first_click_asa: Optional[Coordinates] = None
    second_click_ase: Optional[Coordinates] = None
    second_click_asa: Optional[Coordinates] = None
    ase_saved_ui_scaling: Optional[float] = None
    asa_saved_ui_scaling: Optional[float] = None

    # ── Version-aware property accessors ─────────────────────────────────────
    # The rest of the codebase uses these — they transparently route
    # to the _ase / _asa field matching the current game version.

    @property
    def game_version(self) -> Optional[str]:
        return self.last_selected_game_version

    @game_version.setter
    def game_version(self, value: Optional[str]) -> None:
        self.last_selected_game_version = value

    @property
    def game_path(self) -> Optional[str]:
        if self.last_selected_game_version == "ase":
            return self.ase_game_path
        if self.last_selected_game_version == "asa":
            return self.asa_game_path
        return None

    @game_path.setter
    def game_path(self, value: Optional[str]) -> None:
        if self.last_selected_game_version == "ase":
            self.ase_game_path = value
        elif self.last_selected_game_version == "asa":
            self.asa_game_path = value

    @property
    def inventory_keybind(self) -> str:
        """Returns the detected keybind, or 'i' as runtime fallback."""
        if self.last_selected_game_version == "asa":
            return self.asa_inventory_keybind or "i"
        return self.ase_inventory_keybind or "i"

    @inventory_keybind.setter
    def inventory_keybind(self, value: Optional[str]) -> None:
        """Set the keybind. None or empty = not detected."""
        clean = value or ""
        if self.last_selected_game_version == "asa":
            self.asa_inventory_keybind = clean
        else:
            self.ase_inventory_keybind = clean
        self._keybind_from_file = bool(clean)

    @property
    def first_click(self) -> Optional[Coordinates]:
        if self.last_selected_game_version == "asa":
            return self.first_click_asa
        return self.first_click_ase

    @first_click.setter
    def first_click(self, value: Optional[Coordinates]) -> None:
        if self.last_selected_game_version == "asa":
            self.first_click_asa = value
        else:
            self.first_click_ase = value

    @property
    def second_click(self) -> Optional[Coordinates]:
        if self.last_selected_game_version == "asa":
            return self.second_click_asa
        return self.second_click_ase

    @second_click.setter
    def second_click(self, value: Optional[Coordinates]) -> None:
        if self.last_selected_game_version == "asa":
            self.second_click_asa = value
        else:
            self.second_click_ase = value

    @property
    def saved_ui_scaling(self) -> Optional[float]:
        if self.last_selected_game_version == "asa":
            return self.asa_saved_ui_scaling
        return self.ase_saved_ui_scaling

    @saved_ui_scaling.setter
    def saved_ui_scaling(self, value: Optional[float]) -> None:
        if self.last_selected_game_version == "asa":
            self.asa_saved_ui_scaling = value
        else:
            self.ase_saved_ui_scaling = value

    # ── Persistence ──────────────────────────────────────────────────────────

    @classmethod
    def load(cls, path: Path = SETTINGS_FILE) -> Settings:
        """Read settings.txt into a Settings object."""
        settings = cls()
        if not path.exists():
            return settings

        raw = _read_key_value_file(path)

        settings.last_selected_game_version = raw.get("last_selected_game_version")
        settings.ase_game_path = raw.get("ase_game_path")
        settings.asa_game_path = raw.get("asa_game_path")
        settings.hotkey = raw.get("hotkey")
        settings.deactivation_hotkey = raw.get("deactivation_hotkey")

        for suffix in ("ase", "asa"):
            fc_key = f"{suffix}_first_click_coords"
            sc_key = f"{suffix}_second_click_coords"
            ui_key = f"{suffix}_saved_ui_scaling"
            if fc_key in raw:
                setattr(settings, f"first_click_{suffix}", Coordinates.from_string(raw[fc_key]))
            if sc_key in raw:
                setattr(settings, f"second_click_{suffix}", Coordinates.from_string(raw[sc_key]))
            if ui_key in raw:
                try:
                    setattr(settings, f"{suffix}_saved_ui_scaling", float(raw[ui_key]))
                except ValueError:
                    pass

        if "ask_version_on_start" in raw:
            settings.ask_version_on_start = raw["ask_version_on_start"].lower() == "true"

        return settings

    def save(self, path: Path = SETTINGS_FILE) -> None:
        """Write current state back to settings.txt."""
        pairs: dict[str, str] = {}

        if self.last_selected_game_version:
            pairs["last_selected_game_version"] = self.last_selected_game_version
        if self.hotkey:
            pairs["hotkey"] = self.hotkey
        if self.deactivation_hotkey:
            pairs["deactivation_hotkey"] = self.deactivation_hotkey
        if self.ask_version_on_start is not None:
            pairs["ask_version_on_start"] = str(self.ask_version_on_start)

        # Per-version fields
        if self.ase_game_path:
            pairs["ase_game_path"] = self.ase_game_path
        if self.asa_game_path:
            pairs["asa_game_path"] = self.asa_game_path

        for suffix in ("ase", "asa"):
            fc = getattr(self, f"first_click_{suffix}")
            sc = getattr(self, f"second_click_{suffix}")
            ui = getattr(self, f"{suffix}_saved_ui_scaling")
            if fc:
                pairs[f"{suffix}_first_click_coords"] = str(fc)
            if sc:
                pairs[f"{suffix}_second_click_coords"] = str(sc)
            if ui is not None:
                pairs[f"{suffix}_saved_ui_scaling"] = f"{ui:.6f}"

        lines = [f"{k}={v}\n" for k, v in pairs.items()]
        path.write_text("".join(lines), encoding="utf-8")

    # ── Validation ───────────────────────────────────────────────────────────

    @property
    def is_ready(self) -> bool:
        return all([
            self.game_version,
            self.hotkey,
            self.deactivation_hotkey,
            self.first_click,
            self.second_click,
        ])

    def needs_calibration(self, current_ui_scaling: float) -> bool:
        """True if coordinates were never calibrated or UIScaling changed."""
        if not self.first_click or not self.second_click:
            return True
        if self.saved_ui_scaling is None:
            return True
        return abs(self.saved_ui_scaling - current_ui_scaling) > 0.001

    def validate_coordinates(self) -> None:
        if not self.first_click or not self.second_click:
            raise SettingsError(
                'Coordinates not calibrated! Run QuickArmorSwap setup to calibrate.'
            )


def _read_file_text(path: Path) -> str:
    """Read a text file, auto-detecting common Windows encodings."""
    for enc in ("utf-8-sig", "utf-8", "utf-16", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except (UnicodeDecodeError, ValueError):
            continue
    return path.read_text(encoding="latin-1", errors="replace")


def _read_key_value_file(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in _read_file_text(path).splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", maxsplit=1)
        data[key.strip()] = value.strip()
    return data


# ═══════════════════════════════════════════════════════════════════════════════
#  Ark Input.ini — inventory keybind detection
# ═══════════════════════════════════════════════════════════════════════════════

# Maps Unreal Engine key names → keyboard-library key names.
# Only non-gamepad keys that make sense for a keyboard macro.
_ARK_KEY_MAP: dict[str, str] = {
    # Letters (UE uses single uppercase)
    **{chr(c): chr(c).lower() for c in range(ord("A"), ord("Z") + 1)},
    # Number row
    **{f"Zero": "0", "One": "1", "Two": "2", "Three": "3", "Four": "4",
       "Five": "5", "Six": "6", "Seven": "7", "Eight": "8", "Nine": "9"},
    # F-keys
    **{f"F{n}": f"f{n}" for n in range(1, 13)},
    # Numpad
    "NumPadZero": "num 0", "NumPadOne": "num 1", "NumPadTwo": "num 2",
    "NumPadThree": "num 3", "NumPadFour": "num 4", "NumPadFive": "num 5",
    "NumPadSix": "num 6", "NumPadSeven": "num 7", "NumPadEight": "num 8",
    "NumPadNine": "num 9",
    # Common named keys
    "Tab": "tab", "Enter": "enter", "SpaceBar": "space", "Escape": "esc",
    "BackSpace": "backspace", "Insert": "insert", "Delete": "delete",
    "Home": "home", "End": "end", "PageUp": "page up", "PageDown": "page down",
    "Left": "left", "Right": "right", "Up": "up", "Down": "down",
    "CapsLock": "caps lock", "Slash": "/", "BackSlash": "\\",
    "Comma": ",", "Period": ".", "Semicolon": ";", "Quote": "'",
    "LeftBracket": "[", "RightBracket": "]", "Hyphen": "-", "Equals": "=",
    "Tilde": "`",
    # Modifier keys
    "LeftShift": "left shift", "RightShift": "right shift",
    "LeftControl": "left ctrl", "RightControl": "right ctrl",
    "LeftAlt": "left alt", "RightAlt": "right alt",
    # Mouse (not usable as keyboard hotkeys — will be skipped)
    "LeftMouseButton": None, "RightMouseButton": None,
    "MiddleMouseButton": None, "MouseScrollUp": None, "MouseScrollDown": None,
    "ThumbMouseButton": None, "ThumbMouseButton2": None,
}

# Gamepad keys start with "Gamepad_" — always skip them.
_GAMEPAD_PREFIX = "Gamepad_"


def read_inventory_keybind(game_path: Path, game_version: str) -> Optional[str]:
    """
    Read the ShowMyInventory keybind from Ark's Input.ini.

    Returns a key name compatible with the ``keyboard`` library,
    or ``None`` if the file/entry is not found.
    """
    if game_version == "ase":
        ini_path = game_path / "ShooterGame" / "Saved" / "Config" / "WindowsNoEditor" / "Input.ini"
    else:
        ini_path = game_path / "ShooterGame" / "Saved" / "Config" / "Windows" / "Input.ini"

    if not ini_path.exists():
        return None

    try:
        content = _read_file_text(ini_path)
    except Exception:
        return None

    # Match Key=<KEY> anywhere within a ShowMyInventory mapping line.
    # ASE format: ...,ActionName="ShowMyInventory",Key=Tab,bShift=False,...
    # ASA format: ...,ActionName="ShowMyInventory",bShift=False,...,Key=I)
    pattern = re.compile(
        r'ActionMappings=\(ActionName="ShowMyInventory"[^)]*?,\s*Key=(\w+)',
    )

    for match in pattern.finditer(content):
        ark_key = match.group(1)

        # Skip gamepad bindings
        if ark_key.startswith(_GAMEPAD_PREFIX) or ark_key == "None":
            continue

        # Try our mapping table
        mapped = _ARK_KEY_MAP.get(ark_key)
        if mapped is not None:
            return mapped

        # If not in map but looks like a single letter, lowercase it
        if len(ark_key) == 1 and ark_key.isalpha():
            return ark_key.lower()

    return None


def validate_game_path(raw_path: str, game_version: str) -> Optional[Path]:
    """
    Check that the given path is a valid Ark game folder.
    Returns the resolved Path or None if invalid.
    """
    p = Path(raw_path.strip().strip('"').strip("'"))

    if not p.is_dir():
        return None

    expected_folder = "ARKSurvivalEvolved" if game_version == "ase" else "Ark Survival Ascended"

    # Accept both: user gives the exact folder, or a parent
    if p.name == expected_folder:
        return p
    candidate = p / expected_folder
    if candidate.is_dir():
        return candidate

    # Lenient: if ShooterGame subfolder exists, it's probably right
    if (p / "ShooterGame").is_dir():
        return p

    return None


def check_disable_menu_transitions(game_path: Path, game_version: str) -> None:
    """
    Verify that 'bDisableMenuTransitions' is set to True in GameUserSettings.ini.

    The macro relies on instant menu transitions — without this setting
    the click timings will miss their targets.
    """
    if game_version == "ase":
        ini_path = game_path / "ShooterGame" / "Saved" / "Config" / "WindowsNoEditor" / "GameUserSettings.ini"
    else:
        ini_path = game_path / "ShooterGame" / "Saved" / "Config" / "Windows" / "GameUserSettings.ini"

    if not ini_path.exists():
        raise SettingsError(
            f"GameUserSettings.ini not found at:\n"
            f"  {ini_path}\n\n"
            f"Make sure Ark has been launched at least once so the config files are created."
        )

    try:
        content = _read_file_text(ini_path)
    except Exception as exc:
        raise SettingsError(f"Could not read GameUserSettings.ini: {exc}") from exc

    # Look for the key anywhere in the file (under [/Script/ShooterGame.ShooterGameUserSettings])
    match = re.search(r'bDisableMenuTransitions\s*=\s*(\w+)', content)

    if not match or match.group(1).lower() != "true":
        raise SettingsError(
            "Required Ark setting not enabled!\n\n"
            '  "Disable Menu Transitions" must be checked (set to True).\n\n'
            "  How to fix:\n"
            "    1. Open the game\n"
            '    2. ASE: Go to Options → Advanced / ASA: Go to Settings → General → UI\n'
            '    3. Enable "Disable Menu Transitions"\n'
            "    4. Save and restart QuickArmorSwap\n\n"
            "  This setting is required so the inventory opens instantly,\n"
            "  allowing the macro to click at the correct positions."
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  Ark display settings & coordinate calculation
# ═══════════════════════════════════════════════════════════════════════════════

def read_game_display_settings(game_path: Path, game_version: str) -> tuple[float, bool, int, int, bool]:
    """
    Read UIScaling and resolution from GameUserSettings.ini.

    Returns ``(ui_scaling, ui_from_file, res_x, res_y, res_from_file)``.
    Falls back to ``1.0`` for UIScaling and screen dimensions for resolution.
    """
    screen = pyautogui.size()
    default_res_x, default_res_y = screen.width, screen.height

    if game_version == "ase":
        ini_path = game_path / "ShooterGame" / "Saved" / "Config" / "WindowsNoEditor" / "GameUserSettings.ini"
    else:
        ini_path = game_path / "ShooterGame" / "Saved" / "Config" / "Windows" / "GameUserSettings.ini"

    if not ini_path.exists():
        return 1.0, False, default_res_x, default_res_y, False

    try:
        content = _read_file_text(ini_path)
    except Exception:
        return 1.0, False, default_res_x, default_res_y, False

    ui_match = re.search(r'UIScaling\s*=\s*([\d.]+)', content)
    ui_scaling = float(ui_match.group(1)) if ui_match else 1.0

    rx_match = re.search(r'ResolutionSizeX\s*=\s*(\d+)', content)
    ry_match = re.search(r'ResolutionSizeY\s*=\s*(\d+)', content)
    res_from_file = bool(rx_match and ry_match)
    res_x = int(rx_match.group(1)) if rx_match else default_res_x
    res_y = int(ry_match.group(1)) if ry_match else default_res_y

    return ui_scaling, bool(ui_match), res_x, res_y, res_from_file


# Reference resolution for the linear model
_REF_W, _REF_H = 3840, 2160

# Linear model coefficients derived from two reference points at 3840×2160:
#   UIScaling=1.000000 → first=(320,580)  second=(330,670)
#   UIScaling=0.710935 → first=(780,700)  second=(790,795)
_FIRST_X  = (-1591.15, 1911.15)   # (slope, intercept)
_FIRST_Y  = ( -415.06,  995.06)
_SECOND_X = (-1591.15, 1921.15)
_SECOND_Y = ( -432.56, 1102.56)


def calculate_coordinates(
    ui_scaling: float, res_x: int, res_y: int,
) -> tuple[Coordinates, Coordinates]:
    """
    Estimate click positions for the given UIScaling and resolution.
    Uses a linear model calibrated at 3840×2160, then scales to the
    actual resolution.
    """
    def _calc(coeff: tuple[float, float], scale: float) -> int:
        slope, intercept = coeff
        ref_value = slope * ui_scaling + intercept
        return max(0, round(ref_value * scale))

    sx = res_x / _REF_W
    sy = res_y / _REF_H

    first  = Coordinates(x=_calc(_FIRST_X, sx),  y=_calc(_FIRST_Y, sy))
    second = Coordinates(x=_calc(_SECOND_X, sx), y=_calc(_SECOND_Y, sy))

    return first, second


# ═══════════════════════════════════════════════════════════════════════════════
#  Interactive Coordinate Calibration
# ═══════════════════════════════════════════════════════════════════════════════

_CROSSHAIR_SIZE = 18
_LABEL_OFFSET   = 26

# Colors
_C_ACTIVE_1   = "#00ff88"   # green — active first marker
_C_INACTIVE_1 = "#005533"   # dim green
_C_ACTIVE_2   = "#ff8800"   # orange — active second marker
_C_INACTIVE_2 = "#553300"   # dim orange
_C_INSTR_BG   = "#111111"   # near-black (opaque on transparent-black window)
_C_INSTR_FG   = "#ffffff"


def run_calibration(
    initial_first: Coordinates,
    initial_second: Coordinates,
) -> Optional[tuple[Coordinates, Coordinates]]:
    """
    Full-screen transparent overlay with two crosshair markers.
    Uses ``keyboard.on_press_key()`` per key for reliable global input
    even when a fullscreen game has focus.
    Tkinter only handles drawing — it never needs keyboard focus.

    Returns the confirmed (first, second) coordinates, or None if cancelled.
    """

    sw, sh = pyautogui.size()

    state: dict = {
        "fx": initial_first.x,
        "fy": initial_first.y,
        "sx": initial_second.x,
        "sy": initial_second.y,
        "phase": 1,
        "result": None,
        "dirty": True,
    }

    done_event = threading.Event()
    hooks: list = []  # track all registered hooks for cleanup

    # ── Movement helpers ─────────────────────────────────────────────────

    def _move(axis: str, delta: int) -> None:
        if done_event.is_set():
            return
        prefix = "f" if state["phase"] == 1 else "s"
        key = f"{prefix}{axis}"
        step = 10 if keyboard.is_pressed("shift") else 1
        limit = (sw - 1) if axis == "x" else (sh - 1)
        state[key] = max(0, min(limit, state[key] + delta * step))
        state["dirty"] = True

    def _confirm(_event=None) -> None:
        if done_event.is_set():
            return
        if state["phase"] == 1:
            state["phase"] = 2
            state["dirty"] = True
        else:
            state["result"] = (
                Coordinates(state["fx"], state["fy"]),
                Coordinates(state["sx"], state["sy"]),
            )
            done_event.set()

    def _cancel(_event=None) -> None:
        if done_event.is_set():
            return
        state["result"] = None
        done_event.set()

    # ── Register one hook per key ────────────────────────────────────────

    hooks.append(keyboard.on_press_key("up",    lambda e: _move("y", -1)))
    hooks.append(keyboard.on_press_key("down",  lambda e: _move("y",  1)))
    hooks.append(keyboard.on_press_key("left",  lambda e: _move("x", -1)))
    hooks.append(keyboard.on_press_key("right", lambda e: _move("x",  1)))
    hooks.append(keyboard.on_press_key("enter", _confirm))
    hooks.append(keyboard.on_press_key("esc",   _cancel))

    # ── Tk overlay thread (drawing only) ─────────────────────────────────

    root_ref: list = []

    def _overlay_thread() -> None:
        root = tk.Tk()
        root_ref.append(root)
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.attributes("-transparentcolor", "black")
        root.geometry(f"{sw}x{sh}+0+0")

        canvas = tk.Canvas(root, width=sw, height=sh, bg="black", highlightthickness=0)
        canvas.pack()

        def _draw_crosshair(cx: int, cy: int, color: str, label: str) -> None:
            s = _CROSSHAIR_SIZE
            canvas.create_oval(cx - s, cy - s, cx + s, cy + s,
                               outline=color, width=2, tags="markers")
            canvas.create_line(cx - s - 6, cy, cx + s + 6, cy,
                               fill=color, width=1, tags="markers")
            canvas.create_line(cx, cy - s - 6, cx, cy + s + 6,
                               fill=color, width=1, tags="markers")
            canvas.create_text(cx + _LABEL_OFFSET, cy - _LABEL_OFFSET,
                               text=label, fill=color,
                               font=("Segoe UI", 11, "bold"), anchor="w", tags="markers")
            canvas.create_text(cx + _LABEL_OFFSET, cy - _LABEL_OFFSET + 18,
                               text=f"({cx}, {cy})", fill=color,
                               font=("Segoe UI", 9), anchor="w", tags="markers")

        def _draw_instructions() -> None:
            bar_h = 52
            canvas.create_rectangle(0, 0, sw, bar_h,
                                    fill=_C_INSTR_BG, outline="", tags="markers")
            if state["phase"] == 1:
                txt = ("  QuickArmorSwap CALIBRATION  │  Step 1/2: Move the GREEN marker to the middle of the "
                       "inventory folder  │  Arrow keys = 1 px  │  Shift+Arrow = 10 px  │  Enter = confirm  │  Esc = cancel")
            else:
                txt = ("  QuickArmorSwap CALIBRATION  │  Step 2/2: Move the ORANGE marker to the "
                       "context menu entry 'Equip all items'  │  Arrow keys = 1 px  │  Shift+Arrow = 10 px  │  Enter = confirm  │  Esc = cancel")
            canvas.create_text(16, bar_h // 2, text=txt,
                               fill=_C_INSTR_FG, font=("Segoe UI", 11),
                               anchor="w", tags="markers")

        def redraw() -> None:
            canvas.delete("markers")
            _draw_instructions()
            c1 = _C_ACTIVE_1 if state["phase"] == 1 else _C_INACTIVE_1
            _draw_crosshair(state["fx"], state["fy"], c1, "1st click (inventory folder)")
            c2 = _C_ACTIVE_2 if state["phase"] == 2 else _C_INACTIVE_2
            _draw_crosshair(state["sx"], state["sy"], c2, "2nd click (context menu entry)")

        def _poll() -> None:
            if done_event.is_set():
                root.destroy()
                return
            if state["dirty"]:
                state["dirty"] = False
                redraw()
            root.after(30, _poll)

        redraw()
        root.after(30, _poll)
        root.mainloop()

        # ── Tear down Tcl state on THIS thread ──────────────────────────
        # Without this, Python's GC would free the Tcl interpreter from
        # the main thread later → "Tcl_AsyncDelete: wrong thread".
        try:
            root.tk.call("destroy", ".")
        except Exception:
            pass
        root_ref.clear()  # drop the reference so GC has nothing to finalize

    overlay_thread = threading.Thread(target=_overlay_thread, daemon=True)
    overlay_thread.start()

    # ── Block until user confirms or cancels ─────────────────────────────

    try:
        done_event.wait()
    finally:
        for h in hooks:
            keyboard.unhook(h)
        done_event.set()  # ensure overlay closes if it hasn't

    overlay_thread.join(timeout=3)
    return state["result"]


# ═══════════════════════════════════════════════════════════════════════════════
#  Platform helpers
# ═══════════════════════════════════════════════════════════════════════════════

def get_os_label() -> str:
    system = platform.system()
    if system == "Windows":
        ver = platform.win32_ver()[0]
        return f"Windows {ver}" if ver else "Windows"
    if system == "Linux":
        return "Linux"
    raise PlatformError("Unsupported OS — currently Windows and Linux only.")


# ═══════════════════════════════════════════════════════════════════════════════
#  In-Game Overlay  (transparent floating text via Tkinter)
# ═══════════════════════════════════════════════════════════════════════════════

class Overlay:
    """
    HUD-style text overlay rendered on a single persistent Tk thread.

    One Tk root + one window is reused for every message. New calls to
    ``show()`` replace the current text instantly (no stacking). A
    dedicated thread owns the Tk mainloop so it can be shut down
    cleanly — no more "Tcl_AsyncDelete: wrong thread" errors.
    """

    # ── Color presets ────────────────────────────────────────────────────────
    COLOR_NORMAL  = "#00e5ff"   # cyan / teal
    COLOR_WARNING = "#ffab00"   # amber
    COLOR_DANGER  = "#ff1744"   # red
    COLOR_SUCCESS = "#00e676"   # green

    FONT_FAMILY    = "Segoe UI Black"
    FONT_FALLBACKS = ("Segoe UI", "Arial Black", "Helvetica", "OCR A Extended")
    FONT_SIZE      = 28
    DISPLAY_MS     = 2200
    FADE_STEPS     = 12

    # ── Internal state (class-level, shared across all callers) ──────────
    _queue: queue.Queue       = queue.Queue()
    _root: Optional[tk.Tk]    = None
    _main_label: Optional[tk.Label] = None
    _sub_label: Optional[tk.Label]  = None
    _thread: Optional[threading.Thread] = None
    _ready   = threading.Event()
    _stopped = threading.Event()   # signals when Tk is fully torn down
    _fade_id: Optional[str]   = None

    # ── Public API ───────────────────────────────────────────────────────────

    @classmethod
    def show(cls, text: str, *, color: str = COLOR_NORMAL, subtext: str = "") -> None:
        """Fire-and-forget: display *text* for ~2 s, replacing any current overlay."""
        cls._ensure_thread()
        cls._queue.put(("show", text, color, subtext))

    @classmethod
    def shutdown(cls) -> None:
        """Cleanly destroy the Tk root from its owning thread and wait."""
        if cls._thread is not None and cls._thread.is_alive():
            cls._queue.put(("quit",))
            cls._stopped.wait(timeout=5)   # wait for Tcl to be fully gone
            cls._thread.join(timeout=2)
            cls._thread = None
        # Drain any leftover messages
        while not cls._queue.empty():
            try:
                cls._queue.get_nowait()
            except queue.Empty:
                break

    # ── Thread lifecycle ─────────────────────────────────────────────────────

    @classmethod
    def _ensure_thread(cls) -> None:
        if cls._thread is not None and cls._thread.is_alive():
            return
        cls._ready.clear()
        cls._stopped.clear()
        cls._thread = threading.Thread(target=cls._mainloop, daemon=True)
        cls._thread.start()
        cls._ready.wait(timeout=5)

    @classmethod
    def _pick_font(cls, root: tk.Tk) -> str:
        available = set(tkfont.families(root))
        for candidate in (cls.FONT_FAMILY, *cls.FONT_FALLBACKS):
            if candidate in available:
                return candidate
        return "TkDefaultFont"

    @classmethod
    def _mainloop(cls) -> None:
        """Runs on the dedicated overlay thread — owns all Tk objects."""
        root = None
        try:
            root = tk.Tk()
            cls._root = root
            root.overrideredirect(True)
            root.configure(bg="black")
            root.attributes("-topmost", True)
            root.attributes("-transparentcolor", "black")
            try:
                root.attributes("-disabled", True)
            except tk.TclError:
                pass

            chosen_font = cls._pick_font(root)

            cls._main_label = tk.Label(
                root,
                text="",
                font=(chosen_font, cls.FONT_SIZE, "bold"),
                fg=cls.COLOR_NORMAL,
                bg="black",
                padx=24,
                pady=4,
            )
            cls._main_label.pack()

            cls._sub_label = tk.Label(
                root,
                text="",
                font=(chosen_font, cls.FONT_SIZE // 2),
                fg="#888888",
                bg="black",
                padx=24,
            )
            cls._sub_label.pack()

            # Start hidden
            root.withdraw()

            cls._ready.set()

            # Poll the queue every 50 ms from inside the Tk event loop
            cls._poll()
            root.mainloop()

        except Exception:
            pass
        finally:
            # ── CRITICAL: release all Tcl state on THIS thread ───────────
            cls._root = None
            cls._main_label = None
            cls._sub_label = None
            cls._fade_id = None
            if root is not None:
                try:
                    root.destroy()
                except Exception:
                    pass
                # Explicitly break Python's reference to the Tcl interpreter
                # so it won't be GC'd later from the main thread.
                try:
                    root.tk.call("destroy", ".")
                except Exception:
                    pass
                del root
            cls._stopped.set()

    # ── Queue polling (runs inside Tk thread) ────────────────────────────────

    @classmethod
    def _poll(cls) -> None:
        try:
            while not cls._queue.empty():
                msg = cls._queue.get_nowait()

                if msg[0] == "quit":
                    cls._cancel_fade()
                    cls._root.destroy()
                    return

                if msg[0] == "show":
                    _, text, color, subtext = msg
                    cls._display(text, color, subtext)

            cls._root.after(50, cls._poll)
        except Exception:
            pass

    # ── Display logic (always called from the Tk thread) ─────────────────────

    @classmethod
    def _display(cls, text: str, color: str, subtext: str) -> None:
        root = cls._root

        # Cancel any running fade so the new message starts fully opaque
        cls._cancel_fade()
        root.attributes("-alpha", 1.0)

        # Update labels
        cls._main_label.configure(text=text, fg=color)
        cls._sub_label.configure(text=subtext)

        # Reposition — center horizontally at top of screen
        root.update_idletasks()
        w = root.winfo_reqwidth()
        sw = pyautogui.size().width
        root.geometry(f"+{(sw - w) // 2}+38")

        root.deiconify()
        root.lift()

        # Schedule fade-out
        hold_ms = cls.DISPLAY_MS - (cls.FADE_STEPS * 40)
        cls._fade_id = root.after(max(hold_ms, 400), cls._fade, 0)

    @classmethod
    def _fade(cls, step: int) -> None:
        if step >= cls.FADE_STEPS:
            cls._root.withdraw()
            cls._fade_id = None
            return
        alpha = 1.0 - (step / cls.FADE_STEPS)
        try:
            cls._root.attributes("-alpha", alpha)
        except tk.TclError:
            return
        cls._fade_id = cls._root.after(40, cls._fade, step + 1)

    @classmethod
    def _cancel_fade(cls) -> None:
        if cls._fade_id is not None:
            try:
                cls._root.after_cancel(cls._fade_id)
            except (tk.TclError, ValueError):
                pass
            cls._fade_id = None


# ═══════════════════════════════════════════════════════════════════════════════
#  Terminal UI  (rich-powered pretty printing)
# ═══════════════════════════════════════════════════════════════════════════════

def show_banner() -> None:
    get_os_label()

    if HAS_RICH:
        title = Text("QuickArmorSwap", style="bold bright_cyan")

        version = Text(f" {APP_VERSION}", style="dim")

        credit = Text("© 2024-2026 by ", style="dim")
        credit.append("AEYCEN", style="bold cyan")
        credit.append(" / ", style="dim")
        credit.append("2_L_8", style="bold yellow")

        body = Text.assemble(title, "\n", version, "\n", credit, justify="center")
        panel = Panel(
            body,
            box=box.DOUBLE_EDGE,
            border_style="bright_magenta",
            padding=(1, 4),
        )
        console.print()
        console.print(panel, justify="center")
    else:
        print()
        print(f"  ╔══════════════════════════════════════════╗")
        print(f"  ║              QuickArmorSwap              ║")
        print(f"  ║             {APP_VERSION:<16}            ║")
        print(f"  ║       © 2024-2026 by AEYCEN / 2_L_8      ║")
        print(f"  ╚══════════════════════════════════════════╝")
        print()


_GAME_NAMES = {
    "ase": "Ark: Survival Evolved",
    "asa": "Ark: Survival Ascended",
}


def show_status_table(settings: Settings, set_count: int) -> None:
    """Display a compact overview of all active keybinds and settings."""
    ui_str = f"{settings.saved_ui_scaling:.4f}" if settings.saved_ui_scaling else "1.0000"
    ui_source = "synced" if settings._ui_scaling_from_file else "default"
    kb_source = "synced" if settings._keybind_from_file else "default"
    res_str = f"{settings._res_x} × {settings._res_y} px"
    res_source = "synced" if settings._resolution_from_file else "screen max"
    game_name = _GAME_NAMES.get(settings.game_version, "—")

    if not HAS_RICH:
        print(f"  Game:                     {game_name}")
        print(f"  Game path:                {settings.game_path}")
        print(f"  Resolution:               {res_str} ({res_source})")
        print(f"  UI Scaling:               {ui_str} ({ui_source})")
        print(f"  Open inventory keybind:   {settings.inventory_keybind} ({kb_source})")
        print(f"  Adjust armor set count:   Alt+1 (-)  /  Alt+2 (+)")
        return

    table = Table(
        box=box.SIMPLE_HEAVY,
        show_header=False,
        border_style="bright_black",
        padding=(0, 2),
    )
    table.add_column("Key", style="dim", min_width=20)
    table.add_column("Value", style="bold")

    # Truncate long path for display
    display_path = settings.game_path or "—"
    if len(display_path) > 100:
        display_path = "…" + display_path[-99:]

    table.add_row("Game", f"[bright_cyan]{game_name}[/]")
    table.add_row("Game path", f"[dim]{display_path}[/]")
    table.add_row("Resolution", f"[dim]{res_str}[/]  [dim italic]({res_source})[/]")
    table.add_row("UI Scaling", f"[dim]{ui_str}[/]  [dim italic]({ui_source})[/]")
    table.add_row("Open inventory keybind", f"[dim]{settings.inventory_keybind}[/]  [dim italic]({kb_source})[/]")
    table.add_row("Adjust armor set count", "[dim]Alt+1[/] (−)  /  [dim]Alt+2[/] (+)")

    console.print()
    console.print(table)


def show_running(hotkey: str) -> None:
    if HAS_RICH:
        msg = Text()
        msg.append(" ● ", style="bold bright_green")
        msg.append("RUNNING", style="bold bright_green")
        msg.append("  —  press ", style="dim")
        msg.append(hotkey, style="bold bright_magenta")
        msg.append(" to swap armor", style="dim")
        console.print(msg)
    else:
        print(f"  ● RUNNING — press '{hotkey}' to swap armor")


def show_exit_hint(deactivation_hotkey: str) -> None:
    if HAS_RICH:
        msg = Text()
        msg.append("  Press ", style="dim")
        msg.append(deactivation_hotkey, style="bold red")
        msg.append(" to stop QuickArmorSwap.\n", style="dim")
        console.print(msg)
    else:
        print(f"  Press '{deactivation_hotkey}' to stop QuickArmorSwap.\n")


def prompt_choice(label: str, choices: list[str], default: Optional[str] = None) -> str:
    """Let the user pick from a list. Returns the chosen value."""
    fallback = default if default in choices else choices[0]
    if HAS_RICH:
        return Prompt.ask(f"  {label}", choices=choices, default=fallback)
    while True:
        hint = "/".join(c.upper() if c == fallback else c for c in choices)
        raw = input(f"  {label} [{hint}]: ").strip().lower()
        if raw == "":
            return fallback
        if raw in choices:
            return raw
        print(f"  Invalid — choose one of: {', '.join(choices)}")


def prompt_text(label: str, default: str = "") -> str:
    if HAS_RICH:
        return Prompt.ask(f"  {label}", default=default or None) or default
    raw = input(f"  {label}: ").strip()
    return raw or default


def prompt_int(label: str, *, minimum: int = 1) -> int:
    if HAS_RICH:
        while True:
            val = IntPrompt.ask(f"  {label}")
            if val >= minimum:
                return val
            console.print(f"  [red]Please enter a number ≥ {minimum}.[/]")
    while True:
        raw = input(f"  {label}: ").strip()
        if raw.isdigit() and int(raw) >= minimum:
            return int(raw)
        print(f"  Invalid — enter a whole number ≥ {minimum}.")


def prompt_yes_no(label: str, default: bool = True) -> bool:
    """Ask a yes/no question. Returns True for yes, False for no."""
    hint = "Y/n" if default else "y/N"
    if HAS_RICH:
        raw = Prompt.ask(f"  {label}", choices=["y", "n"], default="y" if default else "n")
        return raw.lower() == "y"
    while True:
        raw = input(f"  {label} [{hint}]: ").strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Invalid — enter y or n.")


# ═══════════════════════════════════════════════════════════════════════════════
#  Macro Logic
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MacroState:
    """Mutable runtime state shared across hotkey callbacks."""

    settings: Settings
    set_count: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    # ── Hotkey callbacks ─────────────────────────────────────────────────────

    def perform_swap(self) -> None:
        with self._lock:
            if self.set_count <= 0:
                Overlay.show("NO SETS LEFT", color=Overlay.COLOR_DANGER)
                return

            self.set_count -= 1
            remaining = self.set_count

        s = self.settings

        pyautogui.hotkey(s.inventory_keybind)
        time.sleep(0.2)
        pyautogui.click(x=s.first_click.x, y=s.first_click.y, button="right")
        pyautogui.click(x=s.second_click.x, y=s.second_click.y)
        pyautogui.hotkey("esc")

        self._show_count(remaining)

    def decrement_count(self) -> None:
        with self._lock:
            if self.set_count > 0:
                self.set_count -= 1
            count = self.set_count
        self._show_count(count)

    def increment_count(self) -> None:
        with self._lock:
            self.set_count += 1
            count = self.set_count
        self._show_count(count)

    @staticmethod
    def _show_count(count: int) -> None:
        if count == 0:
            Overlay.show("0 sets left", color=Overlay.COLOR_DANGER, subtext="Restock!")
        elif count <= 2:
            Overlay.show(f"{count} set{'s' if count != 1 else ''} left", color=Overlay.COLOR_WARNING)
        else:
            Overlay.show(f"{count} sets left", color=Overlay.COLOR_NORMAL)


# ═══════════════════════════════════════════════════════════════════════════════
#  Setup Wizard  (first-run interactive configuration)
# ═══════════════════════════════════════════════════════════════════════════════

def run_setup(settings: Settings) -> Settings:
    """Walk the user through missing settings. Returns the updated object."""
    is_first_run = settings.last_selected_game_version is None

    # ── Game version selection ───────────────────────────────────────────────

    if is_first_run:
        if HAS_RICH:
            console.print()
            console.print(
                Panel(
                    "[bold]First-time setup[/]\nAnswer a few questions to get started",
                    border_style="bright_cyan",
                    box=box.ROUNDED,
                    padding=(1, 3),
                ),
                justify="center",
            )
        else:
            print("\n  ── First-time setup ──\n")

        version = prompt_choice("Ark version", choices=["ase", "asa"])
        settings.game_version = version

        ask_every_time = prompt_yes_no("Ask for game version on every start?", default=True)
        settings.ask_version_on_start = ask_every_time

    elif settings.ask_version_on_start:
        previous = settings.last_selected_game_version or "asa"
        version = prompt_choice("Ark version", choices=["ase", "asa"], default=previous)
        settings.game_version = version

    # ── Remaining setup (game path, hotkeys, calibration) ────────────────────
    needs_setup = (
        not settings.game_path
        or not settings.hotkey
        or not settings.deactivation_hotkey
    )

    if needs_setup and not is_first_run:
        if HAS_RICH:
            console.print()
            console.print(
                Panel(
                    "[bold]Setup[/]\nSome settings are missing — let's fill them in.",
                    border_style="bright_cyan",
                    box=box.ROUNDED,
                    padding=(1, 3),
                ),
                justify="center",
            )
        else:
            print("\n  ── Setup ──\n")

    # Game path
    if not settings.game_path:
        if settings.game_version == "ase":
            folder_name = "ARKSurvivalEvolved"
        else:
            folder_name = "Ark Survival Ascended"

        if HAS_RICH:
            console.print(f'  Enter the full path to your [bold]"{folder_name}"[/] game folder.')
            console.print(f'  [dim]Example: C:\\Program Files (x86)\\Steam\\steamapps\\common\\{folder_name}[/]')
        else:
            print(f'  Enter the full path to your "{folder_name}" game folder.')
            print(f'  Example: C:\\Program Files (x86)\\Steam\\steamapps\\common\\{folder_name}')

        while True:
            raw = prompt_text("Game folder path")
            validated = validate_game_path(raw, settings.game_version)
            if validated is not None:
                settings.game_path = str(validated)
                break
            if HAS_RICH:
                console.print(f'  [red]Folder not found or invalid.[/] Make sure the path ends with "{folder_name}" and the folder exists.')
            else:
                print(f'  Folder not found or invalid. Make sure the path ends with "{folder_name}" and the folder exists.')

        # Auto-detect inventory keybind from Input.ini
        detected_key = read_inventory_keybind(Path(settings.game_path), settings.game_version)
        settings.inventory_keybind = detected_key  # None → empty → property returns "i"

        display_key = detected_key or "i"
        if HAS_RICH:
            if detected_key:
                console.print(f'  [dim]Inventory keybind:[/] [bright_cyan]{display_key}[/] [green]✓ from Input.ini[/]')
            else:
                console.print(f'  [dim]Inventory keybind:[/] [bright_cyan]{display_key}[/] [dim](default — not found in Input.ini)[/]')
        else:
            if detected_key:
                print(f'  Inventory keybind: {display_key} (from Input.ini)')
            else:
                print(f'  Inventory keybind: {display_key} (default — not found in Input.ini)')

    # Path already set — still always re-read keybind from game files
    elif settings.game_path:
        detected_key = read_inventory_keybind(Path(settings.game_path), settings.game_version)
        settings.inventory_keybind = detected_key

    # Verify "Disable Menu Transitions" is enabled in Ark settings
    if settings.game_path:
        check_disable_menu_transitions(Path(settings.game_path), settings.game_version)

    # Hotkey
    if not settings.hotkey:
        settings.hotkey = prompt_text("Macro hotkey (e.g. '+' or 'alt+l')", default="+")

    # Deactivation hotkey
    if not settings.deactivation_hotkey:
        settings.deactivation_hotkey = prompt_text("Stop hotkey (e.g. '#' or 'esc')", default="#")

    # ── Persist settings collected so far ────────────────────────────────────
    # Save now so that game_path, last_selected_game_version, and hotkeys
    # are kept even if the calibration step below is cancelled.
    settings.save()

    # ── Coordinate calibration ───────────────────────────────────────────────
    if settings.game_path:
        ui_scaling, ui_from_file, res_x, res_y, res_from_file = read_game_display_settings(
            Path(settings.game_path), settings.game_version,
        )
        settings._ui_scaling_from_file = ui_from_file
        settings._res_x = res_x
        settings._res_y = res_y
        settings._resolution_from_file = res_from_file

        if settings.needs_calibration(ui_scaling):
            # Explain why
            if settings.saved_ui_scaling is not None and settings.first_click:
                reason = (
                    f"UIScaling changed ({settings.saved_ui_scaling:.4f} → {ui_scaling:.4f}). "
                    "Click positions need to be re-calibrated."
                )
            else:
                reason = "Click positions have not been calibrated yet."

            if HAS_RICH:
                console.print()
                console.print(
                    Panel(
                        f"[yellow bold]⚠  Calibration needed[/]\n\n"
                        f"  {reason}\n\n"
                        f"  Detected:  [dim]Resolution[/] [bold]{res_x}×{res_y}[/]  "
                        f"│  [dim]UIScaling[/] [bold]{ui_scaling:.4f}[/]\n\n"
                        f"  An overlay with two crosshair markers will appear.\n"
                        f"  Open Ark with your [bold]inventory visible[/], then position each marker:\n\n"
                        f"    [bright_green]GREEN[/]  marker → Inventory folder (right-click target)\n"
                        f"    [yellow]ORANGE[/] marker → Context menu entry 'equip all items'\n\n"
                        f"  Controls:\n"
                        f"    [dim]Arrow keys[/]         move 1 px\n"
                        f"    [dim]Shift + Arrow keys[/] move 10 px\n"
                        f"    [dim]Enter[/]              confirm position\n"
                        f"    [dim]Esc[/]                cancel",
                        border_style="yellow",
                        box=box.ROUNDED,
                        padding=(1, 3),
                    ),
                )
                console.print()
                console.print("  [dim]Press[/] [bold]Enter[/] [dim]to start calibration (works in-game too)…[/]")
            else:
                print(f"\n  ⚠  Calibration needed: {reason}")
                print(f"     Resolution: {res_x}×{res_y}  |  UIScaling: {ui_scaling:.4f}")
                print("     Open Ark with inventory visible, then position the markers.")
                print("     Arrow keys = 1px, Shift+Arrows = 10px, Enter = confirm, Esc = cancel")
                print("\n  Press Enter to start calibration (works in-game too)…")

            keyboard.wait("enter")  # global hook — works even when game has focus
            time.sleep(0.15)        # small delay so the Enter release doesn't bleed

            # Calculate starting positions from the linear model
            est_first, est_second = calculate_coordinates(ui_scaling, res_x, res_y)

            if HAS_RICH:
                console.print(
                    f"  [dim]Estimated positions:[/]  "
                    f"1st [bright_green]({est_first.x}, {est_first.y})[/]  "
                    f"2nd [yellow]({est_second.x}, {est_second.y})[/]"
                )

            result = run_calibration(est_first, est_second)

            if result is None:
                raise QuickArmorSwapError("Calibration cancelled. Run the program again to retry.")

            settings.first_click, settings.second_click = result
            settings.saved_ui_scaling = ui_scaling

            if HAS_RICH:
                console.print(
                    f"\n  [green]✓ Calibrated![/]  "
                    f"1st [bright_green]({settings.first_click.x}, {settings.first_click.y})[/]  "
                    f"2nd [yellow]({settings.second_click.x}, {settings.second_click.y})[/]"
                )
            else:
                print(f"  ✓ Calibrated!  1st ({settings.first_click})  2nd ({settings.second_click})")

    settings.save()
    return settings


# ═══════════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    # ── Banner ───────────────────────────────────────────────────────────────
    show_banner()

    # ── Load / create settings ───────────────────────────────────────────────
    if not SETTINGS_FILE.exists():
        SETTINGS_FILE.touch()

    settings = Settings.load()

    # Interactive setup for anything missing
    settings = run_setup(settings)

    # Validate coordinates
    settings.validate_coordinates()

    # ── Armor set count ──────────────────────────────────────────────────────
    set_count = prompt_int("How many armor sets do you have?", minimum=1)

    # ── Build state & register hotkeys ───────────────────────────────────────
    state = MacroState(settings=settings, set_count=set_count)

    try:
        keyboard.add_hotkey(settings.hotkey, state.perform_swap)
        keyboard.add_hotkey("alt+1", state.decrement_count)
        keyboard.add_hotkey("alt+2", state.increment_count)
    except Exception as exc:
        raise QuickArmorSwapError(f"Failed to register hotkeys: {exc}") from exc

    # ── Running ──────────────────────────────────────────────────────────────
    show_status_table(settings, set_count)
    show_running(settings.hotkey)
    show_exit_hint(settings.deactivation_hotkey)

    # Block until deactivation hotkey
    keyboard.wait(settings.deactivation_hotkey)

    Overlay.shutdown()

    if HAS_RICH:
        console.print("  [dim]QuickArmorSwap stopped. GG![/]\n")
    else:
        print("  QuickArmorSwap stopped. GG!\n")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _exit_code = 0
    try:
        main()
    except (QuickArmorSwapError, SettingsError, PlatformError) as exc:
        Overlay.shutdown()
        if HAS_RICH:
            console.print(f"\n  [bold red]Error:[/] {exc}\n")
        else:
            print(f"\n  Error: {exc}\n")
        _exit_code = 1
    except KeyboardInterrupt:
        Overlay.shutdown()
        if HAS_RICH:
            console.print("\n  [dim]Interrupted. Bye![/]\n")
        else:
            print("\n  Interrupted. Bye!\n")

    os._exit(_exit_code)
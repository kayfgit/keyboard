"""Configuration: VK codes, constants, and API key loading."""

import os

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_groq_api_key():
    return os.environ.get("GROQ_API_KEY", "")


# Windows Virtual Key codes for chord keys
# Left hand: A(pinky) S(ring) D(mid) F(index) C(thumb)
# Right hand: M(thumb) J(index) K(mid) L(ring) ;(pinky)
VK_A = 0x41
VK_S = 0x53
VK_D = 0x44
VK_F = 0x46
VK_C = 0x43
VK_M = 0x4D
VK_J = 0x4A
VK_K = 0x4B
VK_L = 0x4C
VK_OEM_1 = 0xBA  # semicolon on US layout
VK_SPACE = 0x20

# Toggle hotkey: Alt+Q
VK_Q_TOGGLE = 0x51

# LLKHF_INJECTED flag — set on keystrokes we inject ourselves
LLKHF_INJECTED = 0x10

# Map VK codes to internal key names
VK_TO_KEY = {
    VK_A: 'a',
    VK_S: 's',
    VK_D: 'd',
    VK_F: 'f',
    VK_C: 'c',
    VK_M: 'm',
    VK_J: 'j',
    VK_K: 'k',
    VK_L: 'l',
    VK_OEM_1: ';',
}

# Set of all chord VK codes for quick lookup
CHORD_VK_CODES = set(VK_TO_KEY.keys())

# Modifier VK codes — always pass through (both generic and side-specific)
MODIFIER_VKS = {
    0x10, 0x11, 0x12,          # Shift, Ctrl, Alt (generic)
    0xA0, 0xA1,                # LShift, RShift
    0xA2, 0xA3,                # LCtrl, RCtrl
    0xA4, 0xA5,                # LMenu(Alt), RMenu(Alt)
    0x5B, 0x5C,                # LWin, RWin
}

# System keys that always pass through even when engine is ON
PASSTHROUGH_VKS = {
    0x1B,                      # Escape
    0x09,                      # Tab (for Alt+Tab)
    0x2C,                      # Print Screen
    0x90,                      # Num Lock
    0x14,                      # Caps Lock
    0x91,                      # Scroll Lock
    0x2D, 0x2E,                # Insert, Delete
    0x70, 0x71, 0x72, 0x73,    # F1-F4
    0x74, 0x75, 0x76, 0x77,    # F5-F8
    0x78, 0x79, 0x7A, 0x7B,    # F9-F12
}


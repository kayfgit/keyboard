"""Global keyboard hook: pynput listener with win32_event_filter suppression.

ALL chord processing happens inside _win32_filter. pynput's suppress_event()
raises SuppressException which we must let propagate to actually suppress keys.
"""

import ctypes
import sys
import time
import traceback

from pynput import keyboard
from pynput.keyboard import Controller, Key
from pynput._util.win32 import SystemHook

from config import (
    VK_TO_KEY, VK_SPACE, VK_Q_TOGGLE, VK_BACKSPACE,
    LLKHF_INJECTED, MODIFIER_VKS, PASSTHROUGH_VKS,
)
from overlay import notify_held_keys

user32 = ctypes.windll.user32
user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = ctypes.c_short

controller = Controller()


class KeyboardHook:
    """Global keyboard interceptor (Plover-style)."""

    def __init__(self, chord_engine, on_toggle, on_space, on_token,
                 on_backspace, on_mode_toggle, on_cheatsheet, on_enter,
                 on_mode_change=None):
        self.engine = chord_engine
        self.on_toggle = on_toggle
        self.on_space = on_space
        self.on_token = on_token
        self.on_backspace = on_backspace
        self.on_mode_toggle = on_mode_toggle
        self.on_cheatsheet = on_cheatsheet
        self.on_enter = on_enter
        self.on_mode_change = on_mode_change  # Just updates display, no toggle
        self.enabled = False
        self.converting = False
        self._listener = None

    def start(self):
        self._listener = keyboard.Listener(
            on_press=self._noop,
            on_release=self._noop,
            win32_event_filter=self._win32_filter,
        )
        self._listener.start()
        print("  Keyboard hook started", flush=True)

    def stop(self):
        if self._listener:
            self._listener.stop()

    def toggle(self):
        # If in text mode, switch to semantic instead of disabling
        if self.enabled and self.engine.mode == 'text':
            # Finalize any pending text buffer first
            if self.engine.text_buffer:
                text = ''.join(self.engine.text_buffer)
                self.engine.token_buffer.append(text)
                self.engine.text_buffer.clear()
            self.engine.mode = 'semantic'
            # Update display without toggling engine again
            if self.on_mode_change:
                self.on_mode_change('semantic')
            return
        # Otherwise toggle enabled/disabled
        self.enabled = not self.enabled
        if not self.enabled:
            self.engine.reset()
            self.converting = False
            notify_held_keys(set())  # Hide overlay

    @staticmethod
    def _noop(key):
        pass

    def _vk_to_char(self, vk):
        """Convert VK code to character for text mode tracking."""
        # Letters A-Z (0x41-0x5A)
        if 0x41 <= vk <= 0x5A:
            shift = user32.GetAsyncKeyState(0x10) & 0x8000
            char = chr(vk)
            return char if shift else char.lower()
        # Numbers 0-9 (0x30-0x39)
        if 0x30 <= vk <= 0x39:
            return chr(vk)
        # Common punctuation
        VK_CHARS = {
            0xBA: ';', 0xBB: '=', 0xBC: ',', 0xBD: '-',
            0xBE: '.', 0xBF: '/', 0xC0: '`', 0xDB: '[',
            0xDC: '\\', 0xDD: ']', 0xDE: "'",
        }
        return VK_CHARS.get(vk)

    def _win32_filter(self, msg, data):
        try:
            return self._process_event(msg, data)
        except SystemHook.SuppressException:
            raise
        except Exception:
            traceback.print_exc()
            sys.stdout.flush()

    def _process_event(self, msg, data):
        is_down = msg in (0x100, 0x104)
        is_up = msg in (0x101, 0x105)
        if not (is_down or is_up):
            return

        vk = data.vkCode
        flags = data.flags

        # Never suppress our own injected keystrokes
        if flags & LLKHF_INJECTED:
            return

        # --- Toggle hotkey: Alt+Q ---
        if vk == VK_Q_TOGGLE and is_down:
            alt = user32.GetAsyncKeyState(0x12) & 0x8000
            if alt:
                self.toggle()
                self.on_toggle()
                self._listener.suppress_event()
                return

        # Engine OFF → pass everything through
        if not self.enabled:
            return

        # Always pass through modifier keys
        if vk in MODIFIER_VKS:
            return

        # Always pass through system/function keys
        if vk in PASSTHROUGH_VKS:
            return

        # Pass through any key pressed with Ctrl/Alt/Win (system shortcuts)
        ctrl = user32.GetAsyncKeyState(0x11) & 0x8000
        alt = user32.GetAsyncKeyState(0x12) & 0x8000
        lwin = user32.GetAsyncKeyState(0x5B) & 0x8000
        rwin = user32.GetAsyncKeyState(0x5C) & 0x8000
        if ctrl or alt or lwin or rwin:
            return

        # --- Text mode: pure QWERTY typing (no chord mechanics) ---
        if self.engine.mode == 'text':
            # Backspace in text mode: track and pass through
            if vk == VK_BACKSPACE:
                if is_down and not self.converting:
                    self.engine.pop_text_char()
                return  # Let backspace through

            # Space in text mode: expand or pass through
            if vk == VK_SPACE:
                if is_down and not self.converting:
                    # If we have tokens or text, expand
                    if self.engine.token_buffer or self.engine.text_buffer:
                        self.on_space()
                        self._listener.suppress_event()
                        return
                return  # No buffer, let space through

            # All keys in text mode: pass through and track immediately
            if is_down and not self.converting:
                char = self._vk_to_char(vk)
                if char:
                    self.engine.add_text_char(char)
                    self.on_token(char)
            return  # Pass through

        # --- Semantic mode: chord-based input ---
        key_name = VK_TO_KEY.get(vk)
        if key_name is not None:
            if not self.converting:
                if is_down:
                    self.engine.key_down(key_name)
                    notify_held_keys(self.engine.held_keys)
                elif is_up:
                    result = self.engine.key_up(key_name)
                    notify_held_keys(self.engine.held_keys)
                    if result is not None:
                        self._handle_chord_result(result)
            self._listener.suppress_event()
            return

        # --- Space ---
        if vk == VK_SPACE:
            if not self.converting and is_down and self.engine.token_buffer:
                self.on_space()
            self._listener.suppress_event()
            return

        # All other keys in semantic mode: suppress (Plover-style)
        self._listener.suppress_event()

    def _handle_chord_result(self, result):
        action = result[0]
        if action == 'token':
            token = result[1]
            # Type token with space separator if not first
            if len(self.engine.token_buffer) > 1:
                controller.type(' ' + token)
            else:
                controller.type(token)
            self.on_token(token)
        elif action == 'type_chars':
            # Text mode: type chord keys as regular characters
            chars = result[1]
            for char in chars:
                controller.type(char)
                self.engine.add_text_char(char)
            self.on_token(''.join(chars))
        elif action == 'backspace':
            self.on_backspace()
        elif action == 'enter':
            self.on_enter()
        elif action == 'toggle_mode':
            self.on_mode_toggle()
        elif action == 'cheatsheet':
            self.on_cheatsheet()
        elif action == 'invalid':
            pass  # Silent

    @staticmethod
    def type_text(text):
        controller.type(text)

    @staticmethod
    def send_backspace(count=1):
        """Send backspace keystrokes with small delays for reliability."""
        for _ in range(count):
            controller.tap(Key.backspace)
            time.sleep(0.01)  # 10ms delay between backspaces

    @staticmethod
    def send_enter():
        controller.tap(Key.enter)

    @staticmethod
    def send_ctrl_backspace():
        """Send Ctrl+Backspace to delete the previous word."""
        with controller.pressed(Key.ctrl):
            controller.tap(Key.backspace)

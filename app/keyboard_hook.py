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
from search_popup import is_search_open, request_search_close
from language_popup import is_popup_open as is_language_popup_open

VK_ESCAPE = 0x1B

user32 = ctypes.windll.user32
user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = ctypes.c_short

controller = Controller()


class KeyboardHook:
    """Global keyboard interceptor (Plover-style)."""

    def __init__(self, chord_engine, on_toggle, on_send_ai, on_token,
                 on_backspace, on_mode_toggle, on_cheatsheet, on_enter,
                 on_search, on_mode_change=None, on_clear_context=None,
                 on_language=None):
        self.engine = chord_engine
        self.on_toggle = on_toggle
        self.on_send_ai = on_send_ai
        self.on_token = on_token
        self.on_backspace = on_backspace
        self.on_mode_toggle = on_mode_toggle
        self.on_cheatsheet = on_cheatsheet
        self.on_enter = on_enter
        self.on_search = on_search
        self.on_mode_change = on_mode_change  # Just updates display, no toggle
        self.on_clear_context = on_clear_context  # Clear AI context
        self.on_language = on_language  # Language selector popup
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
            result = self._process_event(msg, data)
            return result
        except SystemHook.SuppressException:
            raise
        except Exception as e:
            print(f"Event processing error: {e}", flush=True)
            traceback.print_exc()
            sys.stdout.flush()

    def _process_event(self, msg, data):
        is_down = msg in (0x100, 0x104)
        is_up = msg in (0x101, 0x105)
        if not (is_down or is_up):
            return

        vk = data.vkCode
        flags = data.flags

        # Debug: uncomment to see all key events
        # print(f"Key event: vk={vk}, down={is_down}, enabled={self.enabled}", flush=True)

        # Never suppress our own injected keystrokes
        if flags & LLKHF_INJECTED:
            return

        # --- Toggle hotkey: Alt+Q ---
        if vk == VK_Q_TOGGLE and is_down:
            alt = user32.GetAsyncKeyState(0x12) & 0x8000
            if alt:
                print(f"Alt+Q pressed, enabled={self.enabled}", flush=True)
                try:
                    self.toggle()
                    self.on_toggle()
                    print(f"Alt+Q handled, enabled={self.enabled}", flush=True)
                except Exception as e:
                    print(f"Toggle error: {e}", flush=True)
                    traceback.print_exc()
                    sys.stdout.flush()
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
            # Special case: Escape closes search popup if open
            if vk == VK_ESCAPE and is_down and is_search_open():
                request_search_close()
            return

        # When search or language popup is open, pass through ALL keys for typing
        # Only intercept complete multi-key chords (C+M, C+J, C+L)
        if is_search_open() or is_language_popup_open():
            key_name = VK_TO_KEY.get(vk)
            if key_name is None:
                return  # Not a chord key, pass through

            # Track held keys for popup chord detection (separate from engine)
            if not hasattr(self, '_popup_held'):
                self._popup_held = set()

            if is_down:
                self._popup_held.add(key_name)
            elif is_up:
                # Check for control chords before removing key
                held = self._popup_held.copy()
                self._popup_held.discard(key_name)

                # Detect specific chords: C+M (enter), C+J (search), C+L (language)
                if len(held) == 2 and 'c' in held:
                    other_key = (held - {'c'}).pop()
                    if other_key == 'm':
                        self._handle_chord_result(('enter',))
                        return
                    elif other_key == 'j':
                        self._handle_chord_result(('search',))
                        return
                    elif other_key == 'l':
                        self._handle_chord_result(('language',))
                        return

            return  # Let all keys pass through for typing

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

            # Space in text mode: just pass through (send via chord now)
            if vk == VK_SPACE:
                return  # Let space through

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

        # --- Space in semantic mode: suppressed (use all-10-keys chord to send) ---
        if vk == VK_SPACE:
            self._listener.suppress_event()
            return

        # All other keys in semantic mode: suppress (Plover-style)
        self._listener.suppress_event()

    def _handle_chord_result(self, result):
        try:
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
            elif action == 'send_ai':
                self.on_send_ai()
            elif action == 'backspace':
                self.on_backspace()
            elif action == 'enter':
                self.on_enter()
            elif action == 'search':
                self.on_search()
            elif action == 'toggle_mode':
                self.on_mode_toggle()
            elif action == 'cheatsheet':
                self.on_cheatsheet()
            elif action == 'clear_context':
                if self.on_clear_context:
                    self.on_clear_context()
            elif action == 'language':
                if self.on_language:
                    self.on_language()
            elif action == 'arrow':
                direction = result[1]
                self._send_arrow(direction)
            elif action == 'invalid':
                pass  # Silent
        except Exception as e:
            print(f"Chord handler error: {e}", flush=True)
            traceback.print_exc()
            sys.stdout.flush()

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

    @staticmethod
    def _send_arrow(direction):
        """Send arrow key press."""
        arrow_keys = {
            'left': Key.left,
            'right': Key.right,
            'up': Key.up,
            'down': Key.down,
        }
        key = arrow_keys.get(direction)
        if key:
            controller.tap(key)

"""Chord Keyboard Desktop App — entry point.

Flow:
  1. User chords keys → phoneme typed into focused app immediately
  2. Space → phonemes sent to AI → AI result replaces typed phonemes
  3. C+M → backspace (deletes last phoneme/word from app + buffer)
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chord_engine import ChordEngine
from ai_engine import AIEngine
from keyboard_hook import KeyboardHook
from tray import TrayApp
from feedback import beep_toggle_on, beep_toggle_off
from config import get_groq_api_key


def main():
    engine = ChordEngine()
    pending_chars = [0]

    def on_ai_result(text):
        count = pending_chars[0]
        pending_chars[0] = 0
        print(f"  Replacing {count} chars with: {text}", flush=True)
        if count > 0:
            KeyboardHook.send_backspace(count)
            time.sleep(0.05)
        KeyboardHook.type_text(text)
        hook.converting = False

    def on_ai_error(phonemes, error):
        pending_chars[0] = 0
        hook.converting = False
        print(f"  AI error: {error}", flush=True)

    ai = AIEngine(on_result=on_ai_result, on_error=on_ai_error)

    def on_toggle():
        tray.set_enabled(hook.enabled)
        status = "ON" if hook.enabled else "OFF"
        print(f"[Engine {status}]", flush=True)
        if hook.enabled:
            beep_toggle_on()
        else:
            beep_toggle_off()

    def on_space():
        phonemes, char_count = engine.flush_buffer()
        if phonemes:
            pending_chars[0] = char_count
            hook.converting = True
            ai.convert(phonemes)
            print(f"  Converting: {phonemes} ({char_count} chars)", flush=True)
            tray.set_tooltip_buffer("converting...")

    def on_chord(phoneme):
        buf = engine.get_buffer_display()
        print(f"  Chord: {phoneme}  Buffer: [{buf}]", flush=True)
        tray.set_tooltip_buffer(buf)

    def on_backspace():
        """C+M chord — delete last phoneme (whole unit) from app and buffer."""
        popped = engine.pop_last_phoneme()
        if popped:
            # Delete the entire phoneme (could be multiple chars like "str", "ing")
            KeyboardHook.send_backspace(len(popped))
            buf = engine.get_buffer_display()
            print(f"  Backspace: -{popped}  Buffer: [{buf}]", flush=True)
            tray.set_tooltip_buffer(buf)
        else:
            # Buffer empty — send Ctrl+Backspace to delete previous word
            KeyboardHook.send_ctrl_backspace()
            print("  Ctrl+Backspace (delete word)", flush=True)

    def on_enter():
        KeyboardHook.send_enter()

    hook = KeyboardHook(
        chord_engine=engine,
        on_toggle=on_toggle,
        on_space=on_space,
        on_chord=on_chord,
        on_backspace=on_backspace,
        on_enter=on_enter,
    )

    def tray_toggle():
        hook.toggle()
        tray.set_enabled(hook.enabled)
        status = "ON" if hook.enabled else "OFF"
        print(f"[Engine {status}] (tray)", flush=True)
        if hook.enabled:
            beep_toggle_on()
        else:
            beep_toggle_off()

    def tray_language(lang):
        ai.set_language(lang)
        print(f"[Language: {lang}]", flush=True)

    def tray_raw_mode(enabled):
        ai.set_raw_mode(enabled)
        mode = "raw (no punctuation)" if enabled else "formal"
        print(f"[Mode: {mode}]", flush=True)

    def tray_quit():
        hook.stop()
        ai.stop()

    tray = TrayApp(
        on_toggle=tray_toggle,
        on_language_change=tray_language,
        on_raw_mode_change=tray_raw_mode,
        on_quit=tray_quit,
    )

    api_key = get_groq_api_key()
    print("=" * 50, flush=True)
    print("  Chord Keyboard Desktop App", flush=True)
    print("=" * 50, flush=True)
    if api_key:
        print("  Groq AI: enabled", flush=True)
    else:
        print("  Groq AI: disabled (no GROQ_API_KEY)", flush=True)
    print(flush=True)
    print("  Alt+Q  = toggle ON/OFF", flush=True)
    print("  C+M    = backspace (word)", flush=True)
    print("  Space  = convert to text", flush=True)
    print("=" * 50, flush=True)

    ai.start()
    hook.start()
    tray.run()


if __name__ == '__main__':
    main()

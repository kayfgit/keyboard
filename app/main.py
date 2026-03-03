"""Chord Keyboard Desktop App — Semantic Mode

Flow:
  1. User chords keys → token typed into focused app immediately
  2. All 10 keys → tokens sent to AI → AI result replaces typed tokens
  3. C+; → backspace (deletes last token/char, or undo last expansion)
  4. C+M → enter (new line)
  5. C+J → search popup (find tokens by name)
  6. S+C+M → toggle semantic/text mode
  7. C+M+K → show cheatsheet popup

Modes:
  - Semantic: chord keys produce UPPERCASE tokens
  - Text: normal QWERTY typing (lowercase)

Inline Correction:
  - After AI expansion, C+; undoes the expansion and restores original tokens
  - User can then edit tokens and retry
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chord_engine import ChordEngine
from ai_engine import AIEngine
from keyboard_hook import KeyboardHook
from tray import TrayApp
from feedback import beep_toggle_on, beep_toggle_off, beep_mode_semantic, beep_mode_text, beep_undo
from config import get_groq_api_key
from overlay import start_overlay
from search_popup import toggle_search


def main():
    engine = ChordEngine()
    pending_chars = [0]

    # Track last expansion for undo capability
    last_expansion = {
        'tokens': '',        # Original tokens sent to AI
        'result_len': 0,     # Length of AI result (to delete on undo)
        'can_undo': False,   # Whether undo is available
    }

    def clear_undo():
        """Clear undo state (called when user types new tokens)."""
        last_expansion['can_undo'] = False

    def on_ai_result(text):
        count = pending_chars[0]
        pending_chars[0] = 0
        print(f"  AI: {text}", flush=True)
        if count > 0:
            KeyboardHook.send_backspace(count)
            time.sleep(0.05)
        KeyboardHook.type_text(text)
        hook.converting = False

        # Store for undo - expansion is now undoable
        last_expansion['result_len'] = len(text)
        last_expansion['can_undo'] = True
        print(f"  (C+; to undo)", flush=True)

    def on_ai_error(tokens, error):
        pending_chars[0] = 0
        hook.converting = False
        last_expansion['can_undo'] = False
        print(f"  AI error: {error}", flush=True)

    ai = AIEngine(on_result=on_ai_result, on_error=on_ai_error)

    def on_toggle():
        tray.set_enabled(hook.enabled)
        status = "ON" if hook.enabled else "OFF"
        print(f"[Engine {status}]", flush=True)
        clear_undo()
        if hook.enabled:
            beep_toggle_on()
        else:
            beep_toggle_off()

    def on_send_ai():
        """All 10 keys chord — send tokens to AI for expansion."""
        clear_undo()  # Clear any previous undo state
        tokens, char_count = engine.flush_buffer()
        if tokens:
            pending_chars[0] = char_count
            hook.converting = True
            # Store tokens for potential undo
            last_expansion['tokens'] = tokens
            last_expansion['can_undo'] = False  # Not undoable until result arrives
            ai.expand(tokens)
            print(f"  Expanding: {tokens} ({char_count} chars)", flush=True)
            tray.set_tooltip_buffer("expanding...")

    def on_token(token):
        """Handle semantic token or phoneme."""
        clear_undo()  # New token typed, clear undo
        buf = engine.get_buffer_display()
        print(f"  Token: {token}  Buffer: [{buf}]", flush=True)
        tray.set_tooltip_buffer(buf)

    def on_search():
        """C+J chord — toggle search popup."""
        print("  on_search called", flush=True)
        toggle_search()
        print("  on_search completed", flush=True)

    def on_backspace():
        """C+; chord — undo expansion, or delete last token/char."""
        # Check if we can undo last expansion
        if last_expansion['can_undo']:
            result_len = last_expansion['result_len']
            tokens = last_expansion['tokens']

            # Delete AI result
            KeyboardHook.send_backspace(result_len)
            time.sleep(0.05)

            # Type original tokens back
            KeyboardHook.type_text(tokens)

            # Restore tokens to buffer
            for token in tokens.split():
                engine.token_buffer.append(token)

            last_expansion['can_undo'] = False
            buf = engine.get_buffer_display()
            print(f"  Undo: restored [{buf}]", flush=True)
            tray.set_tooltip_buffer(buf)
            beep_undo()
            return

        # In text mode, first try to delete from text_buffer
        if engine.mode == 'text' and engine.text_buffer:
            engine.pop_text_char()
            KeyboardHook.send_backspace(1)
            buf = engine.get_buffer_display()
            print(f"  Backspace (text): Buffer: [{buf}]", flush=True)
            tray.set_tooltip_buffer(buf)
            return

        # Otherwise delete last token
        token, is_marker = engine.pop_last_token()
        if token:
            # Delete the token + space before it (if not first)
            delete_len = len(token)
            if len(engine.token_buffer) > 0:
                delete_len += 1  # Include space separator
            KeyboardHook.send_backspace(delete_len)
            buf = engine.get_buffer_display()
            print(f"  Backspace: -{token}  Buffer: [{buf}]", flush=True)
            tray.set_tooltip_buffer(buf)
        else:
            # Buffer empty — send Ctrl+Backspace to delete previous word
            KeyboardHook.send_ctrl_backspace()
            print("  Ctrl+Backspace (delete word)", flush=True)

    def on_mode_toggle():
        """S+C+M chord — toggle semantic/text mode."""
        clear_undo()
        new_mode = engine.toggle_mode()
        tray.set_mode(new_mode)
        if new_mode == 'semantic':
            beep_mode_semantic()
        else:
            beep_mode_text()
        print(f"  Mode: {new_mode}", flush=True)

    def on_mode_change(new_mode):
        """Mode changed without toggling (e.g., Alt+Q in text mode)."""
        clear_undo()
        tray.set_mode(new_mode)
        if new_mode == 'semantic':
            beep_mode_semantic()
        else:
            beep_mode_text()
        print(f"  Mode: {new_mode}", flush=True)

    def on_cheatsheet():
        """C+M+K chord — show cheatsheet popup."""
        from cheatsheet import show_cheatsheet
        show_cheatsheet(engine.mode)

    def on_enter():
        """C+M chord — enter/new line."""
        clear_undo()
        KeyboardHook.send_enter()

    hook = KeyboardHook(
        chord_engine=engine,
        on_toggle=on_toggle,
        on_send_ai=on_send_ai,
        on_token=on_token,
        on_backspace=on_backspace,
        on_mode_toggle=on_mode_toggle,
        on_cheatsheet=on_cheatsheet,
        on_enter=on_enter,
        on_search=on_search,
        on_mode_change=on_mode_change,
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

    def tray_quit():
        hook.stop()
        ai.stop()

    tray = TrayApp(
        on_toggle=tray_toggle,
        on_quit=tray_quit,
    )

    api_key = get_groq_api_key()
    print("=" * 50, flush=True)
    print("  Chord Keyboard — Semantic Mode", flush=True)
    print("=" * 50, flush=True)
    if api_key:
        print("  Groq AI: enabled", flush=True)
    else:
        print("  Groq AI: disabled (no GROQ_API_KEY)", flush=True)
    print(flush=True)
    print("  Alt+Q     = toggle ON/OFF", flush=True)
    print("  ALL 10    = send to AI (expand)", flush=True)
    print("  C+;       = backspace (delete token)", flush=True)
    print("  C+M       = enter (new line)", flush=True)
    print("  C+J       = search tokens", flush=True)
    print("  S+C+M     = toggle semantic/text", flush=True)
    print("  C+M+K     = show cheatsheet", flush=True)
    print(flush=True)
    print("  Chord preview overlay enabled", flush=True)
    print("=" * 50, flush=True)

    # Start overlay for chord preview
    start_overlay()

    ai.start()
    hook.start()
    tray.run()


if __name__ == '__main__':
    main()

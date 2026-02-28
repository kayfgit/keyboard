"""Floating overlay: shows possible chord completions as keys are held."""

import queue
import threading
import tkinter as tk
from chord_engine import SEMANTICS, LEFT_KEY_ORDER, RIGHT_KEY_ORDER

# Global queue for thread-safe updates
_update_queue = queue.Queue()
_overlay_instance = None

# Category names based on left-hand key combinations
# M extends the category (shown as +)
CATEGORIES = {
    frozenset({'A'}): 'ACTIONS',
    frozenset({'S'}): 'SUBJECTS',
    frozenset({'D'}): 'QUALITY',
    frozenset({'F'}): 'CONNECT',
    frozenset({'C'}): 'RESPOND',
    frozenset({'A', 'F'}): 'SYMBOLS',
    frozenset({'A', 'S'}): 'DAILY',
    frozenset({'D', 'S'}): 'NOUNS',
    frozenset({'A', 'D'}): 'TIME',
    frozenset({'F', 'D'}): 'STATES',
    frozenset({'S', 'F'}): 'PRONOUNS',
    frozenset({'A', 'C'}): 'NEGATION',
    frozenset({'F', 'C'}): 'PREPOSITIONS',
    frozenset({'D', 'C'}): 'STYLE',
    frozenset({'S', 'C'}): 'VERBS',
    frozenset({'A', 'D', 'S'}): 'TECH',
}


class ChordOverlay:
    """Transparent floating window showing chord possibilities."""

    def __init__(self):
        global _overlay_instance
        _overlay_instance = self

        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window

        # Create overlay window
        self.overlay = tk.Toplevel(self.root)
        self.overlay.withdraw()  # Start hidden

        # Window styling
        self.overlay.overrideredirect(True)  # No title bar
        self.overlay.attributes('-topmost', True)  # Always on top
        self.overlay.attributes('-alpha', 0.95)  # Slight transparency
        self.overlay.configure(bg='#1e1e1e')

        # Content frame with padding
        self.frame = tk.Frame(self.overlay, bg='#1e1e1e', padx=12, pady=8)
        self.frame.pack(fill='both', expand=True)

        # Header showing current keys held
        self.header = tk.Label(
            self.frame,
            text='',
            font=('Consolas', 14, 'bold'),
            fg='#569cd6',
            bg='#1e1e1e',
            anchor='w'
        )
        self.header.pack(fill='x', pady=(0, 6))

        # Content area for possibilities
        self.content = tk.Label(
            self.frame,
            text='',
            font=('Consolas', 11),
            fg='#d4d4d4',
            bg='#1e1e1e',
            anchor='nw',
            justify='left'
        )
        self.content.pack(fill='both', expand=True)

        # Position in bottom-right corner
        self._position_window()

        # Track state
        self.visible = False
        self.current_keys = set()

        # Build lookup for efficient filtering
        self._build_prefix_lookup()

    def _build_prefix_lookup(self):
        """Build a lookup for finding tokens by held keys."""
        self.prefix_lookup = {}

        for chord, token in SEMANTICS.items():
            parts = chord.split('+')
            left = frozenset(p for p in parts if p in LEFT_KEY_ORDER)
            right = frozenset(p for p in parts if p in RIGHT_KEY_ORDER)
            all_keys = left | right

            # Store by sorted key tuple for consistent matching
            key = tuple(sorted(all_keys))
            self.prefix_lookup[key] = (chord, token, left, right)

    def _position_window(self):
        """Position overlay in bottom-right corner of screen."""
        self.overlay.update_idletasks()
        screen_w = self.overlay.winfo_screenwidth()
        screen_h = self.overlay.winfo_screenheight()
        # Position with margin from edges (pulled up from bottom)
        x = screen_w - 400
        y = screen_h - 500
        self.overlay.geometry(f'+{x}+{y}')

    def _format_chord(self, chord):
        """Format chord for display, highlighting keys not yet pressed."""
        parts = chord.split('+')
        formatted = []
        for p in parts:
            key = p.upper() if p != ';' else ';'
            if key.lower() in self.current_keys or key in self.current_keys:
                formatted.append(f'[{p}]')  # Already held
            else:
                formatted.append(p)  # Still needed
        return '+'.join(formatted)

    def update(self, held_keys):
        """Update overlay with current held keys."""
        self.current_keys = set(k.upper() if k != ';' else ';' for k in held_keys)

        if not held_keys:
            self.hide()
            return

        # Find matching tokens
        matches = []
        held_upper = set(k.upper() if k != ';' else k for k in held_keys)

        for key_tuple, (chord, token, left, right) in self.prefix_lookup.items():
            chord_keys = set(key_tuple)
            # Check if held keys are a subset of this chord's keys
            if held_upper <= chord_keys:
                remaining = chord_keys - held_upper
                matches.append((len(remaining), chord, token, remaining))

        # Sort by remaining keys needed (closest matches first)
        matches.sort(key=lambda x: (x[0], x[2]))

        if not matches:
            self.hide()
            return

        # Detect category from left-hand keys
        left_held = frozenset(k for k in held_upper if k in LEFT_KEY_ORDER)
        category = CATEGORIES.get(left_held, '')

        # Add + suffix if M (thumb) is held for extended category
        if category and 'M' in held_upper:
            category += '+'

        # Format header with category
        held_str = '+'.join(sorted(held_upper, key=lambda k:
            (LEFT_KEY_ORDER + RIGHT_KEY_ORDER).index(k) if k in LEFT_KEY_ORDER + RIGHT_KEY_ORDER else 99))
        if category:
            self.header.config(text=f'{category}  ({held_str})')
        else:
            self.header.config(text=f'Holding: {held_str}')

        # Format content (show top matches)
        lines = []
        shown = 0
        max_show = 12

        # Group by remaining key count
        exact = [(c, t, r) for rem, c, t, r in matches if rem == 0]
        partial = [(c, t, r) for rem, c, t, r in matches if rem > 0]

        if exact:
            lines.append('--- READY ---')
            for chord, token, _ in exact[:3]:
                lines.append(f'  {token}')
                shown += 1

        if partial and shown < max_show:
            if exact:
                lines.append('')
            lines.append('--- ADD KEYS ---')
            for chord, token, remaining in partial[:max_show - shown]:
                remaining_str = '+'.join(sorted(remaining))
                lines.append(f'  +{remaining_str} -> {token}')

        self.content.config(text='\n'.join(lines))
        self.show()

    def show(self):
        """Show the overlay."""
        if not self.visible:
            self.overlay.deiconify()
            self.visible = True
        self._position_window()

    def hide(self):
        """Hide the overlay."""
        if self.visible:
            self.overlay.withdraw()
            self.visible = False

    def _check_queue(self):
        """Check for updates from keyboard hook thread."""
        try:
            while True:
                held_keys = _update_queue.get_nowait()
                self.update(held_keys)
        except queue.Empty:
            pass
        # Schedule next check
        self.root.after(16, self._check_queue)  # ~60fps

    def run(self):
        """Start the overlay mainloop."""
        self._check_queue()
        self.root.mainloop()

    def destroy(self):
        """Clean up."""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass


def notify_held_keys(held_keys):
    """Thread-safe function to update overlay with held keys."""
    _update_queue.put(set(held_keys))


def start_overlay():
    """Start overlay in a background thread."""
    def _run():
        overlay = ChordOverlay()
        overlay.run()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread

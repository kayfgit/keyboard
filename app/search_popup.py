"""Search popup: quickly find tokens by name."""

import tkinter as tk
from chord_engine import SEMANTICS, TOKEN_TO_CHORD

# Category mapping for display
CHORD_TO_CATEGORY = {
    'A': 'ACTIONS', 'S': 'SUBJECTS', 'D': 'QUALITY', 'F': 'CONNECT', 'C': 'RESPOND',
    'A+F': 'SYMBOLS', 'A+S': 'DAILY', 'D+S': 'NOUNS', 'A+D': 'TIME',
    'F+D': 'STATES', 'S+F': 'PRONOUNS', 'A+C': 'NEGATION', 'F+C': 'PREPOSITIONS',
    'D+C': 'STYLE', 'S+C': 'VERBS', 'A+D+S': 'TECH',
}


def _get_category(chord):
    """Extract category from chord string."""
    parts = chord.split('+')
    left_keys = [p for p in parts if p in ['A', 'S', 'D', 'F', 'C']]
    left_combo = '+'.join(sorted(left_keys))

    # Check for extended (with M)
    has_m = 'M' in parts

    category = CHORD_TO_CATEGORY.get(left_combo, 'OTHER')
    if has_m:
        category += '+'
    return category


class SearchPopup:
    """Quick search popup for finding tokens."""

    def __init__(self, on_close=None):
        self.on_close = on_close
        self.root = tk.Tk()
        self.root.title("Token Search")
        self.root.geometry("500x400")
        self.root.configure(bg='#1a1a2e')
        self.root.attributes('-topmost', True)

        # Center on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 400) // 2
        self.root.geometry(f'+{x}+{y}')

        # Search entry
        self.search_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.search_frame.pack(fill='x', padx=15, pady=15)

        tk.Label(
            self.search_frame,
            text="Search:",
            font=('Consolas', 12),
            fg='#e0e0e0',
            bg='#1a1a2e'
        ).pack(side='left')

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            font=('Consolas', 14),
            bg='#16213e',
            fg='#e0e0e0',
            insertbackground='#e0e0e0',
            relief='flat',
            width=30
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        self.search_entry.bind('<KeyRelease>', self._on_search)

        # Focus the entry after window is shown (needs delay for tkinter)
        self.root.after(50, self._grab_focus)

        # Results area
        self.results_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.results_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Canvas with scrollbar for results
        self.canvas = tk.Canvas(self.results_frame, bg='#1a1a2e', highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.results_frame, orient='vertical', command=self.canvas.yview)
        self.results_inner = tk.Frame(self.canvas, bg='#1a1a2e')

        self.results_inner.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0, 0), window=self.results_inner, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

        # Mouse wheel scrolling
        self.canvas.bind_all('<MouseWheel>', lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units'))

        # Hint at bottom
        hint = tk.Label(
            self.root,
            text="Press C+J to close",
            font=('Consolas', 9),
            fg='#666666',
            bg='#1a1a2e'
        )
        hint.pack(pady=(0, 10))

        # Build token list
        self.tokens = []
        for chord, token in SEMANTICS.items():
            category = _get_category(chord)
            self.tokens.append((token, chord, category))
        self.tokens.sort(key=lambda x: x[0])

        # Show hint initially (no results until user types)
        self._show_hint()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Check for external close requests
        self._check_close()

    def _check_close(self):
        """Check if close was requested from another thread."""
        if is_close_requested():
            print("  _check_close: close detected, closing", flush=True)
            self.close()
        else:
            self.root.after(50, self._check_close)

    def _grab_focus(self):
        """Force focus to the search entry after window is shown."""
        self.root.lift()
        self.root.focus_force()
        self.search_entry.focus_set()

    def _on_search(self, event=None):
        query = self.search_var.get().upper().strip()
        if not query:
            self._show_hint()
            return

        # Filter tokens
        matches = []
        for token, chord, category in self.tokens:
            if query in token:
                # Prioritize exact matches and prefix matches
                if token == query:
                    priority = 0
                elif token.startswith(query):
                    priority = 1
                else:
                    priority = 2
                matches.append((priority, token, chord, category))

        matches.sort(key=lambda x: (x[0], x[1]))
        results = [(t, c, cat) for _, t, c, cat in matches[:20]]
        self._show_results(results)

    def _show_hint(self):
        """Show initial hint instead of results."""
        for widget in self.results_inner.winfo_children():
            widget.destroy()

        tk.Label(
            self.results_inner,
            text="Type to search tokens...",
            font=('Consolas', 11),
            fg='#666666',
            bg='#1a1a2e'
        ).pack(pady=20)

        tk.Label(
            self.results_inner,
            text="Examples: GREET, MAKE, FUNCTION, TODAY",
            font=('Consolas', 10),
            fg='#555555',
            bg='#1a1a2e'
        ).pack()

        self.canvas.update_idletasks()

    def _show_results(self, results):
        # Clear existing
        for widget in self.results_inner.winfo_children():
            widget.destroy()

        if not results:
            tk.Label(
                self.results_inner,
                text="No matches found",
                font=('Consolas', 11),
                fg='#666666',
                bg='#1a1a2e'
            ).pack(pady=20)
            return

        for token, chord, category in results:
            frame = tk.Frame(self.results_inner, bg='#16213e', padx=10, pady=8)
            frame.pack(fill='x', pady=2)

            # Token name (large)
            tk.Label(
                frame,
                text=token,
                font=('Consolas', 12, 'bold'),
                fg='#4ade80',
                bg='#16213e',
                anchor='w'
            ).pack(fill='x')

            # Chord and category
            info_frame = tk.Frame(frame, bg='#16213e')
            info_frame.pack(fill='x')

            tk.Label(
                info_frame,
                text=f"Chord: {chord}",
                font=('Consolas', 10),
                fg='#569cd6',
                bg='#16213e'
            ).pack(side='left')

            tk.Label(
                info_frame,
                text=f"  |  {category}",
                font=('Consolas', 10),
                fg='#f5a04a',
                bg='#16213e'
            ).pack(side='left')

        # Force canvas to update
        self.canvas.update_idletasks()

    def close(self):
        try:
            if self.on_close:
                self.on_close()
        except Exception as e:
            print(f"Search close callback error: {e}", flush=True)
        try:
            self.root.destroy()
        except:
            pass

    def run(self):
        self.root.mainloop()


# Global state
_search_open = False
_close_requested = False
_search_instance = None


def toggle_search():
    """Toggle search popup - open if closed, close if open."""
    global _search_open, _close_requested, _search_instance

    print(f"  toggle_search: _search_open={_search_open}", flush=True)

    # If open, request close
    if _search_open:
        _close_requested = True
        print("  toggle_search: requesting close", flush=True)
        return None

    _search_open = True
    _close_requested = False
    print("  toggle_search: opening new search", flush=True)

    import threading

    def _run():
        global _search_open, _search_instance
        try:
            _search_instance = SearchPopup(on_close=_clear_ref)
            _search_instance.run()
        except Exception as e:
            print(f"Search popup error: {e}", flush=True)
        finally:
            _search_open = False
            _search_instance = None

    def _clear_ref():
        global _search_open
        _search_open = False

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread


def is_close_requested():
    """Check if close was requested (called from tkinter thread)."""
    global _close_requested
    if _close_requested:
        _close_requested = False
        return True
    return False


def is_search_open():
    """Check if search popup is currently open."""
    return _search_open


def request_search_close():
    """Request the search popup to close (called from keyboard hook)."""
    global _close_requested
    if _search_open:
        _close_requested = True
        print("  Search close requested", flush=True)

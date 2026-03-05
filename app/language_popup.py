"""Language selector popup: choose output language for AI expansion."""

import tkinter as tk

# Supported languages with shortcuts
LANGUAGES = [
    ('EN', 'English'),
    ('PT-BR', 'Brazilian Portuguese'),
    ('ES', 'Spanish'),
    ('FR', 'French'),
    ('DE', 'German'),
    ('IT', 'Italian'),
    ('NL', 'Dutch'),
    ('PL', 'Polish'),
    ('RU', 'Russian'),
    ('UK', 'Ukrainian'),
    ('ZH', 'Chinese (Simplified)'),
    ('ZH-TW', 'Chinese (Traditional)'),
    ('JA', 'Japanese'),
    ('KO', 'Korean'),
    ('VI', 'Vietnamese'),
    ('TH', 'Thai'),
    ('ID', 'Indonesian'),
    ('MS', 'Malay'),
    ('TL', 'Filipino/Tagalog'),
    ('HI', 'Hindi'),
    ('BN', 'Bengali'),
    ('TA', 'Tamil'),
    ('TE', 'Telugu'),
    ('MR', 'Marathi'),
    ('UR', 'Urdu'),
    ('AR', 'Arabic'),
    ('FA', 'Persian/Farsi'),
    ('HE', 'Hebrew'),
    ('TR', 'Turkish'),
    ('EL', 'Greek'),
    ('CS', 'Czech'),
    ('SK', 'Slovak'),
    ('HU', 'Hungarian'),
    ('RO', 'Romanian'),
    ('BG', 'Bulgarian'),
    ('HR', 'Croatian'),
    ('SR', 'Serbian'),
    ('SV', 'Swedish'),
    ('NO', 'Norwegian'),
    ('DA', 'Danish'),
    ('FI', 'Finnish'),
    ('SW', 'Swahili'),
    ('AF', 'Afrikaans'),
]


class LanguagePopup:
    """Language selector popup with search."""

    def __init__(self, current_language, on_select, on_close=None):
        self.current_language = current_language
        self.on_select = on_select
        self.on_close = on_close
        self.selected_index = 0
        self.filtered_languages = list(LANGUAGES)

        self.root = tk.Tk()
        self.root.title("Select Language")
        self.root.geometry("400x500")
        self.root.configure(bg='#1a1a2e')
        self.root.attributes('-topmost', True)

        # Center on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 400) // 2
        y = (self.root.winfo_screenheight() - 500) // 2
        self.root.geometry(f'+{x}+{y}')

        # Header
        header = tk.Label(
            self.root,
            text="Select Output Language",
            font=('Consolas', 14, 'bold'),
            fg='#569cd6',
            bg='#1a1a2e'
        )
        header.pack(pady=(15, 5))

        # Current language display
        self.current_label = tk.Label(
            self.root,
            text=f"Current: {current_language}",
            font=('Consolas', 10),
            fg='#888888',
            bg='#1a1a2e'
        )
        self.current_label.pack(pady=(0, 10))

        # Search entry
        self.search_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.search_frame.pack(fill='x', padx=15, pady=(0, 10))

        tk.Label(
            self.search_frame,
            text="Search:",
            font=('Consolas', 11),
            fg='#e0e0e0',
            bg='#1a1a2e'
        ).pack(side='left')

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._on_search_trace)  # Use trace for reliable updates
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            font=('Consolas', 12),
            bg='#16213e',
            fg='#e0e0e0',
            insertbackground='#e0e0e0',
            relief='flat',
            width=25
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        self.search_entry.bind('<Return>', self._on_confirm)
        self.search_entry.bind('<Up>', self._on_up)
        self.search_entry.bind('<Down>', self._on_down)

        # Focus entry after window shown
        self.root.after(50, self._grab_focus)

        # Results area with scrollbar
        self.results_frame = tk.Frame(self.root, bg='#1a1a2e')
        self.results_frame.pack(fill='both', expand=True, padx=15, pady=(0, 10))

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
            text="Type to filter | Enter to select | Esc to close",
            font=('Consolas', 9),
            fg='#666666',
            bg='#1a1a2e'
        )
        hint.pack(pady=(0, 10))

        # Show initial list
        self._show_results()

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind('<Escape>', lambda e: self.close())

        # Check for external close requests
        self._check_close()

    def _check_close(self):
        """Check if close was requested from another thread."""
        if is_close_requested():
            self.close()
        else:
            self.root.after(50, self._check_close)

    def _grab_focus(self):
        """Force focus to the search entry."""
        self.root.lift()
        self.root.focus_force()
        self.search_entry.focus_set()

    def _on_search_trace(self, *args):
        """Called when search_var changes (via trace)."""
        self._on_search()

    def _on_search(self, event=None):
        """Filter languages based on search query."""
        query = self.search_var.get().upper().strip()

        if not query:
            self.filtered_languages = list(LANGUAGES)
        else:
            self.filtered_languages = []
            for code, name in LANGUAGES:
                # Match by code or name
                if query in code.upper() or query in name.upper():
                    # Prioritize exact code match, then prefix, then contains
                    if code.upper() == query:
                        priority = 0
                    elif code.upper().startswith(query):
                        priority = 1
                    elif name.upper().startswith(query):
                        priority = 2
                    else:
                        priority = 3
                    self.filtered_languages.append((priority, code, name))

            self.filtered_languages.sort(key=lambda x: (x[0], x[2]))
            self.filtered_languages = [(c, n) for _, c, n in self.filtered_languages]

        self.selected_index = 0
        self._show_results()

    def _on_up(self, event=None):
        """Move selection up."""
        if self.filtered_languages and self.selected_index > 0:
            self.selected_index -= 1
            self._show_results()
        return 'break'

    def _on_down(self, event=None):
        """Move selection down."""
        if self.filtered_languages and self.selected_index < len(self.filtered_languages) - 1:
            self.selected_index += 1
            self._show_results()
        return 'break'

    def _on_confirm(self, event=None):
        """Confirm selection."""
        if self.filtered_languages:
            code, name = self.filtered_languages[self.selected_index]
            self.on_select(code, name)
            self.close()
        return 'break'

    def _show_results(self):
        """Display filtered language list."""
        for widget in self.results_inner.winfo_children():
            widget.destroy()

        if not self.filtered_languages:
            tk.Label(
                self.results_inner,
                text="No matches found",
                font=('Consolas', 11),
                fg='#666666',
                bg='#1a1a2e'
            ).pack(pady=20)
            return

        for i, (code, name) in enumerate(self.filtered_languages):
            is_selected = (i == self.selected_index)
            is_current = (name == self.current_language or code == self.current_language)

            bg_color = '#2d4a7c' if is_selected else '#16213e'

            frame = tk.Frame(self.results_inner, bg=bg_color, padx=10, pady=6)
            frame.pack(fill='x', pady=1)

            # Bind click to select
            frame.bind('<Button-1>', lambda e, idx=i: self._click_select(idx))

            # Code (shortcut)
            code_label = tk.Label(
                frame,
                text=code,
                font=('Consolas', 11, 'bold'),
                fg='#4ade80' if is_current else '#f5a04a',
                bg=bg_color,
                width=8,
                anchor='w'
            )
            code_label.pack(side='left')
            code_label.bind('<Button-1>', lambda e, idx=i: self._click_select(idx))

            # Name
            name_color = '#4ade80' if is_current else '#e0e0e0'
            name_label = tk.Label(
                frame,
                text=name,
                font=('Consolas', 11),
                fg=name_color,
                bg=bg_color,
                anchor='w'
            )
            name_label.pack(side='left', fill='x', expand=True)
            name_label.bind('<Button-1>', lambda e, idx=i: self._click_select(idx))

            # Current indicator
            if is_current:
                tk.Label(
                    frame,
                    text="(current)",
                    font=('Consolas', 9),
                    fg='#4ade80',
                    bg=bg_color
                ).pack(side='right')

        self.canvas.update_idletasks()

        # Scroll to show selected item
        if self.filtered_languages:
            # Calculate position to scroll to
            item_height = 30  # Approximate height per item
            scroll_pos = self.selected_index * item_height
            canvas_height = self.canvas.winfo_height()
            total_height = len(self.filtered_languages) * item_height

            if total_height > canvas_height:
                fraction = scroll_pos / total_height
                self.canvas.yview_moveto(max(0, min(1, fraction - 0.3)))

    def _click_select(self, index):
        """Handle click selection."""
        self.selected_index = index
        self._show_results()
        # Double-click selects
        self.root.after(10, self._on_confirm)

    def close(self):
        """Close the popup."""
        try:
            if self.on_close:
                self.on_close()
        except Exception as e:
            print(f"Language popup close callback error: {e}", flush=True)
        try:
            self.root.destroy()
        except:
            pass

    def run(self):
        self.root.mainloop()


# Global state
_popup_open = False
_close_requested = False
_popup_instance = None


def open_language_popup(current_language, on_select, on_close=None):
    """Open language selector popup."""
    global _popup_open, _close_requested, _popup_instance

    if _popup_open:
        _close_requested = True
        return None

    _popup_open = True
    _close_requested = False

    import threading

    def _run():
        global _popup_open, _popup_instance
        try:
            _popup_instance = LanguagePopup(
                current_language=current_language,
                on_select=on_select,
                on_close=_on_close_wrapper
            )
            _popup_instance.run()
        except Exception as e:
            print(f"Language popup error: {e}", flush=True)
        finally:
            _popup_open = False
            _popup_instance = None
            # Call user's on_close callback
            if on_close:
                try:
                    on_close()
                except Exception as e:
                    print(f"Language popup on_close error: {e}", flush=True)

    def _on_close_wrapper():
        global _popup_open
        _popup_open = False

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread


def is_close_requested():
    """Check if close was requested."""
    global _close_requested
    if _close_requested:
        _close_requested = False
        return True
    return False


def is_popup_open():
    """Check if popup is open."""
    return _popup_open


def request_popup_close():
    """Request popup to close."""
    global _close_requested
    if _popup_open:
        _close_requested = True

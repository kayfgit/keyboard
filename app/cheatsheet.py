"""Cheatsheet popup window with search functionality."""

import tkinter as tk
from tkinter import ttk

from chord_engine import SEMANTICS, TOKEN_TO_CHORD, CONSONANTS, VOWELS


# Organize tokens by category for display
CATEGORIES = {
    'ACTIONS (A)': ['MAKE', 'CHANGE', 'REMOVE', 'FIX', 'FIND', 'SHOW', 'TRY', 'USE',
                    'EXPLAIN', 'IMPROVE', 'COMPARE', 'ANALYZE', 'SUMMARIZE', 'EXPAND', 'SIMPLIFY'],
    'ACTIONS+ (A+M)': ['ADD', 'KEEP', 'GIVE', 'TAKE', 'THINK', 'HELP', 'CHECK',
                       'LIST', 'COMBINE', 'SPLIT', 'GENERATE', 'TRANSLATE', 'REWRITE', 'FORMAT'],
    'SUBJECTS (S)': ['THIS', 'THAT', 'IT', 'IDEA', 'TEXT', 'CODE', 'QUESTION',
                     'ANSWER', 'PROBLEM', 'SOLUTION', 'EXAMPLE', 'RESULT', 'REASON', 'WAY', 'POINT'],
    'SUBJECTS+ (S+M)': ['FILE', 'FUNCTION', 'DATA', 'NAME', 'LIST', 'STEP', 'PART',
                        'OPTION', 'ERROR', 'OUTPUT', 'INPUT', 'CONTENT', 'CONTEXT', 'DETAIL'],
    'QUALITY (D)': ['GOOD', 'BAD', 'MORE', 'LESS', 'SIMPLE', 'COMPLEX', 'NEW',
                    'OLD', 'SAME', 'DIFFERENT', 'GENERAL', 'SPECIFIC', 'MAIN', 'OTHER', 'ALL'],
    'QUALITY+ (D+M)': ['FAST', 'SLOW', 'BIG', 'SMALL', 'SHORT', 'LONG', 'CLEAR',
                       'BETTER', 'WORSE', 'CORRECT', 'WRONG', 'SIMILAR', 'EXACT', 'ENOUGH'],
    'CONNECT (F)': ['AND', 'OR', 'BUT', 'SO', 'IF', 'THEN', 'BECAUSE',
                    'WITH', 'WITHOUT', 'FOR', 'TO', 'FROM', 'LIKE', 'AS', 'ABOUT'],
    'CONNECT+ (F+M)': ['ALSO', 'HOWEVER', 'INSTEAD', 'RATHER', 'BEFORE', 'AFTER', 'WHILE',
                       'WHEN', 'WHERE', 'ALTHOUGH', 'UNLESS', 'UNTIL', 'SINCE', 'WHETHER'],
    'RESPOND (C)': ['YES', 'NO', 'MAYBE', 'OK', 'THANKS', 'PLEASE', 'SORRY',
                    'WAIT', 'DONE', 'AGAIN', 'WHAT', 'WHY', 'HOW', 'WHICH', 'WHO'],
    'RESPOND+ (C+M)': ['CONTINUE', 'STOP', 'UNDO', 'SKIP', 'FOCUS', 'IGNORE', 'REMEMBER',
                       'FORGET', 'CONFIRM', 'NEVERMIND', 'PERFECT', 'ALMOST', 'NOT_QUITE', 'EXACTLY'],
    'PRONOUNS (S+F)': ['I', 'YOU', 'WE', 'THEY', 'HE', 'SHE', 'SOMEONE', 'EVERYONE', 'ANYONE', 'NOONE',
                       'SOMETHING', 'EVERYTHING', 'ANYTHING', 'NOTHING', 'ITSELF'],
    'PRONOUNS+ (S+F+M)': ['MY', 'YOUR', 'OUR', 'THEIR', 'HIS', 'HER', 'MYSELF', 'ME', 'US', 'THEM',
                          'HIMSELF', 'HERSELF', 'THEMSELVES', 'OURSELVES', 'YOURSELF'],
    'NEGATION (A+C)': ['NOT', 'CAN', 'WILL', 'SHOULD', 'NEVER', 'CANNOT', 'WONT', 'MUST', 'MIGHT', 'WOULD',
                       'ALWAYS', 'SOMETIMES', 'USUALLY', 'BARELY', 'HARDLY'],
    'NEGATION+ (A+C+M)': ['DONT', 'DIDNT', 'DOESNT', 'ISNT', 'HAVENT', 'WASNT', 'WERENT', 'COULDNT', 'SHOULDNT', 'WOULDNT',
                          'ARENT', 'WONT_BE', 'CANT_BE', 'MUSTNT', 'NEEDNT'],
    'PREPOSITIONS (F+C)': ['IN', 'ON', 'AT', 'BY', 'OUT', 'UP', 'DOWN', 'OVER', 'UNDER', 'THROUGH',
                           'WITHIN', 'THROUGHOUT', 'ALONG', 'AGAINST', 'AMONG'],
    'PREPOSITIONS+ (F+C+M)': ['INTO', 'ONTO', 'NEAR', 'AROUND', 'BETWEEN', 'BEHIND', 'ABOVE', 'BELOW', 'BESIDE', 'ACROSS',
                              'TOWARD', 'AWAY', 'APART', 'TOGETHER', 'INSIDE'],
    'DAILY (A+S)': ['GREET', 'ASK', 'TELL', 'WANT', 'NEED', 'KNOW', 'MEET',
                    'CALL', 'SEND', 'GET', 'START', 'FINISH', 'SCHEDULE', 'CANCEL', 'COMPLETE'],
    'DAILY+ (A+S+M)': ['GO', 'COME', 'LEAVE', 'STAY', 'RETURN', 'BRING', 'ARRIVE',
                       'PUT', 'MOVE', 'OPEN', 'SEE', 'HEAR', 'FEEL', 'CLOSE', 'TOUCH'],
    'VERBS (S+C)': ['PLAY', 'WORK', 'REST', 'SLEEP', 'WAKE', 'EAT', 'DRINK',
                    'READ', 'WRITE', 'SPEAK', 'LISTEN', 'WATCH', 'LEARN', 'TEACH', 'PRACTICE'],
    'VERBS+ (S+C+M)': ['RUN', 'WALK', 'SIT', 'STAND', 'JUMP', 'CLIMB', 'FALL',
                       'PUSH', 'PULL', 'HOLD', 'DROP', 'THROW', 'CATCH', 'CARRY', 'DRAG'],
    'NOUNS (D+S)': ['NAME', 'PERSON', 'PLACE', 'THING', 'TEAM', 'COMPANY', 'GROUP',
                    'PROJECT', 'MEETING', 'EVENT', 'WORLD', 'HOME', 'OFFICE', 'ROOM', 'BUILDING'],
    'NOUNS+ (D+S+M)': ['EMAIL', 'MESSAGE', 'PHONE', 'MONEY', 'DOCUMENT', 'REPORT',
                       'TASK', 'ISSUE', 'REQUEST', 'UPDATE', 'SCREEN', 'BUTTON', 'WINDOW', 'LINK', 'IMAGE'],
    'TIME (A+D)': ['TODAY', 'TOMORROW', 'NOW', 'LATER', 'SOON', 'YESTERDAY', 'ALWAYS',
                   'TIME', 'DATE', 'MOMENT', 'WEEK', 'MONTH', 'YEAR', 'HOUR', 'MINUTE'],
    'TIME+ (A+D+M)': ['MORNING', 'AFTERNOON', 'EVENING', 'NIGHT', 'NOON', 'MIDNIGHT', 'WEEKEND',
                      'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY', 'ONCE', 'TWICE', 'OFTEN', 'RARELY'],
    'STATES (F+D)': ['HAPPY', 'BUSY', 'READY', 'SURE', 'AVAILABLE', 'INTERESTED', 'EXCITED',
                     'URGENT', 'IMPORTANT', 'NECESSARY', 'POSSIBLE', 'IMPOSSIBLE', 'REQUIRED', 'OPTIONAL', 'RECOMMENDED'],
    'STATES+ (F+D+M)': ['SAD', 'ANGRY', 'TIRED', 'CONFUSED', 'WORRIED', 'NERVOUS', 'CALM',
                        'BORED', 'STUCK', 'LOST', 'FOUND', 'BROKEN', 'FIXED', 'PENDING', 'COMPLETE'],
    'STYLE (D+C)': ['FORMAL', 'CASUAL', 'POLITE', 'DIRECT', 'TECHNICAL', 'FRIENDLY', 'PROFESSIONAL',
                    'BRIEF', 'DETAILED', 'AS_QUESTION', 'AS_COMMAND', 'AS_REQUEST', 'AS_STATEMENT', 'AS_LIST', 'AS_SUMMARY'],
    'STYLE+ (D+C+M)': ['REPROMPT', 'URGENT_TONE', 'GENTLE', 'FIRM', 'HUMOROUS', 'SERIOUS', 'EMPATHETIC',
                       'CONFIDENT', 'HUMBLE', 'ENTHUSIASTIC', 'SKEPTICAL', 'SUPPORTIVE', 'CRITICAL', 'NEUTRAL', 'PERSUASIVE'],
    'SYMBOLS (A+F)': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', ',', '?', '!', ':'],
    'SYMBOLS+ (A+F+M)': ['-', '_', '/', '@', '#', '$', '%', '&', '*', '+', '=', '(', ')', '"', ';'],
    'TECH (A+D+S)': ['DEBUG', 'TEST', 'BUILD', 'DEPLOY', 'COMMIT', 'PUSH', 'PULL',
                     'MERGE', 'BRANCH', 'CLONE', 'INSTALL', 'UNINSTALL', 'UPGRADE', 'CONFIGURE', 'INITIALIZE'],
    'TECH+ (A+D+S+M)': ['SERVER', 'CLIENT', 'DATABASE', 'API', 'ENDPOINT', 'REQUEST_NOUN', 'RESPONSE',
                        'QUERY', 'CACHE', 'LOG', 'VARIABLE', 'CONSTANT', 'PARAMETER', 'ARGUMENT', 'EXCEPTION'],
}


class CheatsheetWindow:
    def __init__(self, mode='semantic'):
        self.mode = mode
        self.root = tk.Tk()
        self.root.title(f"Chord Cheatsheet — {mode.capitalize()}")
        self.root.geometry("700x500")
        self.root.configure(bg='#1a1a2e')

        # Make window stay on top
        self.root.attributes('-topmost', True)

        self._setup_ui()
        self._populate_list()

    def _setup_ui(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#1a1a2e')
        style.configure('TLabel', background='#1a1a2e', foreground='#e0e0e0', font=('Consolas', 10))
        style.configure('Header.TLabel', font=('Consolas', 12, 'bold'), foreground='#f5a04a')
        style.configure('TEntry', fieldbackground='#16213e', foreground='#e0e0e0')

        # Search frame
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(search_frame, text="Search:", style='TLabel').pack(side='left')

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Consolas', 12),
            bg='#16213e',
            fg='#e0e0e0',
            insertbackground='#e0e0e0',
            relief='flat'
        )
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        self.search_entry.focus_set()

        # Bind to key events for search
        self.search_entry.bind('<KeyRelease>', self._on_search)
        self.search_entry.bind('<Return>', self._on_search)

        # Mode indicator
        mode_text = "SEMANTIC" if self.mode == 'semantic' else "PHONEMIC"
        mode_color = '#4ade80' if self.mode == 'semantic' else '#f59e6e'
        mode_label = tk.Label(
            search_frame,
            text=mode_text,
            font=('Consolas', 10, 'bold'),
            bg='#1a1a2e',
            fg=mode_color
        )
        mode_label.pack(side='right', padx=10)

        # Scrollable content
        container = ttk.Frame(self.root)
        container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        canvas = tk.Canvas(container, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        self.content_frame = ttk.Frame(canvas)

        self.content_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=self.content_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        canvas.bind_all('<MouseWheel>', _on_mousewheel)

        # Close on Escape
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def _populate_list(self, filter_text=''):
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        filter_text = filter_text.lower()

        if self.mode == 'semantic':
            self._populate_semantic(filter_text)
        else:
            self._populate_phonemic(filter_text)

    def _populate_semantic(self, filter_text):
        row = 0
        for category, tokens in CATEGORIES.items():
            # Filter tokens
            matching = [t for t in tokens if filter_text in t.lower()]
            if not matching:
                continue

            # Category header
            header = tk.Label(
                self.content_frame,
                text=category,
                font=('Consolas', 11, 'bold'),
                bg='#1a1a2e',
                fg='#f5a04a',
                anchor='w'
            )
            header.grid(row=row, column=0, columnspan=4, sticky='w', pady=(10, 5))
            row += 1

            # Tokens in grid
            col = 0
            for token in matching:
                chord = TOKEN_TO_CHORD.get(token, '?')
                text = f"{chord}: {token}"

                token_label = tk.Label(
                    self.content_frame,
                    text=text,
                    font=('Consolas', 9),
                    bg='#16213e',
                    fg='#e0e0e0',
                    padx=8,
                    pady=4,
                    anchor='w'
                )
                token_label.grid(row=row, column=col, sticky='w', padx=2, pady=2)

                col += 1
                if col >= 4:
                    col = 0
                    row += 1

            if col > 0:
                row += 1

    def _populate_phonemic(self, filter_text):
        # Consonants
        header = tk.Label(
            self.content_frame,
            text="CONSONANTS (Left Hand)",
            font=('Consolas', 11, 'bold'),
            bg='#1a1a2e',
            fg='#f5a04a',
            anchor='w'
        )
        header.grid(row=0, column=0, columnspan=4, sticky='w', pady=(10, 5))

        row = 1
        col = 0
        for code, phoneme in sorted(CONSONANTS.items()):
            if phoneme is None:
                continue
            if filter_text and filter_text not in phoneme.lower():
                continue

            text = f"{code:02d}: {phoneme}"
            label = tk.Label(
                self.content_frame,
                text=text,
                font=('Consolas', 9),
                bg='#16213e',
                fg='#a78bfa',
                padx=8,
                pady=4,
                anchor='w'
            )
            label.grid(row=row, column=col, sticky='w', padx=2, pady=2)

            col += 1
            if col >= 4:
                col = 0
                row += 1

        if col > 0:
            row += 1

        # Vowels
        header = tk.Label(
            self.content_frame,
            text="VOWELS (Right Hand)",
            font=('Consolas', 11, 'bold'),
            bg='#1a1a2e',
            fg='#f5a04a',
            anchor='w'
        )
        header.grid(row=row, column=0, columnspan=4, sticky='w', pady=(10, 5))
        row += 1

        col = 0
        for code, phoneme in sorted(VOWELS.items()):
            if phoneme is None:
                continue
            if filter_text and filter_text not in phoneme.lower():
                continue

            text = f"{code:02d}: {phoneme}"
            label = tk.Label(
                self.content_frame,
                text=text,
                font=('Consolas', 9),
                bg='#16213e',
                fg='#4ade80',
                padx=8,
                pady=4,
                anchor='w'
            )
            label.grid(row=row, column=col, sticky='w', padx=2, pady=2)

            col += 1
            if col >= 4:
                col = 0
                row += 1

    def _on_search(self, event=None):
        self._populate_list(self.search_var.get())

    def winfo_exists(self):
        try:
            return self.root.winfo_exists()
        except:
            return False

    def lift(self):
        self.root.lift()

    def focus_force(self):
        self.root.focus_force()

    def run(self):
        self.root.mainloop()


def show_cheatsheet(mode='semantic'):
    """Show cheatsheet popup (non-blocking)."""
    import threading

    def _run():
        window = CheatsheetWindow(mode)
        window.run()

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    # Return a proxy object for the window
    class WindowProxy:
        def __init__(self):
            self._exists = True

        def winfo_exists(self):
            return self._exists

        def lift(self):
            pass

        def focus_force(self):
            pass

    return WindowProxy()

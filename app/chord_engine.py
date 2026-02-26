"""Chord engine: mapping tables and chord state machine.

Pure logic — no I/O, no threads. Ported from index.html.
"""

# Universal consonant map (left hand, 5-bit code)
CONSONANTS = {
    0:  None,
    1:  'f',    2:  'p',    3:  'st',   4:  't',
    5:  's',    6:  'θ',    7:  'ð',    8:  'r',
    9:  'ʃ',    10: 'nd',   11: 'tr',   12: 'k',
    13: 'h',    14: 'pr',   15: 'str',  16: 'b',
    17: 'v',    18: 'm',    19: 'w',    20: 'd',
    21: 'z',    22: 'n',    23: 'dʒ',   24: 'l',
    25: 'ʒ',    26: 'nt',   27: 'tʃ',   28: 'g',
    29: 'sp',   30: 'ŋ',    31: 'j',
}

# Universal vowel map (right hand, 5-bit code)
# 6 base vowels + 5 modified vowels + 20 VC chunks
VOWELS = {
    0:  None,
    1:  'i',    2:  'o',    3:  'u',    4:  'e',
    5:  'ə',    6:  'at',   7:  'in',   8:  'a',
    9:  'an',   10: 'on',   11: 'it',   12: 'er',
    13: 'or',   14: 'al',   15: 'ing',  16: 'ot',
    17: 'ī',    18: 'ō',    19: 'ū',    20: 'ē',
    21: 'et',   22: 'ut',   23: 'en',   24: 'ā',
    25: 'un',   26: 'ad',   27: 'is',   28: 'il',
    29: 'aw',   30: 'oi',   31: 'ow',
}

# Bit positions for each key within its hand
LEFT_KEYS = {'c': 4, 'f': 3, 'd': 2, 's': 1, 'a': 0}
RIGHT_KEYS = {'m': 4, 'j': 3, 'k': 2, 'l': 1, ';': 0}

ALL_CHORD_KEYS = set(LEFT_KEYS) | set(RIGHT_KEYS)


class ChordEngine:
    """State machine for chord detection and phoneme buffering."""

    def __init__(self):
        self.held_keys = set()       # currently held chord keys
        self.chord_buffer = set()    # all keys pressed in current chord
        self.chord_active = False
        self.phoneme_buffer = []     # accumulated phonemes awaiting AI conversion

    def is_chord_key(self, key):
        return key in ALL_CHORD_KEYS

    def key_down(self, key):
        """Register a chord key press. Returns nothing — chord fires on key_up."""
        if key not in ALL_CHORD_KEYS:
            return
        if key in self.held_keys:
            return

        if not self.chord_active:
            self.chord_active = True
            self.chord_buffer.clear()

        self.held_keys.add(key)
        self.chord_buffer.add(key)

    def key_up(self, key):
        """Register a chord key release. Returns a result when all keys are released.

        Returns:
            None — if keys are still held
            ('phoneme', str) — a phoneme was produced
            ('backspace',) — C+M control chord
            ('enter',) — all-10-keys control chord
            ('invalid',) — unrecognized chord
            ('empty',) — no keys contributed a code
        """
        if key not in ALL_CHORD_KEYS:
            return None

        self.held_keys.discard(key)

        if self.chord_active and len(self.held_keys) == 0:
            result = self._fire_chord()
            self.chord_active = False
            self.chord_buffer.clear()
            return result

        return None

    def _get_left_code(self):
        code = 0
        for key in self.chord_buffer:
            if key in LEFT_KEYS:
                code |= (1 << LEFT_KEYS[key])
        return code

    def _get_right_code(self):
        code = 0
        for key in self.chord_buffer:
            if key in RIGHT_KEYS:
                code |= (1 << RIGHT_KEYS[key])
        return code

    def _has_left(self):
        return any(k in LEFT_KEYS for k in self.chord_buffer)

    def _has_right(self):
        return any(k in RIGHT_KEYS for k in self.chord_buffer)

    def _fire_chord(self):
        left_code = self._get_left_code()
        right_code = self._get_right_code()

        # Control chords
        if left_code == 16 and right_code == 16:  # both thumbs (C+M)
            return ('backspace',)
        if left_code == 31 and right_code == 31:  # all 10 keys
            return ('enter',)

        # Phoneme lookup
        result = ''
        valid = True

        if self._has_left() and left_code != 0:
            c = CONSONANTS.get(left_code)
            if c:
                result += c
            else:
                valid = False

        if self._has_right() and right_code != 0:
            v = VOWELS.get(right_code)
            if v:
                result += v
            else:
                valid = False

        if result and valid:
            self.phoneme_buffer.append(result)
            return ('phoneme', result)
        elif not valid:
            return ('invalid',)
        else:
            return ('empty',)

    def pop_last_phoneme(self):
        """Remove and return the last phoneme from buffer, or None."""
        if self.phoneme_buffer:
            return self.phoneme_buffer.pop()
        return None

    def flush_buffer(self):
        """Take all buffered phonemes. Returns (joined_string, char_count)."""
        if not self.phoneme_buffer:
            return '', 0
        text = ''.join(self.phoneme_buffer)
        self.phoneme_buffer.clear()
        return text, len(text)

    def get_buffer_display(self):
        """Return current buffer contents for display."""
        return ''.join(self.phoneme_buffer)

    def get_buffer_char_count(self):
        """Return total character count of all phonemes in buffer."""
        return sum(len(p) for p in self.phoneme_buffer)

    def reset(self):
        """Clear all state."""
        self.held_keys.clear()
        self.chord_buffer.clear()
        self.chord_active = False
        self.phoneme_buffer.clear()

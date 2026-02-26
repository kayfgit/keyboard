"""Audio feedback using winsound beeps."""

import threading
import winsound


def _beep(freq, duration):
    """Play a beep in a background thread to avoid blocking."""
    threading.Thread(
        target=winsound.Beep, args=(freq, duration), daemon=True
    ).start()


def beep_chord():
    """Short high beep — chord fired successfully."""
    _beep(1200, 30)


def beep_convert():
    """Two-tone ascending — AI conversion complete."""
    def _play():
        winsound.Beep(800, 40)
        winsound.Beep(1200, 40)
    threading.Thread(target=_play, daemon=True).start()


def beep_error():
    """Low buzz — invalid chord or error."""
    _beep(300, 80)


def beep_toggle_on():
    """Ascending tone — engine enabled."""
    def _play():
        winsound.Beep(600, 50)
        winsound.Beep(900, 50)
    threading.Thread(target=_play, daemon=True).start()


def beep_toggle_off():
    """Descending tone — engine disabled."""
    def _play():
        winsound.Beep(900, 50)
        winsound.Beep(600, 50)
    threading.Thread(target=_play, daemon=True).start()

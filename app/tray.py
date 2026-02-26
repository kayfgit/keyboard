"""System tray icon with toggle/language/raw mode/quit menu."""

import pystray
from PIL import Image, ImageDraw

from config import AI_LANGUAGES


def _create_icon_image(enabled):
    """Create a 64x64 tray icon — green circle when ON, gray when OFF."""
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    color = (74, 222, 128, 255) if enabled else (120, 120, 120, 255)
    margin = 8
    draw.ellipse([margin, margin, size - margin, size - margin], fill=color)
    text_color = (0, 0, 0, 255) if enabled else (60, 60, 60, 255)
    draw.text((size // 2 - 6, size // 2 - 8), "K", fill=text_color)
    return img


class TrayApp:
    """System tray icon for the chord keyboard daemon."""

    def __init__(self, on_toggle, on_language_change, on_raw_mode_change, on_quit):
        self.on_toggle = on_toggle
        self.on_language_change = on_language_change
        self.on_raw_mode_change = on_raw_mode_change
        self.on_quit = on_quit
        self.enabled = False
        self.lang = 'en'
        self.raw_mode = False
        self._icon = None

    def _build_menu(self):
        lang_items = []
        for code, name in AI_LANGUAGES.items():
            lang_items.append(
                pystray.MenuItem(
                    f"{'● ' if code == self.lang else '  '}{name}",
                    lambda _, c=code: self._set_language(c),
                )
            )

        return pystray.Menu(
            pystray.MenuItem(
                lambda _: f"{'■ ON' if self.enabled else '□ OFF'}  (Alt+Q)",
                self._toggle,
                default=True,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Language", pystray.Menu(*lang_items)),
            pystray.MenuItem(
                lambda _: f"{'● ' if self.raw_mode else '○ '}Raw mode (no punctuation)",
                self._toggle_raw_mode,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )

    def _toggle(self, icon, item):
        self.on_toggle()

    def _set_language(self, lang):
        self.lang = lang
        self.on_language_change(lang)
        self.update()

    def _toggle_raw_mode(self, icon, item):
        self.raw_mode = not self.raw_mode
        self.on_raw_mode_change(self.raw_mode)
        self.update()

    def _quit(self, icon, item):
        self.on_quit()
        icon.stop()

    def update(self):
        if self._icon:
            self._icon.icon = _create_icon_image(self.enabled)
            self._icon.menu = self._build_menu()
            self._icon.title = self._get_tooltip()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.update()

    def set_tooltip_buffer(self, buffer_text):
        if self._icon:
            self._icon.title = self._get_tooltip(buffer_text)

    def _get_tooltip(self, buffer_text=''):
        status = "ON" if self.enabled else "OFF"
        lang_name = AI_LANGUAGES.get(self.lang, self.lang)
        mode = " [raw]" if self.raw_mode else ""
        tip = f"Chord Keyboard [{status}] — {lang_name}{mode}"
        if buffer_text:
            tip += f"\nBuffer: {buffer_text}"
        return tip

    def run(self):
        self._icon = pystray.Icon(
            "chord-keyboard",
            icon=_create_icon_image(self.enabled),
            title=self._get_tooltip(),
            menu=self._build_menu(),
        )
        self._icon.run()

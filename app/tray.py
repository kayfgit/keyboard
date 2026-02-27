"""System tray icon with toggle/mode indicator/quit menu."""

import pystray
from PIL import Image, ImageDraw, ImageFont


def _create_icon_image(enabled, mode='semantic'):
    """Create a 64x64 tray icon showing ON/OFF state and mode."""
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background color: green=ON, gray=OFF
    if enabled:
        bg_color = (74, 222, 128, 255) if mode == 'semantic' else (245, 158, 110, 255)
    else:
        bg_color = (120, 120, 120, 255)

    margin = 4
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=8,
        fill=bg_color
    )

    # Mode letter: S=semantic, P=phonemic
    letter = 'S' if mode == 'semantic' else 'P'
    text_color = (0, 0, 0, 255) if enabled else (60, 60, 60, 255)

    # Try to use a larger font
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()

    # Center the letter
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 4
    draw.text((x, y), letter, fill=text_color, font=font)

    return img


class TrayApp:
    """System tray icon for the chord keyboard daemon."""

    def __init__(self, on_toggle, on_quit):
        self.on_toggle = on_toggle
        self.on_quit = on_quit
        self.enabled = False
        self.mode = 'semantic'
        self._icon = None

    def _build_menu(self):
        mode_display = "Semantic" if self.mode == 'semantic' else "Phonemic"
        return pystray.Menu(
            pystray.MenuItem(
                lambda _: f"{'ON' if self.enabled else 'OFF'}  (Alt+Q)",
                self._toggle,
                default=True,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                lambda _: f"Mode: {mode_display}  (S+C+M)",
                None,
                enabled=False,
            ),
            pystray.MenuItem(
                "Cheatsheet  (C+M+K)",
                self._show_cheatsheet,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )

    def _toggle(self, icon, item):
        self.on_toggle()

    def _show_cheatsheet(self, icon, item):
        from cheatsheet import show_cheatsheet
        show_cheatsheet(self.mode)

    def _quit(self, icon, item):
        self.on_quit()
        icon.stop()

    def update(self):
        if self._icon:
            self._icon.icon = _create_icon_image(self.enabled, self.mode)
            self._icon.menu = self._build_menu()
            self._icon.title = self._get_tooltip()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.update()

    def set_mode(self, mode):
        self.mode = mode
        self.update()

    def set_tooltip_buffer(self, buffer_text):
        if self._icon:
            self._icon.title = self._get_tooltip(buffer_text)

    def _get_tooltip(self, buffer_text=''):
        status = "ON" if self.enabled else "OFF"
        mode_name = "Semantic" if self.mode == 'semantic' else "Phonemic"
        tip = f"Chord Keyboard [{status}] — {mode_name}"
        if buffer_text:
            tip += f"\nBuffer: {buffer_text}"
        return tip

    def run(self):
        self._icon = pystray.Icon(
            "chord-keyboard",
            icon=_create_icon_image(self.enabled, self.mode),
            title=self._get_tooltip(),
            menu=self._build_menu(),
        )
        self._icon.run()

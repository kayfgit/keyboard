# Universal Chord Keyboard

A 10-key chord-based keyboard system that combines stenography concepts with AI-powered text expansion. Designed for developers communicating with AI coding assistants.

**[Try the Web Demo](https://kayfgit.github.io/keyboard/semantic.html)** | **[Cheatsheet](https://YOUR_USERNAME.github.io/keyboard/semantic-cheatsheet.html)**

The web demo is a limited preview. For the full experience, install the desktop app which includes:
- 280+ semantic tokens vs ~150 in web demo
- 40+ output languages
- System tray integration
- Live chord preview overlay
- Searchable token popup
- Text mode (QWERTY typing)

**Tip:** Add your free [Groq API key](https://console.groq.com/keys) in the web demo to enable real AI expansion.

## Concept

Instead of typing every character, you press key combinations (chords) to encode **intent**, and AI expands it to natural language. One layout works across all languages.

```
Input:  MAKE FUNCTION ASYNC
Output: Create an async function.

Input:  POLITE GREET NAME wren INTERESTED DISCUSS PROJECT
Output: Hello, Mr. Wren. I'm interested in discussing the project with you.
```

## Two Modes

| Mode | Purpose | Example |
|------|---------|---------|
| **Semantic** | Encode meaning with chords (UPPERCASE) | `FIX BUG LOGIN` |
| **Text** | Normal QWERTY typing (lowercase) | `backspace key` |

Combine both: `MAKE backspace KEEP REMOVE WHEN holding`

## Hand Layout

```
LEFT HAND                    RIGHT HAND
A=pinky  S=ring  D=mid       M=thumb  J=index  K=mid
F=index  C=thumb             L=ring   ;=pinky
```

## Controls

| Chord | Action |
|-------|--------|
| **Alt+Q** | Toggle keyboard ON/OFF |
| **All 10 keys** | Send to AI (expand tokens) |
| **C+;** | Backspace (delete last token) |
| **C+M** | Enter (new line) |
| **C+J** | Search tokens popup |
| **C+L** | Select output language |
| **S+C+M** | Toggle semantic/text mode |
| **C+M+K** | Show cheatsheet |

## Installation

```bash
cd app
pip install -r requirements.txt
set GROQ_API_KEY=your_key_here
python main.py
```

Requires Python 3.10+ and a [Groq API key](https://console.groq.com/).

## Features

- ~280 semantic tokens for developer workflows
- 40+ output languages
- Live chord preview overlay
- Searchable token cheatsheet
- System tray integration

## Project Structure

```
app/
  main.py           # Entry point
  chord_engine.py   # Chord detection & vocabulary
  ai_engine.py      # Groq API integration
  keyboard_hook.py  # Global keyboard capture
  overlay.py        # Live preview
  cheatsheet.py     # Token reference
```

## License

MIT

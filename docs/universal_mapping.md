# Universal Phonemic Chord Mapping — Complete Reference

## Design Philosophy

Instead of full IPA precision per language, this system uses a **minimal universal phoneme inventory** that works across all languages with a single layout. The AI handles disambiguation of merged sound categories.

**Key principle:** Type sounds "just enough" to distinguish words statistically. Let the AI resolve ambiguity from context.

---

## Hand Layout

```
LEFT HAND (Consonant)                    RIGHT HAND (Vowel)

Thumb  = Voicing (C)                     Thumb  = Modifier (M)
Index  = Place bit 1 (F)                 Index  = Height bit 1 (J)
Middle = Place bit 2 (D)                 Middle = Height bit 2 (K)
Ring   = Manner bit 1 (S)               Ring   = Backness bit 1 (L)
Pinky  = Manner bit 2 (A)               Pinky  = Backness bit 2 (;)
```

Key bindings:
```
LEFT:  A=pinky  S=ring  D=mid  F=index  C=thumb
RIGHT: M=thumb  J=index  K=mid  L=ring  ;=pinky
```

---

## Consonant Map (Left Hand — 32 slots)

### Base Consonants (19)

| Code | Binary | Keys | Symbol | Sound | Example |
|------|--------|------|--------|-------|---------|
| 0 | 00000 | — | *(null)* | no consonant | vowel-only syllable |
| 1 | 00001 | A | f | voiceless labiodental fric | **f**an |
| 2 | 00010 | S | p | voiceless bilabial stop | **p**an |
| 4 | 00100 | D | t | voiceless alveolar stop | **t**ap |
| 5 | 00101 | D+A | s | voiceless alveolar fric | **s**un |
| 8 | 01000 | F | r | generic rhotic | **r**un |
| 9 | 01001 | F+A | ʃ | voiceless postalveolar fric | **sh**e |
| 12 | 01100 | F+D | k | voiceless velar stop | **k**ey |
| 13 | 01101 | F+D+A | h | voiceless glottal fric | **h**at |
| 16 | 10000 | C | b | voiced bilabial stop | **b**at |
| 17 | 10001 | C+A | v | voiced labiodental fric | **v**an |
| 18 | 10010 | C+S | m | voiced bilabial nasal | **m**an |
| 19 | 10011 | C+S+A | w | voiced labial-velar approx | **w**et |
| 20 | 10100 | C+D | d | voiced alveolar stop | **d**ay |
| 21 | 10101 | C+D+A | z | voiced alveolar fric | **z**oo |
| 22 | 10110 | C+D+S | n | voiced alveolar nasal | **n**et |
| 24 | 11000 | C+F | l | voiced alveolar lateral | **l**et |
| 25 | 11001 | C+F+A | ʒ | voiced postalveolar fric | vi**s**ion |
| 28 | 11100 | C+F+D | g | voiced velar stop | **g**et |
| 30 | 11110 | C+F+D+S | ŋ | voiced velar nasal | si**ng** |
| 31 | 11111 | C+F+D+S+A | j | voiced palatal approx | **y**es |

### Consonant Chunks (12)

| Code | Binary | Keys | Symbol | Type | Example |
|------|--------|------|--------|------|---------|
| 3 | 00011 | S+A | st | cluster | **st**op |
| 6 | 00110 | D+S | θ | th (voiceless) | **th**ink |
| 7 | 00111 | D+S+A | ð | th (voiced) | **th**e |
| 10 | 01010 | F+S | nd | cluster | a**nd** |
| 11 | 01011 | F+S+A | tr | cluster | **tr**ee |
| 14 | 01110 | F+D+S | pr | cluster | **pr**o |
| 15 | 01111 | F+D+S+A | str | cluster | **str**ing |
| 23 | 10111 | C+D+S+A | dʒ | affricate | **j**udge |
| 26 | 11010 | C+F+S | nt | cluster | wa**nt** |
| 27 | 11011 | C+F+S+A | tʃ | affricate | **ch**urch |
| 29 | 11101 | C+F+D+A | sp | cluster | **sp**in |

---

## Vowel Map (Right Hand — 32 slots)

### Base Vowels (6)

| Code | Binary | Keys | Symbol | Sound | Covers (in English) |
|------|--------|------|--------|-------|---------------------|
| 0 | 00000 | — | *(null)* | no vowel | bare consonant |
| 1 | 00001 | ; | i | high front | ɪ (bit), iː (see), unstressed i |
| 2 | 00010 | L | o | mid back | ɒ (not), ɔ (more), unstressed o |
| 3 | 00011 | L+; | u | high back | ʊ (put), uː (blue) |
| 4 | 00100 | K | e | mid front | ɛ (bed), unstressed e |
| 5 | 00101 | K+; | ə | schwa | ə (about), ʌ (cup) |
| 8 | 01000 | J | a | low | æ (cat), ɑ (father) |

### Modified Vowels (5)

Pattern: M (thumb) + same keys as base vowel = long/diphthong variant.

| Code | Binary | Keys | Symbol | Pattern | AI interprets as |
|------|--------|------|--------|---------|------------------|
| 17 | 10001 | M+; | ī | M + i(;) | iː (see) or aɪ (eye) |
| 20 | 10100 | M+K | ē | M + e(K) | eɪ (day, make) |
| 24 | 11000 | M+J | ā | M + a(J) | ɑː (father, car) |
| 18 | 10010 | M+L | ō | M + o(L) | oʊ (go) or ɔː (thought) |
| 19 | 10011 | M+L+; | ū | M + u(L+;) | uː (blue, food) |

### VC Chunks (20)

Vowel + coda consonant in one right-hand chord. Saves 1 chord per use.

| Code | Binary | Keys | Chunk | Example words | Chord example |
|------|--------|------|-------|---------------|---------------|
| 6 | 00110 | K+L | at | cat, bat, hat | k+at = "cat" |
| 7 | 00111 | K+L+; | in | sin, bin, win | w+in = "win" |
| 9 | 01001 | J+; | an | can, man, ran | k+an = "can" |
| 10 | 01010 | J+L | on | con, don, upon | d+on = "done" |
| 11 | 01011 | J+L+; | it | sit, bit, hit | s+it = "sit" |
| 12 | 01100 | J+K | er | her, per, better | h+er = "her" |
| 13 | 01101 | J+K+; | or | for, nor, more | f+or = "for" |
| 14 | 01110 | J+K+L | al | shall, pal, call | —+al = "all" |
| 15 | 01111 | J+K+L+; | ing | going, running | suffix chunk |
| 16 | 10000 | M | ot | not, hot, got | n+ot = "not" |
| 21 | 10101 | M+K+; | et | set, bet, let | g+et = "get" |
| 22 | 10110 | M+K+L | ut | but, cut, hut | b+ut = "but" |
| 23 | 10111 | M+K+L+; | en | pen, ten, hen | t+en = "ten" |
| 25 | 11001 | M+J+; | un | sun, fun, run | s+un = "sun" |
| 26 | 11010 | M+J+L | ad | bad, had, sad | b+ad = "bad" |
| 27 | 11011 | M+J+L+; | is | is, his, this | ð+is = "this" |
| 28 | 11100 | M+J+K | il | fill, still, will | w+il = "will" |
| 29 | 11101 | M+J+K+; | aw | saw, law, draw | s+aw = "saw" |
| 30 | 11110 | M+J+K+L | oi | boy, toy, enjoy | b+oi = "boy" |
| 31 | 11111 | M+J+K+L+; | ow | how, now, cow | h+ow = "how" |

---

## Control Chords

| Action | Chord | Keys |
|--------|-------|------|
| Backspace | Both thumbs | C + M |
| Enter | All 10 keys | A+S+D+F+C + M+J+K+L+; |
| Send to AI | Physical spacebar | Space |

---

## Typing Examples

### "The cat sat on the mat." — 6 chords

| Chord | Left | Right | Output |
|-------|------|-------|--------|
| 1 | ð (D+S+A) | ə (K+;) | ðə |
| 2 | k (F+D) | at (K+L) | kat |
| 3 | s (D+A) | at (K+L) | sat |
| 4 | — | on (J+L) | on |
| 5 | ð (D+S+A) | ə (K+;) | ðə |
| 6 | m (C+S) | at (K+L) | mat |

Stream: `ðəkatsatonðəmat` → AI: "The cat sat on the mat."

### "Please write the answer." — 8 chords

| Chord | Left | Right | Output |
|-------|------|-------|--------|
| 1 | p (S) | i (;) | pi |
| 2 | l (C+F) | ī (M+;) | lī |
| 3 | z (C+D+A) | — | z |
| 4 | r (F) | ī (M+;) | rī |
| 5 | t (D) | — | t |
| 6 | ð (D+S+A) | ə (K+;) | ðə |
| 7 | — | an (J+;) | an |
| 8 | s (D+A) | er (J+K) | ser |

Stream: `plīzrītðəanser` → AI: "Please write the answer."

### Chunk savings vs old system

| Word | Old system | New system | Savings |
|------|-----------|------------|---------|
| for | 2 (f+ɔː, r) | 1 (f+or) | **-1** |
| her | 2 (h+ɜː, r) | 1 (h+er) | **-1** |
| or | 2 (—+ɔː, r) | 1 (—+or) | **-1** |
| will | 2 (w+ɪl) | 1 (w+il) | same* |
| thing | 3 (θ+ɪŋ) | 1 (θ+ing) | **-2** |
| running | 4+ | 2 (r+un, —+ing) | **-2+** |

*will was already 1 chord with old ɪl combo

---

## Cross-Language Usage

The layout is **universal** — the same physical chords for all languages. Only the AI output language changes (via the AI:EN/AI:PT toggle).

### Portuguese on the universal layout

| Portuguese sound | How to type | Notes |
|-----------------|-------------|-------|
| /ɾ/ (tap r) | r (F) | AI interprets from position (intervocalic) |
| /h/ (guttural r) | r (F) | AI interprets from position (initial/rr) |
| /ɲ/ (nh) | n + j (2 chords) | C+D+S then C+F+D+S+A |
| /ʎ/ (lh) | l + j (2 chords) | C+F then C+F+D+S+A |
| Nasal vowels | vowel + n/m | AI detects nasal context |
| /tʃ/ (ti) | tʃ (C+F+S+A) | Same as English "ch" |
| /dʒ/ (di) | dʒ (C+D+S+A) | Same as English "j" |

### Future languages

Any language can use this layout without remapping. The AI prompt for each language explains how to interpret the simplified phonemic stream in that language's context.

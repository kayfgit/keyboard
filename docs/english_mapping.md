# English Featural Chord Mapping — Complete Reference

## Overview

This document defines the complete chord-to-phoneme mapping for English. Each chord is a simultaneous press of multiple fingers. Left hand encodes consonants, right hand encodes vowels. One chord = one syllable.

---

## Hand Layout

```
LEFT HAND (Consonant)                    RIGHT HAND (Vowel)

Thumb  = Voicing                         Thumb  = Modifier (diphthong/long)
Index  = Place bit 1                     Index  = Height bit 1
Middle = Place bit 2                     Middle = Height bit 2
Ring   = Manner bit 1                    Ring   = Backness+Rounding bit 1
Pinky  = Manner bit 2                    Pinky  = Backness+Rounding bit 2
```

Bit notation: `0` = finger UP, `1` = finger DOWN.
Finger order (left): `[Thumb, Index, Middle, Ring, Pinky]`
Finger order (right): `[Thumb, Index, Middle, Ring, Pinky]`

---

## Left Hand — Consonant Features

### Place of Articulation (Index + Middle)

| Code | Place | Description |
|------|-------|-------------|
| `00` | **Labial** | Lips together or lip-to-teeth (p, b, f, v, m, w) |
| `01` | **Alveolar** | Tongue on ridge behind teeth (t, d, s, z, n, l, and dental θ, ð) |
| `10` | **Postalveolar** | Tongue behind the ridge (tʃ, dʒ, ʃ, ʒ, ɹ) |
| `11` | **Velar/Other** | Back of tongue to soft palate + glottal (k, g, ŋ, h, j) |

### Manner of Articulation (Ring + Pinky)

| Code | Manner | Description |
|------|--------|-------------|
| `00` | **Stop** | Complete airflow blockage, then release. Includes affricates at postalveolar. |
| `01` | **Fricative** | Narrow gap creates turbulent airflow |
| `10` | **Nasal** | Air flows through the nose |
| `11` | **Approximant** | Tongue approaches but doesn't create turbulence. Includes lateral /l/. |

### Voicing (Thumb)

| Code | Voicing | Description |
|------|---------|-------------|
| `0` | **Voiceless** | Vocal cords not vibrating |
| `1` | **Voiced** | Vocal cords vibrating |

---

## Complete Consonant Table

### Grid View (Place x Manner x Voicing)

```
              STOP          FRICATIVE       NASAL         APPROXIMANT
            VL    V       VL     V       VL*    V       VL*    V
          ┌─────┬─────┬──────┬──────┬──────┬─────┬──────┬─────┐
Labial    │  p  │  b  │  f   │  v   │  —   │  m  │  —   │  w  │
  (00)    │     │     │      │      │      │     │      │     │
          ├─────┼─────┼──────┼──────┼──────┼─────┼──────┼─────┤
Alveolar  │  t  │  d  │  s   │  z   │  θ*  │  n  │  ð*  │  l  │
  (01)    │     │     │      │      │      │     │      │     │
          ├─────┼─────┼──────┼──────┼──────┼─────┼──────┼─────┤
Postalv   │  tʃ │  dʒ │  ʃ   │  ʒ   │  —   │  —  │  —   │  ɹ  │
  (10)    │     │     │      │      │      │     │      │     │
          ├─────┼─────┼──────┼──────┼──────┼─────┼──────┼─────┤
Velar     │  k  │  g  │  h   │  —   │  —   │  ŋ  │  —   │  j  │
  (11)    │     │     │      │      │      │     │      │     │
          └─────┴─────┴──────┴──────┴──────┴─────┴──────┴─────┘

* VL Nasal and VL Approximant don't exist in English.
  θ and ð are placed in these unused slots.
```

### Every Consonant with 5-Bit Code

Format: `[Thumb, Index, Middle, Ring, Pinky]`

| # | Sound | IPA | Example | Place | Manner | Voice | Code | Fingers Down |
|---|-------|-----|---------|-------|--------|-------|------|-------------|
| 1 | p | /p/ | **p**at | Labial | Stop | VL | `00000` | (none — all up!) |
| 2 | b | /b/ | **b**at | Labial | Stop | V | `10000` | Thumb |
| 3 | t | /t/ | **t**ap | Alveolar | Stop | VL | `00100` | Index |
| 4 | d | /d/ | **d**og | Alveolar | Stop | V | `10100` | Thumb+Index |
| 5 | k | /k/ | **c**at | Velar | Stop | VL | `00110` | Index+Middle |
| 6 | g | /g/ | **g**o | Velar | Stop | V | `10110` | Thumb+Index+Middle |
| 7 | tʃ | /tʃ/ | **ch**ip | Postalv | Stop | VL | `00010` | Middle |
| 8 | dʒ | /dʒ/ | **j**am | Postalv | Stop | V | `10010` | Thumb+Middle |
| 9 | f | /f/ | **f**an | Labial | Fric | VL | `00001` | Pinky |
| 10 | v | /v/ | **v**an | Labial | Fric | V | `10001` | Thumb+Pinky |
| 11 | θ | /θ/ | **th**ink | Alveolar | *VL Nasal | VL | `00111` | Index+Middle+Pinky |
| 12 | ð | /ð/ | **th**is | Alveolar | *VL Appr | VL | `00101` | Index+Pinky |
| 13 | s | /s/ | **s**it | Alveolar | Fric | VL | `00101` | Index+Pinky |

Wait — collision between ð and s! Let me recalculate.

**Recalculation:**

The code is: `[Thumb, Index, Middle, Ring, Pinky]`
- Thumb = Voicing
- Index = Place bit 1 (HIGH bit)
- Middle = Place bit 2 (LOW bit)
- Ring = Manner bit 1 (HIGH bit)
- Pinky = Manner bit 2 (LOW bit)

Place encoding:
- Labial = `00` → Index=0, Middle=0
- Alveolar = `01` → Index=0, Middle=1
- Postalveolar = `10` → Index=1, Middle=0
- Velar = `11` → Index=1, Middle=1

Manner encoding:
- Stop = `00` → Ring=0, Pinky=0
- Fricative = `01` → Ring=0, Pinky=1
- Nasal = `10` → Ring=1, Pinky=0
- Approximant = `11` → Ring=1, Pinky=1

Now recalculating all codes:

| # | Sound | IPA | Example | Place | Manner | Voice | Thumb | Index | Middle | Ring | Pinky | Code |
|---|-------|-----|---------|-------|--------|-------|-------|-------|--------|------|-------|------|
| 1 | p | /p/ | **p**at | Lab 00 | Stop 00 | VL 0 | 0 | 0 | 0 | 0 | 0 | `00000` |
| 2 | b | /b/ | **b**at | Lab 00 | Stop 00 | V 1 | 1 | 0 | 0 | 0 | 0 | `10000` |
| 3 | f | /f/ | **f**an | Lab 00 | Fric 01 | VL 0 | 0 | 0 | 0 | 0 | 1 | `00001` |
| 4 | v | /v/ | **v**an | Lab 00 | Fric 01 | V 1 | 1 | 0 | 0 | 0 | 1 | `10001` |
| 5 | m | /m/ | **m**an | Lab 00 | Nas 10 | V 1 | 1 | 0 | 0 | 1 | 0 | `10010` |
| 6 | w | /w/ | **w**et | Lab 00 | App 11 | V 1 | 1 | 0 | 0 | 1 | 1 | `10011` |
| 7 | t | /t/ | **t**ap | Alv 01 | Stop 00 | VL 0 | 0 | 0 | 1 | 0 | 0 | `00100` |
| 8 | d | /d/ | **d**og | Alv 01 | Stop 00 | V 1 | 1 | 0 | 1 | 0 | 0 | `10100` |
| 9 | s | /s/ | **s**it | Alv 01 | Fric 01 | VL 0 | 0 | 0 | 1 | 0 | 1 | `00101` |
| 10 | z | /z/ | **z**oo | Alv 01 | Fric 01 | V 1 | 1 | 0 | 1 | 0 | 1 | `10101` |
| 11 | θ | /θ/ | **th**ink | Alv 01 | Nas 10 | VL 0 | 0 | 0 | 1 | 1 | 0 | `00110` |
| 12 | n | /n/ | **n**ot | Alv 01 | Nas 10 | V 1 | 1 | 0 | 1 | 1 | 0 | `10110` |
| 13 | ð | /ð/ | **th**is | Alv 01 | App 11 | VL 0 | 0 | 0 | 1 | 1 | 1 | `00111` |
| 14 | l | /l/ | **l**eg | Alv 01 | App 11 | V 1 | 1 | 0 | 1 | 1 | 1 | `10111` |
| 15 | tʃ | /tʃ/ | **ch**ip | Post 10 | Stop 00 | VL 0 | 0 | 1 | 0 | 0 | 0 | `01000` |
| 16 | dʒ | /dʒ/ | **j**am | Post 10 | Stop 00 | V 1 | 1 | 1 | 0 | 0 | 0 | `11000` |
| 17 | ʃ | /ʃ/ | **sh**ip | Post 10 | Fric 01 | VL 0 | 0 | 1 | 0 | 0 | 1 | `01001` |
| 18 | ʒ | /ʒ/ | vi**s**ion | Post 10 | Fric 01 | V 1 | 1 | 1 | 0 | 0 | 1 | `11001` |
| 19 | ɹ | /ɹ/ | **r**ed | Post 10 | App 11 | V 1 | 1 | 1 | 0 | 1 | 1 | `11011` |
| 20 | k | /k/ | **c**at | Vel 11 | Stop 00 | VL 0 | 0 | 1 | 1 | 0 | 0 | `01100` |
| 21 | g | /g/ | **g**o | Vel 11 | Stop 00 | V 1 | 1 | 1 | 1 | 0 | 0 | `11100` |
| 22 | h | /h/ | **h**at | Vel 11 | Fric 01 | VL 0 | 0 | 1 | 1 | 0 | 1 | `01101` |
| 23 | ŋ | /ŋ/ | si**ng** | Vel 11 | Nas 10 | V 1 | 1 | 1 | 1 | 1 | 0 | `11110` |
| 24 | j | /j/ | **y**es | Vel 11 | App 11 | V 1 | 1 | 1 | 1 | 1 | 1 | `11111` |

### Collision Check

All 24 codes are unique. Additionally:
- `00000` (all fingers up) with no right hand = no output (rest position)
- `00000` with right hand = bare /p/ + vowel (but /p/ with no fingers is weird...)

**Important note:** Code `00000` (no fingers pressed) maps to /p/. This means "no left hand input" and "the consonant /p/" are the same chord. We need to distinguish "no consonant" (vowel-only syllable) from /p/.

**Solution:** Reserve `00000` as "no consonant." Reassign /p/ to an unused slot.

Available unused slots (voiceless combinations that are empty):
- `00010` → Labial VL Nasal (doesn't exist) — currently unused
- `00011` → Labial VL Approximant (doesn't exist) — currently unused
- `01010` → Postalveolar VL Nasal — currently unused
- `01011` → Postalveolar VL Approximant — currently unused
- `01110` → Velar VL Nasal — currently unused
- `01111` → Velar VL Approximant — currently unused

**Reassignment:** /p/ moves to `00010` (Labial VL Nasal slot — Ring finger only).

### Revised Consonant Codes (Final)

| # | Sound | IPA | Example | Code | Fingers Down |
|---|-------|-----|---------|------|-------------|
| — | *(none)* | — | vowel-only syllable | `00000` | *(no left hand)* |
| 1 | p | /p/ | **p**at | `00010` | Ring |
| 2 | b | /b/ | **b**at | `10000` | Thumb |
| 3 | f | /f/ | **f**an | `00001` | Pinky |
| 4 | v | /v/ | **v**an | `10001` | Thumb+Pinky |
| 5 | m | /m/ | **m**an | `10010` | Thumb+Ring |
| 6 | w | /w/ | **w**et | `10011` | Thumb+Ring+Pinky |
| 7 | t | /t/ | **t**ap | `00100` | Middle |
| 8 | d | /d/ | **d**og | `10100` | Thumb+Middle |
| 9 | s | /s/ | **s**it | `00101` | Middle+Pinky |
| 10 | z | /z/ | **z**oo | `10101` | Thumb+Middle+Pinky |
| 11 | θ | /θ/ | **th**ink | `00110` | Middle+Ring |
| 12 | n | /n/ | **n**ot | `10110` | Thumb+Middle+Ring |
| 13 | ð | /ð/ | **th**is | `00111` | Middle+Ring+Pinky |
| 14 | l | /l/ | **l**eg | `10111` | Thumb+Middle+Ring+Pinky |
| 15 | tʃ | /tʃ/ | **ch**ip | `01000` | Index |
| 16 | dʒ | /dʒ/ | **j**am | `11000` | Thumb+Index |
| 17 | ʃ | /ʃ/ | **sh**ip | `01001` | Index+Pinky |
| 18 | ʒ | /ʒ/ | vi**s**ion | `11001` | Thumb+Index+Pinky |
| 19 | ɹ | /ɹ/ | **r**ed | `11011` | Thumb+Index+Ring+Pinky |
| 20 | k | /k/ | **c**at | `01100` | Index+Middle |
| 21 | g | /g/ | **g**o | `11100` | Thumb+Index+Middle |
| 22 | h | /h/ | **h**at | `01101` | Index+Middle+Pinky |
| 23 | ŋ | /ŋ/ | si**ng** | `11110` | Thumb+Index+Middle+Ring |
| 24 | j | /j/ | **y**es | `11111` | All five |

**Unused consonant slots (8 available for clusters or other languages):**
`00000` = no consonant, `00011`, `01010`, `01011`, `01110`, `01111`, `10011` is w... let me recount.

Slots used: 00010, 10000, 00001, 10001, 10010, 10011, 00100, 10100, 00101, 10101, 00110, 10110, 00111, 10111, 01000, 11000, 01001, 11001, 11011, 01100, 11100, 01101, 11110, 11111
That's 24 slots + 00000 (no consonant) = 25 used.
Total slots = 32.
**7 unused slots:** `00011`, `01010`, `01011`, `01110`, `01111`, `10011`... wait, 10011 is w. Let me list all 32 and check:

```
00000 = (none)      10000 = b
00001 = f           10001 = v
00010 = p           10010 = m
00011 = (free)      10011 = w
00100 = t           10100 = d
00101 = s           10101 = z
00110 = θ           10110 = n
00111 = ð           10111 = l
01000 = tʃ          11000 = dʒ
01001 = ʃ           11001 = ʒ
01010 = (free)      11010 = (free)
01011 = (free)      11011 = ɹ
01100 = k           11100 = g
01101 = h           11101 = (free)
01110 = (free)      11110 = ŋ
01111 = (free)      11111 = j
```

**7 free slots:** `00011`, `01010`, `01011`, `01110`, `01111`, `11010`, `11101`

These can be used for:
- Common consonant clusters (st, tr, pr, etc.)
- Sounds from other languages
- Control chords (space, backspace, etc.)

---

## Right Hand — Vowel Features

### Height (Index + Middle)

| Code | Height | Sounds |
|------|--------|--------|
| `00` | **Close** | iː, uː |
| `01` | **Near-close / Mid** | ɪ, ʊ, ə |
| `10` | **Open-mid** | ɛ, ɔː, ʌ, ɜː |
| `11` | **Open** | æ, ɑː, ɒ |

### Backness + Rounding (Ring + Pinky)

| Code | Position | Rationale |
|------|----------|-----------|
| `00` | **Front unrounded** | All English front vowels are unrounded |
| `01` | **Central** | ə, ʌ, ɜː |
| `10` | **Back unrounded** | ɑː |
| `11` | **Back rounded** | uː, ʊ, ɔː, ɒ |

### Modifier (Thumb)

| Code | Mode |
|------|------|
| `0` | **Monophthong** (simple vowel) |
| `1` | **Diphthong / Long** (gliding vowel or length variant) |

---

## Complete Vowel Table

### Monophthongs (Thumb = 0)

| # | Sound | IPA | Example | Height | Back+Rnd | Code | Fingers Down |
|---|-------|-----|---------|--------|----------|------|-------------|
| 1 | iː | /iː/ | s**ee** | Close 00 | Front 00 | `00000` | *(none)* |
| 2 | uː | /uː/ | g**oo**se | Close 00 | Back-R 11 | `00011` | Ring+Pinky |
| 3 | ɪ | /ɪ/ | s**i**t | Near 01 | Front 00 | `00100` | Middle |
| 4 | ə | /ə/ | **a**bout | Near 01 | Central 01 | `00101` | Middle+Pinky |
| 5 | ʊ | /ʊ/ | p**u**t | Near 01 | Back-R 11 | `00111` | Middle+Ring+Pinky |
| 6 | ɛ | /ɛ/ | b**e**d | Open-m 10 | Front 00 | `01000` | Index |
| 7 | ʌ | /ʌ/ | c**u**p | Open-m 10 | Central 01 | `01001` | Index+Pinky |
| 8 | ɔː | /ɔː/ | th**ough**t | Open-m 10 | Back-R 11 | `01011` | Index+Ring+Pinky |
| 9 | æ | /æ/ | c**a**t | Open 11 | Front 00 | `01100` | Index+Middle |
| 10 | ɑː | /ɑː/ | f**a**ther | Open 11 | Back-U 10 | `01110` | Index+Middle+Ring |
| 11 | ɒ | /ɒ/ | l**o**t (BrE) | Open 11 | Back-R 11 | `01111` | Index+Middle+Ring+Pinky |

### Diphthongs & Long Vowels (Thumb = 1)

| # | Sound | IPA | Example | Height | Back+Rnd | Code | Fingers Down |
|---|-------|-----|---------|--------|----------|------|-------------|
| 12 | eɪ | /eɪ/ | d**ay** | Open-m 10 | Front 00 | `11000` | Thumb+Index |
| 13 | ɜː | /ɜː/ | n**ur**se | Open-m 10 | Central 01 | `11001` | Thumb+Index+Pinky |
| 14 | ɔɪ | /ɔɪ/ | b**oy** | Open-m 10 | Back-R 11 | `11011` | Thumb+Index+Ring+Pinky |
| 15 | aɪ | /aɪ/ | m**y** | Open 11 | Front 00 | `11100` | Thumb+Index+Middle |
| 16 | aʊ | /aʊ/ | n**ow** | Open 11 | Back-U 10 | `11110` | Thumb+Index+Middle+Ring |
| 17 | oʊ | /oʊ/ | g**o** | Open 11 | Back-R 11 | `11111` | All five |

### Special Vowel Codes

| Code | Meaning | When |
|------|---------|------|
| `00000` | /iː/ (close front) | Right hand no-mod, no fingers = iː |
| Right hand all up, no chord | **No vowel** | Bare consonant (syllable coda) |

**Note:** Similar to the consonant /p/ problem, `00000` on the right hand maps to /iː/. To distinguish "no vowel" (bare consonant) from /iː/, we detect whether ANY right-hand finger moved during the chord window. If no right-hand activity at all → no vowel. If all right-hand fingers stayed up but a chord was registered → /iː/.

Alternatively, reassign /iː/ to avoid this ambiguity:
- Move /iː/ to `00001` (Pinky only) → Close + Central? Not ideal phonetically.
- Better: "no vowel" = no right hand activity detected by hardware. /iː/ = deliberate "all up" press within the chord window. The hardware/software can distinguish these.

### Vowel Slot Map

```
       Front(00)  Central(01)  Back-U(10)  Back-R(11)
Close   iː(00000)  —(00001)    —(00010)    uː(00011)
  (00)

Near    ɪ(00100)   ə(00101)    —(00110)    ʊ(00111)
  (01)

Open-m  ɛ(01000)   ʌ(01001)    —(01010)    ɔː(01011)
  (10)

Open    æ(01100)   —(01101)    ɑː(01110)   ɒ(01111)
  (11)

--- WITH THUMB (diphthong/long) ---

Close   ʌt(10000)  ɛt(10001)   æn(10010)   ɪl(10011)
  (00)  CVC        CVC         CVC         CVC

Near    ɪz(10100)  ɪs(10101)   ɒn(10110)   ʌn(10111)
  (01)  CVC        CVC         CVC         CVC

Open-m  eɪ(11000)  ɜː(11001)   ɔːl(11010)  ɔɪ(11011)
  (10)                         CVC

Open    aɪ(11100)  æd(11101)   aʊ(11110)   oʊ(11111)
  (11)             CVC
```

**CVC combos (14 slots):** All 14 previously free vowel slots now encode vowel+coda pairs for common English syllable endings. These allow full CVC syllables in a single chord.

---

## Typing Examples — Common English Words

### Simple Words

**"see" /siː/** — 1 chord
```
Chord 1: LEFT s(00101) + RIGHT iː(00000)
Left:  ·  ·  M  ·  P     (middle + pinky)
Right: ·  ·  ·  ·  ·     (no fingers / all up)
```

**"go" /goʊ/** — 1 chord
```
Chord 1: LEFT g(11100) + RIGHT oʊ(11111)
Left:  T  I  M  ·  ·     (thumb + index + middle)
Right: T  I  M  R  P     (all five)
```

**"me" /miː/** — 1 chord
```
Chord 1: LEFT m(10010) + RIGHT iː(00000)
Left:  T  ·  ·  R  ·     (thumb + ring)
Right: ·  ·  ·  ·  ·     (no fingers)
```

**"day" /deɪ/** — 1 chord
```
Chord 1: LEFT d(10100) + RIGHT eɪ(11000)
Left:  T  ·  M  ·  ·     (thumb + middle)
Right: T  I  ·  ·  ·     (thumb + index)
```

### CVC Words — Now Single Chord!

**"cat" /kæt/** — 1 chord (was 2)
```
Chord 1: LEFT k(01100) + RIGHT æt(00010)
Left:  ·  I  M  ·  ·     (index + middle)
Right: ·  ·  ·  R  ·     (ring only)
```

**"not" /nɒt/** — 1 chord (was 2)
```
Chord 1: LEFT n(10110) + RIGHT ɒt(01101)
Left:  T  ·  M  R  ·     (thumb + middle + ring)
Right: ·  ·  M  ·  P     (middle + pinky) — wait, code 01101 = K+M+;
```

**"this" /ðɪs/** — 1 chord (was 2)
```
Chord 1: LEFT ð(00111) + RIGHT ɪs(10101)
Left:  ·  ·  M  R  P     (middle + ring + pinky)
Right: T  ·  M  ·  P     (thumb + middle + pinky)
```

### Two-Chord Words (CV + C or CVC + coda)

**"dog" /dɒg/** — 2 chords (no CVC combo for ɒg)
```
Chord 1: LEFT d(10100) + RIGHT ɒ(01111)
Left:  T  ·  M  ·  ·     (thumb + middle)
Right: ·  I  M  R  P     (index + middle + ring + pinky)

Chord 2: LEFT g(11100) + RIGHT (none)
Left:  T  I  M  ·  ·     (thumb + index + middle)
Right: —                   (no right hand)
```

**"the" /ðə/** — 1 chord (no coda needed)
```
Chord 1: LEFT ð(00111) + RIGHT ə(00101)
Left:  ·  ·  M  R  P     (middle + ring + pinky)
Right: ·  ·  M  ·  P     (middle + pinky)
```

### Three-Chord Words (CVC + CV + C or similar)

**"hello" /hɛloʊ/** — 3 chords
```
Chord 1: LEFT h(01101) + RIGHT ɛ(01000)
Left:  ·  I  M  ·  P     (index + middle + pinky)
Right: ·  I  ·  ·  ·     (index only)

Chord 2: LEFT l(10111) + RIGHT oʊ(11111)
Left:  T  ·  M  R  P     (thumb + middle + ring + pinky)
Right: T  I  M  R  P     (all five)
```

**"water" /wɔːtəɹ/** — 3 chords
```
Chord 1: LEFT w(10011) + RIGHT ɔː(01011)
Left:  T  ·  ·  R  P     (thumb + ring + pinky)
Right: ·  I  ·  R  P     (index + ring + pinky)

Chord 2: LEFT t(00100) + RIGHT ə(00101)
Left:  ·  ·  M  ·  ·     (middle only)
Right: ·  ·  M  ·  P     (middle + pinky)

Chord 3: LEFT ɹ(11011) + RIGHT (none)
Left:  T  I  ·  R  P     (thumb + index + ring + pinky)
Right: —                   (no right hand)
```

**"think" /θɪŋk/** — 3 chords
```
Chord 1: LEFT θ(00110) + RIGHT ɪ(00100)
Left:  ·  ·  M  R  ·     (middle + ring)
Right: ·  ·  M  ·  ·     (middle only)

Chord 2: LEFT ŋ(11110) + RIGHT (none)
Left:  T  I  M  R  ·     (thumb + index + middle + ring)
Right: —

Chord 3: LEFT k(01100) + RIGHT (none)
Left:  ·  I  M  ·  ·     (index + middle)
Right: —
```

### Vowel-Only Syllables

**"a" /ə/** (the article) — 1 chord
```
Chord 1: LEFT (none)(00000) + RIGHT ə(00101)
Left:  ·  ·  ·  ·  ·     (no left hand)
Right: ·  ·  M  ·  P     (middle + pinky)
```

**"I" /aɪ/** — 1 chord
```
Chord 1: LEFT (none)(00000) + RIGHT aɪ(11100)
Left:  ·  ·  ·  ·  ·     (no left hand)
Right: T  I  M  ·  ·     (thumb + index + middle)
```

---

## Chord Count Comparison: 20 Common English Words

| Word | Pronunciation | Before CVC | With CVC | QWERTY keys |
|------|--------------|------------|----------|-------------|
| the | /ðə/ | **1** | **1** | 3 |
| of | /ɒv/ or /əv/ | 2 | 2 | 2 |
| and | /ænd/ | 3 | 3 | 3 |
| a | /ə/ | **1** | **1** | 1 |
| to | /tuː/ | **1** | **1** | 2 |
| in | /ɪn/ | 2 | **1** (ɪn) | 2 |
| is | /ɪz/ | 2 | **1** (ɪz) | 2 |
| you | /juː/ | **1** | **1** | 3 |
| that | /ðæt/ | 2 | **1** (æt) | 4 |
| it | /ɪt/ | 2 | **1** (ɪt) | 2 |
| he | /hiː/ | **1** | **1** | 2 |
| was | /wɒz/ | 2 | 2 | 3 |
| for | /fɔːɹ/ | 2 | 2 | 3 |
| on | /ɒn/ | 2 | **1** (ɒn) | 2 |
| are | /ɑːɹ/ | 2 | 2 | 3 |
| but | /bʌt/ | 2 | **1** (ʌt) | 3 |
| not | /nɒt/ | 2 | **1** (ɒt) | 3 |
| she | /ʃiː/ | **1** | **1** | 3 |
| my | /maɪ/ | **1** | **1** | 2 |
| say | /seɪ/ | **1** | **1** | 3 |
| **Avg** | | **1.65** | **1.25** | **2.55** |

With CVC combos, this system averages **51% fewer actions** than QWERTY (up from 35%). Stenography would still average ~1.0 chords for these words.

---

## Design Gaps & Open Questions

### 1. Consonant Clusters
Words like "string" /stɹɪŋ/ start with 3 consonants. Current approach: 3 separate left-hand chords before the vowel. The 7 free consonant slots could map common clusters:
- `00011` → /st/ (very common)
- `01010` → /tɹ/
- `01011` → /pɹ/
- etc.

### 2. Numbers & Punctuation
Need a "symbol mode" toggle chord. Proposed: a specific left+right hand chord enters symbol mode, where the next chord maps to symbols instead of phonemes. Another chord exits symbol mode.

### 3. Space, Backspace, Enter
Options:
- **Space** = both hands release simultaneously (end of word boundary)
- **Backspace** = a reserved chord (e.g., left thumb only with specific right hand combo)
- **Enter** = another reserved chord

### 4. Word Boundaries
The AI engine needs to know when a word ends. Options:
- A brief pause between words (timing-based)
- An explicit "space" chord
- Both (pause inserts space, chord forces it)

### 5. Disambiguation
When the AI converts phonemes to text incorrectly:
- A "next candidate" chord cycles through alternatives
- A "spell mode" chord switches to letter-by-letter input
- A personal dictionary learns user corrections

### 6. Capital Letters / Shift
A "capitalize next" chord before a word start. Could use one of the free consonant slots.

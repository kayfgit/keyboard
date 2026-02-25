# Feature Analysis — Ergonomics & Frequency Validation

This document verifies that the chord mapping from `english_mapping.md` assigns easy chords to common sounds and hard chords to rare sounds.

---

## English Phoneme Frequency

Source: phoneme frequencies in General American English, based on the CMU Pronouncing Dictionary and spoken corpus data.

### Consonant Frequency (ranked most → least common)

| Rank | Sound | IPA | Frequency % | Chord Code | Fingers Down | Finger Count |
|------|-------|-----|------------|------------|-------------|-------------|
| 1 | n | /n/ | 7.11% | `10110` | T+M+R | 3 |
| 2 | t | /t/ | 6.95% | `00100` | M | **1** |
| 3 | s | /s/ | 4.55% | `00101` | M+P | 2 |
| 4 | ɹ | /ɹ/ | 4.33% | `11011` | T+I+R+P | 4 |
| 5 | l | /l/ | 3.67% | `10111` | T+M+R+P | 4 |
| 6 | d | /d/ | 3.60% | `10100` | T+M | 2 |
| 7 | k | /k/ | 3.20% | `01100` | I+M | 2 |
| 8 | ð | /ð/ | 2.95% | `00111` | M+R+P | 3 |
| 9 | m | /m/ | 2.78% | `10010` | T+R | 2 |
| 10 | z | /z/ | 2.76% | `10101` | T+M+P | 3 |
| 11 | p | /p/ | 2.05% | `00010` | R | **1** |
| 12 | w | /w/ | 1.95% | `10011` | T+R+P | 3 |
| 13 | b | /b/ | 1.81% | `10000` | T | **1** |
| 14 | f | /f/ | 1.81% | `00001` | P | **1** |
| 15 | v | /v/ | 1.57% | `10001` | T+P | 2 |
| 16 | h | /h/ | 1.52% | `01101` | I+M+P | 3 |
| 17 | g | /g/ | 1.25% | `11100` | T+I+M | 3 |
| 18 | ŋ | /ŋ/ | 1.18% | `11110` | T+I+M+R | 4 |
| 19 | ʃ | /ʃ/ | 0.96% | `01001` | I+P | 2 |
| 20 | tʃ | /tʃ/ | 0.52% | `01000` | I | **1** |
| 21 | dʒ | /dʒ/ | 0.44% | `11000` | T+I | 2 |
| 22 | j | /j/ | 0.41% | `11111` | All 5 | 5 |
| 23 | θ | /θ/ | 0.37% | `00110` | M+R | 2 |
| 24 | ʒ | /ʒ/ | 0.07% | `11001` | T+I+P | 3 |

### Vowel Frequency (ranked most → least common)

| Rank | Sound | IPA | Frequency % | Chord Code | Fingers Down | Finger Count |
|------|-------|-----|------------|------------|-------------|-------------|
| 1 | ə | /ə/ | 11.49% | `00101` | M+P | 2 |
| 2 | ɪ | /ɪ/ | 6.56% | `00100` | M | **1** |
| 3 | iː | /iː/ | 3.61% | `00000` | **0** (all up) | **0** |
| 4 | ɛ | /ɛ/ | 2.81% | `01000` | I | **1** |
| 5 | æ | /æ/ | 2.61% | `01100` | I+M | 2 |
| 6 | eɪ | /eɪ/ | 2.14% | `11000` | T+I | 2 |
| 7 | ʌ | /ʌ/ | 1.83% | `01001` | I+P | 2 |
| 8 | aɪ | /aɪ/ | 1.74% | `11100` | T+I+M | 3 |
| 9 | oʊ | /oʊ/ | 1.51% | `11111` | All 5 | 5 |
| 10 | ɑː | /ɑː/ | 1.45% | `01110` | I+M+R | 3 |
| 11 | uː | /uː/ | 1.25% | `00011` | R+P | 2 |
| 12 | ɔː | /ɔː/ | 0.94% | `01011` | I+R+P | 3 |
| 13 | ʊ | /ʊ/ | 0.86% | `00111` | M+R+P | 3 |
| 14 | aʊ | /aʊ/ | 0.51% | `11110` | T+I+M+R | 4 |
| 15 | ɜː | /ɜː/ | 0.45% | `11001` | T+I+P | 3 |
| 16 | ɔɪ | /ɔɪ/ | 0.16% | `11011` | T+I+R+P | 4 |
| 17 | ɒ | /ɒ/ | varies (BrE) | `01111` | I+M+R+P | 4 |

---

## Ergonomic Assessment

### Finger Count Distribution

| Fingers | Difficulty | Consonants in that tier | Vowels in that tier |
|---------|-----------|------------------------|---------------------|
| 0 | Trivial | — | iː (3rd most common) |
| 1 | Easy | t (#2), p (#11), b (#13), f (#14), tʃ (#20) | ɪ (#2), ɛ (#4) |
| 2 | Moderate | s (#3), d (#6), k (#7), m (#9), v (#15), ʃ (#19), dʒ (#21), θ (#23) | ə (#1), æ (#5), eɪ (#6), ʌ (#7), uː (#11) |
| 3 | Hard | n (#1!), ð (#8), z (#10), w (#12), h (#16), g (#17), ʒ (#24) | aɪ (#8), ɑː (#10), ɔː (#12), ʊ (#13), ɜː (#15) |
| 4 | Very hard | ɹ (#4!), l (#5!), ŋ (#18) | aʊ (#14), ɔɪ (#16), ɒ (#17) |
| 5 | Extreme | j (#22) | oʊ (#9!) |

### Problem Spots (high frequency + high finger count)

| Sound | Frequency Rank | Finger Count | Severity |
|-------|---------------|-------------|----------|
| /n/ | #1 consonant | 3 fingers | **MODERATE** — very frequent, 3 fingers is manageable |
| /ɹ/ | #4 consonant | 4 fingers | **HIGH** — common sound, 4 fingers is fatiguing |
| /l/ | #5 consonant | 4 fingers | **HIGH** — common sound, 4 fingers is fatiguing |
| /oʊ/ | #9 vowel | 5 fingers | **MODERATE** — less frequent, but all 5 fingers |

### Good Spots (high frequency + low finger count)

| Sound | Frequency Rank | Finger Count | Assessment |
|-------|---------------|-------------|------------|
| /t/ | #2 consonant | 1 finger | Excellent |
| /ə/ | #1 vowel | 2 fingers | Good |
| /ɪ/ | #2 vowel | 1 finger | Excellent |
| /iː/ | #3 vowel | 0 fingers | Perfect |
| /ɛ/ | #4 vowel | 1 finger | Excellent |
| /b/ | #13 consonant | 1 finger | Good (though b is only moderately common) |
| /f/ | #14 consonant | 1 finger | Good |
| /p/ | #11 consonant | 1 finger | Good |

### Recommended Fixes for Problem Spots

**Issue: /ɹ/ and /l/ require 4 fingers each**

These are the 4th and 5th most common consonants. Having them at 4-finger chords will cause fatigue in fast typing.

**Possible fix:** Swap /ɹ/ and /l/ with less common sounds that currently have easy chords.

- /tʃ/ (rank #20, 0.52%) currently uses 1 finger (`01000`, Index only)
- /ɹ/ (rank #4, 4.33%) currently uses 4 fingers (`11011`)

Swap these:
- /ɹ/ → `01000` (Index only) — now 1 finger for the 4th most common consonant
- /tʃ/ → `11011` (T+I+R+P) — 4 fingers but very rare

Similarly for /l/:
- /b/ (rank #13, 1.81%) currently uses 1 finger (`10000`, Thumb only)
- /l/ (rank #5, 3.67%) currently uses 4 fingers (`10111`)

But /b/ is still moderately common. Better candidate:
- /dʒ/ (rank #21, 0.44%) currently uses 2 fingers (`11000`, T+I)
- Swap /l/ into a 2-finger slot and /dʒ/ into the 4-finger slot.

**After optimization, proposed swaps:**

| Sound | Old Code | New Code | Old Fingers | New Fingers | Freq Rank |
|-------|----------|----------|-------------|-------------|-----------|
| ɹ | `11011` | `01000` | 4 (T+I+R+P) | 1 (I) | #4 |
| tʃ | `01000` | `11011` | 1 (I) | 4 (T+I+R+P) | #20 |
| l | `10111` | `11000` | 4 (T+M+R+P) | 2 (T+I) | #5 |
| dʒ | `11000` | `10111` | 2 (T+I) | 4 (T+M+R+P) | #21 |

**Trade-off:** These swaps break the pure featural logic. /ɹ/ is no longer at Postalveolar+Approximant+Voiced; it's at Postalveolar+Stop+Voiceless — which makes no phonetic sense. But it's ergonomically much better.

**Recommendation:** Offer two modes:
1. **Featural mode** (default for learning) — pure phonetic logic, helps build understanding
2. **Optimized mode** (for speed) — frequency-optimized swaps, better ergonomics

---

## Chords-Per-Word Comparison

### Methodology
- **This system:** Count CV chords + bare consonant chords per word
- **QWERTY:** Count individual key presses per word
- **Stenography:** Approximate stroke count from Plover steno dictionary

### 50-Word Sample (most common English words)

CVC column shows chord count with CVC combos (vowel+coda shortcuts).

| Word | IPA | Before CVC | With CVC | QWERTY | Steno (approx) |
|------|-----|------------|----------|--------|----------------|
| the | /ðə/ | 1 | 1 | 3 | 1 |
| be | /biː/ | 1 | 1 | 2 | 1 |
| to | /tuː/ | 1 | 1 | 2 | 1 |
| of | /ɒv/ | 2 | 2 | 2 | 1 |
| and | /ænd/ | 3 | 3 | 3 | 1 |
| a | /ə/ | 1 | 1 | 1 | 1 |
| in | /ɪn/ | 2 | **1** ɪn | 2 | 1 |
| that | /ðæt/ | 2 | **1** æt | 4 | 1 |
| have | /hæv/ | 2 | 2 | 4 | 1 |
| I | /aɪ/ | 1 | 1 | 1 | 1 |
| it | /ɪt/ | 2 | **1** ɪt | 2 | 1 |
| for | /fɔːɹ/ | 2 | 2 | 3 | 1 |
| not | /nɒt/ | 2 | **1** ɒt | 3 | 1 |
| on | /ɒn/ | 2 | **1** ɒn | 2 | 1 |
| with | /wɪθ/ | 2 | 2 | 4 | 1 |
| he | /hiː/ | 1 | 1 | 2 | 1 |
| as | /æz/ | 2 | 2 | 2 | 1 |
| you | /juː/ | 1 | 1 | 3 | 1 |
| do | /duː/ | 1 | 1 | 2 | 1 |
| at | /æt/ | 2 | **1** æt | 2 | 1 |
| this | /ðɪs/ | 2 | **1** ɪs | 4 | 1 |
| but | /bʌt/ | 2 | **1** ʌt | 3 | 1 |
| his | /hɪz/ | 2 | **1** ɪz | 3 | 1 |
| by | /baɪ/ | 1 | 1 | 2 | 1 |
| from | /fɹɒm/ | 3 | 3 | 4 | 1 |
| say | /seɪ/ | 1 | 1 | 3 | 1 |
| she | /ʃiː/ | 1 | 1 | 3 | 1 |
| or | /ɔːɹ/ | 2 | 2 | 2 | 1 |
| an | /æn/ | 2 | **1** æn | 2 | 1 |
| will | /wɪl/ | 2 | **1** ɪl | 4 | 1 |
| my | /maɪ/ | 1 | 1 | 2 | 1 |
| one | /wʌn/ | 2 | **1** ʌn | 3 | 1 |
| all | /ɔːl/ | 2 | **1** ɔːl | 3 | 1 |
| would | /wʊd/ | 2 | 2 | 5 | 1 |
| there | /ðɛɹ/ | 2 | 2 | 5 | 1 |
| their | /ðɛɹ/ | 2 | 2 | 5 | 1 |
| what | /wɒt/ | 2 | **1** ɒt | 4 | 1 |
| so | /soʊ/ | 1 | 1 | 2 | 1 |
| up | /ʌp/ | 2 | 2 | 2 | 1 |
| out | /aʊt/ | 2 | 2 | 3 | 1 |
| if | /ɪf/ | 2 | 2 | 2 | 1 |
| about | /əbaʊt/ | 3 | 3 | 5 | 1-2 |
| who | /huː/ | 1 | 1 | 3 | 1 |
| get | /gɛt/ | 2 | **1** ɛt | 3 | 1 |
| make | /meɪk/ | 2 | 2 | 4 | 1 |
| can | /kæn/ | 2 | **1** æn | 3 | 1 |
| like | /laɪk/ | 2 | 2 | 4 | 1 |
| time | /taɪm/ | 2 | 2 | 4 | 1 |
| no | /noʊ/ | 1 | 1 | 2 | 1 |
| just | /dʒʌst/ | 3 | 2 (ʌ+st) | 4 | 1 |

### Summary Statistics

| Metric | Before CVC | With CVC | QWERTY | Steno |
|--------|------------|----------|--------|-------|
| **Total actions (50 words)** | 88 | **72** | 147 | ~52 |
| **Average per word** | 1.76 | **1.44** | 2.94 | ~1.04 |
| **Max for any word** | 3 | 3 | 5 | 2 |
| **Single-chord words** | 16/50 (32%) | **32/50 (64%)** | 2/50 (4%) | 48/50 (96%) |

### Analysis

- **CVC combos doubled single-chord coverage** from 32% to 64% of top 50 words, cutting average chords/word by 18%.

- **vs QWERTY:** This system uses **51% fewer actions** on average (up from 40% before CVC). The advantage is largest on long words with simple phonetic structure ("would" = 2 chords vs 5 keys, "there" = 2 vs 5).

- **vs Stenography:** Steno is still faster in raw chord count because it maps entire words/phrases to single strokes. However:
  - Steno requires memorizing ~100,000+ word-specific outlines
  - Steno only works for one language
  - This system's advantage is learnability and universality
  - The gap has narrowed significantly with CVC combos (1.44 vs 1.04)

- **Remaining multi-chord words:** "from" (3), "and" (3), "about" (3) — these need onset clusters or multi-syllable handling. "of", "have", "with", "as", "for", "or" — these have codas (/v/, /v/, /θ/, /z/, /ɹ/, /ɹ/) not covered by the 14 CVC combos.

---

## Finger Fatigue Estimate

Based on the 50-word sample, here's how often each left-hand finger is pressed:

| Finger | Times pressed | % of all presses | Role |
|--------|-------------|-----------------|------|
| Thumb (voice) | ~45 | 51% | Voiced sounds are very common |
| Index (place) | ~30 | 34% | Postalveolar + Velar sounds |
| Middle (place) | ~55 | 63% | Alveolar + Velar (most common places) |
| Ring (manner) | ~25 | 28% | Nasal + Approximant sounds |
| Pinky (manner) | ~30 | 34% | Fricative + Approximant sounds |

Middle finger has the highest load, which is good — it's the strongest finger. Pinky load is moderate, which is acceptable. Thumb has high load but thumbs are strong.

---

## Key Findings

1. **The mapping is functional** — all 24 consonants and 17 vowels fit on 5+5 fingers with no collisions
2. **Common sounds are mostly efficient** — top vowels (ə, ɪ, iː, ɛ) all use 0-2 fingers
3. **/ɹ/ and /l/ are the biggest ergonomic concern** — very common but mapped to 4-finger chords due to their featural position. Frequency-optimized swaps can fix this at the cost of featural purity
4. **40% fewer actions than QWERTY** but **~70% more actions than steno** — the system sits between them in efficiency
5. **Consonant cluster shortcuts** would be the single biggest improvement for reducing chord count
6. **The system's real advantage over steno isn't speed — it's universality and learnability**

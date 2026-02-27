# Semantic Mode — Intent Encoding Reference

## Design Philosophy

Instead of encoding sounds (phonemes) that form words, semantic mode encodes **meaning/intent** directly. The AI expands intent tokens into natural language.

**Key insight:** For AI-assisted coding, you're not writing prose — you're communicating intent. Why encode "please write the answer" phoneme by phoneme when you can encode `[POLITE REQUEST] [WRITE] [ANSWER]` in 3 chords?

---

## Comparison: Phonemic vs Semantic

| Aspect | Phonemic Mode | Semantic Mode |
|--------|--------------|---------------|
| Encodes | Sounds | Meaning |
| "Fix the bug" | ~8 chords | 2 chords (`FIX` + `BUG`) |
| Universal? | Yes (sounds exist in all languages) | Yes (concepts transcend language) |
| Precision | High (exact words) | Low (AI chooses words) |
| Use case | General text | Developer intent / AI prompting |

---

## Hand Layout

```
LEFT HAND (Category)              RIGHT HAND (Select)

A = ACTION (pinky)                M = extend (thumb)
S = TARGET (ring)                 J = slot 1 (index)
D = MODIFIER (middle)             K = slot 2 (middle)
F = LOGIC (index)                 L = slot 3 (ring)
C = META (thumb)                  ; = slot 4 (pinky)
```

**Pattern:** Left hand picks category, right hand picks specific concept within category.

**M (extend):** Adds 15 more options per category. Without M = primary concepts. With M = extended concepts.

---

## Semantic Vocabulary (~120 primitives)

### Actions (A + right hand)

Primary actions (no M):
| Chord | Symbol | Use |
|-------|--------|-----|
| A+J | CREATE | Make something new |
| A+K | DELETE | Remove something |
| A+L | MODIFY | Change something |
| A+; | FIX | Repair/debug |
| A+J+K | FIND | Search/locate |
| A+J+L | SHOW | Display/reveal |
| A+J+; | TEST | Verify/check |
| A+K+L | RUN | Execute |
| A+K+; | EXPLAIN | Describe/clarify |
| A+L+; | REFACTOR | Restructure code |
| A+J+K+L | OPTIMIZE | Improve performance |
| A+J+K+; | DEBUG | Find/fix bugs |
| A+J+L+; | DEPLOY | Ship to production |
| A+K+L+; | IMPORT | Bring in |
| A+J+K+L+; | EXPORT | Send out |

Extended actions (A+M + right):
| Chord | Symbol | Use |
|-------|--------|-----|
| A+M+J | ADD | Append/include |
| A+M+K | REMOVE | Take away |
| A+M+L | RENAME | Change name |
| A+M+; | MOVE | Relocate |
| A+M+J+K | COPY | Duplicate |
| A+M+J+L | UPDATE | Refresh/upgrade |
| A+M+J+; | CHECK | Verify |
| A+M+K+L | BUILD | Compile/construct |
| A+M+K+; | INSTALL | Set up dependency |
| A+M+L+; | CONFIGURE | Set options |
| A+M+J+K+L | GENERATE | Auto-create |
| A+M+J+K+; | VALIDATE | Confirm correctness |
| A+M+J+L+; | CLEAN | Remove artifacts |
| A+M+K+L+; | REVERT | Undo to previous |

### Targets (S + right hand)

Primary targets (no M):
| Chord | Symbol |
|-------|--------|
| S+J | FILE |
| S+K | FUNCTION |
| S+L | CLASS |
| S+; | VARIABLE |
| S+J+K | COMPONENT |
| S+J+L | API |
| S+J+; | DATABASE |
| S+K+L | TEST |
| S+K+; | ERROR |
| S+L+; | BUG |
| S+J+K+L | CODE |
| S+J+K+; | TYPE |
| S+J+L+; | MODULE |
| S+K+L+; | ROUTE |
| S+J+K+L+; | CONFIG |

Extended targets (S+M + right):
| Chord | Symbol |
|-------|--------|
| S+M+J | INTERFACE |
| S+M+K | METHOD |
| S+M+L | PROPERTY |
| S+M+; | PARAMETER |
| S+M+J+K | DEPENDENCY |
| S+M+J+L | ENDPOINT |
| S+M+J+; | QUERY |
| S+M+K+L | SCHEMA |
| S+M+K+; | COMMENT |
| S+M+L+; | LOG |
| S+M+J+K+L | RESPONSE |
| S+M+J+K+; | REQUEST |
| S+M+J+L+; | STATE |
| S+M+K+L+; | EVENT |

### Modifiers (D + right hand)

Primary modifiers (no M):
| Chord | Symbol |
|-------|--------|
| D+J | THIS |
| D+K | THAT |
| D+L | ALL |
| D+; | LAST |
| D+J+K | NEXT |
| D+J+L | NEW |
| D+J+; | CURRENT |
| D+K+L | SAME |
| D+K+; | OTHER |
| D+L+; | EVERY |
| D+J+K+L | FIRST |
| D+J+K+; | EACH |
| D+J+L+; | ONLY |
| D+K+L+; | MAIN |
| D+J+K+L+; | ENTIRE |

Extended modifiers (D+M + right):
| Chord | Symbol |
|-------|--------|
| D+M+J | ASYNC |
| D+M+K | RECURSIVE |
| D+M+L | PUBLIC |
| D+M+; | PRIVATE |
| D+M+J+K | STATIC |
| D+M+J+L | GLOBAL |
| D+M+J+; | LOCAL |
| D+M+K+L | OPTIONAL |
| D+M+K+; | REQUIRED |
| D+M+L+; | DEPRECATED |
| D+M+J+K+L | TEMPORARY |
| D+M+J+K+; | PERMANENT |

### Logic (F + right hand)

Primary logic (no M):
| Chord | Symbol |
|-------|--------|
| F+J | AND |
| F+K | OR |
| F+L | NOT |
| F+; | IF |
| F+J+K | THEN |
| F+J+L | WHEN |
| F+J+; | WHERE |
| F+K+L | WITH |
| F+K+; | WITHOUT |
| F+L+; | FROM |
| F+J+K+L | TO |
| F+J+K+; | INTO |
| F+J+L+; | LIKE |
| F+K+L+; | AS |
| F+J+K+L+; | BEFORE |

Extended logic (F+M + right):
| Chord | Symbol |
|-------|--------|
| F+M+J | AFTER |
| F+M+K | WHILE |
| F+M+L | UNTIL |
| F+M+; | UNLESS |
| F+M+J+K | BECAUSE |
| F+M+J+L | SO |
| F+M+J+; | ALSO |
| F+M+K+L | INSTEAD |
| F+M+K+; | USING |
| F+M+L+; | BASED_ON |

### Meta (C + right hand)

Primary meta (no M):
| Chord | Symbol |
|-------|--------|
| C+J | UNDO |
| C+K | REDO |
| C+L | DONE |
| C+; | CANCEL |
| C+J+K | HELP |
| C+J+L | AGAIN |
| C+J+; | YES |
| C+K+L | NO |
| C+K+; | MAYBE |
| C+L+; | WAIT |
| C+J+K+L | CONFIRM |
| C+J+K+; | SKIP |
| C+J+L+; | MORE |
| C+K+L+; | LESS |
| C+J+K+L+; | PERFECT |

Extended meta (C+M + right):
| Chord | Symbol |
|-------|--------|
| C+M+J | FASTER |
| C+M+K | SIMPLER |
| C+M+L | SAFER |
| C+M+; | BETTER |
| C+M+J+K | CONTINUE |
| C+M+J+L | STOP |
| C+M+J+; | RETRY |
| C+M+K+L | EXAMPLE |
| C+M+K+; | WHY |
| C+M+L+; | HOW |

### Daily Verbs (A+S combo)

| Chord | Symbol | Use |
|-------|--------|-----|
| A+S+J | GREET | Hello, greeting |
| A+S+K | ASK | Ask a question |
| A+S+L | TELL | Tell someone |
| A+S+; | WANT | Want/desire |
| A+S+J+K | NEED | Need something |
| A+S+J+L | KNOW | Know/understand |
| A+S+J+; | MEET | Meet someone |
| A+S+K+L | CALL | Call someone |
| A+S+K+; | SEND | Send something |
| A+S+L+; | GET | Get/obtain |
| A+S+J+K+L | START | Start/begin |
| A+S+J+K+; | FINISH | Finish/complete |
| A+S+J+L+; | SCHEDULE | Schedule event |
| A+S+K+L+; | CANCEL | Cancel event |

### People & Places (D+S combo)

| Chord | Symbol | Use |
|-------|--------|-----|
| D+S+J | NAME | Marks next literal as proper noun |
| D+S+K | PERSON | A person |
| D+S+L | PLACE | A place |
| D+S+; | THING | A thing |
| D+S+J+K | TEAM | Team/group |
| D+S+J+L | COMPANY | Company/org |
| D+S+K+L | PROJECT | Project |
| D+S+K+; | MEETING | Meeting |

### Time (A+D combo)

| Chord | Symbol |
|-------|--------|
| A+D+J | TODAY |
| A+D+K | TOMORROW |
| A+D+L | NOW |
| A+D+; | LATER |
| A+D+J+K | SOON |
| A+D+J+L | YESTERDAY |
| A+D+K+L | TIME |
| A+D+K+; | DATE |

### States (F+D combo)

| Chord | Symbol |
|-------|--------|
| F+D+J | HAPPY |
| F+D+K | BUSY |
| F+D+L | READY |
| F+D+; | SURE |
| F+D+J+K | AVAILABLE |
| F+D+J+L | INTERESTED |
| F+D+K+L | URGENT |
| F+D+K+; | IMPORTANT |

### Symbols (A+F combo)

| Chord | Symbol |
|-------|--------|
| A+F+J | 1 |
| A+F+K | 2 |
| A+F+L | 3 |
| A+F+; | 4 |
| A+F+J+K | 5 |
| A+F+J+L | 6 |
| A+F+J+; | 7 |
| A+F+K+L | 8 |
| A+F+K+; | 9 |
| A+F+L+; | 0 |
| A+F+J+K+L | . |
| A+F+J+K+; | , |
| A+F+J+L+; | ? |
| A+F+K+L+; | ! |
| A+F+J+K+L+; | : |

Extended symbols (A+F+M + right):
| Chord | Symbol |
|-------|--------|
| A+F+M+J | - |
| A+F+M+K | _ |
| A+F+M+L | / |
| A+F+M+; | @ |
| A+F+M+J+K | # |
| A+F+M+J+L | $ |
| A+F+M+J+; | % |
| A+F+M+K+L | & |
| A+F+M+K+; | * |
| A+F+M+L+; | + |
| A+F+M+J+K+L | = |
| A+F+M+J+K+; | ( |
| A+F+M+J+L+; | ) |
| A+F+M+K+L+; | " |

### Style Modifiers (D+C combo) — for reprompt

Use these to restyle the last AI output. Add style modifiers then press REPROMPT.

| Chord | Symbol | Effect |
|-------|--------|--------|
| D+C+J | FORMAL | Professional, formal tone |
| D+C+K | CASUAL | Relaxed, conversational |
| D+C+L | POLITE | Add softeners, please/thanks |
| D+C+; | DIRECT | Blunt, to the point |
| D+C+J+K | TECHNICAL | Precise terminology |
| D+C+J+L | FRIENDLY | Warm, approachable |
| D+C+J+; | PROFESSIONAL | Business-appropriate |
| D+C+K+L | BRIEF | Condense to essentials |
| D+C+K+; | DETAILED | Add more explanation |
| D+C+L+; | AS_QUESTION | Rephrase as question |
| D+C+J+K+L | AS_COMMAND | Rephrase as command |
| D+C+J+K+; | AS_REQUEST | Rephrase as polite request |
| D+C+M+J | REPROMPT | Trigger restyling |

---

## Example Sequences

### Basic

| Intent | Tokens | AI Output |
|--------|--------|-----------|
| Create a function | `CREATE` `FUNCTION` | "Create a new function." |
| Fix bug here | `FIX` `BUG` `THIS` | "Fix the bug in this code." |
| Delete all tests | `DELETE` `ALL` `TEST` | "Delete all tests." |

### Developer Tasks

| Intent | Tokens | AI Output |
|--------|--------|-----------|
| Make function async | `MODIFY` `THIS` `FUNCTION` `ASYNC` | "Modify this function to be async." |
| Add tests for API | `CREATE` `TEST` `ALL` `API` | "Create tests for all API endpoints." |
| Explain the code | `EXPLAIN` `THIS` `CODE` `HOW` | "Explain how this code works." |
| Refactor simpler | `REFACTOR` `THIS` `SIMPLER` | "Refactor this to be simpler." |
| Generate types | `GENERATE` `TYPE` `FROM` `SCHEMA` | "Generate types from the schema." |

### Complex Instructions

| Intent | Tokens | AI Output |
|--------|--------|-----------|
| Add logging to errors | `ADD` `ERROR` `WITH` `LOG` | "Add error handling with logging." |
| Deploy after tests | `DEPLOY` `THIS` `AFTER` `TEST` | "Deploy this after running tests." |
| Find unused vars | `FIND` `VARIABLE` `NOT` `USING` | "Find variables that are not being used." |

### Hybrid Mode (Semantic + Phonemic Names)

Toggle phonemic mode with **S+C+M** to type names phonetically. The AI distinguishes by case:
- **UPPERCASE** = semantic tokens (expand based on meaning)
- **lowercase** = phonemic text (convert to words based on sound)

| Intent | Input | AI Output |
|--------|-------|-----------|
| Greet Wren | `CASUAL GREET NAME wren` | "Hey, Wren!" |
| Ask Ian | `POLITE ASK NAME ian BUSY TODAY AS_QUESTION` | "Hello, Ian. Are you busy today?" |
| Schedule with Viktor | `WANT SCHEDULE MEETING WITH NAME viktorchen TOMORROW` | "I want to schedule a meeting with Dr. Viktor Chen tomorrow." |

---

## Controls

| Action | Chord |
|--------|-------|
| Expand to text | Space |
| Delete last token | C+M (both thumbs) |
| New line | C+; (left thumb + right pinky) |
| Toggle semantic/phonemic | S+C+M |
| Show cheatsheet | C+M+K |

---

## Universality

The semantic vocabulary is **language-independent**. The same tokens work regardless of output language:

| Tokens | English | Portuguese | Chinese |
|--------|---------|------------|---------|
| `CREATE` `FUNCTION` | Create a function. | Crie uma função. | 创建一个函数。 |
| `FIX` `BUG` `THIS` | Fix the bug here. | Corrija o bug aqui. | 修复这里的bug。 |

The AI's language setting determines output language, but the **input is universal**.

---

## Comparison with Phonemic Mode

| Task | Phonemic chords | Semantic chords |
|------|-----------------|-----------------|
| "Fix the bug" | ~6-8 | 2 |
| "Create an async function" | ~12-15 | 3 |
| "Refactor this code to be simpler" | ~20+ | 4 |

For developer intent, semantic mode is **3-5x faster** than phonemic mode.

---

## Limitations

1. **Less precise:** You can't control exact wording — AI chooses
2. **AI-dependent:** Requires server connection, has latency
3. **Domain-specific:** Current vocabulary optimized for developers
4. **Learning curve:** Must memorize ~120 concept-to-chord mappings

---

## Future Extensions

- **Custom vocabularies:** Domain-specific token sets (legal, medical, etc.)
- **User-defined tokens:** Personal shortcuts for frequent phrases
- **Context awareness:** AI remembers conversation context
- **Hybrid mode:** Switch between semantic and phonemic mid-sentence

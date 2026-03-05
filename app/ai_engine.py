"""AI engine: expand semantic tokens to natural language via Groq."""

import queue
import threading

from groq import Groq
from config import get_groq_api_key

SYSTEM_PROMPT = """You are a semantic-to-text expander. Your ONLY job is to output the expanded text—nothing else. No explanations, no reasoning, no commentary. Just the final sentence.

Users input sequences that mix semantic tokens (UPPERCASE) and literal text (lowercase). Expand them into natural, fluent text.

## Input Format
- UPPERCASE = semantic tokens (expand based on meaning)
- lowercase = literal text (use as-is, apply grammar as needed)

## Token Categories

VERBS-CORE: MAKE, CHANGE, ADD, REMOVE, FIND, SHOW, FIX, USE, GET, GIVE, KEEP, TAKE, TRY, PUT, MOVE, HELP, CHECK, OPEN, CLOSE, THINK, LIST, COMBINE, SPLIT, COMPARE, IMPROVE, EXPLAIN, ANALYZE, SUMMARIZE, SIMPLIFY, EXPAND

NOUNS: IT, THIS, THAT, THING, IDEA, WAY, PART, POINT, REASON, PROBLEM, SOLUTION, QUESTION, ANSWER, EXAMPLE, RESULT, FILE, CODE, DATA, TEXT, FUNCTION, LIST, NAME, STEP, OPTION, ERROR, INPUT, OUTPUT, CONTENT, CONTEXT, DETAIL

MODIFIERS: GOOD, BAD, MORE, LESS, NEW, OLD, SAME, DIFFERENT, OTHER, ALL, SIMPLE, COMPLEX, MAIN, GENERAL, SPECIFIC, FAST, SLOW, BIG, SMALL, LONG, SHORT, CLEAR, CORRECT, WRONG, SIMILAR, EXACT, ENOUGH, VERY, TOO, QUITE

CONNECTORS: AND, OR, BUT, SO, IF, THEN, BECAUSE, WITH, WITHOUT, FOR, TO, FROM, AS, LIKE, ABOUT, ALSO, HOWEVER, INSTEAD, RATHER, WHEN, WHERE, WHILE, BEFORE, AFTER, ALTHOUGH, UNLESS, UNTIL, SINCE, WHETHER, THAN

RESPONSES: YES, NO, OK, THANKS, PLEASE, SORRY, WHAT, WHY, HOW, WHICH, WHO, WHEN, WHERE, MAYBE, AGAIN, WAIT, DONE, CONTINUE, STOP, UNDO, SKIP, FOCUS, IGNORE, REMEMBER, FORGET, CONFIRM, PERFECT, ALMOST, EXACTLY

VERBS-SOCIAL: ASK, TELL, SAY, KNOW, WANT, NEED, LIKE, SEND, CALL, MEET, START, FINISH, GREET, INVITE, SCHEDULE, GO, COME, LEAVE, STAY, RETURN, ARRIVE, BRING, SEE, HEAR, FEEL, AGREE, ACCEPT, REJECT, CANCEL

TIME: NOW, TODAY, TOMORROW, YESTERDAY, SOON, LATER, FIRST, LAST, NEXT, PREVIOUS, BEFORE, AFTER, DURING, RECENTLY, FINALLY, TIME, DATE, WEEK, MONTH, YEAR, HOUR, MINUTE, MORNING, AFTERNOON, EVENING, NIGHT, WEEKEND, DAILY, WEEKLY, MONTHLY

SYMBOLS: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, . , ? ! : ; - _ / @ # $ % & * + = ( ) "

MODALS: NOT, CAN, WILL, SHOULD, WOULD, COULD, MIGHT, MUST, MAY, SHALL, ALWAYS, NEVER, SOMETIMES, USUALLY, OFTEN, RARELY, HARDLY, BARELY, ALREADY, STILL, YET, JUST, ONLY, EVEN

NOUNS-THINGS: PLACE, PERSON, HOME, OFFICE, ROOM, BUILDING, WORLD, PHONE, EMAIL, MESSAGE, DOCUMENT, REPORT, PROJECT, MEETING, TEAM, COMPANY, GROUP, EVENT, TASK, ISSUE, REQUEST, UPDATE, MONEY, SCREEN, BUTTON, WINDOW, LINK, IMAGE, PAGE, SITE

PRONOUNS: I, YOU, WE, THEY, HE, SHE, IT, THIS, THAT, WHO, SOMEONE, EVERYONE, ANYONE, NOONE, SOMETHING, MY, YOUR, OUR, THEIR, HIS, HER, ME, US, THEM, SOME, MANY, FEW, NONE, EACH, BOTH

VERBS-PHYSICAL: DO, HAVE, BE, GET, WORK, PLAY, REST, SLEEP, WAKE, EAT, DRINK, RUN, WALK, SIT, STAND, READ, WRITE, SPEAK, LISTEN, WATCH, LEARN, TEACH, HOLD, DROP, CARRY, PUSH, PULL, THROW, CATCH, TOUCH

STATES: READY, BUSY, SURE, HAPPY, SAD, TIRED, ANGRY, WORRIED, CONFUSED, NERVOUS, CALM, EXCITED, BORED, STUCK, LOST, AVAILABLE, INTERESTED, IMPORTANT, URGENT, NECESSARY, REQUIRED, OPTIONAL, POSSIBLE, RECOMMENDED, PENDING, COMPLETE, BROKEN, FIXED, FOUND

STYLE: FORMAL, CASUAL, POLITE, DIRECT, BRIEF, DETAILED, FRIENDLY, PROFESSIONAL, TECHNICAL, SIMPLE, AS_QUESTION, AS_COMMAND, AS_REQUEST, AS_LIST, AS_SUMMARY, GENTLE, FIRM, SERIOUS, HUMOROUS, CONFIDENT, HUMBLE, ENTHUSIASTIC, EMPATHETIC, SUPPORTIVE, CRITICAL, SKEPTICAL, PERSUASIVE, NEUTRAL, URGENT_TONE, REPROMPT

PREPOSITIONS: IN, ON, AT, TO, FROM, WITH, BY, FOR, OF, ABOUT, UP, DOWN, OUT, INTO, THROUGH, OVER, UNDER, BETWEEN, AROUND, BEHIND, ABOVE, BELOW, BESIDE, NEAR, ACROSS, ALONG, TOWARD, AGAINST, HERE, THERE

TECH: DEBUG, TEST, BUILD, RUN, DEPLOY, COMMIT, PUSH, PULL, MERGE, BRANCH, INSTALL, UPDATE, UPGRADE, CONFIGURE, INITIALIZE, SERVER, CLIENT, DATABASE, API, ENDPOINT, REQUEST, RESPONSE, QUERY, CACHE, LOG, VARIABLE, FUNCTION, CLASS, ERROR, EXCEPTION

## Composability Rules
- Use NOT with any token for negation: "CAN NOT" → "can't", "WILL NOT" → "won't"
- Use MORE/LESS with adjectives: "MORE GOOD" → "better", "MORE BAD" → "worse"
- Combine primitives naturally: "POSSIBLE NOT" → "impossible"

## Special Token
- NAME: The next lowercase word is a proper noun (capitalize it, use honorifics with POLITE/FORMAL)

## Rules
1. UPPERCASE tokens → expand based on semantic meaning
2. lowercase text → use literally, apply grammar as needed
3. Apply STYLE tokens (FORMAL, CASUAL, POLITE, etc.) to the entire output tone
4. After NAME token, treat the following lowercase word as a proper noun

## CRITICAL OUTPUT RULE
You MUST output ONLY the final expanded text. NEVER include:
- Explanations of what you're doing
- Reasoning or thinking process
- Phrases like "I'll expand this" or "Based on the context"
- Commentary about the tokens
- Anything other than the direct text expansion
Just output the converted sentence and nothing else.

## Examples
GREET NAME wren → Hello, Wren!
POLITE GREET NAME ian → Hello, Mr. Ian. Nice to meet you.
CASUAL GREET BUSY TODAY AS_QUESTION → Hey, are you busy today?
WANT SCHEDULE MEETING DISCUSS projekt TOMORROW → I want to schedule a meeting to discuss the project tomorrow.
THANKS FOR HELP PERFECT → Thanks for your help, that's perfect!
FORMAL PROFESSIONAL GREET NAME chen INTERESTED DISCUSS PROJECT → Good morning, Mr. Chen. I'm interested in discussing the project with you.
I CAN NOT COME TO MEETING TODAY → I can't come to the meeting today.
CAN YOU SEND ME EMAIL ABOUT PROJECT → Can you send me an email about the project?
WE SHOULD PUT THIS IN DOCUMENT → We should put this in the document.
I NOT KNOW WHERE HE GO → I don't know where he went.
PLEASE GO TO MY OFFICE AND GET PHONE → Please go to my office and get my phone.
EVERYONE IN TEAM MUST SEE THIS REPORT → Everyone on the team must see this report.
I TIRED NEED REST → I'm tired and need to rest.
MORNING MEETING CANCEL → The morning meeting has been cancelled.
PLEASE DEBUG THIS CODE FIND ERROR → Please debug this code and find the error.
I WILL PUSH COMMIT AFTER TEST → I will push the commit after testing.
SAD HEAR THAT HOPE MORE GOOD SOON → I'm sad to hear that. Hope things get better soon.
ENTHUSIASTIC ABOUT NEW PROJECT → I'm enthusiastic about the new project!
WE SHOULD WALK TOGETHER TO OFFICE MORNING → We should walk together to the office in the morning.
MAKE backspace KEEP REMOVE WHEN HOLD → Make the backspace key keep removing when holding."""


class AIEngine:
    """Background worker that expands semantic tokens via Groq."""

    MAX_CONTEXT_TURNS = 5  # Rolling context window size

    def __init__(self, on_result, on_error, on_context_change=None, on_language_change=None):
        self.on_result = on_result
        self.on_error = on_error
        self.on_context_change = on_context_change  # Called when context size changes
        self.on_language_change = on_language_change  # Called when language changes
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._client = None
        self._api_key = get_groq_api_key()
        # Conversation context: list of (tokens, result) tuples
        self._context = []
        self._pending_tokens = None  # Track tokens for context storage
        # Language setting
        self._language = 'English'
        self._language_code = 'EN'

    def start(self):
        self._thread.start()

    def expand(self, tokens_text):
        """Queue token text for AI expansion."""
        self._pending_tokens = tokens_text
        self._queue.put(tokens_text)

    # Keep old method name for compatibility
    def convert(self, text):
        self.expand(text)

    def clear_context(self):
        """Clear conversation context (start fresh)."""
        self._context.clear()
        if self.on_context_change:
            self.on_context_change(0)

    def get_context_size(self):
        """Return number of turns in context."""
        return len(self._context)

    def set_language(self, code, name):
        """Set output language for AI expansion."""
        self._language_code = code
        self._language = name
        if self.on_language_change:
            self.on_language_change(code, name)

    def get_language(self):
        """Get current language name."""
        return self._language

    def get_language_code(self):
        """Get current language code."""
        return self._language_code

    def set_raw_mode(self, enabled):
        pass  # Not used in semantic mode

    def _build_messages(self, tokens):
        """Build message list with context history."""
        # Add language instruction if not English
        if self._language != 'English':
            language_instruction = f"""

## OUTPUT LANGUAGE
You MUST output the expanded text in {self._language}.
- Translate the semantic meaning to {self._language}
- Keep proper nouns (names after NAME token) as-is
- Maintain natural grammar and idioms for {self._language}
- Do NOT output in English unless the target language is English"""
            system_content = SYSTEM_PROMPT + language_instruction
        else:
            system_content = SYSTEM_PROMPT

        messages = [{"role": "system", "content": system_content}]

        # Add context history as conversation turns
        for prev_tokens, prev_result in self._context:
            messages.append({"role": "user", "content": prev_tokens})
            messages.append({"role": "assistant", "content": prev_result})

        # Add current request
        messages.append({"role": "user", "content": tokens})
        return messages

    def _add_to_context(self, tokens, result):
        """Add expansion to context, maintaining max size."""
        self._context.append((tokens, result))
        # Trim to max size
        while len(self._context) > self.MAX_CONTEXT_TURNS:
            self._context.pop(0)
        if self.on_context_change:
            self.on_context_change(len(self._context))

    def _worker(self):
        while True:
            tokens = self._queue.get()
            if tokens is None:
                break

            if not self._api_key:
                # No API key - just return tokens as-is
                self.on_result(tokens)
                continue

            try:
                if self._client is None:
                    self._client = Groq(api_key=self._api_key)

                messages = self._build_messages(tokens)

                response = self._client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    temperature=0.4,
                    max_tokens=512,
                )
                result = response.choices[0].message.content.strip()
                # Strip quotes if model adds them
                if result.startswith('"') and result.endswith('"'):
                    result = result[1:-1]

                # Add to context before calling on_result
                self._add_to_context(tokens, result)

                self.on_result(result)

            except Exception as e:
                self.on_error(tokens, str(e))

    def stop(self):
        self._queue.put(None)

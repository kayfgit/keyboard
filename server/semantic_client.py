"""Groq LLM client for semantic-to-text expansion."""

import os
from groq import Groq

SYSTEM_PROMPT = """You are a semantic-to-text expander. Users input sequences of semantic tokens (concepts/intents) and you expand them into natural, fluent English text.

The user communicates through semantic primitives instead of full sentences. Your job is to expand these into clear, natural language that conveys their intent.

## Token Categories

ACTIONS: MAKE, CHANGE, REMOVE, FIX, FIND, SHOW, TRY, USE, EXPLAIN, IMPROVE, COMPARE, ANALYZE, SUMMARIZE, EXPAND, SIMPLIFY, ADD, KEEP, GIVE, TAKE, THINK, HELP, CHECK, LIST, COMBINE, SPLIT, GENERATE, TRANSLATE, REWRITE, FORMAT

SUBJECTS: THIS, THAT, IT, IDEA, TEXT, CODE, QUESTION, ANSWER, PROBLEM, SOLUTION, EXAMPLE, RESULT, REASON, WAY, POINT, FILE, FUNCTION, DATA, NAME, LIST, STEP, PART, OPTION, ERROR, OUTPUT, INPUT, CONTENT, CONTEXT, DETAIL

QUALITIES: GOOD, BAD, MORE, LESS, SIMPLE, COMPLEX, NEW, OLD, SAME, DIFFERENT, GENERAL, SPECIFIC, MAIN, OTHER, ALL, FAST, SLOW, BIG, SMALL, SHORT, LONG, CLEAR, BETTER, WORSE, CORRECT, WRONG, SIMILAR, EXACT, ENOUGH

CONNECTORS: AND, OR, BUT, SO, IF, THEN, BECAUSE, WITH, WITHOUT, FOR, TO, FROM, LIKE, AS, ABOUT, ALSO, HOWEVER, INSTEAD, RATHER, BEFORE, AFTER, WHILE, WHEN, WHERE, ALTHOUGH, UNLESS, UNTIL, SINCE, WHETHER

RESPONSES: YES, NO, MAYBE, OK, THANKS, PLEASE, SORRY, WAIT, DONE, AGAIN, WHAT, WHY, HOW, WHICH, WHO, CONTINUE, STOP, UNDO, SKIP, FOCUS, IGNORE, REMEMBER, FORGET, CONFIRM, NEVERMIND, PERFECT, ALMOST, NOT_QUITE, EXACTLY

SYMBOLS: Numbers (1-9, 0) and punctuation (. , ? ! : - _ / @ # $ % & * + = ( ) ")

SHORTCUTS: MAKE_THIS, CHANGE_THIS, EXPLAIN_THIS, FIX_THIS, SHOW_ME, HELP_ME, TELL_ME, MORE_DETAIL, LESS_DETAIL, ANOTHER_WAY, SAME_THING, GOOD_IDEA, BAD_IDEA, MAIN_POINT

STYLE MODIFIERS (apply to output tone):
- FORMAL: Professional, formal language
- CASUAL: Relaxed, conversational tone
- POLITE: Add softeners, please/thanks
- DIRECT: Blunt, to the point
- TECHNICAL: Precise terminology
- FRIENDLY: Warm, approachable
- PROFESSIONAL: Business-appropriate
- BRIEF: Condense to essentials
- DETAILED: Add more explanation
- AS_QUESTION: Phrase as a question
- AS_COMMAND: Phrase as a command
- AS_REQUEST: Phrase as a polite request

## Rules

1. Expand tokens into natural, fluent English
2. Infer reasonable context and connections between tokens
3. Keep output concise but complete
4. Preserve the conversational tone - it can be questions, statements, or requests
5. Add articles (a, the) and prepositions where needed
6. Output ONLY the expanded text, no explanations or quotes
7. Symbols should be included literally in the output

## Examples

Input: GOOD BUT MORE GENERAL
Output: Good, but make it more general.

Input: EXPLAIN THIS LIKE SIMPLE
Output: Explain this in simpler terms.

Input: WHAT IF CHANGE THIS TO THAT
Output: What if we change this to that?

Input: YES PERFECT THANKS
Output: Yes, that's perfect. Thanks!

Input: MAKE TEXT SHORT AND CLEAR
Output: Make the text shorter and clearer.

Input: WHY THIS NOT WORK
Output: Why isn't this working?

Input: SHOW EXAMPLE WITH CODE
Output: Show me an example with code.

Input: GOOD IDEA BUT HOW
Output: That's a good idea, but how would we do it?

Input: COMPARE THIS AND THAT
Output: Compare this approach with that one.

Input: FIX_THIS AND MAKE SIMPLE
Output: Fix this and make it simpler.

Input: THINK ABOUT ANOTHER_WAY
Output: Think about another way to do this.

Input: SORRY NEVERMIND UNDO
Output: Sorry, nevermind. Undo that.

Input: MORE_DETAIL ABOUT STEP 3
Output: Give me more detail about step 3.

Input: IF PROBLEM THEN SHOW ERROR
Output: If there's a problem, show the error.

Input: SUMMARIZE MAIN_POINT SHORT
Output: Summarize the main points briefly.

Input: WAIT BEFORE CONTINUE CHECK THIS
Output: Wait, before continuing, check this.

Input: TRANSLATE THIS TO CODE
Output: Translate this into code."""

REPROMPT_SYSTEM = """You are a text style transformer. You will receive:
1. An original text that was generated
2. Style modifiers indicating how to change it

Apply the style modifiers to rewrite the text while preserving the core meaning.

## Style Modifiers

FORMAL - Use formal, professional language
CASUAL - Use relaxed, conversational language
POLITE - Add polite phrasing and softeners
DIRECT - Be blunt and to the point
TECHNICAL - Use precise technical terminology
FRIENDLY - Warm, approachable tone
PROFESSIONAL - Business-appropriate tone
BRIEF - Condense to essential points only
DETAILED - Add more explanation and context
AS_QUESTION - Rephrase as a question
AS_COMMAND - Rephrase as a command/instruction
AS_REQUEST - Rephrase as a polite request

## Rules

1. Preserve the core meaning of the original text
2. Apply ALL specified style modifiers
3. Output ONLY the rewritten text, no explanations
4. Keep it natural and fluent

## Examples

Original: "Fix this bug."
Styles: [POLITE, AS_REQUEST]
Output: Could you please help me fix this bug?

Original: "The function needs error handling."
Styles: [DIRECT, BRIEF]
Output: Add error handling.

Original: "I think we should consider a different approach."
Styles: [FORMAL, AS_QUESTION]
Output: Would it be advisable to explore an alternative approach?"""


def expand_semantic(tokens: list[str], styles: list[str] = None, original_text: str = None) -> str:
    """Expand semantic tokens into natural language.

    Args:
        tokens: List of semantic token strings, e.g. ["CREATE", "FUNCTION", "ASYNC"]
        styles: Optional list of style modifiers for reprompting
        original_text: Optional original text to restyle (for reprompt mode)

    Returns:
        Natural language expansion
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY not set, returning tokens unchanged")
        return " ".join(tokens)

    try:
        client = Groq(api_key=api_key)

        # Reprompt mode: restyle existing text
        if styles and original_text:
            user_content = f"Original: {original_text}\nStyles: {styles}"
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": REPROMPT_SYSTEM},
                    {"role": "user", "content": user_content},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,  # Slightly higher for creative restyling
                max_tokens=256,
            )
        elif styles:
            # Normal expansion with style modifiers
            token_string = " ".join(tokens)
            style_instruction = f"Apply these styles to your output: {', '.join(styles)}"
            user_content = f"{token_string}\n\n[{style_instruction}]"
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.4,
                max_tokens=256,
            )
        else:
            # Normal expansion mode
            token_string = " ".join(tokens)
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": token_string},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                max_tokens=256,
            )

        result = response.choices[0].message.content.strip()
        # Strip quotes if model adds them
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        return result
    except Exception as e:
        print(f"Groq API error: {e}")
        return " ".join(tokens)

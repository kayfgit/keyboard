"""Chord engine: semantic + phonemic modes with token output.

Outputs tokens as typed text, AI replaces on Space.
"""

# Bit positions for each key
LEFT_KEYS = {'c': 4, 'f': 3, 'd': 2, 's': 1, 'a': 0}
RIGHT_KEYS = {'m': 4, 'j': 3, 'k': 2, 'l': 1, ';': 0}
LEFT_KEY_ORDER = ['A', 'S', 'D', 'F', 'C']
RIGHT_KEY_ORDER = ['M', 'J', 'K', 'L', ';']

ALL_CHORD_KEYS = set(LEFT_KEYS) | set(RIGHT_KEYS)

# Phonemic mappings
CONSONANTS = {
    0:  None,
    1:  'f',    2:  'p',    3:  'st',   4:  't',
    5:  's',    6:  'th',   7:  'dh',   8:  'r',
    9:  'sh',   10: 'nd',   11: 'tr',   12: 'k',
    13: 'h',    14: 'pr',   15: 'str',  16: 'b',
    17: 'v',    18: 'm',    19: 'w',    20: 'd',
    21: 'z',    22: 'n',    23: 'j',    24: 'l',
    25: 'zh',   26: 'nt',   27: 'ch',   28: 'g',
    29: 'sp',   30: 'ng',   31: 'y',
}

VOWELS = {
    0:  None,
    1:  'i',    2:  'o',    3:  'u',    4:  'e',
    5:  'uh',   6:  'at',   7:  'in',   8:  'a',
    9:  'an',   10: 'on',   11: 'it',   12: 'er',
    13: 'or',   14: 'al',   15: 'ing',  16: 'ot',
    17: 'ee',   18: 'oh',   19: 'oo',   20: 'ay',
    21: 'et',   22: 'ut',   23: 'en',   24: 'ah',
    25: 'un',   26: 'ad',   27: 'is',   28: 'il',
    29: 'aw',   30: 'oi',   31: 'ow',
}

# Semantic vocabulary - same as semantic.html
SEMANTICS = {
    # ACTIONS (A)
    'A+J': 'MAKE', 'A+K': 'CHANGE', 'A+L': 'REMOVE', 'A+;': 'FIX',
    'A+J+K': 'FIND', 'A+J+L': 'SHOW', 'A+J+;': 'TRY', 'A+K+L': 'USE',
    'A+K+;': 'EXPLAIN', 'A+L+;': 'IMPROVE', 'A+J+K+L': 'COMPARE',
    'A+J+K+;': 'ANALYZE', 'A+J+L+;': 'SUMMARIZE', 'A+K+L+;': 'EXPAND',
    'A+J+K+L+;': 'SIMPLIFY',
    'A+M+J': 'ADD', 'A+M+K': 'KEEP', 'A+M+L': 'GIVE', 'A+M+;': 'TAKE',
    'A+M+J+K': 'THINK', 'A+M+J+L': 'HELP', 'A+M+J+;': 'CHECK',
    'A+M+K+L': 'LIST', 'A+M+K+;': 'COMBINE', 'A+M+L+;': 'SPLIT',
    'A+M+J+K+L': 'GENERATE', 'A+M+J+K+;': 'TRANSLATE',
    'A+M+J+L+;': 'REWRITE', 'A+M+K+L+;': 'FORMAT',

    # SUBJECTS (S)
    'S+J': 'THIS', 'S+K': 'THAT', 'S+L': 'IT', 'S+;': 'IDEA',
    'S+J+K': 'TEXT', 'S+J+L': 'CODE', 'S+J+;': 'QUESTION',
    'S+K+L': 'ANSWER', 'S+K+;': 'PROBLEM', 'S+L+;': 'SOLUTION',
    'S+J+K+L': 'EXAMPLE', 'S+J+K+;': 'RESULT', 'S+J+L+;': 'REASON',
    'S+K+L+;': 'WAY', 'S+J+K+L+;': 'POINT',
    'S+M+J': 'FILE', 'S+M+K': 'FUNCTION', 'S+M+L': 'DATA', 'S+M+;': 'NAME',
    'S+M+J+K': 'LIST', 'S+M+J+L': 'STEP', 'S+M+J+;': 'PART',
    'S+M+K+L': 'OPTION', 'S+M+K+;': 'ERROR', 'S+M+L+;': 'OUTPUT',
    'S+M+J+K+L': 'INPUT', 'S+M+J+K+;': 'CONTENT',
    'S+M+J+L+;': 'CONTEXT', 'S+M+K+L+;': 'DETAIL',

    # QUALITY (D)
    'D+J': 'GOOD', 'D+K': 'BAD', 'D+L': 'MORE', 'D+;': 'LESS',
    'D+J+K': 'SIMPLE', 'D+J+L': 'COMPLEX', 'D+J+;': 'NEW',
    'D+K+L': 'OLD', 'D+K+;': 'SAME', 'D+L+;': 'DIFFERENT',
    'D+J+K+L': 'GENERAL', 'D+J+K+;': 'SPECIFIC', 'D+J+L+;': 'MAIN',
    'D+K+L+;': 'OTHER', 'D+J+K+L+;': 'ALL',
    'D+M+J': 'FAST', 'D+M+K': 'SLOW', 'D+M+L': 'BIG', 'D+M+;': 'SMALL',
    'D+M+J+K': 'SHORT', 'D+M+J+L': 'LONG', 'D+M+J+;': 'CLEAR',
    'D+M+K+L': 'BETTER', 'D+M+K+;': 'WORSE', 'D+M+L+;': 'CORRECT',
    'D+M+J+K+L': 'WRONG', 'D+M+J+K+;': 'SIMILAR',
    'D+M+J+L+;': 'EXACT', 'D+M+K+L+;': 'ENOUGH',

    # CONNECT (F)
    'F+J': 'AND', 'F+K': 'OR', 'F+L': 'BUT', 'F+;': 'SO',
    'F+J+K': 'IF', 'F+J+L': 'THEN', 'F+J+;': 'BECAUSE',
    'F+K+L': 'WITH', 'F+K+;': 'WITHOUT', 'F+L+;': 'FOR',
    'F+J+K+L': 'TO', 'F+J+K+;': 'FROM', 'F+J+L+;': 'LIKE',
    'F+K+L+;': 'AS', 'F+J+K+L+;': 'ABOUT',
    'F+M+J': 'ALSO', 'F+M+K': 'HOWEVER', 'F+M+L': 'INSTEAD', 'F+M+;': 'RATHER',
    'F+M+J+K': 'BEFORE', 'F+M+J+L': 'AFTER', 'F+M+J+;': 'WHILE',
    'F+M+K+L': 'WHEN', 'F+M+K+;': 'WHERE', 'F+M+L+;': 'ALTHOUGH',
    'F+M+J+K+L': 'UNLESS', 'F+M+J+K+;': 'UNTIL',
    'F+M+J+L+;': 'SINCE', 'F+M+K+L+;': 'WHETHER',

    # RESPOND (C)
    'C+J': 'YES', 'C+K': 'NO', 'C+L': 'MAYBE', 'C+;': 'OK',
    'C+J+K': 'THANKS', 'C+J+L': 'PLEASE', 'C+J+;': 'SORRY',
    'C+K+L': 'WAIT', 'C+K+;': 'DONE', 'C+L+;': 'AGAIN',
    'C+J+K+L': 'WHAT', 'C+J+K+;': 'WHY', 'C+J+L+;': 'HOW',
    'C+K+L+;': 'WHICH', 'C+J+K+L+;': 'WHO',
    'C+M+J': 'CONTINUE', 'C+M+K': 'STOP', 'C+M+L': 'UNDO', 'C+M+;': 'SKIP',
    'C+M+J+K': 'FOCUS', 'C+M+J+L': 'IGNORE', 'C+M+J+;': 'REMEMBER',
    'C+M+K+L': 'FORGET', 'C+M+K+;': 'CONFIRM', 'C+M+L+;': 'NEVERMIND',
    'C+M+J+K+L': 'PERFECT', 'C+M+J+K+;': 'ALMOST',
    'C+M+J+L+;': 'NOT_QUITE', 'C+M+K+L+;': 'EXACTLY',

    # SYMBOLS (A+F)
    'A+F+J': '1', 'A+F+K': '2', 'A+F+L': '3', 'A+F+;': '4',
    'A+F+J+K': '5', 'A+F+J+L': '6', 'A+F+J+;': '7',
    'A+F+K+L': '8', 'A+F+K+;': '9', 'A+F+L+;': '0',
    'A+F+J+K+L': '.', 'A+F+J+K+;': ',', 'A+F+J+L+;': '?',
    'A+F+K+L+;': '!', 'A+F+J+K+L+;': ':',
    'A+F+M+J': '-', 'A+F+M+K': '_', 'A+F+M+L': '/', 'A+F+M+;': '@',
    'A+F+M+J+K': '#', 'A+F+M+J+L': '$', 'A+F+M+J+;': '%',
    'A+F+M+K+L': '&', 'A+F+M+K+;': '*', 'A+F+M+L+;': '+',
    'A+F+M+J+K+L': '=', 'A+F+M+J+K+;': '(', 'A+F+M+J+L+;': ')',
    'A+F+M+K+L+;': '"',

    # DAILY (A+S) - common verbs
    'A+S+J': 'GREET', 'A+S+K': 'ASK', 'A+S+L': 'TELL', 'A+S+;': 'WANT',
    'A+S+J+K': 'NEED', 'A+S+J+L': 'KNOW', 'A+S+J+;': 'MEET',
    'A+S+K+L': 'CALL', 'A+S+K+;': 'SEND', 'A+S+L+;': 'GET',
    'A+S+J+K+L': 'START', 'A+S+J+K+;': 'FINISH',
    'A+S+J+L+;': 'SCHEDULE', 'A+S+K+L+;': 'CANCEL', 'A+S+J+K+L+;': 'COMPLETE',
    'A+S+M+J': 'GO', 'A+S+M+K': 'COME', 'A+S+M+L': 'LEAVE', 'A+S+M+;': 'STAY',
    'A+S+M+J+K': 'RETURN', 'A+S+M+J+L': 'BRING', 'A+S+M+J+;': 'ARRIVE',
    'A+S+M+K+L': 'PUT', 'A+S+M+K+;': 'MOVE', 'A+S+M+L+;': 'OPEN',
    'A+S+M+J+K+L': 'SEE', 'A+S+M+J+K+;': 'HEAR', 'A+S+M+J+L+;': 'FEEL',
    'A+S+M+K+L+;': 'CLOSE', 'A+S+M+J+K+L+;': 'TOUCH',

    # VERBS2 (S+C) - more action verbs
    'S+C+J': 'PLAY', 'S+C+K': 'WORK', 'S+C+L': 'REST', 'S+C+;': 'SLEEP',
    'S+C+J+K': 'WAKE', 'S+C+J+L': 'EAT', 'S+C+J+;': 'DRINK',
    'S+C+K+L': 'READ', 'S+C+K+;': 'WRITE', 'S+C+L+;': 'SPEAK',
    'S+C+J+K+L': 'LISTEN', 'S+C+J+K+;': 'WATCH', 'S+C+J+L+;': 'LEARN',
    'S+C+K+L+;': 'TEACH', 'S+C+J+K+L+;': 'PRACTICE',
    'S+C+M+J': 'RUN', 'S+C+M+K': 'WALK', 'S+C+M+L': 'SIT', 'S+C+M+;': 'STAND',
    'S+C+M+J+K': 'JUMP', 'S+C+M+J+L': 'CLIMB', 'S+C+M+J+;': 'FALL',
    'S+C+M+K+L': 'PUSH', 'S+C+M+K+;': 'PULL', 'S+C+M+L+;': 'HOLD',
    'S+C+M+J+K+L': 'DROP', 'S+C+M+J+K+;': 'THROW', 'S+C+M+J+L+;': 'CATCH',
    'S+C+M+K+L+;': 'CARRY', 'S+C+M+J+K+L+;': 'DRAG',

    # PEOPLE/PLACES/THINGS (D+S) - nouns
    'D+S+J': 'NAME', 'D+S+K': 'PERSON', 'D+S+L': 'PLACE', 'D+S+;': 'THING',
    'D+S+J+K': 'TEAM', 'D+S+J+L': 'COMPANY', 'D+S+J+;': 'GROUP',
    'D+S+K+L': 'PROJECT', 'D+S+K+;': 'MEETING', 'D+S+L+;': 'EVENT',
    'D+S+J+K+L': 'WORLD', 'D+S+J+K+;': 'HOME', 'D+S+J+L+;': 'OFFICE',
    'D+S+K+L+;': 'ROOM', 'D+S+J+K+L+;': 'BUILDING',
    'D+S+M+J': 'EMAIL', 'D+S+M+K': 'MESSAGE', 'D+S+M+L': 'PHONE', 'D+S+M+;': 'MONEY',
    'D+S+M+J+K': 'DOCUMENT', 'D+S+M+J+L': 'REPORT', 'D+S+M+J+;': 'TASK',
    'D+S+M+K+L': 'ISSUE', 'D+S+M+K+;': 'REQUEST', 'D+S+M+L+;': 'UPDATE',
    'D+S+M+J+K+L': 'SCREEN', 'D+S+M+J+K+;': 'BUTTON', 'D+S+M+J+L+;': 'WINDOW',
    'D+S+M+K+L+;': 'LINK', 'D+S+M+J+K+L+;': 'IMAGE',

    # TIME (A+D)
    'A+D+J': 'TODAY', 'A+D+K': 'TOMORROW', 'A+D+L': 'NOW', 'A+D+;': 'LATER',
    'A+D+J+K': 'SOON', 'A+D+J+L': 'YESTERDAY', 'A+D+J+;': 'ALWAYS',
    'A+D+K+L': 'TIME', 'A+D+K+;': 'DATE', 'A+D+L+;': 'MOMENT',
    'A+D+J+K+L': 'WEEK', 'A+D+J+K+;': 'MONTH', 'A+D+J+L+;': 'YEAR',
    'A+D+K+L+;': 'HOUR', 'A+D+J+K+L+;': 'MINUTE',
    'A+D+M+J': 'MORNING', 'A+D+M+K': 'AFTERNOON', 'A+D+M+L': 'EVENING', 'A+D+M+;': 'NIGHT',
    'A+D+M+J+K': 'NOON', 'A+D+M+J+L': 'MIDNIGHT', 'A+D+M+J+;': 'WEEKEND',
    'A+D+M+K+L': 'DAILY', 'A+D+M+K+;': 'WEEKLY', 'A+D+M+L+;': 'MONTHLY',
    'A+D+M+J+K+L': 'YEARLY', 'A+D+M+J+K+;': 'ONCE', 'A+D+M+J+L+;': 'TWICE',
    'A+D+M+K+L+;': 'OFTEN', 'A+D+M+J+K+L+;': 'RARELY',

    # STATES (F+D)
    'F+D+J': 'HAPPY', 'F+D+K': 'BUSY', 'F+D+L': 'READY', 'F+D+;': 'SURE',
    'F+D+J+K': 'AVAILABLE', 'F+D+J+L': 'INTERESTED', 'F+D+J+;': 'EXCITED',
    'F+D+K+L': 'URGENT', 'F+D+K+;': 'IMPORTANT', 'F+D+L+;': 'NECESSARY',
    'F+D+J+K+L': 'POSSIBLE', 'F+D+J+K+;': 'IMPOSSIBLE', 'F+D+J+L+;': 'REQUIRED',
    'F+D+K+L+;': 'OPTIONAL', 'F+D+J+K+L+;': 'RECOMMENDED',
    'F+D+M+J': 'SAD', 'F+D+M+K': 'ANGRY', 'F+D+M+L': 'TIRED', 'F+D+M+;': 'CONFUSED',
    'F+D+M+J+K': 'WORRIED', 'F+D+M+J+L': 'NERVOUS', 'F+D+M+J+;': 'CALM',
    'F+D+M+K+L': 'BORED', 'F+D+M+K+;': 'STUCK', 'F+D+M+L+;': 'LOST',
    'F+D+M+J+K+L': 'FOUND', 'F+D+M+J+K+;': 'BROKEN', 'F+D+M+J+L+;': 'FIXED',
    'F+D+M+K+L+;': 'PENDING', 'F+D+M+J+K+L+;': 'COMPLETE',

    # PRONOUNS (S+F)
    'S+F+J': 'I', 'S+F+K': 'YOU', 'S+F+L': 'WE', 'S+F+;': 'THEY',
    'S+F+J+K': 'HE', 'S+F+J+L': 'SHE', 'S+F+J+;': 'SOMEONE',
    'S+F+K+L': 'EVERYONE', 'S+F+K+;': 'ANYONE', 'S+F+L+;': 'NOONE',
    'S+F+M+J': 'MY', 'S+F+M+K': 'YOUR', 'S+F+M+L': 'OUR', 'S+F+M+;': 'THEIR',
    'S+F+M+J+K': 'HIS', 'S+F+M+J+L': 'HER', 'S+F+M+J+;': 'MYSELF',
    'S+F+M+K+L': 'ME', 'S+F+M+K+;': 'US', 'S+F+M+L+;': 'THEM',

    # NEGATION & MODALS (A+C)
    'A+C+J': 'NOT', 'A+C+K': 'CAN', 'A+C+L': 'WILL', 'A+C+;': 'SHOULD',
    'A+C+J+K': 'NEVER', 'A+C+J+L': 'CANNOT', 'A+C+J+;': 'WONT',
    'A+C+K+L': 'MUST', 'A+C+K+;': 'MIGHT', 'A+C+L+;': 'WOULD',
    'A+C+M+J': 'DONT', 'A+C+M+K': 'DIDNT', 'A+C+M+L': 'DOESNT', 'A+C+M+;': 'ISNT',
    'A+C+M+J+K': 'HAVENT', 'A+C+M+J+L': 'WASNT', 'A+C+M+J+;': 'WERENT',
    'A+C+M+K+L': 'COULDNT', 'A+C+M+K+;': 'SHOULDNT', 'A+C+M+L+;': 'WOULDNT',

    # PREPOSITIONS (F+C)
    'F+C+J': 'IN', 'F+C+K': 'ON', 'F+C+L': 'AT', 'F+C+;': 'BY',
    'F+C+J+K': 'OUT', 'F+C+J+L': 'UP', 'F+C+J+;': 'DOWN',
    'F+C+K+L': 'OVER', 'F+C+K+;': 'UNDER', 'F+C+L+;': 'THROUGH',
    'F+C+M+J': 'INTO', 'F+C+M+K': 'ONTO', 'F+C+M+L': 'NEAR', 'F+C+M+;': 'AROUND',
    'F+C+M+J+K': 'BETWEEN', 'F+C+M+J+L': 'BEHIND', 'F+C+M+J+;': 'ABOVE',
    'F+C+M+K+L': 'BELOW', 'F+C+M+K+;': 'BESIDE', 'F+C+M+L+;': 'ACROSS',

    # STYLE (D+C)
    'D+C+J': 'FORMAL', 'D+C+K': 'CASUAL', 'D+C+L': 'POLITE', 'D+C+;': 'DIRECT',
    'D+C+J+K': 'TECHNICAL', 'D+C+J+L': 'FRIENDLY', 'D+C+J+;': 'PROFESSIONAL',
    'D+C+K+L': 'BRIEF', 'D+C+K+;': 'DETAILED', 'D+C+L+;': 'AS_QUESTION',
    'D+C+J+K+L': 'AS_COMMAND', 'D+C+J+K+;': 'AS_REQUEST', 'D+C+J+L+;': 'AS_STATEMENT',
    'D+C+K+L+;': 'AS_LIST', 'D+C+J+K+L+;': 'AS_SUMMARY',
    'D+C+M+J': 'REPROMPT', 'D+C+M+K': 'URGENT_TONE', 'D+C+M+L': 'GENTLE', 'D+C+M+;': 'FIRM',
    'D+C+M+J+K': 'HUMOROUS', 'D+C+M+J+L': 'SERIOUS', 'D+C+M+J+;': 'EMPATHETIC',
    'D+C+M+K+L': 'CONFIDENT', 'D+C+M+K+;': 'HUMBLE', 'D+C+M+L+;': 'ENTHUSIASTIC',
    'D+C+M+J+K+L': 'SKEPTICAL', 'D+C+M+J+K+;': 'SUPPORTIVE', 'D+C+M+J+L+;': 'CRITICAL',
    'D+C+M+K+L+;': 'NEUTRAL', 'D+C+M+J+K+L+;': 'PERSUASIVE',

    # PRONOUNS extended (S+F)
    'S+F+J+K+L': 'SOMETHING', 'S+F+J+K+;': 'EVERYTHING', 'S+F+J+L+;': 'ANYTHING',
    'S+F+K+L+;': 'NOTHING', 'S+F+J+K+L+;': 'ITSELF',
    'S+F+M+J+K+L': 'HIMSELF', 'S+F+M+J+K+;': 'HERSELF', 'S+F+M+J+L+;': 'THEMSELVES',
    'S+F+M+K+L+;': 'OURSELVES', 'S+F+M+J+K+L+;': 'YOURSELF',

    # NEGATION extended (A+C)
    'A+C+J+K+L': 'ALWAYS', 'A+C+J+K+;': 'SOMETIMES', 'A+C+J+L+;': 'USUALLY',
    'A+C+K+L+;': 'BARELY', 'A+C+J+K+L+;': 'HARDLY',
    'A+C+M+J+K+L': 'ARENT', 'A+C+M+J+K+;': 'WONT_BE', 'A+C+M+J+L+;': 'CANT_BE',
    'A+C+M+K+L+;': 'MUSTNT', 'A+C+M+J+K+L+;': 'NEEDNT',

    # PREPOSITIONS extended (F+C)
    'F+C+J+K+L': 'WITHIN', 'F+C+J+K+;': 'THROUGHOUT', 'F+C+J+L+;': 'ALONG',
    'F+C+K+L+;': 'AGAINST', 'F+C+J+K+L+;': 'AMONG',
    'F+C+M+J+K+L': 'TOWARD', 'F+C+M+J+K+;': 'AWAY', 'F+C+M+J+L+;': 'APART',
    'F+C+M+K+L+;': 'TOGETHER', 'F+C+M+J+K+L+;': 'INSIDE',

    # SYMBOLS extended (A+F)
    'A+F+M+J+K+L+;': ';',

    # TECH (A+D+S) - programming/tech terms - using 3-key left combo
    'A+D+S+J': 'DEBUG', 'A+D+S+K': 'TEST', 'A+D+S+L': 'BUILD', 'A+D+S+;': 'DEPLOY',
    'A+D+S+J+K': 'COMMIT', 'A+D+S+J+L': 'PUSH', 'A+D+S+J+;': 'PULL',
    'A+D+S+K+L': 'MERGE', 'A+D+S+K+;': 'BRANCH', 'A+D+S+L+;': 'CLONE',
    'A+D+S+J+K+L': 'INSTALL', 'A+D+S+J+K+;': 'UNINSTALL', 'A+D+S+J+L+;': 'UPGRADE',
    'A+D+S+K+L+;': 'CONFIGURE', 'A+D+S+J+K+L+;': 'INITIALIZE',
    'A+D+S+M+J': 'SERVER', 'A+D+S+M+K': 'CLIENT', 'A+D+S+M+L': 'DATABASE', 'A+D+S+M+;': 'API',
    'A+D+S+M+J+K': 'ENDPOINT', 'A+D+S+M+J+L': 'REQUEST_NOUN', 'A+D+S+M+J+;': 'RESPONSE',
    'A+D+S+M+K+L': 'QUERY', 'A+D+S+M+K+;': 'CACHE', 'A+D+S+M+L+;': 'LOG',
    'A+D+S+M+J+K+L': 'VARIABLE', 'A+D+S+M+J+K+;': 'CONSTANT', 'A+D+S+M+J+L+;': 'PARAMETER',
    'A+D+S+M+K+L+;': 'ARGUMENT', 'A+D+S+M+J+K+L+;': 'EXCEPTION',
}

# Build normalized lookup (sort keys for consistent matching)
def _sort_keys(keys, order):
    return sorted(keys, key=lambda k: order.index(k) if k in order else 99)

def _normalize_chord(left_keys, right_keys):
    sl = _sort_keys(left_keys, LEFT_KEY_ORDER)
    sr = _sort_keys(right_keys, RIGHT_KEY_ORDER)
    return '+'.join(sl) + '+' + '+'.join(sr)

SEMANTICS_LOOKUP = {}
for chord, token in SEMANTICS.items():
    parts = chord.split('+')
    left = [p for p in parts if p in LEFT_KEY_ORDER]
    right = [p for p in parts if p in RIGHT_KEY_ORDER]
    norm = _normalize_chord(left, right)
    SEMANTICS_LOOKUP[norm] = token

# Reverse lookup for cheatsheet
TOKEN_TO_CHORD = {v: k for k, v in SEMANTICS.items()}


class ChordEngine:
    """State machine for chord detection in semantic/phonemic modes."""

    def __init__(self):
        self.held_keys = set()
        self.chord_buffer = set()
        self.chord_active = False
        self.token_buffer = []  # List of tokens (strings)
        self.mode = 'semantic'  # 'semantic' or 'text'
        self.text_buffer = []   # Characters typed in text mode

    def is_chord_key(self, key):
        return key in ALL_CHORD_KEYS

    def key_down(self, key):
        if key not in ALL_CHORD_KEYS:
            return
        if key in self.held_keys:
            return
        if not self.chord_active:
            self.chord_active = True
            self.chord_buffer.clear()
        self.held_keys.add(key)
        self.chord_buffer.add(key)

    def key_up(self, key):
        """Returns result when all keys released."""
        if key not in ALL_CHORD_KEYS:
            return None
        self.held_keys.discard(key)

        if self.chord_active and len(self.held_keys) == 0:
            result = self._fire_chord()
            self.chord_active = False
            self.chord_buffer.clear()
            return result
        return None

    def _get_codes(self):
        left = sum(1 << LEFT_KEYS[k] for k in self.chord_buffer if k in LEFT_KEYS)
        right = sum(1 << RIGHT_KEYS[k] for k in self.chord_buffer if k in RIGHT_KEYS)
        return left, right

    def _get_chord_key(self):
        left = [k.upper() for k in self.chord_buffer if k in LEFT_KEYS]
        right = [k.upper() if k != ';' else ';' for k in self.chord_buffer if k in RIGHT_KEYS]
        if not left or not right:
            return None
        return _normalize_chord(left, right)

    def _fire_chord(self):
        left_code, right_code = self._get_codes()

        # Control: C+M = backspace
        if left_code == 16 and right_code == 16:
            return ('backspace',)

        # Control: C+; = enter (left thumb + right pinky)
        if left_code == 16 and right_code == 1:  # C=16, ;=1
            return ('enter',)

        # Control: S+C+M = toggle mode
        if left_code == 18 and right_code == 16:  # S+C = 2+16=18, M=16
            return ('toggle_mode',)

        # Control: C+M+K = show cheatsheet
        if left_code == 16 and right_code == 20:  # C=16, M+K=16+4=20
            return ('cheatsheet',)

        if self.mode == 'semantic':
            return self._fire_semantic()
        else:
            return self._fire_text_mode(left_code, right_code)

    def _fire_semantic(self):
        chord_key = self._get_chord_key()
        if chord_key and chord_key in SEMANTICS_LOOKUP:
            token = SEMANTICS_LOOKUP[chord_key]
            self.token_buffer.append(token)
            return ('token', token)
        return ('invalid',)

    def _fire_text_mode(self, left_code, right_code):
        # Text mode: type the chord keys as regular characters
        # This handles cases where user presses chord keys in text mode
        keys = []
        for k in self.chord_buffer:
            if k == ';':
                keys.append(';')
            else:
                keys.append(k.lower())
        if keys:
            return ('type_chars', keys)
        return ('invalid',)

    def toggle_mode(self):
        """Switch between semantic and text modes.

        No markers needed - AI distinguishes by case:
        - UPPERCASE = semantic tokens
        - lowercase = regular text (typed via QWERTY)
        """
        if self.mode == 'semantic':
            # Switching to text mode - finalize any pending text
            self.mode = 'text'
        else:
            # Switching back to semantic - finalize typed text as token
            if self.text_buffer:
                text = ''.join(self.text_buffer)
                self.token_buffer.append(text)
                self.text_buffer.clear()
            self.mode = 'semantic'
        return self.mode

    def add_text_char(self, char):
        """Add a character typed in text mode."""
        self.text_buffer.append(char)

    def pop_text_char(self):
        """Remove last character from text buffer. Returns True if removed."""
        if self.text_buffer:
            self.text_buffer.pop()
            return True
        return False

    def get_text_buffer(self):
        """Get current text being typed in text mode."""
        return ''.join(self.text_buffer)

    def pop_last_token(self):
        """Remove last token. Returns (token, is_special)."""
        if self.token_buffer:
            token = self.token_buffer.pop()
            return token, False
        return None, False

    def flush_buffer(self):
        """Get all tokens for AI conversion. Returns (text, char_count)."""
        # Include any pending text from text mode
        if self.text_buffer:
            text = ''.join(self.text_buffer)
            self.token_buffer.append(text)
            self.text_buffer.clear()

        if not self.token_buffer:
            return '', 0
        # Format: tokens separated by spaces
        text = ' '.join(self.token_buffer)
        char_count = len(text)
        self.token_buffer.clear()
        return text, char_count

    def get_buffer_display(self):
        """Get buffer for display."""
        parts = list(self.token_buffer)
        if self.text_buffer:
            parts.append(''.join(self.text_buffer) + '_')  # Show cursor
        return ' '.join(parts)

    def reset(self):
        self.held_keys.clear()
        self.chord_buffer.clear()
        self.chord_active = False
        self.token_buffer.clear()
        self.text_buffer.clear()
        self.mode = 'semantic'

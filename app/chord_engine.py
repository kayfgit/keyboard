"""Chord engine: semantic + text modes with token output.

Outputs tokens as typed text, AI replaces on all-10-keys chord.
"""

# Bit positions for each key
LEFT_KEYS = {'c': 4, 'f': 3, 'd': 2, 's': 1, 'a': 0}
RIGHT_KEYS = {'m': 4, 'j': 3, 'k': 2, 'l': 1, ';': 0}
LEFT_KEY_ORDER = ['A', 'S', 'D', 'F', 'C']
RIGHT_KEY_ORDER = ['M', 'J', 'K', 'L', ';']

ALL_CHORD_KEYS = set(LEFT_KEYS) | set(RIGHT_KEYS)

# =============================================================================
# SEMANTIC VOCABULARY - Reorganized v2
# =============================================================================
# Categories:
#   A       = VERBS-CORE (abstract manipulation)
#   S       = NOUNS (concepts, abstract things)
#   D       = MODIFIERS (adjectives, adverbs, intensifiers)
#   F       = CONNECTORS (logic, conjunctions)
#   C       = RESPONSES (dialog flow)
#   A+S     = VERBS-SOCIAL (communication, interpersonal)
#   A+D     = TIME (temporal, sequence)
#   A+F     = SYMBOLS (numbers, punctuation)
#   A+C     = MODALS (can, will, should, frequency)
#   S+D     = NOUNS-THINGS (objects, places)
#   S+F     = PRONOUNS (personal, quantifiers)
#   S+C     = VERBS-PHYSICAL (body actions)
#   D+F     = STATES (emotions, conditions)
#   D+C     = STYLE (tone modifiers)
#   F+C     = PREPOSITIONS (spatial, relational)
#   A+D+S   = TECH (programming)
#
# Right-hand positions are frequency-based:
#   J = most common, K = second, L = third, ; = fourth
#   M extends each category with 15 more tokens
# =============================================================================

SEMANTICS = {
    # =========================================================================
    # A — VERBS-CORE (abstract manipulation)
    # =========================================================================
    'A+J': 'MAKE', 'A+K': 'CHANGE', 'A+L': 'ADD', 'A+;': 'REMOVE',
    'A+J+K': 'FIND', 'A+J+L': 'SHOW', 'A+J+;': 'FIX',
    'A+K+L': 'USE', 'A+K+;': 'GET', 'A+L+;': 'GIVE',
    'A+J+K+L': 'KEEP', 'A+J+K+;': 'TAKE', 'A+J+L+;': 'TRY',
    'A+K+L+;': 'PUT', 'A+J+K+L+;': 'MOVE',
    'A+M+J': 'HELP', 'A+M+K': 'CHECK', 'A+M+L': 'OPEN', 'A+M+;': 'CLOSE',
    'A+M+J+K': 'THINK', 'A+M+J+L': 'LIST', 'A+M+J+;': 'COMBINE',
    'A+M+K+L': 'SPLIT', 'A+M+K+;': 'COMPARE', 'A+M+L+;': 'IMPROVE',
    'A+M+J+K+L': 'EXPLAIN', 'A+M+J+K+;': 'ANALYZE', 'A+M+J+L+;': 'SUMMARIZE',
    'A+M+K+L+;': 'SIMPLIFY', 'A+M+J+K+L+;': 'EXPAND',

    # =========================================================================
    # S — NOUNS (concepts, abstract things)
    # =========================================================================
    'S+J': 'IT', 'S+K': 'THIS', 'S+L': 'THAT', 'S+;': 'THING',
    'S+J+K': 'IDEA', 'S+J+L': 'WAY', 'S+J+;': 'PART',
    'S+K+L': 'POINT', 'S+K+;': 'REASON', 'S+L+;': 'PROBLEM',
    'S+J+K+L': 'SOLUTION', 'S+J+K+;': 'QUESTION', 'S+J+L+;': 'ANSWER',
    'S+K+L+;': 'EXAMPLE', 'S+J+K+L+;': 'RESULT',
    'S+M+J': 'FILE', 'S+M+K': 'CODE', 'S+M+L': 'DATA', 'S+M+;': 'TEXT',
    'S+M+J+K': 'FUNCTION', 'S+M+J+L': 'LIST', 'S+M+J+;': 'NAME',
    'S+M+K+L': 'STEP', 'S+M+K+;': 'OPTION', 'S+M+L+;': 'ERROR',
    'S+M+J+K+L': 'INPUT', 'S+M+J+K+;': 'OUTPUT', 'S+M+J+L+;': 'CONTENT',
    'S+M+K+L+;': 'CONTEXT', 'S+M+J+K+L+;': 'DETAIL',

    # =========================================================================
    # D — MODIFIERS (adjectives, adverbs, intensifiers)
    # =========================================================================
    'D+J': 'GOOD', 'D+K': 'BAD', 'D+L': 'MORE', 'D+;': 'LESS',
    'D+J+K': 'NEW', 'D+J+L': 'OLD', 'D+J+;': 'SAME',
    'D+K+L': 'DIFFERENT', 'D+K+;': 'OTHER', 'D+L+;': 'ALL',
    'D+J+K+L': 'SIMPLE', 'D+J+K+;': 'COMPLEX', 'D+J+L+;': 'MAIN',
    'D+K+L+;': 'GENERAL', 'D+J+K+L+;': 'SPECIFIC',
    'D+M+J': 'FAST', 'D+M+K': 'SLOW', 'D+M+L': 'BIG', 'D+M+;': 'SMALL',
    'D+M+J+K': 'LONG', 'D+M+J+L': 'SHORT', 'D+M+J+;': 'CLEAR',
    'D+M+K+L': 'CORRECT', 'D+M+K+;': 'WRONG', 'D+M+L+;': 'SIMILAR',
    'D+M+J+K+L': 'EXACT', 'D+M+J+K+;': 'ENOUGH', 'D+M+J+L+;': 'VERY',
    'D+M+K+L+;': 'TOO', 'D+M+J+K+L+;': 'QUITE',

    # =========================================================================
    # F — CONNECTORS (logic, conjunctions)
    # =========================================================================
    'F+J': 'AND', 'F+K': 'OR', 'F+L': 'BUT', 'F+;': 'SO',
    'F+J+K': 'IF', 'F+J+L': 'THEN', 'F+J+;': 'BECAUSE',
    'F+K+L': 'WITH', 'F+K+;': 'WITHOUT', 'F+L+;': 'FOR',
    'F+J+K+L': 'TO', 'F+J+K+;': 'FROM', 'F+J+L+;': 'AS',
    'F+K+L+;': 'LIKE', 'F+J+K+L+;': 'ABOUT',
    'F+M+J': 'ALSO', 'F+M+K': 'HOWEVER', 'F+M+L': 'INSTEAD', 'F+M+;': 'RATHER',
    'F+M+J+K': 'WHEN', 'F+M+J+L': 'WHERE', 'F+M+J+;': 'WHILE',
    'F+M+K+L': 'BEFORE', 'F+M+K+;': 'AFTER', 'F+M+L+;': 'ALTHOUGH',
    'F+M+J+K+L': 'UNLESS', 'F+M+J+K+;': 'UNTIL', 'F+M+J+L+;': 'SINCE',
    'F+M+K+L+;': 'WHETHER', 'F+M+J+K+L+;': 'THAN',

    # =========================================================================
    # C — RESPONSES (dialog flow)
    # =========================================================================
    'C+J': 'YES', 'C+K': 'NO', 'C+L': 'OK', 'C+;': 'THANKS',
    'C+J+K': 'PLEASE', 'C+J+L': 'SORRY', 'C+J+;': 'WHAT',
    'C+K+L': 'WHY', 'C+K+;': 'HOW', 'C+L+;': 'WHICH',
    'C+J+K+L': 'WHO', 'C+J+K+;': 'WHEN', 'C+J+L+;': 'WHERE',
    'C+K+L+;': 'MAYBE', 'C+J+K+L+;': 'AGAIN',
    'C+M+J': 'WAIT', 'C+M+K': 'DONE', 'C+M+L': 'CONTINUE', 'C+M+;': 'STOP',
    'C+M+J+K': 'UNDO', 'C+M+J+L': 'SKIP', 'C+M+J+;': 'FOCUS',
    'C+M+K+L': 'IGNORE', 'C+M+K+;': 'REMEMBER', 'C+M+L+;': 'FORGET',
    'C+M+J+K+L': 'CONFIRM', 'C+M+J+K+;': 'PERFECT', 'C+M+J+L+;': 'ALMOST',
    'C+M+K+L+;': 'EXACTLY',

    # =========================================================================
    # A+S — VERBS-SOCIAL (communication, interpersonal)
    # =========================================================================
    'A+S+J': 'ASK', 'A+S+K': 'TELL', 'A+S+L': 'SAY', 'A+S+;': 'KNOW',
    'A+S+J+K': 'WANT', 'A+S+J+L': 'NEED', 'A+S+J+;': 'LIKE',
    'A+S+K+L': 'SEND', 'A+S+K+;': 'CALL', 'A+S+L+;': 'MEET',
    'A+S+J+K+L': 'START', 'A+S+J+K+;': 'FINISH', 'A+S+J+L+;': 'GREET',
    'A+S+K+L+;': 'INVITE', 'A+S+J+K+L+;': 'SCHEDULE',
    'A+S+M+J': 'GO', 'A+S+M+K': 'COME', 'A+S+M+L': 'LEAVE', 'A+S+M+;': 'STAY',
    'A+S+M+J+K': 'RETURN', 'A+S+M+J+L': 'ARRIVE', 'A+S+M+J+;': 'BRING',
    'A+S+M+K+L': 'SEE', 'A+S+M+K+;': 'HEAR', 'A+S+M+L+;': 'FEEL',
    'A+S+M+J+K+L': 'AGREE', 'A+S+M+J+K+;': 'ACCEPT', 'A+S+M+J+L+;': 'REJECT',
    'A+S+M+K+L+;': 'CANCEL',

    # =========================================================================
    # A+D — TIME (temporal, sequence)
    # =========================================================================
    'A+D+J': 'NOW', 'A+D+K': 'TODAY', 'A+D+L': 'TOMORROW', 'A+D+;': 'YESTERDAY',
    'A+D+J+K': 'SOON', 'A+D+J+L': 'LATER', 'A+D+J+;': 'FIRST',
    'A+D+K+L': 'LAST', 'A+D+K+;': 'NEXT', 'A+D+L+;': 'PREVIOUS',
    'A+D+J+K+L': 'BEFORE', 'A+D+J+K+;': 'AFTER', 'A+D+J+L+;': 'DURING',
    'A+D+K+L+;': 'RECENTLY', 'A+D+J+K+L+;': 'FINALLY',
    'A+D+M+J': 'TIME', 'A+D+M+K': 'DATE', 'A+D+M+L': 'WEEK', 'A+D+M+;': 'MONTH',
    'A+D+M+J+K': 'YEAR', 'A+D+M+J+L': 'HOUR', 'A+D+M+J+;': 'MINUTE',
    'A+D+M+K+L': 'MORNING', 'A+D+M+K+;': 'AFTERNOON', 'A+D+M+L+;': 'EVENING',
    'A+D+M+J+K+L': 'NIGHT', 'A+D+M+J+K+;': 'WEEKEND', 'A+D+M+J+L+;': 'DAILY',
    'A+D+M+K+L+;': 'WEEKLY', 'A+D+M+J+K+L+;': 'MONTHLY',

    # =========================================================================
    # A+F — SYMBOLS (numbers, punctuation)
    # =========================================================================
    'A+F+J': '1', 'A+F+K': '2', 'A+F+L': '3', 'A+F+;': '4',
    'A+F+J+K': '5', 'A+F+J+L': '6', 'A+F+J+;': '7',
    'A+F+K+L': '8', 'A+F+K+;': '9', 'A+F+L+;': '0',
    'A+F+J+K+L': '.', 'A+F+J+K+;': ',', 'A+F+J+L+;': '?',
    'A+F+K+L+;': '!', 'A+F+J+K+L+;': ':',
    'A+F+M+J': '-', 'A+F+M+K': '_', 'A+F+M+L': '/', 'A+F+M+;': '@',
    'A+F+M+J+K': '#', 'A+F+M+J+L': '$', 'A+F+M+J+;': '%',
    'A+F+M+K+L': '&', 'A+F+M+K+;': '*', 'A+F+M+L+;': '+',
    'A+F+M+J+K+L': '=', 'A+F+M+J+K+;': '(', 'A+F+M+J+L+;': ')',
    'A+F+M+K+L+;': '"', 'A+F+M+J+K+L+;': ';',

    # =========================================================================
    # A+C — MODALS (can, will, should, frequency adverbs)
    # =========================================================================
    'A+C+J': 'NOT', 'A+C+K': 'CAN', 'A+C+L': 'WILL', 'A+C+;': 'SHOULD',
    'A+C+J+K': 'WOULD', 'A+C+J+L': 'COULD', 'A+C+J+;': 'MIGHT',
    'A+C+K+L': 'MUST', 'A+C+K+;': 'MAY', 'A+C+L+;': 'SHALL',
    'A+C+J+K+L': 'ALWAYS', 'A+C+J+K+;': 'NEVER', 'A+C+J+L+;': 'SOMETIMES',
    'A+C+K+L+;': 'USUALLY', 'A+C+J+K+L+;': 'OFTEN',
    'A+C+M+J': 'RARELY', 'A+C+M+K': 'HARDLY', 'A+C+M+L': 'BARELY', 'A+C+M+;': 'ALREADY',
    'A+C+M+J+K': 'STILL', 'A+C+M+J+L': 'YET', 'A+C+M+J+;': 'JUST',
    'A+C+M+K+L': 'ONLY', 'A+C+M+K+;': 'EVEN',

    # =========================================================================
    # S+D — NOUNS-THINGS (objects, places)
    # =========================================================================
    'S+D+J': 'PLACE', 'S+D+K': 'PERSON', 'S+D+L': 'HOME', 'S+D+;': 'OFFICE',
    'S+D+J+K': 'ROOM', 'S+D+J+L': 'BUILDING', 'S+D+J+;': 'WORLD',
    'S+D+K+L': 'PHONE', 'S+D+K+;': 'EMAIL', 'S+D+L+;': 'MESSAGE',
    'S+D+J+K+L': 'DOCUMENT', 'S+D+J+K+;': 'REPORT', 'S+D+J+L+;': 'PROJECT',
    'S+D+K+L+;': 'MEETING', 'S+D+J+K+L+;': 'TEAM',
    'S+D+M+J': 'COMPANY', 'S+D+M+K': 'GROUP', 'S+D+M+L': 'EVENT', 'S+D+M+;': 'TASK',
    'S+D+M+J+K': 'ISSUE', 'S+D+M+J+L': 'REQUEST', 'S+D+M+J+;': 'UPDATE',
    'S+D+M+K+L': 'MONEY', 'S+D+M+K+;': 'SCREEN', 'S+D+M+L+;': 'BUTTON',
    'S+D+M+J+K+L': 'WINDOW', 'S+D+M+J+K+;': 'LINK', 'S+D+M+J+L+;': 'IMAGE',
    'S+D+M+K+L+;': 'PAGE', 'S+D+M+J+K+L+;': 'SITE',

    # =========================================================================
    # S+F — PRONOUNS (personal, quantifiers)
    # =========================================================================
    'S+F+J': 'I', 'S+F+K': 'YOU', 'S+F+L': 'WE', 'S+F+;': 'THEY',
    'S+F+J+K': 'HE', 'S+F+J+L': 'SHE', 'S+F+J+;': 'IT',
    'S+F+K+L': 'THIS', 'S+F+K+;': 'THAT', 'S+F+L+;': 'WHO',
    'S+F+J+K+L': 'SOMEONE', 'S+F+J+K+;': 'EVERYONE', 'S+F+J+L+;': 'ANYONE',
    'S+F+K+L+;': 'NOONE', 'S+F+J+K+L+;': 'SOMETHING',
    'S+F+M+J': 'MY', 'S+F+M+K': 'YOUR', 'S+F+M+L': 'OUR', 'S+F+M+;': 'THEIR',
    'S+F+M+J+K': 'HIS', 'S+F+M+J+L': 'HER', 'S+F+M+J+;': 'ME',
    'S+F+M+K+L': 'US', 'S+F+M+K+;': 'THEM', 'S+F+M+L+;': 'SOME',
    'S+F+M+J+K+L': 'MANY', 'S+F+M+J+K+;': 'FEW', 'S+F+M+J+L+;': 'NONE',
    'S+F+M+K+L+;': 'EACH', 'S+F+M+J+K+L+;': 'BOTH',

    # =========================================================================
    # S+C — VERBS-PHYSICAL (body actions)
    # =========================================================================
    'S+C+J': 'DO', 'S+C+K': 'HAVE', 'S+C+L': 'BE', 'S+C+;': 'GET',
    'S+C+J+K': 'WORK', 'S+C+J+L': 'PLAY', 'S+C+J+;': 'REST',
    'S+C+K+L': 'SLEEP', 'S+C+K+;': 'WAKE', 'S+C+L+;': 'EAT',
    'S+C+J+K+L': 'DRINK', 'S+C+J+K+;': 'RUN', 'S+C+J+L+;': 'WALK',
    'S+C+K+L+;': 'SIT', 'S+C+J+K+L+;': 'STAND',
    'S+C+M+J': 'READ', 'S+C+M+K': 'WRITE', 'S+C+M+L': 'SPEAK', 'S+C+M+;': 'LISTEN',
    'S+C+M+J+K': 'WATCH', 'S+C+M+J+L': 'LEARN', 'S+C+M+J+;': 'TEACH',
    'S+C+M+K+L': 'HOLD', 'S+C+M+K+;': 'DROP', 'S+C+M+L+;': 'CARRY',
    'S+C+M+J+K+L': 'PUSH', 'S+C+M+J+K+;': 'PULL', 'S+C+M+J+L+;': 'THROW',
    'S+C+M+K+L+;': 'CATCH', 'S+C+M+J+K+L+;': 'TOUCH',

    # =========================================================================
    # D+F — STATES (emotions, conditions)
    # =========================================================================
    'D+F+J': 'READY', 'D+F+K': 'BUSY', 'D+F+L': 'SURE', 'D+F+;': 'HAPPY',
    'D+F+J+K': 'SAD', 'D+F+J+L': 'TIRED', 'D+F+J+;': 'ANGRY',
    'D+F+K+L': 'WORRIED', 'D+F+K+;': 'CONFUSED', 'D+F+L+;': 'NERVOUS',
    'D+F+J+K+L': 'CALM', 'D+F+J+K+;': 'EXCITED', 'D+F+J+L+;': 'BORED',
    'D+F+K+L+;': 'STUCK', 'D+F+J+K+L+;': 'LOST',
    'D+F+M+J': 'AVAILABLE', 'D+F+M+K': 'INTERESTED', 'D+F+M+L': 'IMPORTANT', 'D+F+M+;': 'URGENT',
    'D+F+M+J+K': 'NECESSARY', 'D+F+M+J+L': 'REQUIRED', 'D+F+M+J+;': 'OPTIONAL',
    'D+F+M+K+L': 'POSSIBLE', 'D+F+M+K+;': 'RECOMMENDED', 'D+F+M+L+;': 'PENDING',
    'D+F+M+J+K+L': 'COMPLETE', 'D+F+M+J+K+;': 'BROKEN', 'D+F+M+J+L+;': 'FIXED',
    'D+F+M+K+L+;': 'FOUND',

    # =========================================================================
    # D+C — STYLE (tone modifiers)
    # =========================================================================
    'D+C+J': 'FORMAL', 'D+C+K': 'CASUAL', 'D+C+L': 'POLITE', 'D+C+;': 'DIRECT',
    'D+C+J+K': 'BRIEF', 'D+C+J+L': 'DETAILED', 'D+C+J+;': 'FRIENDLY',
    'D+C+K+L': 'PROFESSIONAL', 'D+C+K+;': 'TECHNICAL', 'D+C+L+;': 'SIMPLE',
    'D+C+J+K+L': 'AS_QUESTION', 'D+C+J+K+;': 'AS_COMMAND', 'D+C+J+L+;': 'AS_REQUEST',
    'D+C+K+L+;': 'AS_LIST', 'D+C+J+K+L+;': 'AS_SUMMARY',
    'D+C+M+J': 'GENTLE', 'D+C+M+K': 'FIRM', 'D+C+M+L': 'SERIOUS', 'D+C+M+;': 'HUMOROUS',
    'D+C+M+J+K': 'CONFIDENT', 'D+C+M+J+L': 'HUMBLE', 'D+C+M+J+;': 'ENTHUSIASTIC',
    'D+C+M+K+L': 'EMPATHETIC', 'D+C+M+K+;': 'SUPPORTIVE', 'D+C+M+L+;': 'CRITICAL',
    'D+C+M+J+K+L': 'SKEPTICAL', 'D+C+M+J+K+;': 'PERSUASIVE', 'D+C+M+J+L+;': 'NEUTRAL',
    'D+C+M+K+L+;': 'URGENT_TONE', 'D+C+M+J+K+L+;': 'REPROMPT',

    # =========================================================================
    # F+C — PREPOSITIONS (spatial, relational)
    # =========================================================================
    'F+C+J': 'IN', 'F+C+K': 'ON', 'F+C+L': 'AT', 'F+C+;': 'TO',
    'F+C+J+K': 'FROM', 'F+C+J+L': 'WITH', 'F+C+J+;': 'BY',
    'F+C+K+L': 'FOR', 'F+C+K+;': 'OF', 'F+C+L+;': 'ABOUT',
    'F+C+J+K+L': 'UP', 'F+C+J+K+;': 'DOWN', 'F+C+J+L+;': 'OUT',
    'F+C+K+L+;': 'INTO', 'F+C+J+K+L+;': 'THROUGH',
    'F+C+M+J': 'OVER', 'F+C+M+K': 'UNDER', 'F+C+M+L': 'BETWEEN', 'F+C+M+;': 'AROUND',
    'F+C+M+J+K': 'BEHIND', 'F+C+M+J+L': 'ABOVE', 'F+C+M+J+;': 'BELOW',
    'F+C+M+K+L': 'BESIDE', 'F+C+M+K+;': 'NEAR', 'F+C+M+L+;': 'ACROSS',
    'F+C+M+J+K+L': 'ALONG', 'F+C+M+J+K+;': 'TOWARD', 'F+C+M+J+L+;': 'AGAINST',
    'F+C+M+K+L+;': 'HERE', 'F+C+M+J+K+L+;': 'THERE',

    # =========================================================================
    # A+D+S — TECH (programming)
    # =========================================================================
    'A+D+S+J': 'DEBUG', 'A+D+S+K': 'TEST', 'A+D+S+L': 'BUILD', 'A+D+S+;': 'RUN',
    'A+D+S+J+K': 'DEPLOY', 'A+D+S+J+L': 'COMMIT', 'A+D+S+J+;': 'PUSH',
    'A+D+S+K+L': 'PULL', 'A+D+S+K+;': 'MERGE', 'A+D+S+L+;': 'BRANCH',
    'A+D+S+J+K+L': 'INSTALL', 'A+D+S+J+K+;': 'UPDATE', 'A+D+S+J+L+;': 'UPGRADE',
    'A+D+S+K+L+;': 'CONFIGURE', 'A+D+S+J+K+L+;': 'INITIALIZE',
    'A+D+S+M+J': 'SERVER', 'A+D+S+M+K': 'CLIENT', 'A+D+S+M+L': 'DATABASE', 'A+D+S+M+;': 'API',
    'A+D+S+M+J+K': 'ENDPOINT', 'A+D+S+M+J+L': 'REQUEST', 'A+D+S+M+J+;': 'RESPONSE',
    'A+D+S+M+K+L': 'QUERY', 'A+D+S+M+K+;': 'CACHE', 'A+D+S+M+L+;': 'LOG',
    'A+D+S+M+J+K+L': 'VARIABLE', 'A+D+S+M+J+K+;': 'FUNCTION', 'A+D+S+M+J+L+;': 'CLASS',
    'A+D+S+M+K+L+;': 'ERROR', 'A+D+S+M+J+K+L+;': 'EXCEPTION',
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
    """State machine for chord detection in semantic/text modes."""

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

        # Control: All 10 keys = send to AI
        if left_code == 31 and right_code == 31:  # All keys: 1+2+4+8+16=31
            return ('send_ai',)

        # Control: C+; = backspace (left thumb + right pinky)
        if left_code == 16 and right_code == 1:  # C=16, ;=1
            return ('backspace',)

        # Control: C+M = enter (both thumbs)
        if left_code == 16 and right_code == 16:  # C=16, M=16
            return ('enter',)

        # Control: C+J = search popup (left thumb + right index)
        if left_code == 16 and right_code == 8:  # C=16, J=8
            return ('search',)

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

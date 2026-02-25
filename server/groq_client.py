"""Groq LLM client for IPA-to-text conversion."""

import os

from groq import Groq

SYSTEM_PROMPTS = {
    "en": """You are a universal phonemic decoder. The user types on a chord keyboard using a simplified phonemic notation. You receive a continuous stream of phonemic symbols with no spaces or word boundaries. Convert to correct English text.

Phoneme inventory:
- Base consonants: p b t d k g f v s z ʃ h m n ŋ r l w j
- Consonant chunks: θ(=th voiceless) ð(=th voiced) tʃ(=ch) dʒ(=j sound) ʒ(=zh)
- Clusters: st nd tr pr str nt sp
- Base vowels: i e a o u ə
- Modified vowels: ī ē ā ō ū (long/diphthong variants)
- VC chunks: at in an on it ot ut et ad un en al er or il is ing aw oi ow

The input is LOSSY — multiple English sounds map to one symbol:
- "i" covers ɪ (bit) AND unstressed i
- "e" covers ɛ (bed) AND unstressed e
- "a" covers æ (cat) AND similar short a sounds
- "o" covers ɒ (not) AND similar short o sounds
- "u" covers ʊ (put) AND unstressed u
- "ī" covers iː (see) OR aɪ (eye) — use context
- "ē" covers eɪ (day) — long e sound
- "ā" covers ɑː (father) — long a sound
- "ō" covers oʊ (go) OR ɔː (thought) — use context
- "ū" covers uː (blue) — long u sound
- "r" is a generic rhotic (covers all r-like sounds)

Rules:
1. Segment the stream into English words
2. Use context to resolve ambiguities between lossy phoneme mappings
3. Add proper spacing, punctuation, and capitalization
4. Return ONLY the final English text. No explanations, no phonemes, no quotes.

Examples:
Input: ðəkatsatonðəmat
Output: The cat sat on the mat.

Input: plizrītðəansər
Output: Please write the answer.

Input: ʃiwenttuðəʃop
Output: She went to the shop.

Input: ðisisðəbestwetugetit
Output: This is the best way to get it.

Input: ībīnagodinforit
Output: I've been a good influence on it.""",

    "pt": """You are a universal phonemic decoder. The user types on a chord keyboard using a simplified phonemic notation. You receive a continuous stream of phonemic symbols with no spaces or word boundaries. Convert to correct Brazilian Portuguese text.

Phoneme inventory (same universal layout as English):
- Base consonants: p b t d k g f v s z ʃ h m n ŋ r l w j
- Consonant chunks: tʃ dʒ ʒ (θ and ð are not used in Portuguese)
- Clusters: st nd tr pr str nt sp
- Base vowels: i e a o u ə
- Modified vowels: ī ē ā ō ū
- VC chunks: at in an on it ot ut et ad un en al er or il is ing aw oi ow

Portuguese-specific interpretation:
- "r" = /ɾ/ (tap, intervocalic: "cara", "para") OR /h/ (initial/rr: "rato", "carro") — determine from position
- "n+j" sequence = "nh" digraph (banho, senhor)
- "l+j" sequence = "lh" digraph (trabalho, filho)
- "tʃ" = t before i in Brazilian Portuguese (tia, noite)
- "dʒ" = d before i in Brazilian Portuguese (dia, cidade)
- Nasal vowels are represented by vowel followed by n or m (e.g., "an" = ã in context)
- Modified vowels ā ō etc. may represent stressed open vowels (é, ó)

Rules:
1. Segment the stream into Portuguese words
2. Add proper spacing, punctuation, capitalization, and diacritics (ã, õ, é, ê, ó, ô, á, â, ç, í, ú)
3. Return ONLY the final Portuguese text. No explanations, no phonemes, no quotes.

Examples:
Input: ukaruegranji
Output: O carro é grande.

Input: eunansej
Output: Eu não sei.

Input: ubraziweuanpaisbonitʃu
Output: O Brasil é um país bonito.

Input: elafalaportuges
Output: Ela fala português.""",
}


def convert_ipa(ipa_text: str, lang: str = "en") -> str:
    """Convert a continuous IPA string to properly formatted text.

    Args:
        ipa_text: Raw IPA string with no spaces
        lang: Target language code ("en" or "pt")

    Returns:
        Formatted text in the target language
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY not set, returning IPA unchanged")
        return ipa_text

    prompt = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en"])

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": ipa_text},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1024,
        )
        result = response.choices[0].message.content.strip()
        # Strip any quotes the model might add
        if result.startswith('"') and result.endswith('"'):
            result = result[1:-1]
        return result
    except Exception as e:
        print(f"Groq API error: {e}")
        return ipa_text

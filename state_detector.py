import re
import language_tool_python
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize

# Ensure punkt tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Set the nltk data path explicitly (optional but safe)
nltk.data.path.append("C:/nltk_data")  # Adjust path if needed

# Initialize the grammar checker
tool = language_tool_python.LanguageTool('en-US')


def detect_states(text):
    """
    Analyze the input text and return a list of detected states
    indicating quality or correction needs.
    """
    states = []

    # --- S1: Long Sentences (over 25 words)
    sentences = sent_tokenize(text)
    long_sentences = [s for s in sentences if len(s.split()) > 25]
    if long_sentences:
        states.append("S1")

    # --- S2: Passive Voice
    matches = tool.check(text)
    passive_matches = [m for m in matches if "passive voice" in m.message.lower()]
    if passive_matches:
        states.append("S2")

    # --- S3: Grammar Issues (more than ~5%)
    words = text.lower().split()
    if len(matches) > max(2, len(words) // 20):
        states.append("S3")

    # --- S4: Repetition (same word repeated too often)
    word_counts = Counter(words)
    repeated_words = [w for w, c in word_counts.items() if c > 5 and len(w) > 3]
    if repeated_words:
        states.append("S4")

    # --- S5: No issues found = High Quality
    if not states:
        states.append("S5")

    return states

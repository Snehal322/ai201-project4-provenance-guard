import re
import statistics

# 0.0  → human-like

# 1.0 → AI-like

def stylometric_score(text):

    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    words = re.findall(r"\b\w+\b", text.lower())

    if len(words) == 0:
        return 0.5

    # ---------- Feature 1 ----------
    # Type Token Ratio

    ttr = len(set(words)) / len(words)

    # ---------- Feature 2 ----------
    # Sentence Length Variance

    sentence_lengths = [len(s.split()) for s in sentences]

    if len(sentence_lengths) > 1:
        variance = statistics.pvariance(sentence_lengths)
    else:
        variance = 0

    # ---------- Feature 3 ----------
    # Average Sentence Length

    avg_len = sum(sentence_lengths) / len(sentence_lengths)

    score = 0

    if ttr < 0.45:
        score += 0.4

    if variance < 20:
        score += 0.3

    if avg_len > 20:
        score += 0.3

    return round(min(score,1),2)
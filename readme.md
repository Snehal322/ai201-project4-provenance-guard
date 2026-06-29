## Project Overview

Provenance Guard is a backend system that helps creative platforms estimate whether submitted text is more likely to be human-written or AI-generated. Rather than making a binary decision, the system combines multiple detection signals into a confidence score, displays a transparency label to readers, records every decision in an audit log, and allows creators to appeal classifications they believe are incorrect.

The system is designed to prioritize transparency over certainty by explicitly communicating uncertainty and providing an appeals process for disputed classifications.

---------------

# Features

   - POST `/submit` endpoint for content attribution
   - Multi-signal detection pipeline
   - Confidence scoring
   - Three transparency label variants
   - Appeals workflow
   - Rate limiting
   - Structured audit log
   - GET `/log` endpoint for audit inspection

---

# System Architecture


Submission flow

```
   User
      │
      ▼
   POST /submit
      │
      ▼
   LLM Detection (Groq)
      │
      ▼
   Stylometric Analysis
      │
      ▼
   Confidence Scoring
      │
      ▼
   Transparency Label
      │
      ▼
   Audit Log
      │
      ▼
   JSON Response

```

Appeal flow

   ```
   User
      │
      ▼
   POST /appeal
      │
      ▼
   Update Status → under_review
      │
      ▼
   Append Appeal to Audit Log
      │
      ▼
   JSON Confirmation


```

---

# Detection Signals

## Signal 1 – LLM Classification (Groq)

The first signal uses the Groq Llama 3.3 model to classify whether the writing appears AI-generated or human-written.

The model returns:
   - attribution
   - confidence score between 0 and 1

This signal captures semantic coherence, writing style, and overall language patterns.

### Strengths

   - Understands context
   - Recognizes AI writing style
   - Captures semantic patterns

### Limitations

- Can mistake polished human writing for AI
- Depends on prompt quality

---

## Signal 2 – Stylometric Heuristics

The second signal uses measurable writing statistics.

Features:
   - Type Token Ratio
   - Sentence Length Variance
   - Average Sentence Length

These metrics capture structural characteristics that often differ between AI and human writing.

### Strengths

   - Fast
   - Explainable
   - Independent from the LLM

### Limitations

   - Short texts provide little evidence.
   - Formal human writing can resemble AI output.
   - Creative writing may intentionally mimic AI-like structure.

---

# Confidence Scoring

The two signals are combined using a weighted average.

```
Confidence = (0.6 × LLM Score) + (0.4 × Stylometric Score)
```

The LLM receives slightly more weight because it captures semantic information beyond simple statistical patterns.

---

## Confidence Thresholds

| Confidence | Attribution |
|------------|-------------|
| 0.70 – 1.00 | Likely AI |
| 0.31 – 0.69 | Uncertain |
| 0.00 – 0.30 | Likely Human |


--------

## Example Confidence Scores

### Example 1 — High Confidence AI

**Input**

   > "Artificial intelligence represents a transformative paradigm shift in modern society..."

Output

   - LLM Score: 0.91
   - Stylometric Score: 0.82
   - Final Confidence: **0.87**

Transparency Label:

   > Likely AI-generated. Our system found strong evidence that this content was generated using AI.

 
---

### Example 2 — High Confidence Human

**Input**

   > "ok so i finally tried that ramen place downtown and honestly it wasn't great..."

Output

   - LLM Score: 0.16
   - Stylometric Score: 0.24
   - Final Confidence: **0.19**

Transparency Label:

   > Likely written by a human. Our system found strong evidence that this content was written by a person.

---

# Transparency Labels

## High-confidence AI

   > "Likely AI-generated. Our system found strong evidence that this content was generated using AI."

---

## High-confidence Human

   > "Likely written by a human. Our system found strong evidence that this content was written by a person."

---

## Uncertain

   > "Unable to determine confidently. The available evidence is mixed."

---

# Appeals Workflow

Creators can challenge a classification using:

```
POST /appeal
```

Required fields:
   - content_id
   - creator_reasoning

When an appeal is received:
   - status changes to **under_review**
   - creator reasoning is stored
   - audit log is updated
   - confirmation is returned

Automatic reclassification is intentionally not performed.

---

# Rate Limiting

Flask-Limiter protects the submission endpoint.

```
10 requests per minute
100 requests per day
```

### Why these limits?

A normal creator submits content only occasionally, so these limits allow normal use while reducing abuse from automated scripts.

Example:

```
200
200
200
200
200
200
200
200
200
200
429
429
``` 

The final requests are rejected once the limit is exceeded.

---

# Audit Log

Every submission stores:
   - timestamp
   - content_id
   - creator_id
   - attribution
   - confidence
   - LLM score
   - stylometric score
   - transparency label
   - status
   - appeal reasoning (if present)

Example:

```json
   {
   "content_id":"...",
   "creator_id":"user1",
   "confidence":0.82,
   "llm_score":0.91,
   "stylometric_score":0.74,
   "attribution":"likely_ai",
   "status":"classified"
   }

```
---

# Known Limitations

The system performs best on longer pieces of writing. Very short text provides limited stylometric evidence, making classification less reliable.

Formal academic writing may also resemble AI-generated text because both often contain long, consistent sentence structures
and a formal vocabulary. This can increase false positives.

Similarly, heavily edited AI-generated text may appear more human-like and receive lower confidence scores.

---

# Spec Reflection

The planning specification was valuable because it required defining the detection signals, confidence thresholds, transparency labels, and API endpoints before implementation. This made the coding process more organized and ensured the implementation matched the intended design.

One implementation change was the confidence scoring. 
The original specification described a conceptual combination of signals, but during implementation I adopted a weighted average (60% LLM and 40% stylometric) because it produced more stable and interpretable confidence scores.

---

# AI Usage

## Example 1

I used ChatGPT to generate the initial Flask application structure, including the POST `/submit` endpoint and API skeleton. 
I reviewed the generated code and modified it to match my planned API contract and confidence-scoring workflow.

---

## Example 2

I used ChatGPT to help implement the appeals workflow and audit logging. The generated code provided the overall structure, 
but I modified the audit log fields, appeal status updates, and JSON response format to match my project specification.

---

# Demo Walkthrough

The demo video demonstrates:
   - submitting human-written content
   - submitting AI-generated content
   - confidence score calculation
   - transparency labels
   - viewing the audit log
   - submitting an appeal
   - updated appeal status
   - rate limiting
   - explanation of the detection pipeline

---

# Future Improvements

- Add additional stylometric features
- Use multiple LLMs as an ensemble
- Store audit logs in a database
- Human reviewer dashboard
- Provenance certificates for verified creators
- Better confidence calibration using labeled datasets

---------

# Technologies Used

- Python
- Flask
- Groq API
- Flask-Limiter
- JSON
- Regular Expressions
- Statistics module
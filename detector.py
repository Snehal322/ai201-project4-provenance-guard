from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = """
You detect whether writing appears human-written or AI-generated.

Return ONLY JSON.

{
 "attribution":"likely_ai" or "likely_human",
 "score":0.0-1.0
}
"""

def llm_signal(text):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        response_format={"type":"json_object"},
        messages=[
            {"role":"system","content":PROMPT},
            {"role":"user","content":text}
        ]
    )

    return response.choices[0].message.content


''' 

O/p:
{
 "attribution":"likely_ai",
 "score":0.84
}
'''
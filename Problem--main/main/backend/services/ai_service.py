import os
from groq import Groq

_api_key = os.getenv("GROQ_API_KEY")
if not _api_key:
    raise EnvironmentError("GROQ_API_KEY is not set. Add it to your .env file.")

client = Groq(api_key=_api_key)
MODEL = "llama3-70b-8192"

def correct_code(code: str, language: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert code reviewer. Return ONLY corrected code with no explanation, no markdown, no backticks."},
            {"role": "user", "content": f"Fix this {language} code:\n\n{code}"}
        ],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()

def convert_code(code: str, language: str) -> tuple:
    target = "javascript" if language == "python" else "python"
    target_label = "JavaScript" if target == "javascript" else "Python"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert programmer. Return ONLY the converted code with no explanation, no markdown, no backticks."},
            {"role": "user", "content": f"Convert this {language} code to {target_label}. Preserve all logic and comments:\n\n{code}"}
        ],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip(), target

def explain_code(code: str, language: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a coding tutor. Give a concise plain-English explanation of what the code does."},
            {"role": "user", "content": f"Explain this {language} code:\n\n{code}"}
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()

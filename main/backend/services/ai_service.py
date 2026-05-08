import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("EMERGENT_LLM_KEY"))
MODEL = "claude-sonnet-4-5"

def correct_code(code: str, language: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system="You are an expert code reviewer. Return ONLY corrected code with no explanation, no markdown, no backticks.",
        messages=[{"role": "user", "content": f"Fix this {language} code:\n\n{code}"}]
    )
    return response.content[0].text

def convert_code(code: str, language: str) -> tuple[str, str]:
    target = "javascript" if language == "python" else "python"
    target_label = "JavaScript" if target == "javascript" else "Python"
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system="You are an expert programmer. Return ONLY the converted code with no explanation, no markdown, no backticks.",
        messages=[{"role": "user", "content": f"Convert this {language} code to {target_label}. Preserve all logic and comments:\n\n{code}"}]
    )
    return response.content[0].text, target

def explain_code(code: str, language: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system="You are a coding tutor. Give a concise plain-English explanation of what the code does.",
        messages=[{"role": "user", "content": f"Explain this {language} code:\n\n{code}"}]
    )
    return response.content[0].text

import subprocess
import os
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = Anthropic(api_key=os.getenv("EMERGENT_LLM_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    language: str

@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    file_ext = "py" if request.language == "python" else "js"
    temp_file = f"temp_{uuid.uuid4()}.{file_ext}"
    
    with open(temp_file, "w") as f:
        f.write(request.code)
    
    try:
        cmd = ["python3", temp_file] if request.language == "python" else ["node", temp_file]
        process = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return {"result": process.stdout if process.stdout else process.stderr}
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out."}
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.post("/api/ai/correct")
async def correct_code(request: CodeRequest):
    prompt = f"Fix the following {request.language} code. Provide ONLY the corrected code without explanation:\n\n{request.code}"
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"corrected_code": response.content[0].text}

@app.post("/api/ai/convert")
async def convert_code(request: CodeRequest):
    target = "JavaScript" if request.language == "python" else "Python"
    prompt = f"Convert this {request.language} code to {target}. Preserve logic and comments:\n\n{request.code}"
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"converted_code": response.content[0].text, "new_language": target.lower()}

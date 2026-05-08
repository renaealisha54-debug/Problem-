from pydantic import BaseModel, validator
from typing import Optional

SUPPORTED_LANGUAGES = {"python", "javascript"}
MAX_CODE_LENGTH = 50000

class CodeRequest(BaseModel):
    code: str
    language: str

    @validator("language")
    def validate_language(cls, v):
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language must be one of: {SUPPORTED_LANGUAGES}")
        return v

    @validator("code")
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError("Code cannot be empty.")
        if len(v) > MAX_CODE_LENGTH:
            raise ValueError(f"Code exceeds maximum length of {MAX_CODE_LENGTH} characters.")
        return v

class BuildRequest(BaseModel):
    code: str
    app_name: Optional[str] = "ProblemCode App"
    package_name: Optional[str] = "com.problemcode.app"

    @validator("package_name")
    def validate_package(cls, v):
        parts = v.split(".")
        if len(parts) < 2:
            raise ValueError("Package name must have at least two segments e.g. com.example")
        return v

class ExecutionResult(BaseModel):
    result: Optional[str] = None
    error: Optional[str] = None
    exit_code: Optional[int] = None

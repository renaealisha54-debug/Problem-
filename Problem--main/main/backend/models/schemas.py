from pydantic import BaseModel, field_validator
from typing import Optional

SUPPORTED_LANGUAGES = {"python", "javascript"}
MAX_CODE_LENGTH = 50000


class CodeRequest(BaseModel):
    code: str
    language: str

    @field_validator("language")
    @classmethod
    def validate_language(cls, v):
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Language must be one of: {SUPPORTED_LANGUAGES}")
        return v

    @field_validator("code")
    @classmethod
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

    @field_validator("code")
    @classmethod
    def validate_code(cls, v):
        if not v or not v.strip():
            raise ValueError("Code cannot be empty.")
        if len(v) > MAX_CODE_LENGTH:
            raise ValueError(f"Code exceeds maximum length of {MAX_CODE_LENGTH} characters.")
        return v

    @field_validator("app_name")
    @classmethod
    def validate_app_name(cls, v):
        if not v or not v.strip():
            return "ProblemCode App"
        return v.strip()

    @field_validator("package_name")
    @classmethod
    def validate_package(cls, v):
        if not v:
            return "com.problemcode.app"
        parts = v.split(".")
        if len(parts) < 2:
            raise ValueError("Package name must have at least two segments e.g. com.example")
        for part in parts:
            if not part.isidentifier():
                raise ValueError(f"Invalid package segment: '{part}'")
        return v


class ExecutionResult(BaseModel):
    result: Optional[str] = None
    error: Optional[str] = None
    exit_code: Optional[int] = None

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Stable Wandbox compiler map
COMPILER_MAP = {
    "python": "cpython-3.12.7",
    "javascript": "nodejs-20.17.0",
    "typescript": "typescript-5.6.2",
    "java": "openjdk-jdk-22+36",
    "c": "gcc-13.2.0-c",
    "cpp": "gcc-13.2.0",
    "csharp": "mono-6.12.0.199",
    "go": "go-1.23.2",
    "rust": "rust-1.82.0",
    "ruby": "ruby-3.4.9",
    "php": "php-8.3.12",
    "swift": "swift-6.0.1",
    "sql": "sqlite-3.46.1",
    "kotlin": "gcc-13.2.0",  # fallback - kotlin not on wandbox
}

NON_EXECUTABLE = {"html", "css", "json", "markdown", "yaml"}


class ExecuteRequest(BaseModel):
    language: str
    code: str


class ExecuteResponse(BaseModel):
    success: bool
    output: Optional[str] = ""
    error: Optional[str] = ""
    status: Optional[str] = "0"


@router.post("/execute", response_model=ExecuteResponse)
async def execute_code(req: ExecuteRequest):
    if req.language in NON_EXECUTABLE:
        return ExecuteResponse(
            success=False,
            error=f"Execution is not supported for {req.language.upper()}. This language is markup/config only.",
        )

    compiler = COMPILER_MAP.get(req.language)
    if not compiler:
        return ExecuteResponse(
            success=False,
            error=f"Language '{req.language}' is not supported for execution yet.",
        )

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://wandbox.org/api/compile.json",
                json={"compiler": compiler, "code": req.code},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()

        output = data.get("program_output", "") or ""
        compiler_error = data.get("compiler_error", "") or ""
        program_error = data.get("program_error", "") or ""
        status = data.get("status", "0")

        if compiler_error:
            return ExecuteResponse(
                success=False,
                output=output,
                error=f"Compiler Error:\n{compiler_error}",
                status=status,
            )
        if program_error:
            return ExecuteResponse(
                success=False,
                output=output,
                error=f"Runtime Error:\n{program_error}",
                status=status,
            )

        return ExecuteResponse(
            success=True,
            output=output if output else "Code executed successfully (no output).",
            status=status,
        )

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Code execution timed out after 30 seconds.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution engine error: {str(e)}")

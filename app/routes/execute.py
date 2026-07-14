import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Stable Wandbox compiler map
COMPILER_MAP = {
    "python":     "cpython-3.12.7",
    "javascript": "nodejs-20.17.0",
    "typescript": "typescript-5.6.2",
    "java":       "openjdk-jdk-22+36",
    "c":          "gcc-13.2.0-c",
    "cpp":        "gcc-13.2.0",
    "csharp":     "mono-6.12.0.199",
    "go":         "go-1.23.2",
    "rust":       "rust-1.82.0",
    "ruby":       "ruby-3.4.9",
    "php":        "php-8.3.12",
    "swift":      None,   # Wandbox Swift is broken server-side
    "kotlin":     None,   # Kotlin not on Wandbox
    "sql":        "sqlite-3.46.1",
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
    # Handle markup/config languages
    if req.language in NON_EXECUTABLE:
        return ExecuteResponse(
            success=False,
            error=f"Execution is not supported for {req.language.upper()}. "
                  f"This language is markup/config only — paste it and use 'Explain Code' instead.",
        )

    compiler = COMPILER_MAP.get(req.language)

    # Handle languages not yet supported by the execution engine
    if compiler is None:
        lang_display = req.language.capitalize()
        return ExecuteResponse(
            success=False,
            error=f"⚠️  {lang_display} execution is temporarily unavailable due to a cloud provider issue.\n"
                  f"Please try Python, JavaScript, C++, Go, Rust, Ruby, PHP, C#, C, TypeScript, Java, or SQL.",
        )

    if not compiler:
        return ExecuteResponse(
            success=False,
            error=f"Language '{req.language}' is not supported for execution yet.",
        )

    # Build the Wandbox request payload
    code = req.code

    # Java: Wandbox saves the file as 'prog.java' so 'public class Main' fails.
    # Automatically strip 'public' from top-level class declarations to make it work.
    if req.language == "java":
        import re
        code = re.sub(r'^(\s*)public\s+(class\s+\w+)', r'\1\2', code, flags=re.MULTILINE)

    payload: dict = {"compiler": compiler, "code": code}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://wandbox.org/api/compile.json",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()

        output = data.get("program_output", "") or ""
        compiler_error = data.get("compiler_error", "") or ""
        program_error = data.get("program_error", "") or ""
        status = data.get("status", "0")

        # Compiler error takes priority
        if compiler_error:
            return ExecuteResponse(
                success=False,
                output=output,
                error=f"Compiler Error:\n{compiler_error}",
                status=status,
            )

        # Runtime error
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
        raise HTTPException(
            status_code=504,
            detail="Code execution timed out after 30 seconds. Try simplifying your code."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution engine error: {str(e)}"
        )

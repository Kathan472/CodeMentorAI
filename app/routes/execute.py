"""
app/routes/execute.py
---------------------
Code Execution API endpoint.

Uses the Wandbox (wandbox.org) cloud compiler service to safely run user-submitted
code in an isolated sandbox. Supports 11 languages: Python, JavaScript, TypeScript,
Java, C, C++, C#, Go, Rust, Ruby, and PHP.

NOTE: Swift and Kotlin are listed in the language selector for AI explanation only —
they are NOT executable via Wandbox at this time. Submitting them for execution
will return a graceful error message.

HOW INPUT WORKS:
  Programs that read from stdin (e.g. Python's input(), C++ cin, Java Scanner)
  receive their input via the "stdin" field in the request body. All lines of
  input must be pre-entered, separated by newlines. Wandbox feeds them to the
  program in order — it does NOT support interactive/live input.
"""

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# ---------------------------------------------------------------------------
# Compiler Map — maps our language keys → Wandbox compiler identifiers
# ---------------------------------------------------------------------------
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
    "swift":      None,   # Wandbox Swift is not available — AI-explain only
    "kotlin":     None,   # Wandbox Kotlin is not available — AI-explain only
}

# Languages that are markup/config and cannot be executed at all
NON_EXECUTABLE = {"html", "css", "json", "markdown", "yaml"}


# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------
class ExecuteRequest(BaseModel):
    language: str
    code: str
    stdin: Optional[str] = ""


class ExecuteResponse(BaseModel):
    success: bool
    output: Optional[str] = ""
    error: Optional[str] = ""
    status: Optional[str] = "0"


# ---------------------------------------------------------------------------
# POST /api/code/execute
# ---------------------------------------------------------------------------
@router.post("/execute", response_model=ExecuteResponse)
async def execute_code(req: ExecuteRequest):
    """
    Sends the user's code to Wandbox for cloud-based execution.

    - `language`: One of the supported language keys (e.g. "python", "cpp")
    - `code`: The source code to execute
    - `stdin`: (Optional) Newline-separated input lines for programs that use stdin

    Returns the program output, or a compiler/runtime error if execution fails.
    """
    # Reject markup/config languages — they can't be run
    if req.language in NON_EXECUTABLE:
        return ExecuteResponse(
            success=False,
            error=(
                f"Execution is not supported for {req.language.upper()}. "
                "This language is markup/config only — paste it and use 'Explain Code' instead."
            ),
        )

    compiler = COMPILER_MAP.get(req.language)

    # Languages not yet supported by Wandbox — return a helpful message
    if compiler is None:
        lang_display = req.language.capitalize()
        return ExecuteResponse(
            success=False,
            error=(
                f"⚠️  {lang_display} execution is temporarily unavailable due to a cloud provider issue.\n"
                "Please try Python, JavaScript, C++, Go, Rust, Ruby, PHP, C#, C, TypeScript, or Java."
            ),
        )

    # Unknown language entirely
    if not compiler:
        return ExecuteResponse(
            success=False,
            error=f"Language '{req.language}' is not supported for execution yet.",
        )

    # ---------------------------------------------------------------------------
    # Pre-process code for specific languages
    # ---------------------------------------------------------------------------
    code = req.code

    if req.language == "java":
        # Wandbox saves Java files as 'prog.java', so 'public class X' would fail
        # to compile because the filename must match the class name.
        # We strip 'public' from top-level class declarations as a workaround.
        import re
        code = re.sub(
            r"^(\s*)public\s+(class\s+\w+)", r"\1\2", code, flags=re.MULTILINE
        )

    # ---------------------------------------------------------------------------
    # Send to Wandbox API
    # ---------------------------------------------------------------------------
    payload: dict = {"compiler": compiler, "code": code, "stdin": req.stdin or ""}

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

        # Compiler error (syntax/type errors) takes priority
        if compiler_error:
            return ExecuteResponse(
                success=False,
                output=output,
                error=f"Compiler Error:\n{compiler_error}",
                status=status,
            )

        # Runtime error (crash, exception, segfault)
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
            detail="Code execution timed out after 30 seconds. Try simplifying your code.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution engine error: {str(e)}")

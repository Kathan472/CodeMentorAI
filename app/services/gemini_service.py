import os
import json
import httpx
# pyrefly: ignore [missing-import]
from google import genai
from fastapi import HTTPException
from app.prompts import get_prompt_for_language


class GeminiService:
    def __init__(self):
        # 1. Gemini Config
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_key or self.gemini_key == "your_gemini_api_key_here":
            self.gemini_configured = False
            self.gemini_client = None
        else:
            self.gemini_client = genai.Client(api_key=self.gemini_key)
            self.gemini_configured = True
        self.gemini_model_name = "gemini-3.5-flash"

        # 2. NVIDIA Config
        self.nvidia_key = os.getenv("NVIDIA_API_KEY")
        self.nvidia_configured = bool(
            self.nvidia_key and self.nvidia_key != "your_nvidia_api_key_here"
        )

        # 3. OpenRouter Config
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.openrouter_configured = bool(
            self.openrouter_key
            and self.openrouter_key != "your_openrouter_api_key_here"
        )

        # Prioritized fallback chain:
        # Choice 1: OpenRouter Kimi (highly capable)
        # Choice 2: OpenRouter DeepSeek (extremely powerful reasoning)
        # Choice 3: NVIDIA API model (highly capable, extremely fast)
        # Choice 4-6: OpenRouter Free models (prioritized by coding / reasoning quality)
        # Choice 7: Gemini (configured fallback)
        self.fallback_models = []

        if self.openrouter_configured:
            self.fallback_models.append(
                {"provider": "openrouter", "model": "moonshotai/kimi-k2.6"}
            )
            self.fallback_models.append(
                {"provider": "openrouter", "model": "deepseek-ai/deepseek-v4-pro"}
            )

        if self.nvidia_configured:
            self.fallback_models.append(
                {
                    "provider": "nvidia",
                    "model": "nvidia/llama-3.3-nemotron-super-49b-v1",
                }
            )

        if self.openrouter_configured:
            self.fallback_models.extend(
                [
                    {"provider": "openrouter", "model": "qwen/qwen3-coder:free"},
                    {
                        "provider": "openrouter",
                        "model": "meta-llama/llama-3.3-70b-instruct:free",
                    },
                    {"provider": "openrouter", "model": "google/gemma-4-31b-it:free"},
                ]
            )

        if self.gemini_configured:
            self.fallback_models.append(
                {"provider": "gemini", "model": self.gemini_model_name}
            )

    @property
    def configured(self) -> bool:
        return len(self.fallback_models) > 0

    async def explain_code(self, language: str, code: str) -> str:
        """
        Takes the programming language and the source code,
        and requests an explanation using the fallback chain.
        """
        if not self.configured:
            raise HTTPException(
                status_code=503,
                detail="No AI providers are configured. Please check your .env file.",
            )

        system_instruction = get_prompt_for_language(language)
        user_prompt = f"Explain code in {language}:\n```\n{code}\n```"
        full_prompt = (
            f"SYSTEM INSTRUCTION:\n{system_instruction}\n\n"
            f"USER CODE (Language: {language}):\n```\n{code}\n```\n\n"
            f"Please explain the code above following the formatting rules in the SYSTEM INSTRUCTION."
        )

        for attempt in self.fallback_models:
            provider = attempt["provider"]
            model = attempt["model"]
            try:
                if provider == "nvidia":
                    return await self._call_nvidia_non_stream(
                        model, system_instruction, user_prompt
                    )
                elif provider == "openrouter":
                    return await self._call_openrouter_non_stream(
                        model, system_instruction, user_prompt
                    )
                elif provider == "gemini":
                    return await self._call_gemini_non_stream(full_prompt)
            except Exception as e:
                print(
                    f"Fallback warning: Attempt using {provider} ({model}) failed: {e}"
                )
                continue

        raise HTTPException(
            status_code=500, detail="All configured AI models failed to respond."
        )

    async def explain_code_stream(self, language: str, code: str):
        """
        Streams the explanation from the fallback model chain.
        """
        if not self.configured:
            yield "No AI providers are configured. Please check your .env file."
            return

        system_instruction = get_prompt_for_language(language)
        user_prompt = f"Explain code in {language}:\n```\n{code}\n```"
        full_prompt = (
            f"SYSTEM INSTRUCTION:\n{system_instruction}\n\n"
            f"USER CODE (Language: {language}):\n```\n{code}\n```\n\n"
            f"Please explain the code above following the formatting rules in the SYSTEM INSTRUCTION."
        )

        success = False
        last_error = ""

        for attempt in self.fallback_models:
            provider = attempt["provider"]
            model = attempt["model"]
            try:
                if provider == "nvidia":
                    async for chunk in self._stream_nvidia(
                        model, system_instruction, user_prompt
                    ):
                        success = True
                        yield chunk
                elif provider == "openrouter":
                    async for chunk in self._stream_openrouter(
                        model, system_instruction, user_prompt
                    ):
                        success = True
                        yield chunk
                elif provider == "gemini":
                    async for chunk in self._stream_gemini(full_prompt):
                        success = True
                        yield chunk

                if success:
                    break
            except Exception as e:
                last_error = str(e)
                print(
                    f"Fallback warning: Stream using {provider} ({model}) failed: {e}"
                )
                continue

        if not success:
            yield f"\n\n**Error: All configured AI models failed to respond.**\nLast Error: {last_error}"

    async def explain_repo_stream(self, repo_url: str, repo_context: str):
        """
        Streams the explanation of an entire GitHub repository.
        """
        if not self.configured:
            yield "No AI providers are configured. Please check your .env file."
            return

        system_instruction = (
            "You are an expert Software Architect and Code Mentor. "
            "You have been provided with the source code of an entire GitHub repository. "
            "Explain what this codebase does, its architecture, how it works, and important details. "
            "Be comprehensive but readable. Break your explanation into clear sections (e.g., Overview, Architecture, Key Components, How to Run)."
        )
        user_prompt = f"Repository URL: {repo_url}\n\nHere is the concatenated source code:\n\n{repo_context}"

        full_prompt = (
            f"SYSTEM INSTRUCTION:\n{system_instruction}\n\n"
            f"USER PROMPT:\n{user_prompt}\n\n"
            "Please provide your architectural explanation."
        )

        success = False
        last_error = ""

        # Some fallback models might fail due to context size, so the loop is important
        for attempt in self.fallback_models:
            provider = attempt["provider"]
            model = attempt["model"]
            try:
                if provider == "nvidia":
                    async for chunk in self._stream_nvidia(
                        model, system_instruction, user_prompt
                    ):
                        success = True
                        yield chunk
                elif provider == "openrouter":
                    async for chunk in self._stream_openrouter(
                        model, system_instruction, user_prompt
                    ):
                        success = True
                        yield chunk
                elif provider == "gemini":
                    async for chunk in self._stream_gemini(full_prompt):
                        success = True
                        yield chunk

                if success:
                    break
            except Exception as e:
                last_error = str(e)
                print(
                    f"Fallback warning: Repo stream using {provider} ({model}) failed: {e}"
                )
                continue

        if not success:
            yield f"\n\n**Error: All configured AI models failed to respond.**\nLast Error: {last_error}"

    async def followup_stream(self, context: str, question: str):
        """
        Streams a follow-up answer using the fallback model chain.
        """
        if not self.configured:
            yield "No AI providers are configured. Please check your .env file."
            return

        user_prompt = f"Previous context:\n{context}\n\nFollow-up question: {question}"

        success = False
        last_error = ""

        for attempt in self.fallback_models:
            provider = attempt["provider"]
            model = attempt["model"]
            try:
                if provider == "nvidia":
                    async for chunk in self._stream_nvidia(
                        model,
                        "You are an expert AI mentor explaining code.",
                        user_prompt,
                    ):
                        success = True
                        yield chunk
                elif provider == "openrouter":
                    async for chunk in self._stream_openrouter(
                        model,
                        "You are an expert AI mentor explaining code.",
                        user_prompt,
                    ):
                        success = True
                        yield chunk
                elif provider == "gemini":
                    full_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer using Markdown."
                    async for chunk in self._stream_gemini(full_prompt):
                        success = True
                        yield chunk

                if success:
                    break
            except Exception as e:
                last_error = str(e)
                print(
                    f"Fallback warning: Followup stream using {provider} ({model}) failed: {e}"
                )
                continue

        if not success:
            yield f"\n\n**Error: All configured AI models failed to respond.**\nLast Error: {last_error}"

    # --- NVIDIA API Helpers ---
    async def _call_nvidia_non_stream(
        self, model: str, system_prompt: str, user_prompt: str
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.nvidia_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 2048,
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"]

    async def _stream_nvidia(self, model: str, system_prompt: str, user_prompt: str):
        headers = {
            "Authorization": f"Bearer {self.nvidia_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 2048,
            "stream": True,
        }
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            chunk = data_json["choices"][0]["delta"].get("content", "")
                            if chunk:
                                yield chunk
                        except Exception:
                            pass

    # --- OpenRouter API Helpers ---
    async def _call_openrouter_non_stream(
        self, model: str, system_prompt: str, user_prompt: str
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "CodeMentorAI",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"]

    async def _stream_openrouter(
        self, model: str, system_prompt: str, user_prompt: str
    ):
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "CodeMentorAI",
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "stream": True,
        }
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            data_json = json.loads(data_str)
                            chunk = data_json["choices"][0]["delta"].get("content", "")
                            if chunk:
                                yield chunk
                        except Exception:
                            pass

    # --- Gemini API Helpers ---
    async def _call_gemini_non_stream(self, prompt: str) -> str:
        response = await self.gemini_client.aio.models.generate_content(
            model=self.gemini_model_name, contents=prompt
        )
        return response.text

    async def _stream_gemini(self, prompt: str):
        response = await self.gemini_client.aio.models.generate_content_stream(
            model=self.gemini_model_name, contents=prompt
        )
        async for chunk in response:
            if chunk.text:
                yield chunk.text


# Create a singleton instance to be used across the app
gemini_service = GeminiService()

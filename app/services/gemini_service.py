import os
import google.generativeai as genai
from fastapi import HTTPException
from app.prompts import get_prompt_for_language

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            self.configured = False
        else:
            genai.configure(api_key=api_key)
            self.configured = True
            
            # Use gemini-1.5-flash as it is the fastest, highly capable, and has a generous free tier.
            self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def explain_code(self, language: str, code: str) -> str:
        """
        Takes the programming language and the source code, 
        fetches the appropriate tailored system prompt,
        and requests an explanation from the Gemini API.
        """
        if not self.configured:
            raise HTTPException(
                status_code=503, 
                detail="Gemini API is not configured. Please add a valid GEMINI_API_KEY to your .env file."
            )

        # 1. Get the language-specific system prompt
        system_instruction = get_prompt_for_language(language)

        # 2. Combine the prompt and the user's code
        # Note: Since the generative model allows system instructions natively in newer SDK versions,
        # we can just prepend it or use the `system_instruction` param if we initialize the model with it.
        # To be safe across 0.3.0 versions, we prepend it as a strong instruction.
        full_prompt = (
            f"SYSTEM INSTRUCTION:\n{system_instruction}\n\n"
            f"USER CODE (Language: {language}):\n```\n{code}\n```\n\n"
            f"Please explain the code above following the formatting rules in the SYSTEM INSTRUCTION."
        )

        try:
            response = await self.model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

    async def explain_code_stream(self, language: str, code: str):
        """
        Streams the explanation from the Gemini API chunk by chunk.
        """
        if not self.configured:
            yield "Gemini API is not configured. Please add a valid GEMINI_API_KEY to your .env file."
            return

        system_instruction = get_prompt_for_language(language)
        full_prompt = (
            f"SYSTEM INSTRUCTION:\n{system_instruction}\n\n"
            f"USER CODE (Language: {language}):\n```\n{code}\n```\n\n"
            f"Please explain the code above following the formatting rules in the SYSTEM INSTRUCTION."
        )

        try:
            response = await self.model.generate_content_async(full_prompt, stream=True)
            async for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"\n\n**Error from Gemini API:** {str(e)}"

    async def followup_stream(self, context: str, question: str):
        """
        Streams a follow-up answer using the provided conversation context.
        """
        if not self.configured:
            yield "Gemini API is not configured. Please add a valid GEMINI_API_KEY to your .env file."
            return
            
        full_prompt = (
            f"{context}\n"
            f"User's Follow-up Question: {question}\n\n"
            f"Please answer the user's question clearly and concisely. Format using Markdown."
        )
        
        try:
            response = await self.model.generate_content_async(full_prompt, stream=True)
            async for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"\n\n**Error from Gemini API:** {str(e)}"

# Create a singleton instance to be used across the app
gemini_service = GeminiService()

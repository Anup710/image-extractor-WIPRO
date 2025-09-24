import os
import base64
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from models import ImageData

load_dotenv()

class GPTService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

    async def process_chat(
        self,
        prompt: str,
        images: Optional[List[ImageData]] = None,
        template: Optional[str] = None
    ) -> str:
        try:
            # Apply template if provided
            final_prompt = self._apply_template(prompt, template)

            # Prepare messages
            messages = [
                {
                    "role": "user",
                    "content": self._build_message_content(final_prompt, images)
                }
            ]

            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4000,
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"GPT API error: {str(e)}")

    def _apply_template(self, prompt: str, template: Optional[str]) -> str:
        if not template:
            return prompt

        # Basic template system - can be expanded
        templates = {
            "analyze": f"Please analyze the following images and provide detailed insights: {prompt}",
            "describe": f"Please describe what you see in the images: {prompt}",
            "technical": f"Provide a technical analysis of the images with focus on: {prompt}",
            "default": prompt
        }

        return templates.get(template, templates["default"])

    def _build_message_content(self, prompt: str, images: Optional[List[ImageData]]):
        content = [{"type": "text", "text": prompt}]

        if images:
            for image in images:
                content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{image.content_type};base64,{image.content}"
                    }
                })

        return content
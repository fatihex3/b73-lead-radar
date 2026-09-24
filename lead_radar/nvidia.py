from openai import OpenAI

from lead_radar.config import Settings


class NvidiaClient:
    def __init__(self, settings: Settings):
        if not settings.nvidia_api_key:
            raise RuntimeError(
                "NVIDIA_API_KEY is missing."
            )

        self.settings = settings

        self.client = OpenAI(
            api_key=settings.nvidia_api_key,
            base_url=settings.nvidia_base_url,
        )

    def chat(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=model,
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content or ""

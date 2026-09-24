import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    telegram_allowed_user_id: int | None

    nvidia_api_key: str
    nvidia_base_url: str

    fast_model: str
    deep_model: str

    database_path: str
    log_level: str


def get_settings() -> Settings:
    allowed_user = os.getenv("TELEGRAM_ALLOWED_USER_ID", "").strip()

    return Settings(
        telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        telegram_allowed_user_id=int(allowed_user) if allowed_user else None,

        nvidia_api_key=os.getenv("NVIDIA_API_KEY", ""),
        nvidia_base_url=os.getenv(
            "NVIDIA_BASE_URL",
            "https://integrate.api.nvidia.com/v1",
        ),

        fast_model=os.getenv(
            "FAST_MODEL",
            "nvidia/nemotron-3.5-lightning-30b-a3b",
        ),

        deep_model=os.getenv(
            "DEEP_MODEL",
            "nvidia/nemotron-3-ultra-550b-a55b",
        ),

        database_path=os.getenv("DATABASE_PATH", "leads.db"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )

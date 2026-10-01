import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    local_explainer_enabled: bool = os.getenv(
        "ENABLE_LOCAL_EXPLAINER", "false"
    ).lower() in {"1", "true", "yes"}
    local_explainer_model: str = os.getenv(
        "LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    ).strip()


settings = Settings()

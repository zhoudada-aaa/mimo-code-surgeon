from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass


@dataclass
class LLMConfig:
    api_key: str | None
    base_url: str
    model: str
    temperature: float = 0.2

    @classmethod
    def from_env(cls) -> "LLMConfig":
        return cls(
            api_key=os.getenv("MIMO_API_KEY"),
            base_url=os.getenv("MIMO_BASE_URL", "https://your-openai-compatible-endpoint/v1/chat/completions"),
            model=os.getenv("MIMO_MODEL", "mimo-v2.5"),
            temperature=float(os.getenv("MIMO_TEMPERATURE", "0.2")),
        )


class OpenAICompatibleClient:
    def __init__(self, config: LLMConfig | None = None):
        self.config = config or LLMConfig.from_env()

    @property
    def configured(self) -> bool:
        return bool(self.config.api_key and self.config.base_url)

    def chat(self, system: str, user: str) -> str:
        if not self.configured:
            raise RuntimeError("MIMO_API_KEY is not configured. Use --mode mock or set .env variables.")

        payload = {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        req = urllib.request.Request(
            self.config.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]

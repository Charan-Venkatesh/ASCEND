from abc import ABC, abstractmethod

import httpx
from openai import OpenAI

from app.core.config import settings


class AIProvider(ABC):
    @abstractmethod
    def generate(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        raise NotImplementedError


class NvidiaProvider(AIProvider):
    def generate(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        if not settings.nvidia_api_key:
            raise RuntimeError("NVIDIA_API_KEY is not configured")
        response = httpx.post(
            f"{settings.nvidia_base_url}/chat/completions",
            headers={"Authorization": f"Bearer {settings.nvidia_api_key}", "Content-Type": "application/json"},
            json={"model": settings.nvidia_model, "messages": messages, "temperature": temperature},
            timeout=45,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


class OpenAIProvider(AIProvider):
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def generate(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        if self.client is None:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        response = self.client.chat.completions.create(model=settings.openai_model, messages=messages, temperature=temperature)
        return response.choices[0].message.content or ""


class ProviderChain(AIProvider):
    def __init__(self) -> None:
        self.providers: list[AIProvider] = [NvidiaProvider(), OpenAIProvider()]

    def generate(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        failures: list[str] = []
        for provider in self.providers:
            try:
                return provider.generate(messages, temperature)
            except Exception as exc:
                failures.append(f"{provider.__class__.__name__}: {exc}")
        return "I cannot reach the configured AI providers right now. Based on your evidence, state your assumption, test it with a small lab, and record what changed."

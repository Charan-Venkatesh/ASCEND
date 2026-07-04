import json
from typing import Any

from redis import Redis

from app.core.config import settings


class EventBus:
    def __init__(self) -> None:
        self.redis = Redis.from_url(settings.redis_url, decode_responses=True)

    def publish(self, stream: str, event_type: str, payload: dict[str, Any]) -> str:
        return self.redis.xadd(stream, {"event_type": event_type, "payload": json.dumps(payload, default=str)})

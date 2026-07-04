from uuid import UUID, uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from app.core.config import settings


class MemoryStore:
    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant_url)
        self.collection = settings.qdrant_collection

    def ensure_collection(self) -> None:
        collections = {item.name for item in self.client.get_collections().collections}
        if self.collection not in collections:
            self.client.create_collection(collection_name=self.collection, vectors_config=VectorParams(size=16, distance=Distance.COSINE))

    def embed(self, text: str) -> list[float]:
        values = [0.0] * 16
        for index, byte in enumerate(text.encode("utf-8")[:512]):
            values[index % 16] += float(byte) / 255.0
        norm = sum(v * v for v in values) ** 0.5 or 1.0
        return [v / norm for v in values]

    def store_fact(self, user_id: UUID, text: str, source: str) -> None:
        self.ensure_collection()
        self.client.upsert(
            collection_name=self.collection,
            points=[PointStruct(id=str(uuid4()), vector=self.embed(text), payload={"user_id": str(user_id), "text": text, "source": source})],
        )

    def search(self, user_id: UUID, query: str, limit: int = 5) -> list[str]:
        self.ensure_collection()
        hits = self.client.search(collection_name=self.collection, query_vector=self.embed(query), limit=limit, query_filter=None)
        return [str(hit.payload.get("text")) for hit in hits if hit.payload and hit.payload.get("user_id") == str(user_id)]

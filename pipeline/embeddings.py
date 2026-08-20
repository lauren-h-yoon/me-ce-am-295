"""Voyage embeddings wrapper. Lazy client so importing this module needs no key."""
from __future__ import annotations

import os

from pipeline import config as C

_BATCH = 128


class Embedder:
    def __init__(self, model: str | None = None):
        self.model = model or C.rag.embed_model
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import voyageai
            self._client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
        return self._client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for i in range(0, len(texts), _BATCH):
            batch = texts[i:i + _BATCH]
            resp = self.client.embed(batch, model=self.model, input_type="document")
            out.extend(resp.embeddings)
        return out

    def embed_query(self, text: str) -> list[float]:
        resp = self.client.embed([text], model=self.model, input_type="query")
        return resp.embeddings[0]

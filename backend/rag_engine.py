"""RAG over indexed logs. Heavy deps (faiss, sentence-transformers) load only on first use."""

from __future__ import annotations

from typing import Any


class RAGEngine:

    def __init__(self) -> None:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer

        self._faiss = faiss
        self._np = np

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata: list[Any] = []

    def log_to_text(self, log: Any) -> str:

        text = f"""
        user {log.user_id}
        event {log.event_type}
        ip {log.ip_address}
        resource {log.resource_accessed}
        risk {log.risk_score}
        """

        return text

    def generate_embedding(self, text: str):

        vector = self.model.encode(text)

        return vector

    def index_log(self, log: Any) -> None:

        text = self.log_to_text(log)

        vector = self.generate_embedding(text)

        vector = self._np.array([vector]).astype("float32")

        self.index.add(vector)

        self.metadata.append(log)

    def search(self, query: str, k: int = 5):

        query_vector = self.model.encode(query)

        query_vector = self._np.array([query_vector]).astype("float32")

        _distances, indices = self.index.search(query_vector, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results

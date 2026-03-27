import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class RAGEngine:

    def __init__(self):

        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # FAISS index
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)

        # metadata store
        self.metadata = []

    # -------------------------
    # Convert log to text
    # -------------------------
    def log_to_text(self, log):

        text = f"""
        user {log.user_id}
        event {log.event_type}
        ip {log.ip_address}
        resource {log.resource_accessed}
        risk {log.risk_score}
        """

        return text

    # -------------------------
    # Generate embedding
    # -------------------------
    def generate_embedding(self, text):

        vector = self.model.encode(text)

        return vector

    # -------------------------
    # Index log into vector DB
    # -------------------------
    def index_log(self, log):

        text = self.log_to_text(log)

        vector = self.generate_embedding(text)

        vector = np.array([vector]).astype("float32")

        self.index.add(vector)

        self.metadata.append(log)

    # -------------------------
    # Semantic search
    # -------------------------
    def search(self, query, k=5):

        query_vector = self.model.encode(query)

        query_vector = np.array([query_vector]).astype("float32")

        distances, indices = self.index.search(query_vector, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results
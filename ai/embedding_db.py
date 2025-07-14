import chromadb
from chromadb.config import Settings
import os

class EmbeddingDB:
    def __init__(self, persist_dir):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir, settings=Settings(allow_reset=True))
        self.collection = self.client.get_or_create_collection("law_docs")

    def add_documents(self, docs, embeddings, metadatas, ids):
        self.collection.add(
            documents=docs,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def query(self, embedding, top_k=5):
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        return results
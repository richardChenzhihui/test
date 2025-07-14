from .embedding_db import EmbeddingDB
from .openai_api import get_embedding, ask_gpt

class RAGEngine:
    def __init__(self, db_path):
        self.db = EmbeddingDB(db_path)

    def add_document(self, doc_id, text_blocks, metadata):
        embeddings = [get_embedding(block) for block in text_blocks]
        ids = [f"{doc_id}_{i}" for i in range(len(text_blocks))]
        metadatas = [metadata for _ in text_blocks]
        self.db.add_documents(text_blocks, embeddings, metadatas, ids)

    def query(self, question, top_k=5):
        q_emb = get_embedding(question)
        results = self.db.query(q_emb, top_k=top_k)
        docs = results['documents'][0]
        return docs

    def answer(self, question, top_k=5):
        docs = self.query(question, top_k)
        context = "\n".join(docs)
        answer = ask_gpt(context, question)
        return answer, docs
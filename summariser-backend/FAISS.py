import textwrap
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text):
    
    return [p.strip() for p in text.split('\n') if p.strip()]



def build_faiss_index(chunks):
    embeddings = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings, chunks


def retrieve_relevant_chunks(index, chunks, query, top_k=10, min_relative_score=0.6):
    query_embedding = model.encode([query], convert_to_numpy=True, normalize_embeddings = True)
    scores, indices = index.search(query_embedding, top_k)
    
    top_score = scores[0][0]
    results = []

    for i, score in zip(indices[0], scores[0]):
        # Keep chunks within min_relative_score of the top match
        if score >= top_score * min_relative_score:
            results.append(chunks[i])
            print(score)
            print(chunks[i])

    return results

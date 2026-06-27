# reranking info: https://medium.com/@rossashman/the-art-of-rag-part-3-reranking-with-cross-encoders-688a16b64669
# good video: https://www.youtube.com/watch?v=I9lkQ_eudRA
# rescore results from retrieval with cross-encoding
# could do cross-encoding and LLM reranker (more semantic precision, reasoning)
# the reranker (cross-encoding) uses a transformer architecture with scaled dot product attention to find how relevant a document/chunk is to the query
# cross encoding has low latency and is very quick

from sentence_transformers import CrossEncoder

model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2") # from huggingface

def reranker(query: str, chunks: list[dict]):
    if not chunks:          # no candidates (e.g. nothing uploaded yet) -> nothing to rank
        return []
    sentence_pairs = [(query, chunk["content"]) for chunk in chunks]
    scores = model.predict(sentence_pairs)
    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True) # sticks chunks and scores together like [("a": 0.2), ("b", 0.6)] and sorts by largest score
    return [{**chunk, "score": float(score)} for chunk, score in ranked[:5]] # ** adds a new item to the dict 

# test = reranker('How many ducks are in the pond?', ['The pond is green', 'Jimmy sees 5 ducks in the pond', 'Anna sees a deer in the woods'])
# print(test)
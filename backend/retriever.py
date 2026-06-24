# top x candidates from documents are pulled out based on the query, sent to the reranker
# doing this with RAM memory for now then will switch to vector database

import numpy as np
from embeddings import embed_image, embed_text
from ingestion import ingest

storage = []
def add_to_storage(path):
    """ingest -> chunk -> embed -> store"""
    for chunk in ingest(path):
        if chunk['type'] == 'text':
            vec = embed_text(chunk['content'], prefix='search_document')
        else:
            vec = embed_image(chunk['content'])
        storage.append({'vector': vec, 'meta': chunk})

def retrieve(query, top_k=5):
    """embed the query -> score every stored chunk -> return top k"""
    q = np.array(embed_text(query, prefix='search_query'))
    scored = []
    for item in storage:
        similarity = float(np.dot(q, item['vector'])) # dot product = cosine similarity
        scored.append((similarity, item['meta'])) # append (similarity score, metadata dict) as one tuple
    scored.sort(key=lambda x: x[0], reverse=True) # sort in descending order
    return [meta for _, meta in scored[:top_k]] # returns extracted metadata from dict based on top scores
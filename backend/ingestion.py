# where the upload documents get converted into a readable format and chunked
# storing metadata so that the agent can cite its sources 

import pandas as pd
import pymupdf4llm

def chunk_text(text, size=800, overlap=100):
    """chunking the text by 800 characters with an overlap of 100"""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start: start + size])
        start += size - overlap
    return chunks # list of string chunks like ['i like pizza', 'pizza because']

def load_pdf(path):
    """converting pdf to markdown so it's easier to read/chunk and saving metadata"""
    md = pymupdf4llm.to_markdown(path)
    chunks = []
    for i, piece in enumerate(chunk_text(md)): # using i to number chunks so that it's stored in the metadata and the agent can reference the chunk / where it's from
        chunks.append({"type": "text", "content": piece,
                       "source": path, "page": i})
    return chunks

def load_image(path):
    """do not need to chunk images, only storing metadata because the embedding turns the image into a vector"""
    return [{"type": "image", "content": path, "source": path, "page": 0}]

def ingest(path):
    ext = path.lower().rsplit(".", 1)[-1]
    if ext == "pdf":
        return load_pdf(path)
    elif ext in ("png","jpg","jpeg"):
        return load_image(path)
    else: raise ValueError(f"unsupported file type: {ext}")
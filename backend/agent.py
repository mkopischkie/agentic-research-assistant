# orchestrator
from retriever import retrieve_text, retrieve_image, add_to_storage
from reranker import reranker

def build_context(chunks): # for the llm
    blocks = []
    for i, chunk in enumerate(chunks):
        tag = f"[{i+1}] (source: {chunk['source']}, page: {chunk['page']})"
        if chunk['type'] == 'text':
            blocks.append(f"{tag} \n {chunk['content']}")
        else:
            blocks.append(f"{tag} \n [image: {chunk['content']}]")
    return "\n\n".join(blocks)

def build_citations(chunks): # for user
    return [{"id": i+1, "source": chunk['source'], "page": chunk['page'], "score": chunk.get("score")} for i, chunk in enumerate(chunks)]

def answer(query):
    text_candidates = retrieve_text(query, 15)
    image_candidates = retrieve_image(query, 5)
    top_chunks = reranker(query, text_candidates) + image_candidates # image chunk is the file path so there's no content to read and doesn't need to go through reranker
    context = build_context(top_chunks)
    citations = build_citations(top_chunks)
    response = "No LLM hooked up yet"
    return {"answer": response, "citations": citations, "context": context}

if __name__ == "__main__":
    # ingest ONCE here, not inside answer()
    add_to_storage("uploads/Software_AI Engineer_Data Scientist Resume.pdf")

    result = answer("what programming languages does this candidate know?")

    print("\n=== citations ===")
    for c in result["citations"]:
        score = c["score"]
        score_str = f"{score:.4f}" if score is not None else "n/a"   # images have no score
        print(f"[{c['id']}] {c['source']} p.{c['page']}  score={score_str}")

    print("\n=== context ===")
    print(result["context"])
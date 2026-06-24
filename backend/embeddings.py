# tokenizes the documents so they can be pulled into the retriever and reranker
# for this project, i want to use a multimodal embedding model like voyage-multimodal-3.5 but prefer a free, open-source model instead like nomic
# embeds documents + queries so they can be pulled into the retriever and reranker
# nomic-embed-text-v1.5 (8192-token context) + nomic-embed-vision-v1.5 share ONEblatent space, so text queries can match images

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel, AutoImageProcessor
from PIL import Image

# --- text side (768-dim) ---
text_tokenizer = AutoTokenizer.from_pretrained("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
text_model = AutoModel.from_pretrained("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)

# --- image side (768-dim, same space) ---
img_processor = AutoImageProcessor.from_pretrained("nomic-ai/nomic-embed-vision-v1.5")
vision_model = AutoModel.from_pretrained("nomic-ai/nomic-embed-vision-v1.5", trust_remote_code=True)

def mean_pool(out, mask): # averages many 768-dim vectors into one (with padding so that the averages are the same size) so that we get one vector per sentence
    tok = out[0] # per token vectors (1 sentence, N tokens, 768)
    m = mask.unsqueeze(-1).expand(tok.size()).float() # mask is (1, N) but reshape to (1, N, 768) and the flags are 0, 1 for padding vs real
    return torch.sum(tok * m, 1) / torch.clamp(m.sum(1), min=1e-9) # zeros out padding tokens and takes the average

def embed_text(text: str, prefix: str = "search_query") -> list[float]:
    # prefix: "search_query" for questions, "search_document" for passages
    enc = text_tokenizer([f"{prefix}: {text}"], padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        out = text_model(**enc)
    emb = mean_pool(out, enc["attention_mask"]) # attention masks marks which tokens are real vs padding 
    emb = F.layer_norm(emb, normalized_shape=(emb.shape[1],)) # required for shared space between text and images
    emb = F.normalize(emb, p=2, dim=1) # scale vector to 1 - let's us compare vectors with dot product = cosine similarity
    return emb[0].tolist() # 768 dimensions

def embed_image(image_path: str) -> list[float]:
    inputs = img_processor(Image.open(image_path), return_tensors="pt")
    with torch.no_grad():
        out = vision_model(**inputs).last_hidden_state
    emb = F.normalize(out[:, 0], p=2, dim=1) # no averaging but taking the first slot (CLS token) that's trained to summarize the whole image, normalize to length 1
    return emb[0].tolist()

# test — same idea as before: does tn?
if __name__ == "__main__":
    img = embed_image("uploads/orchid.jpg")
    txt = embed_text("a photo of an orchid")
    similarity = torch.tensor(img) @ torch.tensor(txt)   # both already L2-normalized
    print(similarity)   # higher = m
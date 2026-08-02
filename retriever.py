import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

KB_FOLDER = "knowledge_base"

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

documents = []
embeddings = []

# Read all markdown files
for file in sorted(os.listdir(KB_FOLDER)):
    if file.endswith(".md"):
        with open(os.path.join(KB_FOLDER, file), "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "document": file,
            "passage": text
        })

        # Normalize embeddings
        emb = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        embeddings.append(emb)

embeddings = np.array(embeddings).astype("float32")

# Cosine Similarity Index
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)


def retrieve_documents(question, k=3):

    query = model.encode(
        question,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    scores, ids = index.search(np.array([query]), k)

    print("\nTop Matches")

    results = []

    for score, idx in zip(scores[0], ids[0]):

        print(f"{documents[idx]['document']}   Score: {score:.3f}")

        results.append({
            "document": documents[idx]["document"],
            "passage": documents[idx]["passage"][:500]
        })

    return results
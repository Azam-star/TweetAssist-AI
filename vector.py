import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# =========================
# CONFIG
# =========================
CSV_FILE = r"C:\Users\user\Downloads\LLM Project\twcs_clean_rag_ready.csv"   # ✅ UPDATED
DB_LOCATION = "./chroma_support_db"      # ✅ renamed
COLLECTION_NAME = "customer_support_rag"
BATCH_SIZE = 1000

# =========================
# LOAD DATA
# =========================
print("Loading dataset...")
df = pd.read_csv(CSV_FILE)

print("Rows loaded:", len(df))

# =========================
# EMBEDDING MODEL
# =========================
print("Loading embedding model...")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# =========================
# VECTOR STORE
# =========================
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DB_LOCATION,
    embedding_function=embeddings
)

existing_count = vector_store._collection.count()
print("Existing documents in DB:", existing_count)

# =========================
# PREPARE DOCUMENTS
# =========================
print("Preparing documents...")

documents = []
ids = []

for i, row in df.iterrows():
    text = str(row["clean_text"]).strip()

    if not text:
        continue

    doc = Document(
        page_content=text,  # ✅ tweet text directly
        metadata={
            "author_id": str(row.get("author_id", "")),
            "created_at": str(row.get("created_at", "")),
        },
        id=str(i)
    )

    documents.append(doc)
    ids.append(str(i))

print("Documents prepared:", len(documents))

# =========================
# INGEST (ONLY IF EMPTY)
# =========================
if existing_count == 0:
    print("Ingesting documents into Chroma...")

    for i in range(0, len(documents), BATCH_SIZE):
        batch_docs = documents[i:i + BATCH_SIZE]
        batch_ids = ids[i:i + BATCH_SIZE]

        vector_store.add_documents(
            documents=batch_docs,
            ids=batch_ids
        )

        print(f"Inserted documents {i} to {i + len(batch_docs)}")

    print("Final document count:", vector_store._collection.count())
else:
    print("Using existing embeddings. No re-ingestion needed.")

# =========================
# RETRIEVER
# =========================
retriever = vector_store.as_retriever(
    search_kwargs={"k": 4}   # ✅ tuned for tweets
)

print("✅ Support RAG pipeline ready!")

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from datetime import datetime

# Initialize ChromaDB Persistent Client
client = chromadb.PersistentClient(path="chroma_db")

# Set up embedding function
embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Get or create the collection
collection = client.get_or_create_collection(
    name="chapter_versions",
    embedding_function=embedding_function
)

def save_version(file_path: str, chapter_id: str, version_label="user edit content", source="chapter 1") -> str:
    """Saves a new version of a chapter into ChromaDB"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    timestamp = datetime.now().isoformat()
    doc_id = f"{chapter_id}_{source}_{version_label}_{timestamp}"

    metadata = {
        "chapter_id": chapter_id,
        "source": source,
        "version": version_label,
        "timestamp": timestamp
    }

    collection.add(
        documents=[content],
        ids=[doc_id],
        metadatas=[metadata]
    )

    print(f"✅ Saved: {doc_id}")
    return doc_id

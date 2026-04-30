import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import DB_DIR
from services.embedding_service import embed_texts, embed_query

db_client = chromadb.PersistentClient(path=DB_DIR)


def create_vector_db(text, chat_id):
    collection_name = f"chat_{chat_id.replace('-', '_')}"

    try:
        db_client.delete_collection(collection_name)
    except Exception:
        pass

    collection = db_client.create_collection(collection_name)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    if not chunks:
        return None

    embeddings = embed_texts(chunks)

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

    return collection_name


def search_relevant_chunks(collection_name, question, n_results=5):
    collection = db_client.get_collection(collection_name)

    q_embedding = embed_query(question)

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=n_results
    )

    return results["documents"][0]
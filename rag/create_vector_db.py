import os

import chromadb
from dotenv import load_dotenv
from google import genai

from rag.chunk_documents import load_document, create_chunks


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


chroma_client = chromadb.PersistentClient(
    path="rag/chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="travel_knowledge"
)


if __name__ == "__main__":

    text = load_document("knowledge/kerala_travel.txt")

    chunks = create_chunks(text)

    for i in range(len(chunks)):

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunks[i]
        )

        embedding = response.embeddings[0].values

        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunks[i]],
            embeddings=[embedding]
        )

    print("Total documents stored:", collection.count())
import os

import chromadb
from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


chroma_client = chromadb.PersistentClient(
    path="rag/chroma_db"
)

collection = chroma_client.get_collection(
    name="travel_knowledge"
)


def retrieve_documents(query):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    query_embedding = response.embeddings[0].values

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results


if __name__ == "__main__":

    query = "What are the best adventure activities in Wayanad?"

    results = retrieve_documents(query)

    print("\nRetrieved Documents:\n")

    for i in range(len(results["documents"][0])):

        print(f"\n--- RESULT {i + 1} ---")
        print(results["documents"][0][i])
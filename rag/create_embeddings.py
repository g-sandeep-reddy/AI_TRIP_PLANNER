import os

from dotenv import load_dotenv
from google import genai

from rag.chunk_documents import load_document, create_chunks


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


if __name__ == "__main__":

    text = load_document("knowledge/kerala_travel.txt")

    chunks = create_chunks(text)

    print("Total chunks:", len(chunks))

    for i in range(len(chunks)):

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunks[i]
        )

        embedding = response.embeddings[0].values

        print("\nChunk", i + 1)
        print("Text:", chunks[i][:100])
        print("Embedding dimensions:", len(embedding))
        print("First 10 values:", embedding[:10])
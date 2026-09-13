from pathlib import Path


def load_document(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


def create_chunks(text):

    chunks = text.split("\n\n")

    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    return chunks


if __name__ == "__main__":

    file_path = Path("knowledge/kerala_travel.txt")

    text = load_document(file_path)

    chunks = create_chunks(text)

    print(f"Total chunks: {len(chunks)}")

    for i in range(len(chunks)):
        print("\n--- CHUNK", i + 1, "---")
        print(chunks[i])
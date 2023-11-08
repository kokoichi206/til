import os

import pinecone
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment=os.environ["PINECONE_ENVIRONMENT"],
    )

    index_name = os.environ["PINECONE_INDEX_NAME"]

    if index_name in pinecone.list_indexes():
        pinecone.delete_index(index_name)
        print(f"deleted index: {index_name}")

    pinecone.create_index(
        name=index_name,
        metric="cosine",
        dimension=1536,
    )

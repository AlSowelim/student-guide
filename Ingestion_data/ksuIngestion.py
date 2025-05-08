import gensim
from dotenv import load_dotenv
import os
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
import random
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from typing import List


import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)
# Load environment variables
load_dotenv()

def ingest_docs(batch_size=1000):
    # Load the text file
    with open("/Users/yazeedalfaify/PycharmProjects/ksuRagSystem/darScraped_without_english.txt") as f:
        state_of_the_union = f.read()
        print(f'file {f.name} is read')

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=250)
    print(f'finish splitting')

    # Create documents from the text
    docs = text_splitter.create_documents([state_of_the_union])
    print(f"Total documents to add: {len(docs)}")

    # Process in batches
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i + batch_size]
        print(
            f"Processing batch {i // batch_size + 1}/{len(docs) // batch_size + 1} with {len(batch_docs)} documents")
        PineconeVectorStore.from_documents(
            batch_docs, embeddings, index_name="merged-1500-500"
        )
        print(f"Batch {i // batch_size + 1} loaded to vector store")

    print("****Loading to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()
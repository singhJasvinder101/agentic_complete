from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

load_dotenv()


embedding_model = OpenAIEmbeddings(
    model = "text-embedding-3-large",
)

vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="rag-collection",
    embedding=embedding_model,
)

client = OpenAI()


def process_query(query):
    # relevant chunks from db
    #docs = vector_store.similarity_search("What is the main topic of the document?", k=3)
    docs = vector_store.similarity_search(query)

    #for doc in docs:
        #print(doc.page_content)
        #print(doc.metadata)
        #print("Page Number:", doc.metadata["page"])

    context = "\n\n\n".join([f"Page Number: {doc.metadata['page']}\nContent: {doc.page_content}" for doc in docs])

    SYSTEM_PROMPT = """
    You are a helpful assistant that answers questions based on the context provided from pdf file. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    provide the page_content and page_number of the relevant chunks from the pdf file in your answer.

    Navigate the user to page number for more information.
    Context: {context}

    """

    prompt = SYSTEM_PROMPT.format(context=context)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query}
        ]
    )

    print("Answer:", response.choices[0].message.content)
    return response.choices[0].message.content
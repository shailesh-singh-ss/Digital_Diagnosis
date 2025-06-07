from langchain.schema.runnable import (
    RunnablePassthrough,
    RunnableParallel,
    RunnableLambda
)
from langchain_chroma import Chroma
from instant_answer.prompt import (
    InstantAnswer_prompt,
    InstantAnswer_output_parser
)
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from ingest import embeddings

# Load environment variables from .env file
load_dotenv()

# Initialize the Google LLM models
llm = GoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.5
)

# Prepare our vectorstore & retriever
vectorstores = Chroma(
    persist_directory="db-medembed",
    embedding_function=embeddings
)


def get_similar_cases(query: str,k: int):
    #Extract top k documents from medical knowledge base
    print("Query:",query)
    result = vectorstores.similarity_search(query,k=k)
    print("[INFO] : ", result)
    return result

def similar_cases(x):
    similar_documents = get_similar_cases(x["query"],k=3)
    return similar_documents



# Build our Instant Answer chain
InstantAnswer_chain = (
    RunnableParallel({
        "llm_output":
            RunnablePassthrough.assign(context=RunnableLambda(similar_cases))
            | InstantAnswer_prompt
            # | RunnableLambda(lambda prompt: (print("DEBUG prompt:\n", prompt), prompt)[1])
            | llm,
        "query":   lambda x: x["query"]
    })

    # 4) parse the LLM’s raw output
    | (lambda x: InstantAnswer_output_parser.parse(x["llm_output"]))
)

def generate_instant_answer(query: str):
    """
    Run the chain end-to-end; prints context & prompt,
    returns the parsed answer.
    """
    return InstantAnswer_chain.invoke({
        "query": query
    })  # context is empty for now, can be updated later

from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from diagnosis_symptoms.prompt import initial_prompt, diagnosis_prompt, query_check_prompt, extract_symptoms_prompt,query_reformer_prompt
from ingest import embeddings
# from retrieve_from_graph import retriever
import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from diagnosis_symptoms.retrieve_from_graph import structured_retriever
# from langchain_google_genai import ChatGoogleGenerativeAI


# Load environment variables from a .env file
load_dotenv()

# Define the model to be used for diagnosis
def load_model():
    llm = ChatGroq(model="llama-3.3-70b-versatile", stop_sequences=[])
    return llm




#Define the Genai model 
# def load_gemini():
#     os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
#     llm  = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
#     return llm


# Initialize the LLM
llm = load_model()


opinion_prompt=ChatPromptTemplate.from_template("""You are an assistant for medical diagnostics. Use the following pieces of retrieved context, which reference authoritative medical books and sources containing vast data on diseases, symptoms, and diagnoses, to answer the question. The question will contain a user symptom presentation or description. Your task is to analyze the symptoms, provide a probable diagnosis, and detect potential diseases, explaining your reasoning in a detailed paragraph using medical terminology as a doctor would when describing a diagnosis to a patient.  If you don't know the answer, just say that you are not able to diagnose. 
Question: {question} 
Context: {context} 
Answer:   
""")

# if data is already loaded in vectoredb then run following code
# vectorstores = None
vectorstores = Chroma(persist_directory="db-medembed",embedding_function=embeddings)

vectorstores1= Chroma(persist_directory="db1-medembed",embedding_function=embeddings)


# Create a RetrievalQA chain for diagnosis
qa_chain = RetrievalQA.from_chain_type(
    llm,
    chain_type="stuff",
    retriever=vectorstores.as_retriever(search_kwargs={"k": 5,"filter": {"applicable_gender":{'$in': ['All', 'Male', 'Female']}}}),
    return_source_documents=True
)

def get_similar_cases(query: str,k: int):
    #Extract top k documents from medical knowledge base
    print("Query:",query)
    result = vectorstores.similarity_search(query,k=k)
    return result
    

def format_docs(docs):
    print("Extracted from medical books:",docs)
    return "\n\n".join(doc.page_content for doc in docs)

def get_opinion_from_books(query):
    print("query=",query["symptoms"])
    qa_chain = (
    {
        "context": vectorstores1.as_retriever(search_kwargs={"k": 5}) | format_docs,
        "question": RunnablePassthrough(),
    }
    | opinion_prompt
    | llm
    | StrOutputParser())
    response=qa_chain.invoke(str(query["symptoms"]))
    print("Response from medical books data:",response)
    return response



# Create a conversation memory
memory = ConversationBufferMemory(return_messages=True)


# Define the chain for checkin the level of diagnosis
query_check_chain = (
    RunnablePassthrough()
    | query_check_prompt 
    | llm
    | JsonOutputParser()
)



# Define the chain for asking follow-up questions
symptoms_chain = (
    RunnablePassthrough.assign(chat_history=lambda x: memory.load_memory_variables({})["history"]) 
    | extract_symptoms_prompt 
    | load_model()
    | StrOutputParser()
)


# Define the chain for making a diagnosis

def process_chat_history(x):
    # Get the symptoms 
    symptoms = symptoms_chain.invoke({"input": ""})
    return symptoms

def log_similar_cases_withmetadata(x):
    similar_documents = get_similar_cases(x["symptoms"],k=3)
    return similar_documents

def log_similar_cases_names(x):
    print(x)
    similar_documents = get_similar_cases(x["symptoms"],k=5)
    case_names = [doc.metadata['conditionName'] for doc in similar_documents]
    case_names_string = "\n".join(f"{i + 1}. {name}" for i, name in enumerate(case_names))
    print("case_names_string=",case_names_string)
    return case_names_string

def log_relationships_from_graph(x):
    
    relationships= structured_retriever(x["symptoms"])
    print(relationships)
    return relationships


# Define the chain for asking follow-up questions
follow_up_chain = (
    RunnablePassthrough.assign(chat_history=lambda x: memory.load_memory_variables({})["history"])
    | initial_prompt 
    | llm
    | JsonOutputParser()
)


diagnosis_chain = (
    RunnablePassthrough.assign(chat_history=lambda x: memory.load_memory_variables({})["history"])
    | RunnablePassthrough.assign(symptoms=RunnableLambda(process_chat_history))
    | RunnablePassthrough.assign(similar_cases=RunnableLambda(log_similar_cases_names))
    # | RunnablePassthrough.assign(opinion_from_books=RunnableLambda(get_opinion_from_books))
    | RunnablePassthrough.assign(graph_knowledge_base=RunnableLambda(log_relationships_from_graph))
    | diagnosis_prompt 
    # | RunnableLambda(lambda prompt: (print("DEBUG prompt:\n", prompt), prompt)[1])
    | load_model()
    | JsonOutputParser()
)



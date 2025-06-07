import os
import json
from typing import List
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Neo4jVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from diagnosis_symptoms.prompt import graph_to_naturallanguage_prompt # This must exist



# Load environment variables
load_dotenv()

# Neo4j connection details (required)
NEO4J_URI: str = os.environ["NEO4J_URI"]  
NEO4J_USERNAME: str = os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD: str = os.environ["NEO4J_PASSWORD"]

# Create Neo4j driver (official)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


# Initialize embedding model
embedder = HuggingFaceEmbeddings()


# Groq LLM setup
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Pydantic schema for entities
class Entities(BaseModel):
    names: List[str] = Field(..., description="Extracted diseases, symptoms, etc.")

# Prompt for entity extraction
entity_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are extracting medical entities from user input."),
    ("human", "Extract all diseases, symptoms, causes, treatments, etc., from: {question}")
])

entity_chain = entity_prompt | llm.with_structured_output(Entities)

# Query structured data from Neo4j
def structured_retriever(entities: List) -> str:
    
    output = ""
    

    cypher = """
        CALL db.index.vector.queryNodes("symptom_embedding", 3, $vector)
        YIELD node, score
        WITH node
        MATCH (node)-[r:HAS_SYMPTOM]-(d:Disease)
        RETURN node.id + ' - ' + type(r) + ' -> ' + d.id AS output
        LIMIT 50
    """

    with driver.session() as session:
        for entity in entities:
            try:
                vector = embedder.embed_query(entity)  # Convert text to vector
                records = session.run(cypher, {"vector": vector})
                lines = [record["output"] for record in records]
                output += "\n".join(lines) + "\n"
            except Exception as e:
                print(f"[ERROR] Query failed for '{entity}':", str(e))
    
    return output.strip()


# Final retriever function
def retriever(question: str) -> str:
    print(f"[INFO] User question: {question}")
    
    
    entities = entity_chain.invoke({"question": question})
    print("Extracted Entities:", entities)
    
    # Get structured Neo4j data
    structured_data = structured_retriever(entities.names)

    # Get unstructured data from vector index
    # unstructured_data = [
    #     doc.page_content for doc in vector_index.similarity_search(question, k=3)
    # ]
    # print("[DEBUG] Unstructured data:\n", json.dumps(unstructured_data, indent=2))

    # Merge data
    full_context = f"Structured Data:\n{structured_data}\n\n"

    # Generate NL summary
    output_parser = StrOutputParser()
    summary_chain = graph_to_naturallanguage_prompt | llm | output_parser

    try:
        final_output = summary_chain.invoke({
            "user_query": question,
            "extracted_relationships": full_context
        })
        print("[INFO] Final Answer:\n", final_output)
        return final_output
    except Exception as e:
        print("[ERROR] in LLM chain:", str(e))
        return "Sorry, something went wrong."
    





# Example run
if __name__ == "__main__":
    sample_question = "The patient is a 45-year-old male with chest pain, shortness of breath, and dizziness."
    result = retriever(sample_question)
    print("\n✅ Final Output:\n", result)
    
    # driver.verify_connectivity()

    # model = HuggingFaceEmbeddings()  

    # query_prompt = 'chest pain, shortness of breath'
    # query_embedding = model.embed_query(query_prompt)

    # related_movies, _, _ = driver.execute_query('''
    #     CALL db.index.vector.queryNodes("symptom_embedding", 5, $queryEmbedding)
    #     YIELD node, score
    #     WiTH node
    #     MATCH (node)-[r:HAS_SYMPTOM]-(d:Disease)
    #     RETURN d.id AS Disease, score, node.id AS Symptom, type(r) AS Relationship
    #     ''', queryEmbedding=query_embedding)
    # print(f'Symptom whose plot and title relate to `{query_prompt}`:')
    # for record in related_movies:
    #     print(record)

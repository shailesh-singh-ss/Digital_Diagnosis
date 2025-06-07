from langchain_huggingface import HuggingFaceEmbeddings
import neo4j
import os
from dotenv import load_dotenv  
# Load environment variables
load_dotenv()

# Neo4j connection details
NEO4J_URI = os.getenv("NEO4J_URI")  # e.g., neo4j+s://05e9cceb.databases.neo4j.io
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Verify all required env vars are present
if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
    raise ValueError("Missing Neo4j connection credentials in .env")


def main():
    # Type assertions since we've already verified they're not None
    assert NEO4J_URI is not None
    assert NEO4J_USERNAME is not None
    assert NEO4J_PASSWORD is not None
    
    driver = neo4j.GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    driver.verify_connectivity()

    model = HuggingFaceEmbeddings()  # vector size 384

    batch_size = 100
    batch_n = 1
    movies_with_embeddings = []
    with driver.session() as session:
        # Fetch `Movie` nodes
        result = session.run('MATCH (m:Symptom) RETURN m.id AS symptom')
        for record in result:
            symptom = record.get('symptom')

            # Create embedding for title and plot
            if symptom is not None:
                movies_with_embeddings.append({
                    'symptom': symptom,
                    'embedding': model.embed_query(f'''
                        symptom: {symptom}
                    '''),
                })
            # Import when a batch of movies has embeddings ready; flush buffer
            if len(movies_with_embeddings) == batch_size:
                import_batch(driver, movies_with_embeddings, batch_n)
                movies_with_embeddings = []
                batch_n += 1

        # Flush last batch
        import_batch(driver, movies_with_embeddings, batch_n)

    # Import complete, show counters
    records, _, _ = driver.execute_query('''
    MATCH (m:Symptom WHERE m.embedding IS NOT NULL)
    RETURN count(*) AS countSymptomWithEmbeddings, size(m.embedding) AS embeddingSize
    ''', )
    print(f"""
Embeddings generated and attached to nodes.
Symptom nodes with embeddings: {records[0].get('countSymptomWithEmbeddings')}.
Embedding size: {records[0].get('embeddingSize')}.
    """)


def import_batch(driver, nodes_with_embeddings, batch_n):
    # Add embeddings to Movie nodes
    driver.execute_query('''
    UNWIND $symptom as row
    MATCH (s:Symptom {id: row.symptom})
    CALL db.create.setNodeVectorProperty(s, 'embedding', row.embedding)
    ''', symptom=nodes_with_embeddings)
    print(f'Processed batch {batch_n}.')
    


if __name__ == '__main__':
    main()


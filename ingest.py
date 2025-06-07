from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# Function to load data from CSV files in the specified directory
def load_data(file_path):
    """
    Load documents from CSV files in the given directory.

    Args:
    file_path (str): Path to the directory containing CSV files.

    Returns:
    List of documents loaded from the CSV files.
    """
    loader = CSVLoader(file_path="data/merged_diseases_knowledgebase.csv")
    # documents = [Document(page_content="Some content", metadata={"language": "EN", "author": "Unknown"}),]  #ToDo - Add Metadata
    documents = loader.load()
    # Initialize a list to hold new Document objects with metadata
    new_documents = []

    # Iterate through each document (row) in the loaded data
    for record in documents:
        # Convert the page_content to a dictionary (if needed)
        row_dict = {}
        for line in record.page_content.split('\n'):
            # Check if the line contains a colon
            if ':' in line:
                key, value = line.split(':', 1)  # Split on the first colon
                row_dict[key.strip()] = value.strip()  # Clean up whitespace

        # Create a new Document with original content and metadata
        new_document = Document(page_content=record.page_content, metadata=row_dict)

        # Append the new Document to the list
        new_documents.append(new_document)
    return new_documents

# Function to create text chunks from the loaded documents
def create_text_chunks(documents):
    """
    Split documents into text chunks using a recursive character text splitter.

    Args:
    documents: List of documents to be split into chunks.

    Returns:
    List of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        keep_separator=True,
        add_start_index=True,
        strip_whitespace=True,
    )
    chunks = text_splitter.split_documents(documents)
    return chunks


# downloads embedding model

def hugging_face_embeddings():
    embedding = HuggingFaceEmbeddings(
        model_name = "abhinand/MedEmbed-small-v0.1"
    )
    return embedding


embeddings = hugging_face_embeddings()

# Function to initialize the vector database
def initialize_vectordb():
    """
    Initialize the vector database by loading data, creating text chunks,
    and storing them in a Chroma vector store.
    """
    # Load data from the "data" directory
    extracted_data = load_data("data")


    # # Get Hugging Face embeddings
    # embeddings = hugging_face_embeddings()

    # Create a Chroma vector store and persist it in the "db" directory
    vectorstores = Chroma.from_documents(
        extracted_data,
        embeddings,
        persist_directory="db-medembed"
    )

if __name__ == "__main__":
    initialize_vectordb()

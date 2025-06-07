from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# Function to create document chunks from the medical books for generating embeddings
def load_data():
    """
    Load documents from text files in the given directory.

    Args:
    file_path (str): Path to the directory containing text files.

    Returns:
    List of documents loaded from the text files.
    """
    loader = TextLoader('data/Oxford-Handbook-of-clinical-diagnosis.txt')
    data = loader.load()
    text_splitter =  CharacterTextSplitter(separator = ".",chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    return texts


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
    # Load data from the text files
    extracted_data = load_data()


    # # Get Hugging Face embeddings
    # embeddings = hugging_face_embeddings()

    # Create a Chroma vector store and persist it in the "db1" directory
    vectorstores = Chroma.from_documents(
        extracted_data,
        embeddings,
        persist_directory="db1-medembed"
    )

if __name__ == "__main__":
    initialize_vectordb()

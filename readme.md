# Digital Diagnosis System

An AI-driven health companion that provides an intelligent symptom checker and instant medical Q&A, designed to run locally without storing sensitive health data externally.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Data Ingestion](#data-ingestion)
- [Graph RAG Formation](#graph-rag-formation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Digital Diagnosis System is a Streamlit-based desktop web application providing preliminary health insights. It leverages a medical knowledge graph for symptom analysis and a large language model for instantaneous health-related Q&A. This tool is strictly for educational use and does not replace professional medical advice.

## Features

- **Intelligent Symptom Checker**: Analyze user-entered symptoms against a structured medical knowledge base to suggest possible conditions.
- **Instant Health Q&A**: Ask any health-related question and receive AI-generated answers in real time.
- **Privacy First**: All data processing runs locally; no user health data is stored or shared externally.
- **Responsive UI**: Built with Streamlit and custom CSS for a modern, mobile-friendly interface.
- - **Modular Codebase**: Clearly separated ingestion, embedding, retrieval, graph-RAG, and UI layers.
- - **Graph RAG Retrieval**: Build and query a graph-augmented document store for relationship-aware symptom analysis.

## Architecture

1. **Data Layer**: CSV files under `/data` are ingested, split into chunks, and stored in a Chroma vector database (`/db-medembed`).
2. **Embedding Layer**: Uses HuggingFace MedEmbed-small to convert text chunks into vector embeddings.
3. **Retrieval Layer**: Queries vector store to fetch relevant disease information based on symptoms.
4. **Graph RAG Layer**: Constructs a document graph from scraped sources (`graph_rag/`) and integrates graph embeddings with vector retrieval for enhanced context.
5. **Application Layer**: Streamlit pages (`app.py`) orchestrate symptom checking (`diagnosis_symptoms/diagnosis_page.py`) and instant Q&A (`instant_answer/ia_page.py`).

## Prerequisites

- Python 3.10 or later
- Git (optional, for version control)
- Bash shell for Windows (e.g., WSL Git Bash)
- Access to internet for model downloads

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shailesh-singh-ss/Digital_Diagnosis.git
   cd digital-diagnosis
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\\Scripts\\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Configuration

1. Copy `.env.example` to `.env` and fill in API keys and database credentials:
   ```properties
   GROQ_API_KEY=your_groq_key
   GOOGLE_API_KEY=your_google_key
   NEO4J_URI=neo4j+s://<host>
   NEO4J_USERNAME=<username>
   NEO4J_PASSWORD=<password>
   ```
2. Ensure the `.env` file resides in the project root.

## Data Ingestion

1. Place your medical CSV files in the `/data` folder (default files are provided).
2. Run the ingestion script to build the vector store:
   ```bash
   python ingest.py
   ```
3. The Chroma database will be persisted to `/db-medembed` for fast retrieval.

## Graph RAG Formation

1. Prepare source documents for graph ingestion by running `graph_rag/demo_experiment.ipynb` or placing documents into `graph_rag/demo_graph_documents/`.
2. Use `diagnosis_symptoms/graph_embbeding.py` to load text files (e.g., `Oxford-Handbook-of-clinical-diagnosis.txt`), split into fragments, and generate embedding vectors with HuggingFace MedEmbed-small.
3. Serialize graph document objects (nodes and edges) to `.pkl` files in `graph_rag/demo_graph_documents/` for fast loading.
4. Persist the resulting graph-augmented embeddings to `db1-medembed` for relationship-aware retrieval.
5. The application will auto-load these graph-RAG artifacts at runtime to support multi-hop, context-rich querying in both the symptom checker and instant Q&A.

## Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser.

## Usage

1. **Home Screen**: Choose between Symptom Checker or Instant Q&A.
2. **Symptom Checker**: Enter symptoms, view suggested conditions, and explore details.
3. **Instant Q&A**: Ask free-form health questions and receive AI-driven answers.
4. Use the back button on each page to return to home.

## Project Structure

```
├── app.py                # Main Streamlit app
├── ingest.py             # Data ingestion & vector DB initialization
├── ingest1.py            # (alternate ingestion script)
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys)
├── data/                 # Raw CSV data & static files
├── db-medembed/          # Persisted Chroma vector database
├── diagnosis_symptoms/   # Symptom checker modules and pages
├── instant_answer/       # Instant Q&A modules and pages
└── data_scrapping/       # Jupyter notebook for web scraping
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with detailed description of your changes.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

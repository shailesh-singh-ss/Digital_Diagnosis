# Medical Diagnosis Chatbot

## Description

 Medical diagnosis recommendation systme using Streamlit, LangChain, and various AI models. The recommendation system conducts an interactive consultation with users, asking relevant follow-up questions based on their initial query and symptoms, and provides a potential diagnosis at the end of the consultation.

## Features

- Initial patient information form (age, gender, initial query)
- Dynamic question generation based on patient responses
- Up to 10 follow-up questions
- Utilizes LangChain for question generation and diagnosis
- Incorporates Groq's LLM model for natural language processing (You may change the LLM model in the `load_model` function in `diagnosis.py`)
- Vector database (Chroma) for retrieving similar medical cases
- Final diagnosis generation based on the entire conversation

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/tap-health/tap-health-personalizationAI
    cd diagnosis_recomendation_system
    ```

2. **Create a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate
    # On Windows, use venv\Scripts\activate
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Create a `.env` file in the project root and add your Groq API key:
      ```env
      GROQ_API_KEY=your_groq_api_key_here
      ```

5. **Initialize the database:**
    ```sh
    python ingest.py
    ```

6. **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```

## Usage

1. **Run the Streamlit app:**
    ```sh
    streamlit run app.py
    ```

2. **Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).**

3. **Fill out the initial patient information form and click "Start Diagnosis".**

4. **Answer the follow-up questions provided by the chatbot.**

5. **After receiving the diagnosis, you can start a new consultation if needed.**

## Project Structure

- `app.py`: Main Streamlit application file
- `diagnosis.py`: Contains the core logic for the medical diagnosis system
- `prompt.py`: Defines the prompts used for question generation and diagnosis
- `requirements.txt`: List of Python dependencies
- `.env`: Environment variables file (not included in the repository)

    #### Note: The project structure is subject to change.

    - As mentioned in the functional design, we are using `Chroma` as our Vector DB and passing it to LLM, currently using `ChatGroq(model="llama3-8b-8192")`.
    - For embeddings, we are using `HuggingFaceEmbeddings` with the `sentence-transformers/all-MiniLM-L6-v2` model.

## Dependencies

- Streamlit
- LangChain
- Hugging Face Transformers
- Groq API
- Chroma
- python-dotenv
# Lama Chat Project

This project is designed to process user queries in multiple languages, detect the language of the query, and provide responses in the same language. It utilizes a custom language model API (`OllamaAPI`), a FastAPI web framework for handling HTTP requests, and a language detection library to identify the language of user queries. The responses are translated back to the user's language using a translation service.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Files and Their Functions](#files-and-their-functions)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

The project is organized into the following key components:

- `FastAPI`: A Python web framework used to build the REST API for handling user queries.
- `LangChain`: Used for creating and managing the language model chain.
- `OllamaAPI`: A custom API wrapper around the language model.
- `GoogleTranslator`: A translation service used to translate the model's responses to the user's language.

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/lama-chat-project.git
cd lama-chat-project
```

### Step 2: Set Up a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

```bash
# For Linux/MacOS
python3 -m venv env

# For Windows
python -m venv env
```

### Step 3: Activate the Virtual Environment

```bash
# For Linux/MacOS
source env/bin/activate

# For Windows
env\Scripts\activate
```

### Step 4: Install the Required Packages
Install all required dependencies from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Step 5: Set Up Environment Variables
If there are any specific environment variables needed, you should create a `.env` file in the root directory to store these configurations. The project uses a configuration file (`config.py`) to manage these settings.

### Step 6: Run the Application
After setting up, you can run the FastAPI application using:

```bash
uvicorn app.main:app --reload
```

## Usage

Once the application is running, you can send POST requests to the `/query` endpoint with a JSON payload containing the `query` key. The application will detect the language of the query, process it through the language model, and return a response in the same language.

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"query": "What is the minimum deposit?"}'
```

### Example Response

```json
{
  "result": "The minimum deposit is $100.",
  "run_time": "1.234",
  "language": "en"
}
```

## Folder Structure

```plaintext
lama-chat-project/
│
├── app/
│   ├── __init__.py               # Initializes the FastAPI app
│   ├── models.py                 # Pydantic models used for request validation
│   └── main.py                   # Entry point for the FastAPI application
│
├── lama_model/
│   ├── __init__.py               # Handles the setup and loading of documents into the FAISS index
│   ├── query_handler.py          # Manages the language model chain (RetrievalQA)
│   ├── ollama_api.py             # Custom API wrapper for the language model
│   └── config.py                 # Configuration settings for the project
│
├── env/                          # Virtual environment directory (created after installation)
│
├── requirements.txt              # List of required Python packages
└── README.md                     # Documentation of the project
```

## Files and Their Functions

### app/\_\_init\_\_.py
- Initializes the FastAPI application.

### app/models.py
- Defines the `QueryRequest` Pydantic model, which is used to validate incoming POST requests to the `/query` endpoint.

### app/main.py
- The main entry point of the FastAPI application.
- Handles incoming POST requests, processes queries through the `RetrievalQA` chain, translates the result, and returns the response.

### lama_model/\_\_init\_\_.py
- Manages the setup and loading of documents into the FAISS index.
- Extracts files from a ZIP archive, loads CSV files, and initializes the FAISS vector store for document retrieval.

### lama_model/query_handler.py
- Defines and initializes the `RetrievalQA` chain using the `OllamaAPI` as the language model.
- Configures the retriever for document search using FAISS.

### lama_model/ollama_api.py
- A custom API wrapper around the language model.
- Handles communication with the language model API and processes responses.

### lama_model/config.py
- Stores configuration settings for the project, including model name, size, and paths to required resources.

## Environment Variables

You can define environment-specific configurations in the `.env` file or directly in the `config.py` file. Example variables include:

```plaintext
SEARCH_KWARGS_K=5
ZIP_PATH="qa_trading.zip"
MODEL_NAME="llama3.1"
MODEL_SIZE="8b"
```

from langchain.chains.retrieval_qa.base import RetrievalQA
from . import db
from .config import settings
from .ollama_api import OllamaAPI
from langchain_core.prompts import PromptTemplate

ollama_llm = OllamaAPI(temperature=0.2)

qa_chain = RetrievalQA.from_chain_type(
    llm=ollama_llm,
    return_source_documents=True,
    retriever=db.as_retriever(search_kwargs={"k": settings.SEARCH_KWARGS_K})
)

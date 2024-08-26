import warnings
warnings.filterwarnings('ignore')

import os
import subprocess
import time
from tqdm import tqdm
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import CSVLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
import requests

from zipfile import ZipFile
from .config import settings




zip_path = settings.ZIP_PATH

with ZipFile(zip_path, 'r') as zip:
    zip.extractall('data')

base_dir = 'data'

loaders = {
    '.csv': CSVLoader
}

def create_directory_loader(file_type, directory_path):
    return DirectoryLoader(
        path=directory_path,
        glob=f'**/*{file_type}',
        loader_cls=loaders[file_type],
    )

csv_loader = create_directory_loader('.csv', base_dir)

loaders = [csv_loader]
docs = []

for loader in loaders:
    docs.extend(loader.load())

print(f'Loaded {len(docs)} documents')



model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cuda"}
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)





db = None

for d in tqdm(docs):
    if db:
        db.add_documents([d])
    else:
        db = FAISS.from_documents([d], embeddings)

db.save_local('FAISS_index')







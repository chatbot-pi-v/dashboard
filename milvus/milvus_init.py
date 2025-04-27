from langchain_milvus import Milvus

from config.settings import COLLECTION_NAME, MILVUS_DB_NAME, MILVUS_TOKEN, MILVUS_URI
from embeddings.embedding_model import get_embeddings
from milvus.milvus_db import create_milvus_db
from processing.pdf_loader import load_pdfs

def initialize_milvus(quote):
  create_milvus_db()

  embeddings = get_embeddings()
  documents = load_pdfs(quote)

  print(documents)

  vector_store = Milvus.from_documents(
    documents=documents, 
    embedding=embeddings,
    connection_args={"uri": MILVUS_URI, "token": MILVUS_TOKEN, "db_name": MILVUS_DB_NAME},
    collection_name=COLLECTION_NAME,
    index_params={"index_type": "FLAT", "metric_type": "L2"},
    consistency_level="Strong", 
    drop_old=True
  )

  return vector_store

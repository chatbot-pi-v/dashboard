from langchain_milvus import Milvus
from pymilvus import connections, utility

from config.settings import COLLECTION_NAME, MILVUS_DB_NAME, MILVUS_TOKEN, MILVUS_URI
from embeddings.embedding_model import get_embeddings
from milvus.milvus_db import create_milvus_db
from processing.pdf_loader import load_pdfs
from pymilvus import Collection

def collection_exists(collection_name, uri, token, db_name):
    """
    Verifica se a coleção já existe no Milvus.
    """
    connections.connect(
        alias="default",
        uri=uri,
        token=token,
        db_name=db_name,
    )
    return utility.has_collection(collection_name)

def initialize_milvus(quote):
    # Verifica se a coleção existe
    exists = collection_exists(COLLECTION_NAME, MILVUS_URI, MILVUS_TOKEN, MILVUS_DB_NAME)

    # Cria a coleção apenas se ela não existir
    if not exists:
        create_milvus_db()

    # Carrega embeddings e documentos
    embeddings = get_embeddings()
    documents = load_pdfs(quote)
    print(f"{len(documents)} documentos carregados.")

    # Cria ou atualiza o vetor store no Milvus
    vector_store = Milvus.from_documents(
        documents=documents,
        embedding=embeddings,
        connection_args={
            "uri": MILVUS_URI,
            "token": MILVUS_TOKEN,
            "db_name": MILVUS_DB_NAME
        },
        collection_name=COLLECTION_NAME,
        index_params={
            "index_type": "IVF_FLAT", 
            "metric_type": "IP"
        },
        consistency_level="Strong",
        drop_old=False
    )

    collection = Collection("text_embedding")
    collection.load()

    print("\nNúmero de documentos:", collection.num_entities)
    print("\nInformações da coleção:")
    print(collection.describe())

    return vector_store

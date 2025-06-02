import os
from langchain_milvus import Milvus
from pymilvus import connections, utility, Collection

from config.settings import COLLECTION_NAME, MILVUS_DB_NAME, MILVUS_TOKEN, MILVUS_URI
from embeddings.embedding_model import get_embeddings
from milvus.milvus_db import create_milvus_db
from processing.pdf_loader import load_pdfs


def collection_exists(collection_name, uri, token, db_name):
    connections.connect(
        alias="default",
        uri=uri,
        token=token,
        db_name=db_name,
    )
    return utility.has_collection(collection_name)


def delete_pdfs(folder_path):
    """
    Remove todos os arquivos PDF de uma pasta.
    """
    print(f"folder_path: {folder_path}")
    try:
        os.remove(folder_path)
        print(f"Arquivo removido: {folder_path}")
    except Exception as e:
        print(f"Erro ao remover {folder_path}: {e}")


def initialize_milvus(quote, file_name):
    exists = collection_exists(COLLECTION_NAME, MILVUS_URI, MILVUS_TOKEN, MILVUS_DB_NAME)

    if not exists:
        create_milvus_db()

    embeddings = get_embeddings()
    documents = load_pdfs(quote)
    print(f"{len(documents)} documentos carregados.")

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

    collection = Collection(COLLECTION_NAME)
    collection.load()

    print("\nNúmero de documentos:", collection.num_entities)
    print("\nInformações da coleção:")
    print(collection.describe())

    # 🔥 Remove os PDFs após o upload
    # folder_path = os.path.join("./docs/pdf", file_name)
    delete_pdfs(file_name)

    return vector_store

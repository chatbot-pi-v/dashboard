from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, list_collections

from config.settings import COLLECTION_NAME, MILVUS_DB_NAME, MILVUS_TOKEN, MILVUS_URI

def create_milvus_db():
  #conexão
  connections.connect(
    alias="default", 
    uri=MILVUS_URI, 
    token=MILVUS_TOKEN, 
    db_name=MILVUS_DB_NAME, 
    timeout=60
  )

  fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768),
    FieldSchema(name="file_name", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="quotes", dtype=DataType.VARCHAR, max_length=512),
  ]

  schema = CollectionSchema(fields, description="Coleção de embeddings")

  if COLLECTION_NAME not in list_collections():
    collection = Collection(name=COLLECTION_NAME, schema=schema)
    collection.create_index(
      field_name="vector",
      index_params={
        "index_type": "IVF_SQ8",
        "metric_type": "IP",
        "params": {"nlist": 1024}
      }
    )
    collection.load()
  else:
    collection = Collection(name=COLLECTION_NAME)

  return collection

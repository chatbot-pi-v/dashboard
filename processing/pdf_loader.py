import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from settings_folders import PDF_DIR

def load_pdfs(quote):
  documents = []
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=300)

  for file_name in os.listdir(PDF_DIR):
    file_path = os.path.join(PDF_DIR, file_name)
    if file_name.endswith('.pdf'):
      print(f"Carregando: {file_path}")
      loader = PyPDFLoader(file_path)
      split_docs = loader.load_and_split(text_splitter=text_splitter)

      for doc in split_docs:
          doc.metadata["file_name"] = file_name
          doc.metadata["quotes"] = quote
          
      documents.extend(split_docs)
  
  print("Todos os PDFs foram carregados.")
  for doc in documents:
    print(f"\nDocumento: {doc}\n")
  return documents
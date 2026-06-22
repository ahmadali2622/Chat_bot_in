from langchain_community.document_loaders import TextLoader

loader = TextLoader('scraped_data.txt')
documents = loader.load()

# pdf data 

from langchain_community.document_loaders import PyPDFLoader

loader_pdf = PyPDFLoader('scraped_data.pdf')
documents_pdf = loader_pdf.load()
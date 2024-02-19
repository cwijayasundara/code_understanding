import warnings

from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

load_dotenv()

file_path = "source_code/gpt-4-turbo-research"
# Load
loader = GenericLoader.from_filesystem(
    file_path,
    glob="**/*",
    suffixes=[".py"],
    exclude=["**/non-utf8-encoding.py"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
)
documents = loader.load()
print(len(documents))

""" loop through the files in the documents and print the names of the files """
for doc in documents:
    print(doc)

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=3000, chunk_overlap=200
)
texts = python_splitter.split_documents(documents)
print(len(texts))

db = Chroma.from_documents(texts,
                           OpenAIEmbeddings(disallowed_special=()),
                           persist_directory="./vectorstore")
db.persist()
print("source code uploaded to the vector store")

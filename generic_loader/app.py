from dotenv import load_dotenv
import warnings
from pprint import pprint

warnings.filterwarnings('ignore')

load_dotenv()

from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

loader = GenericLoader.from_filesystem(
    "../source_code/java_21_virtual_threads_research",
    glob="*",
    suffixes=[".java", ".properties"],
    parser=LanguageParser(),
)
docs = loader.load()
print(len(docs))

for document in docs:
    pprint(document.metadata)


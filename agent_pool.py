from swarm import Agent
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_unstructured import UnstructuredLoader
from langchain_openai import OpenAIEmbeddings

from lightrag import LightRAG, QueryParam
from lightrag.llm import gpt_4o_mini_complete, gpt_4o_complete

import dotenv
dotenv.load_dotenv()

# Name of the PDF file used to create the knowledge base
file_path = ("proceeding_publications/PDF_FILE_NAME.pdf")
WORKING_DIR = "lightrag_files"

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete 
)

loader = UnstructuredLoader(
    file_path=file_path,
    #strategy="hi_res",
    strategy="fast",
    partition_via_api=True,
    coordinates=True,
)

docs = []
for doc in loader.lazy_load():
    docs.append(doc)


texts = []
for doc in docs:
    texts.append(doc.page_content)

rag.insert(texts)

# ------------------ Define Agent Functions ------------------

def similarity_search_naive(user_query):
    """Performs a naive similarity search on the knowledge base."""
    return rag.query(user_query, param=QueryParam(mode="naive"))

def transfer_to_knowledge_search():
    """Transfers the conversation to the knowledge search agent."""
    return agent_knowledge_search

def transfer_back_to_gillie():
    """Transfers the conversation back to the main agent."""
    return agent_gillie

# ------------------ Define Agents ------------------

agent_gillie = Agent(
    name="Gillie",
    instructions="""You are a helpful and friendly agent called Gillie.
    You are always allowed to use appropiate emojis to make the conversation more engaging.
    You are working for the Gesellschaft für Informatik in der Landwirtschaft (GIL).
    Most likely the user will ask you questions about topics related to the GIL, agriculture in general, 
    or specific authors and papers.
    If the user is asking for information that requires searching the knowledge base, 
    call Scout to handle it.
    If the user asks anything else than topics to the before mentioned topics, 
    tell him that you are currently not able to answer those questions but you are more than welcome to help finding relevant scientific findings in your knowledge base.
    Your knowledge base will contain proceedings from the last 10 years of the GIL conference.""",
    functions=[transfer_to_knowledge_search],
)

agent_knowledge_search = Agent(
    name="Scout",
    instructions="""You are an expert Agent for searching your knowledge base.
    You are working for the Gesellschaft für Informatik in der Landwirtschaft (GIL).
    You are helping Gillie and the user to find relevant scientific findings in the knowledge base
    which contains the conference proceedings from the last GIL conference.
    Remember it is very important to not make up any information, 
    only provide information that is backed by the knowledge base.
    Your knowledge base will contain proceedings from the last 10 years of the GIL conference.
    If you are done with the search, transfer the conversation back to Gillie.""",
    functions=[similarity_search_naive],
)

# ------------------ Attach Functions to Agents ------------------

agent_gillie.functions.append(transfer_to_knowledge_search)
agent_knowledge_search.functions.append(transfer_back_to_gillie)

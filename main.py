from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from unidecode import unidecode
import os

# Load variables from .env file
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

app = FastAPI()


def getDocType(title: str):
    doc_types = [
        "ban-ghi-nho",
        "ban-thoa-thuan",
        "bao-cao",
        "bien-ban",
        "chuong-trinh",
        "cong-thu",
        "cong-van",
        "de-an",
        "du-an",
        "giay-gioi-thieu",
        "giay-moi",
        "giay-nghi-phep",
        "giay-uy-quyen",
        "hop-dong",
        "huong-dan",
        "ke-hoach",
        "nghi-quyet",
        "phieu-bao",
        "phieu-chuyen",
        "phieu-gui",
        "phuong-an",
        "quy-che",
        "quy-dinh",
        "quyet-dinh",
        "thong-bao",
        "thong-cao",
        "to-trinh",
    ]

    normalized_title = unidecode(title).lower().replace(" ", "-")

    for doc_type in doc_types:
        if doc_type in normalized_title:
            position_find = normalized_title.find(doc_type)
            if position_find == 0 or position_find == 1:
                return doc_type

    return None


@app.get("/")
def index(title: str, type: str):
    # Handle the type of document and load the corresponding criteria
    criteria_path = ""
    if type == "admin-doc":
        doc_type = getDocType(title)

        # If the document type is not found, return "Khác"
        if doc_type == None:
            return {"data": "Khác"}

        criteria_path = "criteria/VBHC/" + doc_type + ".pdf"
        docs_prompt = """
            You are a administrative document classifier.
            You can only choose one criterion from the list of criteria below.
            You are not allowed to modify the criterion content that you have chosen.
            Return the criterion you chosen with no further information.
            If no criteria are satisfied, return 'Khác'.
            For example: "Báo cáo tài chính"
            <context>
                {context}
            </context>
            Document content: {input} 
        """

    if type == "book":
        criteria_path = "criteria/Book/book-type.pdf"
        docs_prompt = """
            You are a book classifier.
            You must choose at least 3 criteria from the list of criteria below.
            You are not allowed to modify the criteria content that you have chosen.
            Separate criteria using the '|'.
            Return the criteria you chosen with no further information.
            If no criteria are satisfied, return 'Khác'.
            For example: "Thần bí|Trinh thám|Kinh dị"
            <context>
                {context}
            </context>
            Book content: {input} 
        """

    # Load Criteria
    loader = PyPDFLoader(criteria_path)
    docs = loader.load_and_split()
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)

    # Create LLM
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_template(docs_prompt)

    # Retrieve the document type
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": title})

    # Return the answer
    res = response["answer"].split("|")
    return {"data": res}

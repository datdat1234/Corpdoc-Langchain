from fastapi import FastAPI
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
import os

# Load variables from .env file
load_dotenv()

app = FastAPI()

@app.get("/")
def index(title: str):
  os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

  reader = PdfReader("./tag/tags.pdf")

  raw_text = ""
  for i, page in enumerate(reader.pages):
      text = page.extract_text()
      if text:
          raw_text += text

  text_splitter = CharacterTextSplitter(
      separator="\n",
      chunk_size=1000,
      chunk_overlap=200,
      length_function=len,
  )
  texts = text_splitter.split_text(raw_text)

  embeddings = OpenAIEmbeddings()

  docsearch = FAISS.from_texts(texts, embeddings)

  chain = load_qa_chain(OpenAI(), chain_type="stuff")

  prompt = """ You are a administrative document classifier.
    You can only choose one criterion from the List of criterias above.
    You are not allowed to modify the criterion content that you have chosen.
    Return the criterion you chosen with no further information.
    If no criteria are satisfied, return 'Khác'.
    The first two words in the Document content will be the first two words in the criterion you choose.
    Document content: """
  query = prompt + title
  docs = docsearch.similarity_search(query)
  res = chain.invoke({"query": "", "input_documents": docs, "question": query})
  return {"data": res['output_text']}
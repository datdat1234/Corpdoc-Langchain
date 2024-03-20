########################## LIBRARY ###############################

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import json
import pika
import os

##################################################################

#######################   FUNCTION   #############################

from src.setPath import returnVBHCPath, setCriteriaPath, getDocType

##################################################################

########################## VARIABLE ##############################

from src.rabbitMQ import params
from src.envLoader import openai_api_key, amqp_mongo_queue

##################################################################

os.environ["OPENAI_API_KEY"] = openai_api_key


def langchainProcessor(req):
    # Create producer connection
    producer_conn = pika.BlockingConnection(params)
    producer_channel = producer_conn.channel()

    # Initialize the producer channel
    producer_channel.queue_declare(queue=amqp_mongo_queue, durable=True)
    producer_channel.basic_qos(prefetch_count=10)

    # Convert the request to JSON
    json_data = json.loads(req)
    type = json_data["data"]["type"]
    title = json_data["data"]["title"]

    # Log request
    logRequest(json_data)

    # Handle the type of document and load the corresponding criteria
    criteria_path = ""
    type_path = ""
    if type == "admin-doc":
        doc_type = getDocType(title)
        type_path = "VBHC/"

        # If the document type is not found, return "Khác"
        if doc_type == None:
            json_data["data"]["criteria"] = "VBHC/Khác"
            data_string = json.dumps(json_data)
            producer_channel.basic_publish(
                exchange="",
                routing_key=amqp_mongo_queue,
                body=data_string,
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                ),
            )
            producer_conn.close()
            return

        type_path += returnVBHCPath(doc_type)
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
        type_path = "Sách/"
        docs_prompt = """
            You are a book classifier.
            You must choose at least 3 unique criteria from the list of criteria below.
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
    vector = FAISS.from_documents(docs, embeddings)

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
    criteria = setCriteriaPath(type, type_path, res)
    json_data["data"]["criteria"] = criteria
    data_string = json.dumps(json_data)

    # Send message to Mongo queue
    producer_channel.basic_publish(
        exchange="",
        routing_key=amqp_mongo_queue,
        body=data_string,
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )
    producer_conn.close()


def logRequest(json_data):
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    str_data = json.dumps(json_data)
    print(current_time_str + " - " + str_data)

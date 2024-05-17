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
from src.dataLoader import getCriteriaData

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
    content = json_data["data"]["ocr"]["body"]
    status = json_data["data"]["status"]
    
    # Check if the status is false
    if status == False:
        # Log false status request
        print("Status is False: ", json_data["data"]["fileId"])
        
        # Log request
        logRequest(json_data)

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
    
    # Handle the type of document and load the corresponding criteria
    criteria_path = "file/" + json_data["data"]["fileId"] + ".pdf"
    level2_type = ""
    type_path = ""

    if type == "admin-doc":
        doc_type = getDocType(title)
        type_path = "VBHC/"

        # If the document type is not found, return "Khác"
        if doc_type == None:
            json_data["data"]["criteria"] = "VBHC/Khác"

            # Log request
            logRequest(json_data)

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

        level2_type = returnVBHCPath(doc_type)
        docs_prompt = """
            You are a administrative document classifier.
            You must choose 3 criteria that you think are most suitable for the Document content.
            The criteria returned are separated by vertical bars, for example: "Báo chí|Bưu chính|Viễn thông" (Do not add any space).
            Only choose the criteria, do not return anymore information.
            For example: The document content is: "Báo cáo thị trường Việt Nam 2023". Thus, the output is "Hành chính|Kinh tế|Tài chính".
            The administrative document criteria are:
            <context>
                {context}
            </context>
            Document content: {input} 
        """

    if type == "book":
        type_path = "Sách/"
        docs_prompt = """
            You are a book classifier.
            You must choose 4 criteria that you think are most suitable for the book content.
            The criteria returned are separated by vertical bars, for example: "Tâm linh|Kịch tính|Kinh điển" (Do not add any space).
            Only choose the criteria, do not return anymore information.
            For example: The book content is: "Nhà giả kim". Thus, the output is "Thần bí|Siêu nhiên|Huyền ảo|Kỳ ảo".
            The book criteria are:
            <context>
                {context}
            </context>
            Book content: {input} 
        """

    # Load criteria data from PG
    getCriteriaData(criteria_path, type)

    # Load Criteria
    loader = PyPDFLoader(criteria_path)
    docs = loader.load_and_split()
    embeddings = OpenAIEmbeddings()
    vector = FAISS.from_documents(docs, embeddings)

    # Remove local file
    os.remove(criteria_path)

    # Create LLM
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_template(docs_prompt)

    # Retrieve the document type
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": content})

    # Return the answer
    res = response["answer"].split("|")
    criteria = setCriteriaPath(type, type_path, res, level2_type)
    json_data["data"]["criteria"] = criteria
    data_string = json.dumps(json_data)

    # Log request
    logRequest(json_data)

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
    print(current_time_str)
    print(json_data)

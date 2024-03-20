from fastapi import FastAPI
from src.langchainGPT import langchainProcessor
from src.rabbitMQ import consumer_channel
from src.envLoader import amqp_langchain_queue
import threading

# Initialize FastAPI
app = FastAPI()


# Define FastAPI route
@app.get("/")
def index():
    return {
        "vi": "Dịch vụ Langchain đang chạy...",
        "en": "Langchain service is running...",
    }


# Start the RabbitMQ consumer
def start_consumer():
    consumer_channel.queue_declare(queue=amqp_langchain_queue, durable=True)

    def callback(ch, method, properties, body):
        req = body.decode("utf-8")
        langchainProcessor(req)

    consumer_channel.basic_consume(amqp_langchain_queue, callback, auto_ack=True)
    consumer_channel.start_consuming()


__name__ = "src.main"
if __name__ == "src.main":
    # Start the consumer in a separate thread
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()

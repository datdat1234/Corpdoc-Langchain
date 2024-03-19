###################### LIBRARY ###################################

from dotenv import load_dotenv
import os

##################################################################

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
amqp_protocol = os.environ.get("AMQP_PROTOCOL")
amqp_username = os.environ.get("AMQP_USERNAME")
amqp_password = os.environ.get("AMQP_PASSWORD")
amqp_hostname = os.environ.get("AMQP_HOSTNAME")
amqp_vhost = os.environ.get("AMQP_VHOST")
amqp_langchain_queue = os.environ.get("AMQP_LANGCHAIN_QUEUE")
amqp_mongo_queue = os.environ.get("AMQP_MONGO_QUEUE")
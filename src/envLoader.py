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
pg_user_name = os.environ.get("PG_USER_NAME")
pg_host_name = os.environ.get("PG_HOST_NAME")
pg_password = os.environ.get("PG_PASSWORD")
pg_main_db = os.environ.get("PG_MAIN_DATABASE")
pg_port = os.environ.get("PG_PORT")
vbhc_query_level1 = os.environ.get("DATA_DICT_QUERY_VBHC_LEVEL1")
vbhc_query_level2 = os.environ.get("DATA_DICT_QUERY_VBHC_LEVEL2")
book_query_hc = os.environ.get("DATA_DICT_QUERY_BOOK_HC")
book_query_phc = os.environ.get("DATA_DICT_QUERY_BOOK_PHC")
#######################   FUNCTION   #############################

from langchainGPT import langchainProcessor
from rabbitMQ import consumer_channel

##################################################################
##################################################################

#######################   VARIABLE   #############################

from envLoader import amqp_langchain_queue

##################################################################
##################################################################

consumer_channel.queue_declare(queue=amqp_langchain_queue, durable=True)


def callback(ch, method, properties, body):
    req = body.decode("utf-8")
    langchainProcessor(req)


consumer_channel.basic_consume(amqp_langchain_queue, callback, auto_ack=True)
consumer_channel.start_consuming()

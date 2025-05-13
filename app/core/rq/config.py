import pika

RMQ_HOST = 'rabbitmq'
RMQ_PORT = 5672

RMQ_USER = 'user'
RMQ_PASSWORD = 'password'

connection_params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),
)


def get_connection():
    return pika.BlockingConnection(
        parameters=connection_params
    )

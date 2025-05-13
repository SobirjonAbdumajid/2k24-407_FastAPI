from app.core.rq.config import get_connection
import logging


def callback(ch, method, properties, body):
    logging.info(f"message {body}")


def subscribe():
    connection = get_connection()
    channel = connection.channel()
    queue_name = 'hello'
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
    print("Work")
    channel.start_consuming()


if __name__ == '__main__':
    subscribe()

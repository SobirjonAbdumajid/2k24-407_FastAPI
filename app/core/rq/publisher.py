from app.core.rq.config import get_connection


def publish():
    connection = get_connection()
    channel = connection.channel()
    queue_name = 'hello'
    channel.queue_declare(queue=queue_name)
    for i in range(1, 10):
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=f'Hello World {i}')
        print(f" [x] Sent 'Hello World!'{i}")


if __name__ == '__main__':
    publish()

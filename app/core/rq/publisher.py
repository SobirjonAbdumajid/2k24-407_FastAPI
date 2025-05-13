from app.core.rq.config import get_connection


def publish():
    connection = get_connection()
<<<<<<< HEAD

    channel = connection.channel()

    queue_name = "hello"
    channel.queue_declare(queue=queue_name)
    for i in range(1, 10):
        message = f"Hello World {i}"
        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent {message}")

if __name__ == "__main__":
=======
    channel = connection.channel()
    queue_name = 'hello'
    channel.queue_declare(queue=queue_name)
    for i in range(1, 10):
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=f'Hello World {i}')
        print(f" [x] Sent 'Hello World!'{i}")


if __name__ == '__main__':
>>>>>>> 5a4b339cf09f72926a3b636ac59be0ce332b59e3
    publish()

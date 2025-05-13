from app.core.rq.config import get_connection


def publish():
    connection = get_connection()

    channel = connection.channel()

    queue_name = "hello"
    channel.queue_declare(queue=queue_name)
    for i in range(1, 10):
        message = f"Hello World {i}"
        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent {message}")

if __name__ == "__main__":
    publish()

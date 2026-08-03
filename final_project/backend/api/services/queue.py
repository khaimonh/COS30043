import json
import os

import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
ORDER_QUEUE_NAME = os.getenv("ORDER_QUEUE_NAME", "orders")
ORDER_DLX_NAME = os.getenv("ORDER_DLX_NAME", "orders.dlx")
ORDER_DLQ_NAME = os.getenv("ORDER_DLQ_NAME", "orders.dlq")


def _connect() -> pika.BlockingConnection:
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)


def _ensure_queue(channel) -> None:
    channel.exchange_declare(exchange=ORDER_DLX_NAME, exchange_type="fanout", durable=True)
    channel.queue_declare(queue=ORDER_DLQ_NAME, durable=True)
    channel.queue_bind(exchange=ORDER_DLX_NAME, queue=ORDER_DLQ_NAME)
    channel.queue_declare(
        queue=ORDER_QUEUE_NAME,
        durable=True,
        arguments={"x-dead-letter-exchange": ORDER_DLX_NAME},
    )


def publish_order(order_id: str) -> None:
    connection = _connect()
    try:
        channel = connection.channel()
        _ensure_queue(channel)
        channel.basic_publish(
            exchange="",
            routing_key=ORDER_QUEUE_NAME,
            body=json.dumps({"order_id": order_id}),
            properties=pika.BasicProperties(delivery_mode=2),  # persistent
        )
    finally:
        connection.close()


def start_consumer(on_order: callable) -> None:
    connection = _connect()
    channel = connection.channel()
    _ensure_queue(channel)
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        payload = json.loads(body)
        order_id = payload["order_id"]
        try:
            on_order(order_id)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=ORDER_QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()

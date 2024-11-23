"""
A GraphQL subscription that listens to a Kafka topic.
"""
from typing import AsyncGenerator

import strawberry
from confluent_kafka import Consumer
from strawberry.scalars import JSON

consumer = Consumer(
    {'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092',
     'group.id': 'doogle-consumer-group', 'auto.offset.reset': 'earliest'})
TOPIC_NAME = "orders"
consumer.subscribe([TOPIC_NAME])


# Define a GraphQL subscription that listens to the Kafka consumer
# pylint: disable=R0903
@strawberry.type
class Message:
  """
  A GraphQL message
  """
  payload: JSON


@strawberry.type
class Subscription:
  """
  A GraphQL subscription that listens to a Kafka topic
  """
  @strawberry.subscription
  async def message_subscription(self) -> AsyncGenerator[Message, None]:
    """
      subscription message
    :return: Message
    """
    # Listen to the Kafka consumer and yield messages
    while True:
      msg = consumer.poll(1.0)
      if msg is None:
        continue
      if msg.error():
        m = Message(payload={"error": f"Consumer error: {msg.error()}"})
        print(m)
        raise ValueError("An error occurred in mst.")
      m = Message(payload={
        "message": f'Received message: {msg.value().decode('utf-8')}'})
      print(m)
      yield m

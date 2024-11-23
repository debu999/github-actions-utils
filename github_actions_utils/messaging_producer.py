"""
  Produce messages to a Kafka topic
"""
import json

from confluent_kafka import Producer

producer = Producer(
    {'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092'})

TOPIC_NAME = "orders"


def delivery_report(err, message):
  """ Called once for each message produced to indicate delivery result.
      Triggered by poll() or flush(). """
  if err is not None:
    print(f'Message delivery failed: {err}')
  else:
    print(
      f'Message delivered to {message.topic()} [{message.partition()}] - data {message.value()} - '
      f'offset is {message.offset()} - message is of type {type(message)}')


for data in range(4):
  # Trigger any available delivery report callbacks from previous produce() calls
  producer.poll(0)

  # Asynchronously produce a message. The delivery report callback will
  # be triggered from the call to poll() above, or flush() below, when the
  # message has been successfully delivered or failed permanently.
  producer.produce(TOPIC_NAME, json.dumps({"data": f"{data}"}).encode('utf-8'),
                   callback=delivery_report)

producer.flush()

"""
  Produce messages to a Kafka topic
"""
import json

from confluent_kafka import Producer

from configuration import CONFIG


def delivery_report(err, message):
  """ Called once for each message produced to indicate delivery result.
      Triggered by poll() or flush(). """
  if err is not None:
    print(f'Message delivery failed: {err}')
  else:
    print(f'Message delivered to topic - {message.topic()} partition -'
          f' [{message.partition()}] - data {message.value()} - '
          f'offset is {message.offset()} - message is of type {type(message)}')


if __name__ == "__main__":
  producer = Producer({'bootstrap.servers': CONFIG.bootstrap_servers})

  for data in range(CONFIG.publish_count):
    # Trigger any available delivery report callbacks from previous produce() calls
    producer.poll(CONFIG.producer_poll_rate)

    # Asynchronously produce a message. The delivery report callback will
    # be triggered from the call to poll() above, or flush() below, when the
    # message has been successfully delivered or failed permanently.
    producer.produce(CONFIG.topic,
                     json.dumps({"data": f"{data}"}).encode('utf-8'),
                     callback=delivery_report)

  producer.flush()

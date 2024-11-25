# pylint: disable=missing-function-docstring

"""
Test suite for the messaging producer functionality using pytest and Redpanda as the Kafka broker.
This module includes fixtures and test cases to validate message production and delivery reports.

Fixtures:
    kafka_container: A pytest fixture that sets up a Redpanda container for testing.

Tests:
    test_multiply: A simple test to validate multiplication logic.
    test_produce_message: Tests the message production functionality by
    producing a message to the Kafka topic.

Examples:
    To run the tests, use the pytest command in the terminal.
"""
import json
import os

import pytest
from confluent_kafka import Producer
from testcontainers.kafka import RedpandaContainer

from github_actions_utils.messaging_producer import delivery_report

os.environ["RYUK_CONTAINER_IMAGE"] = "testcontainers/ryuk:0.9.0"
os.environ["APP_ENV"] = "unittest"

@pytest.fixture(scope="session", name="kafka_broker")
def kafka_container():
  """
  Test suite for the messaging producer functionality using pytest and Redpanda as the Kafka broker.
  This module includes fixtures and test cases to validate message production and delivery reports.

  Fixtures:
      kafka_container: A pytest fixture that sets up a Redpanda container for testing.

  Tests:
      test_multiply: A simple test to validate multiplication logic.
      test_produce_message: Tests the message production functionality
      by producing a message to the Kafka topic.

  Examples:
      To run the tests, use the pytest command in the terminal.
  """

  with RedpandaContainer(
      image="docker.redpanda.com/redpandadata/redpanda:v24.2.11") as redpanda:
    bootstrap_server = redpanda.get_bootstrap_server()
    yield {"bootstrap_servers": bootstrap_server}  #


def test_multiply(kafka_broker):

  assert 5 == 10 // 2
  bs = kafka_broker["bootstrap_servers"]
  print(bs)


def test_produce_message(kafka_broker):
  # Create a producer
  bootstrap_servers = kafka_broker["bootstrap_servers"]
  producer = Producer({'bootstrap.servers': bootstrap_servers})
  # Produce a message
  # Trigger any available delivery report callbacks from previous produce() calls
  producer.poll(0)

  # Asynchronously produce a message. The delivery report callback will
  # be triggered from the call to poll() above, or flush() below, when the
  # message has been successfully delivered or failed permanently.
  producer.produce("orders", json.dumps({"data": "1"}).encode('utf-8'),
                   callback=delivery_report)

  producer.flush()

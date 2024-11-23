# import pytest
# from testcontainers import
# from testcontainers.redpanda import RedpandaContainer
#
# @pytest.fixture
# def redpanda_container():
#   with RedpandaContainer() as container:
#     yield container
#
# def test_publish_event(redpanda_container):
#   # Create a producer
#   producer = redpanda_container.get_producer()
#
#   # Publish an event
#   event = {"key": "test_key", "value": "test_value"}
#   producer.produce("test_topic", event)
#
#   # Verify that the event was published
#   consumer = redpanda_container.get_consumer()
#   messages = consumer.consume("test_topic", 1)
#   assert len(messages) == 1
#   assert messages[0].value == event

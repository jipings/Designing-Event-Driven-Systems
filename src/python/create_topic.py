# generate by Copilot
# -*- coding: utf-8 -*-
"""
Create Kafka Topic using confluent_kafka Python library.
This script creates a Kafka topic with specified number of partitions and replication factor.
"""
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import sys
import time
from loguru import logger

def create_kafka_topic(broker_list, topic_name, num_partitions=1, replication_factor=1):
    """
    Create Kafka Topic。

    Args:
        broker_list (str): Kafka Broker address (e.g., 'localhost:9092').
        topic_name (str): Topic Name.
        num_partitions (int): number of Topic partitions.
        replication_factor (int): number of Topic replication factor.
    """
    # Config AdminClient
    conf = {'bootstrap.servers': broker_list}
    admin_client = AdminClient(conf)

    # Create NewTopic Object
    # NewTopic(topic, num_partitions, replication_factor)
    # Note: replication_factor must less than or equal to Broker number
    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

    # Create Topic
    logger.info(f"Creating Topic: '{topic_name}', partitions: {num_partitions}, replication factor: {replication_factor}")
    fs = admin_client.create_topics([new_topic])

    # Check the result of the create operation
    for topic, f in fs.items():
        try:
            f.result() # Wait for the topic creation to complete
            logger.info(f"Topic '{topic}' created successful!")
        except KafkaException as e:
            # Topic already exists or other errors
            if e.args[0].str() == 'TopicAlreadyExists':
                logger.error(f"Topic '{topic}' already exists.")
            else:
                logger.error(f"Created Topic '{topic}' Failed: {e}")
        except Exception as e:
            logger.error(f"Exception error: {e}")

    # wait for the cluster state to update
    time.sleep(1)

    # Close AdminClient
    admin_client.poll(0) # make sure any pending callbacks are processed
    # admin_client.close()

if __name__ == "__main__":
    KAFKA_BROKER = 'localhost:9092'
    TOPIC_TO_CREATE = 'purchase'
    NUM_PARTITIONS = 3
    REPLICATION_FACTOR = 1

    logger.info(f"Broker: {KAFKA_BROKER}")
    create_kafka_topic(KAFKA_BROKER, TOPIC_TO_CREATE, NUM_PARTITIONS, REPLICATION_FACTOR)

    # Verify Topic creation
    logger.info(f"Topic '{TOPIC_TO_CREATE}' created with {NUM_PARTITIONS} partitions and replication factor {REPLICATION_FACTOR}.")
    logger.info("You can use kafka-topics.sh tool to verify the topic creation.")
    logger.info("Example command: bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic my_test_topic_from_python")

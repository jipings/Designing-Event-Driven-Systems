
import time
from uuid import uuid4

from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from loguru import logger

def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    logger.info('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))

def main():
    topic_name = 'purchase'
    
    schema_registry_client = SchemaRegistryClient({
        'url': 'http://localhost:8081'
    })

    registed_schema = schema_registry_client.get_latest_version(topic_name)
    if not registed_schema:
        logger.error(f"Schema for topic '{topic_name}' not found in Schema Registry.")
        return

    schema_str = registed_schema.schema.schema_str
    logger.info(f"Schema for topic '{topic_name}': {schema_str}")
    
    avro_serializer = AvroSerializer(schema_registry_client, schema_str)
    
    purchase_data = {
        'item': "Laptop",
        'total_cost': 1200.50,
        'customer_id': "test_customer_123",
        'quantity': 2,
        'coupon_codes': ["SUMMER21", "BACK2SCHOOL"],
        'purchase_date': 1748530962653,
    }
    
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    producer.produce(
        topic=topic_name,
        key=uuid4().hex,
        headers={'source': 'python_producer'},
        value=avro_serializer(purchase_data,  SerializationContext(topic_name, MessageField.VALUE)),
        on_delivery=delivery_report  
    )
    producer.poll(0)
    producer.flush()
    time.sleep(1)  # Ensure all messages are sent before exiting

if __name__ == '__main__':
    main()

from confluent_kafka import Consumer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from loguru import logger

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
    
    avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)
    
    consumer_config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'purchase_group',
        'auto.offset.reset': 'earliest',
    }
    
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic_name])
    
    while True:
        try:
            #  SIGINT can't be handled when polling, limit timeout to 1 second.
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            
            event = avro_deserializer(msg.value(), SerializationContext(topic_name, MessageField.VALUE))
            logger.info(f"Received message {msg.key()}: {event}")
        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user.")
            break
        except Exception as e:
            logger.error(f"Error while consuming message: {e}")
    
    consumer.close()
    logger.info("Consumer closed.") 
    
if __name__ == '__main__':
    main()

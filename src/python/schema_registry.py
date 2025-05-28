from confluent_kafka.schema_registry import SchemaRegistryClient, Schema
import time
from loguru import logger

def read_json_file(filepath):
    """return the content of the file as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:  
            return f.read()
    except FileNotFoundError:
        logger.error(f"Error: File '{filepath}' not found.")
        return None

# --- Config ---
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
KAFKA_TOPIC_NAME = "purchase"
AVRO_SCHEMA_PATH = '../../avro/purchase.avsc'

def register_avro_schema(schema_registry_url: str, topic_name: str, schema_str: str, is_key: bool = False) -> int:
    """
    register Avro Schema to Schema Registry Service.

    Args:
        schema_registry_url (str): Schema Registry URL
        topic_name (str): Kafka Topic Name
        schema_str (str): Avro Schema JSON string
        is_key (bool): Schema used for Key will be registered with '-key' suffix, 
                       Schema Registry uses convention of '<topic_name>-key' or '<topic_name>-value' as Subject.
    Returns:
        int: registered Schema ID. if registration fails, return None.
    """
    # 1. Config Schema Registry 
    schema_registry_conf = {'url': schema_registry_url}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    # 2. determine Subject Name
    # Schema Registry uses the convention of '<topic_name>-key' or '<topic_name>-value' as Subject
    subject_suffix = "-key" if is_key else "-value"
    subject_name = f"{topic_name}{subject_suffix}"

    # 3. create Schema object
    schema = Schema(schema_str, 'AVRO')

    try:
        # 4. registry shcema
        # register_schema method will submit the schema to the Schema Registry.
        # if the schema is already registered and the same, it returns the existing Schema ID.
        # if the new schema is different, it will register a new version and return the new Schema ID.
        schema_id = schema_registry_client.register_schema(subject_name, schema)
        logger.info(f"Schema for subject '{subject_name}' successful. Schema ID: {schema_id}")
        return schema_id
    except Exception as e:
        logger.error(f"Register Schema Failed for subject '{subject_name}': {e}")
        return None

if __name__ == "__main__":
    logger.info(f"Register Schema to Schema Registry ({SCHEMA_REGISTRY_URL})...")

    logger.info("\n--- Register Schema Value ---")
    user_value_schema_str = read_json_file(AVRO_SCHEMA_PATH)
    if not user_value_schema_str:
        logger.error("Failed to read user_value_schema.avsc file. Exiting.")
        exit(1)
    value_schema_id = register_avro_schema(SCHEMA_REGISTRY_URL, KAFKA_TOPIC_NAME, user_value_schema_str, is_key=False)

    time.sleep(1)

    if value_schema_id:
        logger.info(f"Schema ID {value_schema_id} registered successful for Topic '{KAFKA_TOPIC_NAME}'")
    else:
        print("\nSchema registered failed, please check the logs above for details.")

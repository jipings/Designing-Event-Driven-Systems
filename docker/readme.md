
> $ docker exec -it -w /opt/kafka/bin broker sh

> $ ./kafka-topics.sh --create --topic my-topic --bootstrap-server broker:29092

> $ ./kafka-console-producer.sh  --topic my-topic --bootstrap-server broker:29092

> $ ./kafka-console-consumer.sh --topic my-topic --from-beginning --bootstrap-server broker:29092

https://docs.confluent.io/platform/current/get-started/platform-quickstart.html#ce-docker-quickstart


# Designing-Event-Driven-Systems
## Reference to https://www.confluent.io/
Concepts and Patterns for Streaming Services with Apache Kafka.

JMS (Java Message Service)
AMQP (Advanced Message Queuing Protocol)
DBMS (datebase management system)

### Linear Scalability
hardware-sympathetic

[log-structured approach](https://en.wikipedia.org/wiki/Transaction_log)
[Netflix advises using several smaller clusters](https://netflixtechblog.com/kafka-inside-keystone-pipeline-dd5aeabaf6bb)
[Confluent Platform Overview](https://docs.confluent.io/platform/current/get-started/platform.html)

### Ensuring Messages Are Durable 

### Load-Balance Services and Make Them Highly Available
If an instance of a service dies, data is redirected and ordering guarantees are maintained.

In fact, Kafka releases are always backward-compatible with the previous version, so you are guaranteed to be able to release a new version without taking your system offline.

### Compacted Topics
By default, topics in Kafka are retention-based: messages are retained for some configurable amount of time. Kafka also ships with a special type of topic that manages keyed datasets - that is, data that has a primary key(identifier) as you might have in a database table. These compacted topics retain only the most recent events, with any old events, for a certain key, being removed. They also support deletes.

LSM trees (log-structure merge-trees)

### Long-Term Data Storage
https://www.confluent.io/blog/okay-store-data-apache-kafka/

Data can be stored in regular topics, which are great for audit or Event Sourcing or compacted topics, which reduce the overall footprint. You can combine the two, getting the best of both worlds at the price of additional storage, by holding both and linking them together with a Kafka Streams job. This pattern is called the latest-versioned pattern.

### Security
TLS (Transport Layer Security)

[Apache Kafka Security 101](https://www.confluent.io/blog/apache-kafka-security-authorization-authentication-encryption/)


### Summary
Kafka is a little different from your average messaging technology. Being designed as a distributed, scalable infrastructure component makes it an ideal backbone through which services can exchange and buffer events. There are obviously a number of elements unique to the technology itself, but the ones that stand out are its abilities to scale, to run always on, and to retain datasets long-term.



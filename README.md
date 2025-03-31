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
CQRS (Command Query Responsibility Segregation)

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

### A Basis for Collaboration
Service-based architectures, like microservices or SOA(Service-Oriented Architecture), are commonly built with synchronous request-response protocols. This approach is very natural. It is, after all, they way we write programs: we make calls to other code modules, await a response, and continue. It also fits closely with a lot of use cases we see each day: front-facing websites where users hit buttons and expect things to happen, then return.

But when we step into a world of many independent services, things start to change. As the number of services grows gradually, the web of synchronous interactions grows with them. `Previously benign availability issues start to trigger far more widespread outages. Our ops engineers often end up as reluctant detectives, playing out distributed murder mysteries as they frantically run from service to service, piecing together snippets of secondhand information. (Who said what, to whom, and when?)`

[SLA(service-level agreement)](https://en.wikipedia.org/wiki/Service-level_agreement)

[Google: The Calculus of Service Availability: You're only as available as the sum of your dependencies.](https://queue.acm.org/detail.cfm?id=3096459)

[Putting Apache Kafka To Use: A Practical Guide to Building an Event Streaming Platform ](https://www.confluent.io/blog/event-streaming-platform-1/)


### Commands, Events, and Queries
[Command Query Separation](https://martinfowler.com/bliki/CommandQuerySeparation.html)

* Commands

Commands are actions -- requests for some operation to be performed by another service, something that will change the state of the system. Commands execute synchronously and typically indicate completion, although they may also include a result.

[ProcessManager](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ProcessManager.html)

* Events

Events are both a fact and a notification. They represent something that happened in the real world but include no expectation of any future action. They travel in only direction and expect no response (sometimes called "fire and forget"), but one may be "synthesized" from a subsequent event.

* Queries

Queries are a request to look something up. Unlike events or commands, queries are free of side effects; they leave the state of the system unchanged.

The beauty of events is they wear two hats: a notification hat that triggers services into action, but also a replication hat that copies data from one service to another. But from a services perspective, evnets lead to less coupling than commands and queries. Loose coupling is a desirable property where interactions cross deployment boundaries, as services with fewer dependencies are easier to change.

### Coupling and Message Brokers

### Is Loose Coupling Always Good?
Loose coupling lets components change independently of one another. Tight coupling lets components extract more value from one another.
Sharing always increases the coupling on whatever we decide to share.


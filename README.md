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

### Essential Date Coupling Is Unavoidable

Functional couplings are optional. Core data couplings are essential.

### Using Events for Notification

Most message brokers provide a publish-subscribe facility where the logic for how message are routed is defined by receivers rather than the senders; this process is known as receiver-driven routing. So the receiver retains control of their presence in the interaction, which makes the system pluggable.

### Using Events to Provide State Transfer

[What do you mean by “Event-Driven”?](https://martinfowler.com/articles/201701-event-driven.html)
[Data intergration](https://en.wikipedia.org/wiki/Data_integration)

### Which Approach to Use
We can summarize the advantages of the pure "query by event-carried state transfer" approach as follows:

* Better isolation and autonomy

Isolation is required for autonomy. Keeping the data needed to drive queries isolated and local means it stays under the service's control.

* Faster data access

Local data is typically faster to access. This is particularly true when data from different services needs to be combined, or where the query spans geographies.

* Where the data needs to be available offline

In the case of a mobile device, ship, plane, train, or the like, replicating the dataset provides a mechanism for moving and resynchronizing when connected.

On the other hand, there are advantages to the REST/RPC approach:

* Simplicity

It's simpler to implement, as there are fewer moving parts and no state to manage.

* Singleton

State lives in only one place (inevitable caching aside!), meaning a value can be changed there and all users see it immediately. This is important for use cases that require synchronicity -- for example, reading a previously updated account balance.

* Centralized control

Command-and-control workflows can be used to centralize business processes in a single controlling service. This make it easier to reason about.

### The Event Collaboration Pattern

[Evnet Collaboration](https://martinfowler.com/eaaDev/EventCollaboration.html)

[scaling microservices event stream](https://www.thoughtworks.com/insights/blog/scaling-microservices-event-stream)

The events service's share form a journal, or "shared narrative," describing exactly how your business evolved over time.

### Relationship with Stream Processing

* Stateful approach

Replicate the Customers table into the Kafka Streams API. This makes use of the event-carried state transfer approach.

The dataset needs to be held, in its entirety, in Kafka. So if we are joining to a table of customers, all customer records must be stored in kafka as events.

The stream processor includes in-process, disk-resident storage to hold the table. There is no external database, and this makes the service stateful. Kafka Streams then applies a number of techniques to make managing this statefulness practical.


* Stateless approach

We process events and look up the appropriate customer with every order that is processed.

### Maxing Request-and Event-Driven Protocols

[Domain driven design](https://en.wikipedia.org/wiki/Domain-driven_design)

### Processing Events with Stateful Functions

[Data Driven Programming](https://en.wikipedia.org/wiki/Data-driven_programming)

[Apache Kafka, Samza, and the Unix Philosophy of Distributed Data](https://www.confluent.io/blog/apache-kafka-samza-and-the-unix-philosophy-of-distributed-data/)

[Toward a Functional Programming Analogy for Microservices](https://www.confluent.io/blog/toward-functional-programming-analogy-microservices/)

[Purely functional programming](https://en.wikipedia.org/wiki/Purely_functional_programming)

[Business events in a world of independently deployable services](https://medium.com/expedia-group-tech/business-events-in-a-world-of-independently-deployable-services-144daf6caa1a)

### The Stateful Streaming Approach

### The Practicalities of Being Stateful

[Kafka num standby replicas](https://kafka.apache.org/10/documentation/streams/developer-guide/config-streams.html#num-standby-replicas)

[Kafka compaction](https://kafka.apache.org/documentation.html#compaction)

An event-driven application uses a single input stream to drive its work. A streaming application blends one or more input streams into one or more output streams. A stateful streaming application also recasts streams to tables (used to do enrichments) and stores intermediary state in the log, so it internalizes all the data it needs.

### Event Sourcing, CQRS, and Other Stateful Patterns

[CQRS](https://martinfowler.com/bliki/CQRS.html)

### Event Sourcing, Command Sourcing, and CQRS in a Nutshell
At a high level, Event Sourcing is just the observation that events (i.e., state changes) are a core element of any system. So, if they are stored, immutably, in the order they were created in, the resulting event log provides a comprehensive audit of exactly what the system by rewinding the log and replaying the events in order.

CQRS is a natural progression from this. As a simple example, you might write events to Kafka (write model), read them back, and then push them into a database (read model). In this case kafka maps the read model onto the write model asynchronously, decoupling the two in time so the two parts can be optimized independently.

### Version Control for Your Data

Event Sourcing ensures every state change in a system is recorded, much like a version control system. As the saying goes, "Accountants don't use erasers".

[Staging data](https://en.wikipedia.org/wiki/Staging_(data))

### Making Events the Source of Truth
Event Sourcing ensures that the state a service communicates and the state a service saves internally are the same.

### Command Query Responsibility Segregation

[Write ahead logging](https://en.wikipedia.org/wiki/Write-ahead_logging)

### Materialized Views

If an event stream is the source of truth, you can have as many different views in as many different shapes, sizes, or technologies as you may need. Each is focused on the use case at hand.

### Polyglot Views

### Whole Fact or Delta
[Domain driven design](https://en.wikipedia.org/wiki/Domain-driven_design)

### Implementing Event Sourcing and CQRS with Kafka

### Build In-Process Views with Tables and State Stores in Kafka Streams

### Writing Through a Database into a Kafka Topic with Kafka Connect
[Change data capture](https://en.wikipedia.org/wiki/Change_data_capture)

### Writing Through a State Store to a Kafka Topic in Kafka Streams

### Unlocking Legacy Systems with CDC

### Query a Read-Optimized View Created in a Datebase

### Memory Images/ Prepopulated Caches

### Rethinking Architecture at Company Scales

### Sharing Data and Services Across an Organization

### Kafka materialized views


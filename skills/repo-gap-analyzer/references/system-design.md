# Distributed System Design Assessment Rubric

This reference guide provides an evaluation rubric for distributed systems architecture, resilience, scalability, and data consistency.
It incorporates patterns and reference principles from the **LinuxTips - Descomplicando o System Design** curriculum (by Matheus Fidelis - github.com/msfidelis).

---

## 1. Data Consistency, Databases & The Theorems

### 1.1 CAP & PACELC Theorems
- **CAP Theorem:** In a distributed network partition (P), a system must trade off Consistency (C) vs Availability (A).
- **PACELC Theorem:** If there is a Partition (P), choose between Availability (A) and Consistency (C); Else (E), choose between Latency (L) and Consistency (C).
- **Audit Checklist:**
  - Has the repository declared whether it operates under CP (Consistency/Partition-tolerance) or AP (Availability/Partition-tolerance)?
  - Are read operations from asynchronous replicas handled with awareness of replication lag (eventual consistency)?
  - Are business-critical financial transactions (e.g., Ledger, Payments) relying on eventual consistency without distributed locking or idempotent reconciliation?

### 1.2 Database & Storage Patterns
- **Indexing & Queries:** Check for N+1 queries, unindexed table scans on high-cardinality search columns, and missing compound indexes for multi-column filters.
- **Connection Management:** Connection pool exhaustion prevention (configured max connections, idle timeouts, leak detection).
- **Partitioning & Sharding:** Data sharding keys chosen to prevent hotspotting (avoiding monotonically increasing keys like auto-increment IDs as shard keys).
- **Read Replicas:** Read-heavy workloads separated into Read/Write connection pools (CQRS at data access level).

---

## 2. Caching Strategies & Resilience

### 2.1 Caching Patterns
- **Cache-Aside (Lazy Loading):** Application queries cache first; on miss, queries DB and populates cache. Good for read-heavy, unpredictable query patterns.
- **Write-Through:** Application writes to cache and DB simultaneously. Consistent, but higher write latency.
- **Write-Back (Write-Behind):** Application writes to cache immediately; async worker writes to DB in batches. High performance, risk of data loss on cache crash.
- **Audit GAPs:**
  - Missing TTLs: Keys stored indefinitely causing Redis OOM (Out Of Memory).
  - Thundering Herd / Cache Stampede: Simultaneous cache misses on hot keys causing database overload. (Mitigation: Mutex lock or probabilistic early expiration / jitter).
  - Stale Data & Invalidation: Lack of explicit cache eviction on entity updates or lack of event-driven cache invalidation.

---

## 3. Distributed Transactions, Event-Driven & Consistency

### 3.1 SAGA Pattern (Choreography vs Orchestration)
- Used for distributed transactions across multiple microservices without 2PC (Two-Phase Commit).
- **Choreography:** Services publish and listen to domain events, deciding local actions autonomously. (Risk: difficult to trace, circular dependencies).
- **Orchestration:** Dedicated coordinator service (Saga Orchestrator) commands participant services and triggers compensating transactions on failure.
- **Audit GAPs:**
  - Multi-service writes without compensating transactions. If step 3 fails, steps 1 and 2 remain dirty.
  - Missing Idempotency: Event consumers lacking idempotency keys, causing duplicate processing when messages are re-delivered (at-least-once delivery).
  - Outbox Pattern Missing: Directly publishing to message broker (Kafka/RabbitMQ) inside a database transaction block without Transactional Outbox (risk of Dual Write failure).

### 3.2 CQRS & Event Sourcing
- **CQRS:** Separating Command (write) models from Query (read) models to optimize read performance and independent scaling.
- **Event Sourcing:** State is stored as an immutable sequence of events rather than current state snapshots.
- **Audit GAPs:** Direct query joins across unbounded domains instead of dedicated read projections.

---

## 4. Resilience Patterns (Fault Tolerance)

Reference: *Patterns de Resiliência - LinuxTips System Design*

| Pattern | Objective | Red Flags / GAP in Codebase |
|---|---|---|
| **Circuit Breaker** | Prevent cascading failures when downstream services are down or slow. | Unprotected HTTP/gRPC client calls without state transitions (CLOSED -> OPEN -> HALF-OPEN). |
| **Retry with Backoff & Jitter** | Handle transient network glitches safely. | Blind retries without exponential backoff, or retries without randomized jitter (causing retry storms on recovered services). Retrying non-idempotent POST requests. |
| **Rate Limiting / Throttling** | Protect system resources from noisy neighbors or DDoS. | Public endpoints without token bucket, leaky bucket, or Redis-based rate limiters. |
| **Bulkhead Pattern** | Isolate critical resources so failure in one pool does not starve the entire system. | Single thread pool or HTTP client pool shared across all external API integrations (a slow vendor halts all requests). |
| **Timeouts & Deadlines** | Avoid lingering hanging connections consuming sockets and memory. | Default infinite timeouts on HTTP clients, DB drivers, or messaging acknowledgments. |
| **Graceful Degradation / Fallback** | Provide cached or degraded response when downstream fails. | Crashing the entire page or request because a non-critical personalization service timed out. |

---

## 5. Architectural Topology, SPOF & Scalability

### 5.1 Single Point of Failure (SPOF)
- Check for single database instances with no automated failover, single master nodes, or in-memory session states blocking horizontal scaling (stateless services required).

### 5.2 Cell-Based Architecture
- Segmenting application services and data into self-contained "cells" (shards of infrastructure). A disaster or outage in one cell only affects a fraction of users, keeping blast radius minimal.

### 5.3 Communication Protocols
- Choosing appropriate transport:
  - **Synchronous:** REST (CRUD / public), gRPC (internal service-to-service, high performance, binary Protobuf).
  - **Asynchronous:** Kafka (high throughput event streaming), RabbitMQ / SQS (complex routing, job queues, task processing).
  - **Real-time:** WebSockets / SSE for bidirectional push.

---

## 6. Observability & Telemetry

### 6.1 The Three Pillars
1. **Metrics:** RED (Rate, Errors, Duration) for services; USE (Utilization, Saturation, Errors) for infrastructure. Prometheus / OpenTelemetry format.
2. **Structured Logging:** JSON logs with context, correlation ID (`X-Correlation-Id`), request ID, user/tenant context. No plain unstructured text logs.
3. **Distributed Tracing:** Trace ID and Span ID propagated across HTTP headers (`traceparent`) and message headers for end-to-end latency visualization.

### 6.2 Health Checks
- Probes configured for orchestration (Kubernetes):
  - **Startup Probe:** Checks if initialization is complete.
  - **Liveness Probe:** Detects deadlocks and triggers pod restarts.
  - **Readiness Probe:** Ensures dependencies (DB, broker) are ready before routing traffic.

# Clean Architecture & Domain Boundaries Assessment Rubric

This reference guide establishes criteria for auditing architectural boundaries, layer separation, and domain isolation in a codebase.

---

## 1. Clean Architecture Layers & The Dependency Rule

### 1.1 The Fundamental Dependency Rule
> **Source code dependencies must point only inward, toward higher-level policies.**
> Nothing in an inner circle can know anything at all about something in an outer circle.

```
+--------------------------------------------------------------+
| Frameworks & Drivers (Web, DB, Devices, External UI, CLI)    |
|   +--------------------------------------------------------+ |
|   | Interface Adapters (Controllers, Presenters, Gateways) | |
|   |   +--------------------------------------------------+ | |
|   |   | Application Business Rules (Use Cases)           | | |
|   |   |   +--------------------------------------------+ | | |
|   |   |   | Enterprise Business Rules (Entities / Core)| | | |
|   |   |   +--------------------------------------------+ | | |
|   |   +--------------------------------------------------+ | |
|   +--------------------------------------------------------+ |
+--------------------------------------------------------------+
```

### 1.2 Layer Responsibilities

1. **Entities / Enterprise Business Rules (Domain Core):**
   - Pure domain logic, business invariants, Value Objects, and domain entities.
   - **Zero external dependencies:** Must not import web frameworks (Spring, Express, FastAPI), database libraries (ORM, SQL, Mongo), or serialization protocols (JSON, Protobuf).
   - Independent of UI, database, or external tools.

2. **Use Cases / Application Business Rules:**
   - Orchestrates the flow of data to and from entities.
   - Directs entities to use their enterprise business rules to achieve use case goals.
   - Defines input/output boundaries (Request/Response DTOs).
   - Defines outbound interfaces (Ports) for persistence, notification, and third-party interactions.

3. **Interface Adapters:**
   - Translates data from the format most convenient for use cases/entities to the format most convenient for external agencies (Web, DB).
   - Includes Controllers, Presenters, Webhook Handlers, and Port Adapters (e.g., `PostgresUserRepository` implementing `UserRepositoryPort`).

4. **Frameworks & Drivers:**
   - The glue code: database engines, HTTP web server engines, message queue brokers.
   - All details live here. Details must depend on abstractions, never the reverse.

---

## 2. Ports and Adapters (Hexagonal Architecture) Alignment

### 2.1 Primary (Driving / Inbound) Ports
- Interfaces exposed by the application layer that tell the application what to do.
- Driven by HTTP Controllers, CLI commands, or Message Queue Consumers.
- **GAP to check:** Are controllers directly executing business logic or calling databases?
  - *Violation:* Fat controllers with validation, transaction management, and queries in a single endpoint handler.

### 2.2 Secondary (Driven / Outbound) Ports
- Interfaces defined by the application/domain layer representing required external capabilities.
- Implemented by Infrastructure adapters (e.g., SQL repositories, Redis cache adapters, Stripe payment adapters).
- **GAP to check:** Are repositories defined as interfaces in the domain/application layer, or is the application directly coupled to concrete ORM classes?
  - *Violation:* Use case directly depends on `TypeORM`, `Hibernate / JPA`, or `Mongoose` models.

---

## 3. Common Architectural Anti-Patterns & GAPs

### 3.1 ORM Entity Leaking (The Dual-Entity Anti-Pattern)
- **GAP:** Using ORM database models (`@Entity`, `@Table`) as domain models.
- **Risk:** Database schema changes ripple through core business logic. Database constraints take precedence over business invariants.
- **Remediation:** Separate Domain Entities (pure, rich behavior) from Persistence Entities (schema mapping), converting between them at the repository adapter boundary using explicit mappers.

### 3.2 Framework Pollution of Domain Core
- **GAP:** Importing framework annotations (`@RestController`, `@Autowired`, `@JsonProperty`, `@SerializedName`) directly into domain entities or value objects.
- **Risk:** Vendor lock-in, testing difficulty, unable to upgrade frameworks without modifying core domain logic.

### 3.3 Circular Layer Dependencies
- **GAP:** Layer A imports Layer B, which imports Layer C, which imports Layer A.
- **Remediation:** Introduce dependency inversion: create a port interface in the dependent layer and implement it in the outer layer.

### 3.4 Bypassed Use Cases (Anemic Flow)
- **GAP:** Presentation controllers injecting database repositories directly to perform CRUD without an intermediary application service or use case.
- **Risk:** Logic duplication across different consumers (REST API, background workers, event consumers).

---

## 4. Domain-Driven Design (DDD) Structural Checklist

- [ ] **Ubiquitous Language:** Class and method names reflect domain vocabulary, not technical jargon (`CustomerRegisteredEvent` vs `UserRowInserted`).
- [ ] **Aggregates & Consistency Boundaries:** Root aggregates encapsulate child entities; external callers cannot mutate internal children directly.
- [ ] **Value Objects:** Immutable objects without conceptual identity used for concepts like `Money`, `Email`, `CPF`, `Address`.
- [ ] **Domain Events:** Raised by aggregates when significant business events occur, decoupling side-effects (e.g., sending emails, updating read-models).

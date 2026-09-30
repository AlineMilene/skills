# Clean Code, SOLID & OOP Technical Assessment Rubric

This reference guide establishes deterministic criteria for evaluating source code against Clean Code, SOLID principles, and Object-Oriented Programming (OOP) paradigms.

---

## 1. Clean Code Evaluation Criteria

### 1.1 Meaningful Names & Intent Revelation
- **Self-explanatory Identifiers:** Names of classes, functions, and variables must explain why they exist, what they do, and how they are used without requiring inline comments.
- **Anti-patterns to flag:**
  - Ambiguous abbreviations (`calc()`, `tmp`, `data`, `info`, `proc`).
  - Misleading names (e.g., naming an array `customerList` when it is a map or set).
  - Hungarian notation or encoding prefixes in modern typed languages (`strName`, `iCount`).

### 1.2 Functions & Methods
- **Small and Focused:** Functions should ideally do one thing, do it well, and do it only. Target fewer than 25-30 lines of code per method.
- **Single Level of Abstraction (SLAP):** Statements within a function must operate at the same conceptual level (e.g., high-level orchestrator methods must not contain raw SQL or low-level socket byte manipulations).
- **Function Arguments:** Prefer 0 to 2 arguments. Flag functions taking 4+ parameters without a parameter object / DTO.
- **Side-Effect Free:** Functions should not silently mutate global state or arguments unless explicitly declared by command/query separation (CQS).

### 1.3 DRY, KISS & YAGNI
- **DRY (Don't Repeat Yourself):** Flag duplicate business logic across different services or controller endpoints.
- **KISS (Keep It Simple, Stupid):** Flag over-engineered abstractions where simple linear code would suffice.
- **YAGNI (You Aren't Gonna Need It):** Flag speculative generality, unused abstractions, empty interfaces with only one implementation that has no foreseeable variation, or dead code.

### 1.4 Error Handling & Defensive Programming
- **Exceptions over Error Codes:** Prefer idiomatic exceptions or Result types over returning error codes or null pointers.
- **Fail Fast:** Invariants, precondition validations, and null checks must occur at the boundary/entry of methods.
- **Anti-patterns to flag:**
  - Empty catch blocks (`catch (Exception e) {}`).
  - Swallowing exceptions without logging or rethrowing.
  - Returning `null` instead of empty collections or Optional.
  - Using exceptions for routine flow control.

### 1.5 Unit Testability
- Methods tightly coupled to static singletons, global state, system clock (`now()`), or `new` keyword instantiations inside business logic are severe testability GAPs.

---

## 2. SOLID Principles Audit Matrix

| Principle | Core Question | Architectural Violation / GAP | Remediation Pattern |
|---|---|---|---|
| **S - Single Responsibility** | Does the class have more than one reason to change? | God classes orchestrating HTTP handling, business calculations, SQL queries, and email notifications. | Extract specialized services, handlers, and domain service objects. |
| **O - Open / Closed** | Can behavior be extended without altering existing source code? | Long `switch-case` or `if-else if` cascades checking entity type codes or enums to execute business variations. | Strategy Pattern, Factory Method, or Polymorphic dispatch. |
| **L - Liskov Substitution** | Can subclasses replace their base types without breaking caller contracts? | Subclass overriding parent method by throwing `NotImplementedException`, or requiring `instanceof` checks before invocation. | Favor composition, split inheritance hierarchies, or introduce narrow interfaces. |
| **I - Interface Segregation** | Are clients forced to depend on methods they do not use? | Fat interfaces containing 15+ methods where consumer classes implement dummy/empty stubs. | Role Interfaces; split into focused, single-purpose interfaces. |
| **D - Dependency Inversion** | Do high-level domain modules depend directly on low-level technical details? | Use cases or domain services directly instantiating `SqlConnection`, `HttpClient`, or third-party SDK clients. | Inversion of Control (IoC), Dependency Injection (DI), Ports and Adapters. |

---

## 3. Object-Oriented Programming (OOP / POO) Concepts

### 3.1 Encapsulation & State Invariants
- **Tell, Don't Ask:** Objects should bundle state with behavior. Calling code should tell the object what operation to perform rather than querying internal state, deciding externally, and setting internal state.
- **Anemic Domain Model vs Rich Domain Model:**
  - *GAP:* Domain entities that are only bags of getters and setters with all business logic living in giant procedural service classes.
  - *Target:* Rich entities with private setters, enforcing business invariants inside constructors and mutation methods.
- **Data Hiding:** Fields must be private or protected. Exposing public mutable arrays or collections without defensive copies violates encapsulation.

### 3.2 Abstraction
- Models should represent business concepts with clear semantic boundaries, hiding infrastructural complexity.
- Premature abstraction (creating multiple abstraction layers for trivial pass-through calls) should be flagged as accidental complexity.

### 3.3 Composition over Inheritance
- Inheritance creates the tightest coupling in OOP (white-box reuse).
- Flag deep class inheritance hierarchies (> 3 levels deep).
- Prefer composing behavior using interfaces and injected dependencies.

### 3.4 Polymorphism
- Replace procedural condition branching with polymorphic behavior.
- Ensure contracts are respected across all implementations.

---

## 4. GAP Severity Scoring for Code Quality

- **CRITICAL:** High risk of regression, severe testability roadblock, catastrophic god-class containing mission-critical domain logic.
- **HIGH:** Widespread SOLID violations (DIP missing, hardcoded dependencies, copy-pasted domain logic across endpoints).
- **MEDIUM:** Inconsistent error handling, anemic domain models with logic scattered in controllers, bloated functions.
- **LOW:** Minor naming inconsistencies, missing documentation for public APIs, minor formatting deviations.

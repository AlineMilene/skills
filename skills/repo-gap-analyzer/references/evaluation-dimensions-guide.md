# Master Guide: 25 Dimensions of Technical Repository Assessment

This reference provides the comprehensive evaluation checklist across all 25 technical dimensions for auditing repositories and detecting architectural GAPs.

---

## 1. Correção (Correctness)
- [ ] **Resolução do Problema:** O código implementa integralmente os requisitos de negócio acordados?
- [ ] **Casos de Sucesso:** Os fluxos nominais ("caminho feliz") produzem os resultados esperados com integridade?
- [ ] **Casos de Erro:** Falhas previsíveis (ex: saldo insuficiente, registro inexistente) são tratadas com mensagens adequadas?
- [ ] **Casos Extremos (Edge Cases):** Listas vazias, valores limites (0, valores negativos, números máximos, strings gigantes)?
- [ ] **Tratamento de Nulos:** Evitar `NullReferenceException` / `TypeError`. Uso de `Nullable<T>`, `Optional`, checagens de guarda (*guard clauses*)?
- [ ] **Consistência:** Resultados de cálculos matemáticos, transações financeiras e ordenações são determinísticos e idempotentes?

---

## 2. Legibilidade (Clean Code)
- [ ] **Nomenclatura:** Classes, variáveis e métodos com nomes expressivos que revelam intenção sem abreviações crípticas?
- [ ] **Tamanho de Métodos:** Métodos enxutos ($\le 25-30$ linhas)?
- [ ] **Responsabilidade Única por Método:** O método faz apenas uma coisa e opera em um único nível de abstração (SLAP)?
- [ ] **Indentação:** No máximo 2 a 3 níveis de aninhamento (`if/for/switch`). Uso de *early return* para desaninhar?
- [ ] **Código Autoexplicativo:** A clareza do código dispensa comentários que apenas repetem o que o código faz?
- [ ] **Comentários Pertinentes:** Apenas para explicar o "porquê" (motivação de negócio ou workaround técnico obrigatório)?
- [ ] **Ausência de Código Morto:** Sem blocos comentados, métodos não referenciados ou imports/usings não utilizados?

---

## 3. Orientação a Objetos (OOP / POO)
- [ ] **Encapsulamento:** Propriedades e campos privados ou protegidos; proteção de invariantes de negócio; adoção de *Tell, Don't Ask*?
- [ ] **Abstração:** Modelagem semântica rica, escondendo detalhes técnicos de baixo nível?
- [ ] **Herança:** Utilizada apenas quando há uma relação genuína de "é um" (`is-a`), sem subclasses forçadas?
- [ ] **Polimorfismo:** Despacho dinâmico e polimórfico substituindo longas cadeias de `switch-case` ou `if/else` baseados em tipos?
- [ ] **Composição sobre Herança:** Favorecer injeção de dependências e composição de interfaces sobre herança concreta?
- [ ] **Baixo Acoplamento:** Módulos e classes dependem de interfaces abstratas, minimizando o impacto de alterações?
- [ ] **Alta Coesão:** Métodos e atributos de uma classe trabalham em torno de um único propósito de domínio?

---

## 4. SOLID
- [ ] **Single Responsibility Principle (SRP):** Cada classe possui um único motivo para mudar (sem God Classes)?
- [ ] **Open/Closed Principle (OCP):** Aberto para extensão, fechado para modificação (uso de Strategy, Factory, Plugins)?
- [ ] **Liskov Substitution Principle (LSP):** Subclasses honram integralmente os contratos de suas classes base (sem lançar `NotImplementedException`)?
- [ ] **Interface Segregation Principle (ISP):** Interfaces pequenas e focadas nas necessidades específicas dos consumidores (*Role Interfaces*)?
- [ ] **Dependency Inversion Principle (DIP):** Módulos de alto nível dependem de abstrações (interfaces), nunca de implementações concretas?

---

## 5. Princípios Gerais de Design
- [ ] **DRY (Don't Repeat Yourself):** Eliminação de duplicação de regras de negócio em múltiplos controladores ou serviços?
- [ ] **KISS (Keep It Simple, Stupid):** Solução mais simples possível que atende aos requisitos, sem arquitetura alienígena?
- [ ] **YAGNI (You Aren't Gonna Need It):** Ausência de código especulativo, tabelas não utilizadas ou abstrações "para o futuro"?
- [ ] **Separation of Concerns (SoC):** Separação estrita entre lógica de apresentação, aplicação, domínio e persistência?

---

## 6. Arquitetura
- [ ] **Camadas Bem Definidas:** Fronteiras explícitas e isoladas?
- [ ] **Domínio Separado da Infraestrutura:** O core de negócio não conhece bibliotecas de banco, mensageria ou web?
- [ ] **Dependências na Direção Correta:** Camadas externas apontam para internas (Dependency Rule do Clean Architecture)?
- [ ] **Organização de Pastas e Modularização:** Estrutura clara e coesa por domínios ou por camadas?
- [ ] **Padrão Arquitetural Adequado:** Aplicação coerente de Clean Architecture, Hexagonal, Onion, Vertical Slice ou MVC tradicional?

---

## 7. Design Patterns
- [ ] **Padrões Criacionais:** Factory Method, Abstract Factory, Builder aplicados para construções complexas?
- [ ] **Padrões Estruturais:** Adapter (integrações externas), Facade (simplificar subsistemas), Decorator (caching, logging)?
- [ ] **Padrões Comportamentais:** Strategy (algoritmos variantes), Observer/Pub-Sub (eventos), Mediator (MediatR/desacoplamento), Specification (regras de filtro)?
- [ ] **Padrões de Dados:** Repository, Unit of Work, CQRS (segregação de leitura e escrita)?
- [ ] **Uso Moderado:** Evitar o anti-padrão de *Patternitis* (adicionar padrões sem necessidade real de flexibilidade)?

---

## 8. Tratamento de Erros
- [ ] **Exceptions Específicas:** Uso de exceções tipadas de domínio em vez de `System.Exception`?
- [ ] **Não Engolir Erros:** Sem blocos `catch` vazios; rethrow correto com `throw;` (preservando stack trace)?
- [ ] **Logs Úteis:** Contexto rico (IDs de correlação, parâmetros de negócio não confidenciais)?
- [ ] **Mensagens Claras:** Mensagens compreensíveis para o desenvolvedor e códigos de erro amigáveis para a API?
- [ ] **Retries Apropriados:** Políticas de retentativa apenas para falhas transitórias de infraestrutura?

---

## 9. Performance
- [ ] **Complexidade $O(n)$:** Ausência de operações $O(n^2)$ ou $O(n^3)$ em loops aninhados com buscas em coleções?
- [ ] **Queries Eficientes:** Eliminação de consultas repetidas na mesma requisição e ausência do problema N+1?
- [ ] **Alocações:** Evitar alocações excessivas no Heap; preferir estruturas de buffer (`ArrayPool`, `StringBuilder`)?
- [ ] **Estratégias de Cache:** Uso de cache local ou distribuído (Redis) para dados de leitura frequente e baixa mutabilidade?
- [ ] **Lazy Loading & Streaming:** Paginação obrigatória em listas e uso de streams (`IAsyncEnumerable<T>`, `Stream`) para grandes volumes?
- [ ] **Paralelismo:** Processamento paralelo controlado (`Task.WhenAll`, `Parallel.ForEachAsync`) com limites de concorrência?

---

## 10. Gerenciamento de Memória (.NET / Runtime)
- [ ] **IDisposable & using:** Todo objeto não-gerenciado ou com ciclo de vida crítico encapsulado em `using var` ou `await using var`?
- [ ] **Objetos Grandes (LOH):** Evitar criação contínua de buffers $\ge 85.000$ bytes que afetam a Large Object Heap?
- [ ] **Boxing / Unboxing:** Eliminar conversões desnecessárias de structs/tipos primitivos para `object`?
- [ ] **Span\<T\> & Memory\<T\>:** Uso de `ReadOnlySpan<char>` em manipulações pesadas de strings/payloads para alocação zero?

---

## 11. Concorrência
- [ ] **Thread Safety:** Singletons e serviços compartilhados livres de estado mutável inseguro?
- [ ] **Race Conditions & Deadlocks:** Prevenção de condições de corrida em dados compartilhados e ordem de locks consistente?
- [ ] **Lock Adequado:** Uso de `SemaphoreSlim` para cenários assíncronos (evitando `lock` sincrônico bloqueante)?
- [ ] **Coleções Concorrentes:** Adoção de `ConcurrentDictionary`, `Channel<T>` em ambientes multi-thread?
- [ ] **CancellationToken:** Cancelamento cooperativo respeitado em todas as tarefas longas?

---

## 12. Programação Assíncrona
- [ ] **Async All The Way:** Fluxo assíncrono de ponta a ponta sem interrupções?
- [ ] **Sem Bloqueios Síncronos:** Proibição estrita de `.Result`, `.Wait()` e `.GetAwaiter().GetResult()`?
- [ ] **Propagação de CancellationToken:** Token repassado até as chamadas de banco e clientes HTTP?
- [ ] **ConfigureAwait(false):** Aplicado consistentemente em bibliotecas utilitárias e de infraestrutura?

---

## 13. Banco de Dados
- [ ] **Queries Eficientes:** Planos de execução com índices cobrindo filtros de busca e ordenações?
- [ ] **Problema N+1:** Uso de `Include`/`Join` ou consultas em lote em vez de carregar relações em loop?
- [ ] **Paginação:** Paginação obrigatória via offset ou keyset (cursor-based pagination)?
- [ ] **Transações & Locks:** Transações curtas; níveis de isolamento adequados (`Read Committed`, `Snapshot`); prevenção de deadlocks?
- [ ] **Bulk Operations:** Inserções e atualizações em lote via bulk copy em vez de comandos individuais linha a linha?

---

## 14. APIs
- [ ] **RESTful Semantics:** Uso correto dos verbos HTTP (GET, POST, PUT, PATCH, DELETE) e URIs de recursos coerentes?
- [ ] **Status HTTP Apropriados:** 200, 201, 204, 400, 401, 403, 404, 409, 422, 500, 503?
- [ ] **Versionamento:** Estratégia clara (URI path `/v1/`, headers de accept ou query params)?
- [ ] **Idempotência:** Suporte a chaves de idempotência (`Idempotency-Key`) em operações mutáveis críticas (pagamentos, pedidos)?
- [ ] **Contratos e DTOs:** DTOs de entrada e saída independentes dos modelos internos do domínio/banco?
- [ ] **Validação de Entrada:** Validação robusta de contratos (FluentValidation, DataAnnotations)?
- [ ] **Rate Limiting:** Proteção contra abusos de taxa na API?

---

## 15. Segurança
- [ ] **Injeção (SQLi / NoSQLi):** Uso exclusivo de consultas parametrizadas e ORMs preparados?
- [ ] **Cross-Site Scripting (XSS) & CSRF:** Sanitização de entradas e proteção anti-forgery onde aplicável?
- [ ] **Segredos e Senhas:** Proibição de senhas, chaves de API ou connection strings hardcoded no código ou Git?
- [ ] **Criptografia:** Senhas com hashing forte (BCrypt, Argon2, PBKDF2); dados sensíveis em repouso e trânsito com TLS 1.3?
- [ ] **Autenticação & Autorização:** Validação estrita de tokens JWT (assinatura, emissor, audiência, expiração) e RBAC/ABAC?
- [ ] **Princípio do Menor Privilégio:** Conexões com banco e chaves de nuvem com apenas as permissões estritamente necessárias?

---

## 16. Observabilidade
- [ ] **Logging Estruturado:** Logs gerados em JSON com pares chave/valor pesquisáveis (sem concatenação de strings soltas)?
- [ ] **CorrelationId & TraceId:** Identificador único propagado em requisições HTTP e filas para rastreabilidade de ponta a ponta?
- [ ] **Métricas:** Métricas de negócio e RED (Rate, Errors, Duration) expostas via Prometheus/OpenTelemetry?
- [ ] **Health Checks:** Endpoints dedicados de `/health/live` e `/health/ready` com checagem de dependências vitais?
- [ ] **Monitoramento & Alertas:** Dashboards e alarmes configurados para erros 5xx e latência p99?

---

## 17. Testabilidade
- [ ] **Código Desacoplado:** Classes dependem de interfaces abstratas, facilitando a substituição em testes?
- [ ] **Injeção de Dependências:** Ausência de chamadas estáticas a relógio do sistema, variáveis globais ou instâncias fixas?
- [ ] **Fácil Criação de Mocks:** Ausência de métodos finais/selados ou construtores privados bloqueantes em dependências externas?

---

## 18. Testes
- [ ] **Testes Unitários:** Foco em lógica de domínio e regras de negócio com execução rápida?
- [ ] **Testes de Integração:** Validação de repositórios, bancos em memória ou containers (Testcontainers) e pipelines HTTP?
- [ ] **Testes de Contrato & E2E:** Validação de contratos de API (Pact) e jornadas críticas do usuário?
- [ ] **Casos Negativos e Extremos:** Testes cobrindo falhas, entradas inválidas, limites e timeouts?
- [ ] **Cobertura de Testes:** Cobertura de branches relevante nos módulos de maior risco de negócio?

---

## 19. Manutenibilidade
- [ ] **Cognitive Load:** Outro desenvolvedor consegue ler e entender o fluxo em minutos?
- [ ] **Facilidade de Evolução:** Adicionar uma nova regra ou variação de negócio requer alterar dezenas de arquivos ou apenas plugar um novo componente?
- [ ] **Blast Radius Controlado:** Alterações em um módulo não quebram funcionalidades não-relacionadas?
- [ ] **Dependências Controladas:** O grafo de dependências entre projetos é limpo e sem ciclos?

---

## 20. Escalabilidade
- [ ] **Stateless Design:** A aplicação armazena sessões em memória local ou suporta execução de N instâncias sem afinidade?
- [ ] **Cache Distribuído:** Camada de cache (Redis) dimensionada com invalidação segura?
- [ ] **Mensageria Assíncrona:** Desacoplamento de processos pesados via filas (RabbitMQ, SQS, Kafka)?
- [ ] **Escala Horizontal:** Capacidade de escalar instâncias sob demanda sem bloqueios concorrentes de recursos?

---

## 21. Cloud Readiness (AWS / Azure / GCP)
- [ ] **The 12-Factor App:** Configurações injetadas via variáveis de ambiente, logs para stdout?
- [ ] **Resiliência de Nuvem:** Circuit Breaker, Retries com Jitter, Timeouts e Fallbacks em toda chamada de rede?
- [ ] **Graceful Shutdown:** A aplicação intercepta `SIGTERM` e finaliza requisições em andamento antes de desligar?
- [ ] **Health Probes da Nuvem:** Compatibilidade nativa com probes do Kubernetes / ECS / App Service?

---

## 22. Domain-Driven Design (DDD)
- [ ] **Entidades vs Value Objects:** Objetos com identidade distinta vs objetos imutáveis identificados por seus valores?
- [ ] **Aggregates & Root Entities:** Encapsulamento de agregados onde toda alteração passa pela raiz do aggregate?
- [ ] **Domain Events:** Emissão de eventos de domínio para desacoplar efeitos colaterais de negócio?
- [ ] **Bounded Context & Linguagem Ubíqua:** Nomenclatura e modelos refletem rigorosamente o vocabulário dos especialistas de domínio?

---

## 23. Qualidade de Dependências
- [ ] **Necessidade Real:** As bibliotecas de terceiros trazem valor substancial ou adicionam peso desnecessário?
- [ ] **Versões Atualizadas:** Uso de versões estáveis e suportadas dos frameworks e bibliotecas?
- [ ] **Segurança & CVEs:** Ausência de vulnerabilidades conhecidas nos pacotes (verificado via `dotnet list package --vulnerable` ou `npm audit`)?
- [ ] **Dependências Ativas:** Bibliotecas mantidas ativamente pela comunidade/mantenedores?

---

## 24. DevOps
- [ ] **CI/CD Automatizado:** Pipelines de compilação, testes e empacotamento automatizados em pull requests?
- [ ] **Build Reproduzível:** Builds determinísticos e conteinerizados (Docker multi-stage builds)?
- [ ] **Análise Estática & Linters:** Execução de linters, analisadores de código e SonarQube integrados na esteira?
- [ ] **Quality Gates:** Falhar o pipeline se a cobertura mínima ou limites de dívida técnica forem violados?

---

## 25. Métricas de Código
- [ ] **Complexidade Ciclomática:** Métodos com score de complexidade ciclomática $\le 10-15$?
- [ ] **Fan In / Fan Out:** Módulos com acoplamento aferente e eferente equilibrados?
- [ ] **Profundidade de Herança (DIT):** Hierarquias de herança com profundidade $\le 3$?
- [ ] **Maintainability Index:** Índice de manutenibilidade do código em níveis saudáveis ($> 70$)?
- [ ] **Tamanho por Arquivo:** Classes $\le 300-400$ linhas; métodos $\le 30$ linhas?
- [ ] **Dívida Técnica:** Rastreamento explícito de TODOs, FIXMEs e code smells acumulados?

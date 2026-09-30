# Technical Gap Assessment Report Template

Use this template structure when delivering the final repository audit report.

---

# 📋 Technical Gap Assessment Report: [Repository / System Name]

**Date:** YYYY-MM-DD  
**Auditor:** [Agent / Skill: repo-gap-analyzer]  
**Repository Scope:** `[Path or URL]`  
**Primary Stack:** `[Languages, Frameworks, DBs]`  

---

## 1. Executive Summary & 25-Dimension Radar

Provide a concise 2-paragraph overview of the codebase's current maturity, key risks, and architectural posture.

### Consolidated Radar Scores (0 to 10 Scale)

| # | Dimension | Score | Status | Key Observation |
|:---:|---|:---:|:---:|---|
| **1** | Correção (Casos de sucesso/erro/edge cases/nulos) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **2** | Legibilidade (Clean Code, Nomes, Métodos) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **3** | Orientação a Objetos (Encapsulamento/Coesão/Acoplamento) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **4** | SOLID (SRP, OCP, LSP, ISP, DIP) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **5** | Princípios Gerais (DRY, KISS, YAGNI, SoC) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **6** | Arquitetura (Camadas, Limites, Padrão Arquitetural) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **7** | Design Patterns (Uso correto vs Sobreuso) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **8** | Tratamento de Erros (Exceptions, Logs, Retries) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **9** | Performance (Complexidade, Loops, Alocações, Streaming) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **10** | Gerenciamento de Memória (IDisposable, Span, Boxing, LOH) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **11** | Concorrência (Thread Safety, Deadlocks, Locks) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **12** | Programação Assíncrona (Async/Await, CancellationToken) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **13** | Banco de Dados (Queries, Índices, N+1, Transactions) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **14** | APIs (REST, HTTP Status, Contratos, Idempotência) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **15** | Segurança (Injeção, Secrets, JWT, Criptografia) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **16** | Observabilidade (Logs Estruturados, Tracing, Métricas) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **17** | Testabilidade (Injeção de Dependências, Mocks) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **18** | Testes (Unitários, Integração, Casos Negativos) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **19** | Manutenibilidade (Cognitive Load, Blast Radius) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **20** | Escalabilidade (Stateless, Horizontal, Mensageria) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **21** | Cloud Readiness (Resiliência, Circuit Breaker, 12-Factor) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **22** | Domain Driven Design (Aggregates, VOs, Events) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **23** | Qualidade de Dependências (CVEs, Versões, Deprecations) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **24** | DevOps (CI/CD, Build Reproduzível, Linters) | X/10 | [PASS/WARN/FAIL] | [Resumo] |
| **25** | Métricas de Código (Complexidade Ciclomática, DIT) | X/10 | [PASS/WARN/FAIL] | [Resumo] |

---

## 2. Technical GAP Matrix

Summary of identified GAPs prioritized by risk severity and remediation effort.

| GAP ID | Dimensão | Finding / Vulnerabilidade | Severidade | Esforço | Risco / Impacto |
|:---:|---|---|:---:|:---:|---|
| **GAP-01** | 6. Arquitetura | Entidades de ORM vazadas no Domínio Core | CRITICAL | HIGH | Acoplamento ao banco de dados; inviabiliza testes puros |
| **GAP-02** | 12. Assincronismo | Uso de `.Result` / `.Wait()` causando sync-over-async | CRITICAL | LOW | Risco iminente de ThreadPool starvation e deadlock |
| **GAP-03** | 10. Memória | Objetos `IDisposable` sem bloco `using` / `DisposeAsync` | HIGH | LOW | Vazamento de sockets e conexões no pool de banco |
| **GAP-04** | 21. Cloud Readiness | Chamadas HTTP externas sem Circuit Breaker / Timeout | HIGH | LOW | Falha em cascata sob indisponibilidade de terceiros |
| **GAP-05** | 13. Banco de Dados | Problema de query N+1 em listagem de entidades filhas | HIGH | MEDIUM | Degradação exponencial de latência e consumo de I/O |
| **GAP-06** | 8. Tratamento de Erros| Blocos `catch` vazios engolindo exceções | MEDIUM | LOW | Falhas silenciosas e perda de diagnóstico |

*Severidade: CRITICAL > HIGH > MEDIUM > LOW*  
*Esforço: LOW (horas) > MEDIUM (dias) > HIGH (sprints)*

---

## 3. In-Depth Findings por Dimensão

Para cada GAP identificado, documente:
- **Localização:** Caminho do arquivo e linhas de código relevantes.
- **Violação Encontrada:** Qual anti-padrão ou falha arquitetural está presente.
- **Impacto & Blast Radius:** O que quebra ou degrada sob escala ou manutenção.
- **Recomendação de Correção:** Solução concreta com comparativo antes/depois.

### Exemplo de Entrada:
```markdown
### GAP-02: Bloqueio Síncrono de Tarefa Assíncrona com .Result
- **Dimensão:** 12. Programação Assíncrona (.NET / C#)
- **Localização:** `src/Infrastructure/Repositories/CustomerRepository.cs` (linhas 88-92)
- **Violação:** Invocação de `_httpClient.GetAsync(url).Result` dentro de método assíncrono.
- **Risco:** Bloqueia a thread da ThreadPool até a resposta HTTP retornar. Sob carga de mais de 50 requisições simultâneas, causa ThreadPool Starvation e colapso da API com timeouts.
- **Recomendação de Correção:**
  - Alterar a assinatura do método para `async Task<CustomerDto>`.
  - Usar `await _httpClient.GetAsync(url, cancellationToken)`.
  - Repassar o `CancellationToken` recebido do endpoint até o cliente HTTP.
```

---

## 4. Plano de Ação & Roadmap de Remediação

Organize as ações em 3 horizontes:

### Fase 1: Quick Wins Imediatos (Baixo Esforço, Alto Impacto)
- Eliminar `.Result` e `.Wait()` em código C#/.NET.
- Envolver streams e conexões em `using var` / `await using var`.
- Configurar Timeouts explícitos em todos os `HttpClient` e clientes de banco.
- Corrigir blocos `catch` vazios e adicionar structured logging com `CorrelationId`.

### Fase 2: Refatoração Estrutural e Arquitetural (Médio Esforço)
- Isolar entidades de domínio do ORM utilizando mappers dedicados.
- Quebrar God Classes aplicando Single Responsibility e Strategy Pattern.
- Resolver queries N+1 adicionando paginação e `Include`/eager loading no banco.
- Implementar interfaces segregadas (ISP) e Inversão de Dependência (DIP).

### Fase 3: Evolução de Escala e Resiliência Distribuída (Estratégico / Alto Esforço)
- Implementar Transactional Outbox Pattern para mensageria assíncrona.
- Orquestração de transações distribuídas com SAGA e compensações.
- Cache-Aside com Redis e proteção contra stampede / jitter.
- Implementação de Circuit Breaker e rastreamento distribuído (OpenTelemetry).

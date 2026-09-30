# 🧠 AI Skills Hub — Repositório de Skills para Agentes de IA

[![Author](https://img.shields.io/badge/author-Aline%20Milene-purple.svg)](https://github.com/AlineMilene)
[![License](https://img.shields.io/badge/license-CC--BY--4.0-green.svg)](LICENSE)
[![Skills Count](https://img.shields.io/badge/skills-1%20dispon%C3%ADvel-blue.svg)](#-cat%C3%A1logo-de-skills)
[![Compatibility](https://img.shields.io/badge/compatibilidade-Cursor%20%7C%20Windsurf%20%7C%20Claude%20%7C%20Devin%20%7C%20Hive%20%7C%20Copilot-orange.svg)](#-instala%C3%A7%C3%A3o-multi-agente)

> Repositório oficial e centralizado de **Skills modulares, padronizadas e agnósticas** para assistentes e agentes autônomos de Inteligência Artificial. Projetado por **Aline Milene** para estender capacidades de raciocínio, auditoria de código, arquitetura de sistemas e automações em qualquer ambiente de desenvolvimento.

---

## 📑 Sumário

- [Visão Geral](#-vis%C3%A3o-geral)
- [Catálogo de Skills](#-cat%C3%A1logo-de-skills)
- [Destaque: repo-gap-analyzer](#-destaque-repo-gap-analyzer)
- [Instalação Rápida Automatizada](#-instala%C3%A7%C3%A3o-r%C3%A1pida-automatizada)
- [Instalação Multi-Agente](#-instala%C3%A7%C3%A3o-multi-agente)
  - [Cursor](#cursor)
  - [Windsurf](#windsurf)
  - [Claude Code](#claude-code)
  - [Devin (Cognition AI)](#devin-cognition-ai)
  - [Hive (Hive AI)](#hive-hive-ai)
  - [GitHub Copilot](#github-copilot)
  - [Aider / Roo Code / Cline](#aider--roo-code--cline)
  - [ChatGPT / Custom GPTs](#chatgpt--custom-gpts)
- [Padrão Arquitetural das Skills](#-padr%C3%A3o-arquitetural-das-skills)
- [Como Adicionar Novas Skills](#-como-adicionar-novas-skills)
- [Autoria e Licença](#-autoria-e-licen%C3%A7a)

---

## 🎯 Visão Geral

Este repositório funciona como um **hub de competências (skills)** para IA. Cada skill é um pacote autocontido com instruções mestre ([`SKILL.md`](skills/repo-gap-analyzer/SKILL.md)), referências aprofundadas e scripts determinísticos em Python para execução imediata em sandboxes ou ambientes locais.

**Principais Vantagens:**
- **100% Agnóstico:** Funciona nativamente em Cursor, Windsurf, Claude Code, Devin, Hive, GitHub Copilot, Gemini e ChatGPT.
- **Progressive Disclosure:** Instruções mestre enxutas para economia de tokens, com referências temáticas carregadas sob demanda pelo modelo.
- **Autonomia & Verificação:** Scripts utilitários inclusos para profiling, geração de relatórios e validação estrutural da própria skill.

---

## 📚 Catálogo de Skills

| Skill | Versão | Categoria | Descrição | Status |
|---|:---:|:---:|---|:---:|
| [**repo-gap-analyzer**](skills/repo-gap-analyzer/SKILL.md) | `1.2.0` | Auditoria & Arquitetura | Diagnóstico técnico profundo em **25 dimensões de engenharia** (Clean Code, Clean Arch, SOLID, POO, C#/.NET, Resiliência, System Design) com geração de **dashboard visual em `.html`**. | ✅ Pronta |

*(Novas skills especializadas serão adicionadas continuamente a este catálogo).*

---

## 🌟 Destaque: `repo-gap-analyzer`

A skill **`repo-gap-analyzer`** é uma auditora técnica avançada capaz de identificar débitos técnicos ocultos e falhas arquiteturais:

### As 25 Dimensões de Engenharia Avaliadas:
1. **Correção:** Casos de sucesso, erro, edge cases, nulos e determinismo.
2. **Legibilidade (Clean Code):** Nomes, métodos $\le 30$ linhas, SLAP e ausência de código morto.
3. **Orientação a Objetos (OOP):** Encapsulamento real (*Tell, Don't Ask*), invariantes e modelos ricos.
4. **SOLID:** Aplicação estrita dos 5 princípios (SRP, OCP, LSP, ISP, DIP).
5. **Princípios Gerais:** DRY, KISS, YAGNI e Separation of Concerns (SoC).
6. **Arquitetura:** Clean Architecture, The Dependency Rule, Hexagonal, Onion e Vertical Slice.
7. **Design Patterns:** Factory, Strategy, Adapter, Decorator, Mediator, CQRS sem sobreuso.
8. **Tratamento de Erros:** Exceções específicas, sem engolir erros, `throw;` correto e logs contextuais.
9. **Performance:** Complexidade $O(n)$, eliminação de queries N+1, buffers e streaming.
10. **Gerenciamento de Memória (.NET):** `IDisposable` com `using var`, buffers na LOH e `Span<T>`.
11. **Concorrência:** Thread safety em singletons, locks com `SemaphoreSlim` e CancellationToken.
12. **Programação Assíncrona:** Sem `.Result` ou `.Wait()`, ConfigureAwait e fluxo não-bloqueante.
13. **Banco de Dados:** Índices para buscas, paginação obrigatória, transactions e bulk operations.
14. **APIs:** Verbos REST, códigos de status HTTP corretos, DTOs desacoplados e idempotência.
15. **Segurança:** Prevenção contra SQLi/XSS/CSRF, secrets fora do Git e validação estrita de JWT.
16. **Observabilidade:** Logging estruturado em JSON com `CorrelationId`, `TraceId` e métricas RED/USE.
17. **Testabilidade:** Injeção de dependências, interfaces segregadas e facilidade de mocks.
18. **Testes:** Pirâmide de testes (unitários, integração e contrato) e cobertura de falhas.
19. **Manutenibilidade:** Carga cognitiva reduzida e blast radius controlado para novas features.
20. **Escalabilidade:** Arquitetura stateless, cache distribuído (Redis) e mensageria assíncrona.
21. **Cloud Readiness:** 12-factor, Circuit Breaker, Retries com Jitter, Timeouts e health probes.
22. **Domain Driven Design (DDD):** Entidades, Value Objects, Aggregates e Domain Events.
23. **Qualidade de Dependências:** Bibliotecas justificadas, sem CVEs e pacotes mantidos ativamente.
24. **DevOps:** CI/CD automatizado, builds multi-stage reproduzíveis e SonarQube na esteira.
25. **Métricas de Código:** Complexidade ciclomática, Fan In/Out, profundidade de herança e tech debt.

### Relatório Visual em `.html`:
A skill gera um arquivo **`gap-analysis-report.html`** executivo, 100% autocontido (sem dependência de internet), com:
- Scorecard com notas e barras de progresso para cada uma das 25 dimensões.
- **Banner vermelho de alerta** destacando explicitamente as disciplinas técnicas ausentes no projeto.
- Matriz analítica de GAPs com severidade, esforço de correção e risco.
- Roadmap de remediação estruturado em 3 horizontes (Quick Wins, Refatoração, Escala).

---

## ⚡ Instalação Rápida Automatizada

O repositório inclui instaladores multiplataforma para instalar qualquer skill em seus projetos com um único comando:

### No Windows (PowerShell)
```powershell
# Instalação padrão (cria em <projeto>/skills/repo-gap-analyzer)
.\install.ps1 -TargetDir "C:\Projetos\meu-microsservico" -Agent "generic"

# Instalação direcionada para Cursor ou Windsurf
.\install.ps1 -TargetDir "C:\Projetos\meu-microsservico" -Agent "cursor" -Force

# Instalação para Devin ou Hive
.\install.ps1 -TargetDir "C:\Projetos\meu-microsservico" -Agent "devin" -Force

# Instalação em todas as pastas compatíveis
.\install.ps1 -TargetDir "C:\Projetos\meu-microsservico" -Agent "all" -Force
```

### No Linux / macOS (Bash)
```bash
chmod +x install.sh

# Instalação padrão
./install.sh --target /caminho/do/projeto --agent generic

# Instalação direcionada com link simbólico
./install.sh --target /caminho/do/projeto --agent cursor --symlink --force
```

---

## 🔌 Instalação Multi-Agente

### Cursor
- Execute `.\install.ps1 -Agent cursor -TargetDir "seu-projeto"` (instala em `.cursor/skills/repo-gap-analyzer`).
- Ou adicione no `.cursorrules`:
  ```markdown
  Para auditorias e análise de GAPs técnicos, siga as instruções em `skills/repo-gap-analyzer/SKILL.md`.
  ```

### Windsurf
- Execute `.\install.ps1 -Agent windsurf -TargetDir "seu-projeto"` (instala em `.windsurf/skills/repo-gap-analyzer`).
- No prompt do Cascade:
  `"Audite este repositório aplicando a skill repo-gap-analyzer e gere o relatório .html"`

### Claude Code
- Instale localmente em `.claude/skills/repo-gap-analyzer` ou globalmente em `~/.claude/skills/repo-gap-analyzer`.
- No terminal:
  `claude "Avalie este repositório aplicando a skill repo-gap-analyzer"`

### Devin (Cognition AI)
- **Via Repositório:** Instale com `.\install.ps1 -Agent devin` ou adicione em `.devin/instructions.md` / `DEVIN.md`:
  ```markdown
  Para auditorias arquiteturais e GAPs técnicos:
  1. Leia as 25 dimensões em `skills/repo-gap-analyzer/SKILL.md`.
  2. Execute `python skills/repo-gap-analyzer/scripts/scan_repo_structure.py .` para mapear o projeto.
  3. Execute `python skills/repo-gap-analyzer/scripts/generate_html_report.py --input <dados.json> --out gap-analysis-report.html`.
  4. Apresente o sumário e entregue o arquivo HTML gerado.
  ```
- **Prompt Direto no Devin:**
  > *"Devin, audite este repositório contra as 25 dimensões descritas em `skills/repo-gap-analyzer/SKILL.md`. Identifique débitos técnicos e gere o relatório executivo HTML executando `python skills/repo-gap-analyzer/scripts/generate_html_report.py`."*

### Hive (Hive AI)
- **Manifesto `hive.yaml`:**
  ```yaml
  skills:
    - name: repo-gap-analyzer
      path: skills/repo-gap-analyzer
      entrypoint: SKILL.md
      scripts:
        scan: python scripts/scan_repo_structure.py
        report: python scripts/generate_html_report.py
  ```
- **No Swarm:** Atribua o arquivo `SKILL.md` como system prompt para o agente com role `Software Architecture Auditor`.

### GitHub Copilot
- Adicione no arquivo `.github/copilot-instructions.md`:
  ```markdown
  Ao solicitar revisão arquitetural ou análise de débitos, aplique o framework das 25 dimensões documentado em `skills/repo-gap-analyzer/SKILL.md`.
  ```

### Aider / Roo Code / Cline
- Aponte a instrução da ferramenta:
  ```bash
  aider --read skills/repo-gap-analyzer/SKILL.md
  ```

### ChatGPT / Custom GPTs
- Carregue o arquivo [`SKILL.md`](skills/repo-gap-analyzer/SKILL.md) na caixa de instruções do GPT e faça upload da pasta `references/` como conhecimento.

---

## 🏛️ Padrão Arquitetural das Skills

Cada skill neste repositório adota a estrutura padronizada:

```
skills/<skill-name>/
├── SKILL.md                          # Instruções universais para qualquer agente de IA
├── skill.json                        # Manifesto de metadados, scripts e compatibilidade
├── scripts/                          # Scripts determinísticos em Python (profiling, relatórios)
└── references/                       # Guias e rubricas aprofundadas carregadas sob demanda
```

---

## ➕ Como Adicionar Novas Skills

1. Crie uma nova pasta em `skills/<nome-da-skill>/`.
2. Adicione o arquivo mestre `SKILL.md` com YAML frontmatter válido (`name`, `description`, `author`, `version`).
3. Crie os guias complementares em `references/` e utilitários em `scripts/`.
4. Valide a conformidade estrutural executando o validador interno:
   ```bash
   python skills/repo-gap-analyzer/scripts/validate_skill.py skills/<nome-da-skill>
   ```

---

## 🎓 Autoria e Licença

- **Autora & Idealizadora:** **[Aline Milene](https://github.com/AlineMilene)**
- **Agradecimentos & Referências Conceituais:**
  - *Clean Architecture & SOLID:* Robert C. Martin (Uncle Bob).
  - *Descomplicando o System Design:* [Matheus Fidelis / LinuxTips](https://github.com/msfidelis/linuxtips-curso-descomplicando-o-system-design).
- **Licença:** Distribuído sob a licença [Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/).

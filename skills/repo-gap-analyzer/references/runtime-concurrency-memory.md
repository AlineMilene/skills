# Runtime Engineering: Memory, Concurrency & Asynchronous Programming

This reference guide establishes strict evaluation criteria for runtime execution, resource management, memory allocations, thread safety, and asynchronous programming, with deep coverage of modern runtimes and specifically **C# / .NET**.

---

## 1. Tratamento de Erros (Dimension 8)

### 1.1 Exceptions Específicas vs Genéricas
- **GAP:** Capturar `catch (Exception ex)` genérico ou `catch (SystemException)` sem necessidade no meio da lógica de negócio.
- **Regra:** Capture apenas as exceções que o método é capaz de tratar ou mitigar (`HttpRequestException`, `SqlException`, `TimeoutException`). Se for capturar a genérica, deve ser apenas no middleware/handler global da borda (Global Exception Filter).
- **GAP:** `throw new Exception("erro")` genérico. Lance exceções de domínio tipadas (`NotFoundException`, `DomainValidationException`, `BusinessRuleException`).

### 1.2 Não Esconder Erros (Swallowed Exceptions)
- **GAP:** `catch (Exception) { /* vazio */ }` ou `catch (Exception) { return null; }` ou `catch (Exception) { return false; }`.
- **Risco:** Corrupção silenciosa de estado e impossibilidade de diagnosticar causas raiz em produção.
- **Regra:** Se capturar para re-lançar, use `throw;` puro para preservar o stack trace original. Nunca faça `throw ex;` (reseta o stack trace).

### 1.3 Logs Úteis & Mensagens Claras
- Mensagens de erro devem conter contexto de negócio (ID da transação, tenant, operação) sem expor senhas ou dados sensíveis (LGPD/PCI-DSS).
- Logar no nível correto: `LogLevel.Error` para falhas não recuperáveis, `LogLevel.Warning` para retries/degradação, `LogLevel.Information` para marcos de fluxo.

### 1.4 Estratégias de Retry
- Retries devem ser aplicados apenas em erros transitórios (HTTP 503, 429, timeouts transitórios de rede).
- **Proibido:** Retries cegos em erros de cliente ou negócio (HTTP 400, 401, 403, 404, 422).

---

## 2. Performance & Eficiência de Algoritmos (Dimension 9)

### 2.1 Complexidade Algorítmica & Loops
- **GAP:** Complexidade quadrática $O(n^2)$ ou superior em loops aninhados desnecessários (ex: buscar um item dentro de uma lista interna com `.FirstOrDefault()` repetidamente em vez de pré-indexar em `Dictionary<TKey, TValue>` ou `HashSet<T>` $O(1)$).
- **Consultas Repetidas:** Consultar o mesmo dado do banco ou cache repetidas vezes na mesma requisição em vez de reutilizar a variável local.

### 2.2 Alocações Excessivas & Streaming
- **GAP:** Carregar listas gigantescas de 100.000 registros na memória (`.ToList()`) em vez de paginar ou usar streaming / `IAsyncEnumerable<T>`.
- **Streaming:** Para leitura/escrita de arquivos, payloads HTTP volumosos ou exportações CSV, use Streams (`Stream`, `PipeReader`, `PipeWriter`) em vez de `byte[]` inteiros em memória.
- **Lazy Loading Cauteloso:** Cuidado com lazy loading descontrolado de ORM que dispara queries invisíveis em loops (efeito N+1).

### 2.3 Paralelismo Consciente
- Usar `Parallel.ForEachAsync` ou `Task.WhenAll` para operações independentes de I/O ou CPU-bound.
- Sempre delimitar o grau de paralelismo (`MaxDegreeOfParallelism`) para evitar exaustão de sockets e conexões com o banco.

---

## 3. Gerenciamento de Memória (Dimension 10 - Foco C# / .NET)

### 3.1 IDisposable & Bloco `using`
- Todo objeto que implementa `IDisposable` (conexões de banco, streams, leitores de arquivo, `HttpClientHandler`, transações) **DEVE** ser gerenciado com instrução `using var x = ...;` ou bloco `using (...)`.
- Para recursos assíncronos que implementam `IAsyncDisposable`, utilize `await using var x = ...;`.
- **GAP Crítico:** Instanciar streams, transações ou conexões sem `using`, causando vazamento de file descriptors, sockets e conexões no pool.

### 3.2 Objetos Grandes & Large Object Heap (LOH)
- No .NET, objetos $\ge 85.000$ bytes vão direto para o LOH (Large Object Heap), que é coletado no Gen 2 (muito custoso e sujeito a fragmentação de memória).
- **Prevenção:** Use `ArrayPool<T>.Shared` ou buffers reutilizáveis para alocações grandes e transitórias.

### 3.3 Boxing & Unboxing de Value Types
- **GAP:** Passar structs/tipos primitivos (`int`, `DateTime`, `struct`) para APIs que recebem `object` ou interfaces não-genéricas, forçando alocação no heap (boxing) e garbage collection posterior.
- **GAP:** Concatenação de strings em loops (`str += item`) em vez de `StringBuilder` ou `DefaultInterpolatedStringHandler`.

### 3.4 `Span<T>`, `ReadOnlySpan<T>` e `Memory<T>`
- Em cenários de parsing, manipulação de texto ou sub-buffers binários, deve-se preferir `ReadOnlySpan<char>` em vez de `.Substring()` (que aloca novas strings no heap a cada chamada).
- Uso de `Memory<T>` para operações assíncronas que não podem conter `Span<T>` na stack frame.

---

## 4. Concorrência & Thread Safety (Dimension 11)

### 4.1 Race Conditions & Estado Compartilhado
- Classes de escopo Singleton ou instâncias compartilhadas estáticas **NUNCA** devem manter estado mutável sem proteção sincronizada.
- **Coleções Concorrentes:** Usar `ConcurrentDictionary<TKey, TValue>`, `ConcurrentQueue<T>` ou `Channel<T>` em vez de `List<T>` ou `Dictionary<TKey, TValue>` acessados concorrentemente.

### 4.2 Deadlocks & Primitivas de Lock
- **Proibido em C#:** Bloquear código assíncrono com `lock(obj)` contendo `await` (o compilador nem permite, mas usar semáforos incorretamente gera o mesmo efeito).
- Para sincronização em fluxos assíncronos, use `SemaphoreSlim(1, 1)` com liberação no bloco `finally`:
  ```csharp
  await _semaphore.WaitAsync(cancellationToken);
  try {
      // trabalho assíncrono
  } finally {
      _semaphore.Release();
  }
  ```

---

## 5. Programação Assíncrona (Dimension 12 - Especialmente C#)

### 5.1 Anti-Padrão Sync-over-Async (Proibição Total de `.Result` e `.Wait()`)
- **VIOLAÇÃO GRAVÍSSIMA:** Chamar `task.Result` ou `task.Wait()` ou `task.GetAwaiter().GetResult()` em código assíncrono.
- **Risco:** Esgotamento do ThreadPool do .NET (*thread pool starvation*) e deadlocks no SynchronizationContext do ASP.NET.
- **Regra:** O fluxo assíncrono deve ser "Async all the way down". Da Controller até o Repositório, todos os métodos devem retornar `Task` ou `Task<T>` e ser invocados com `await`.

### 5.2 Propagação Completa do `CancellationToken`
- Toda API que aceita `CancellationToken` (leituras de banco, chamadas HTTP, leituras de fila) deve recebê-lo repassado do Controller/Endpoint.
- Se o cliente abortar a requisição HTTP (fechar aba, timeout), a query do banco ou chamada externa deve ser imediatamente cancelada no servidor, liberando threads e conexões.

### 5.3 `ConfigureAwait(false)` em Bibliotecas
- Em bibliotecas de infraestrutura e componentes reutilizáveis (não de aplicação final), utilize `.ConfigureAwait(false)` para evitar sincronização desnecessária com o contexto do chamador.

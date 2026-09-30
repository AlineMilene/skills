#!/usr/bin/env python3
"""
Generate a self-contained, visual executive HTML report for technical gap analysis.

Produces a responsive dashboard with health scores across the 25 engineering dimensions,
highlighting missing disciplines, technical debt matrix, and an actionable roadmap.

Usage:
    python scripts/generate_html_report.py --input report-data.json --out gap-analysis-report.html
    python scripts/generate_html_report.py --demo --out demo-report.html
"""

import argparse
import json
import os
import sys
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Relatório Executivo de GAPs Técnicos - {{project_name}}</title>
  <style>
    :root {
      --bg-primary: #0f172a;
      --bg-secondary: #1e293b;
      --bg-card: #334155;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-blue: #38bdf8;
      --accent-purple: #a855f7;
      --critical: #f43f5e;
      --high: #fb923c;
      --medium: #facc15;
      --low: #38bdf8;
      --pass: #34d399;
      --border: #475569;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-main);
      line-height: 1.6;
      padding: 30px 20px;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    header {
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px;
      margin-bottom: 28px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .badge-critical { background: rgba(244, 63, 94, 0.2); color: var(--critical); border: 1px solid var(--critical); }
    .badge-high { background: rgba(251, 146, 60, 0.2); color: var(--high); border: 1px solid var(--high); }
    .badge-medium { background: rgba(250, 204, 21, 0.2); color: var(--medium); border: 1px solid var(--medium); }
    .badge-pass { background: rgba(52, 211, 153, 0.2); color: var(--pass); border: 1px solid var(--pass); }
    h1 { font-size: 2.2rem; font-weight: 800; margin-bottom: 8px; color: #fff; }
    .subtitle { color: var(--text-muted); font-size: 1rem; margin-bottom: 20px; }
    .meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-top: 20px;
      padding-top: 20px;
      border-top: 1px solid rgba(255,255,255,0.1);
    }
    .meta-item { display: flex; flex-direction: column; }
    .meta-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }
    .meta-value { font-size: 1.1rem; font-weight: 700; color: #fff; }
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }
    .stat-card {
      background-color: var(--bg-secondary);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      text-align: center;
      transition: transform 0.2s ease;
    }
    .stat-card:hover { transform: translateY(-3px); }
    .stat-number { font-size: 2.8rem; font-weight: 900; line-height: 1; margin: 10px 0; }
    .stat-label { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; }
    
    .missing-disciplines-section {
      background: linear-gradient(135deg, rgba(244, 63, 94, 0.1) 0%, rgba(30, 41, 59, 0.7) 100%);
      border: 2px solid var(--critical);
      border-radius: 14px;
      padding: 28px;
      margin-bottom: 32px;
    }
    .missing-disciplines-section h2 {
      color: var(--critical);
      font-size: 1.4rem;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .missing-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
      margin-top: 16px;
    }
    .missing-card {
      background-color: var(--bg-secondary);
      border-left: 4px solid var(--critical);
      border-radius: 8px;
      padding: 16px;
    }
    .missing-title { font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; color: #fff; }
    .missing-desc { font-size: 0.9rem; color: var(--text-muted); }

    .section-title {
      font-size: 1.6rem;
      font-weight: 800;
      margin: 40px 0 20px 0;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    
    .dimensions-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }
    .dim-card {
      background-color: var(--bg-secondary);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .dim-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }
    .dim-name { font-weight: 700; font-size: 1rem; color: #fff; }
    .dim-bar-bg {
      background-color: rgba(255,255,255,0.1);
      border-radius: 9999px;
      height: 8px;
      overflow: hidden;
      margin-bottom: 10px;
    }
    .dim-bar-fill { height: 100%; border-radius: 9999px; transition: width 0.5s ease; }
    .dim-notes { font-size: 0.85rem; color: var(--text-muted); }

    table {
      width: 100%;
      border-collapse: collapse;
      background-color: var(--bg-secondary);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 32px;
      border: 1px solid var(--border);
    }
    th, td {
      padding: 14px 18px;
      text-align: left;
      font-size: 0.9rem;
      border-bottom: 1px solid var(--border);
    }
    th {
      background-color: #1e293b;
      color: var(--text-muted);
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
    }
    tr:hover { background-color: rgba(255,255,255,0.02); }

    .roadmap-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .roadmap-col {
      background-color: var(--bg-secondary);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
    }
    .roadmap-col h3 {
      font-size: 1.15rem;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .roadmap-list { list-style: none; }
    .roadmap-list li {
      padding: 10px 0;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      font-size: 0.9rem;
    }
    .roadmap-list li:last-child { border-bottom: none; }

    footer {
      text-align: center;
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-top: 50px;
      padding-top: 20px;
      border-top: 1px solid var(--border);
    }
    @media print {
      body { background-color: #fff; color: #000; }
      header, .stat-card, .dim-card, table, .roadmap-col { border-color: #ccc; background: #fff; color: #000; }
      .subtitle, .meta-label, .dim-notes { color: #555; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
        <div>
          <span class="badge badge-high" style="margin-bottom: 12px;">Auditoria de Arquitetura & Código</span>
          <h1>{{project_name}}</h1>
          <p class="subtitle">Relatório Executivo de Diagnóstico Técnico e Levantamento de GAPs</p>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 3rem; font-weight: 900; color: {{score_color}};">{{overall_score}}<span style="font-size: 1.5rem; color: var(--text-muted);">/10</span></div>
          <div style="font-size: 0.85rem; color: var(--text-muted); font-weight: 600;">ÍNDICE DE MATURIDADE GLOBAL</div>
        </div>
      </div>

      <div class="meta-grid">
        <div class="meta-item">
          <span class="meta-label">Data da Análise</span>
          <span class="meta-value">{{audit_date}}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Avaliador</span>
          <span class="meta-value">{{auditor}}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Stack Principal</span>
          <span class="meta-value">{{tech_stack}}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Diagnóstico Geral</span>
          <span class="meta-value" style="color: {{score_color}};">{{status_verdict}}</span>
        </div>
      </div>
    </header>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">TOTAL DE GAPS IDENTIFICADOS</div>
        <div class="stat-number" style="color: #fff;">{{total_gaps}}</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Nas 25 dimensões</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">CRÍTICOS / EMERGENCIAIS</div>
        <div class="stat-number" style="color: var(--critical);">{{critical_gaps}}</div>
        <div style="font-size: 0.8rem; color: var(--critical);">Risco de indisponibilidade</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">ALTA SEVERIDADE</div>
        <div class="stat-number" style="color: var(--high);">{{high_gaps}}</div>
        <div style="font-size: 0.8rem; color: var(--high);">Débito estrutural grave</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">DISCIPLINAS AUSENTES</div>
        <div class="stat-number" style="color: var(--medium);">{{missing_count}}</div>
        <div style="font-size: 0.8rem; color: var(--medium);">Não implementadas</div>
      </div>
    </div>

    <!-- SEÇÃO DESTACADA: DISCIPLINAS FALTANTES -->
    <section class="missing-disciplines-section">
      <h2>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        Disciplinas Técnicas Ausentes ou Deficientes no Projeto
      </h2>
      <p style="color: #cbd5e1; font-size: 0.95rem;">
        As seguintes áreas fundamentais da engenharia de software não foram encontradas ou apresentam ausência crítica no repositório analisado:
      </p>
      <div class="missing-grid">
        {{missing_disciplines_html}}
      </div>
    </section>

    <!-- SCORECARD DAS 25 DIMENSÕES -->
    <h2 class="section-title">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20v-6M6 20V10M18 20V4"/></svg>
      Maturidade das 25 Dimensões Técnicas
    </h2>
    <div class="dimensions-grid">
      {{dimensions_cards_html}}
    </div>

    <!-- MATRIZ DE GAPS TÉCNICOS -->
    <h2 class="section-title">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>
      Matriz Consolidada de GAPs Técnicos
    </h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Dimensão</th>
          <th>Vulnerabilidade / Falha</th>
          <th>Severidade</th>
          <th>Esforço</th>
          <th>Impacto / Risco</th>
        </tr>
      </thead>
      <tbody>
        {{gaps_rows_html}}
      </tbody>
    </table>

    <!-- PLANO DE AÇÃO E ROADMAP -->
    <h2 class="section-title">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
      Roadmap Priorizado de Remediação
    </h2>
    <div class="roadmap-grid">
      <div class="roadmap-col" style="border-top: 4px solid var(--pass);">
        <h3 style="color: var(--pass);">Fase 1: Quick Wins (0 a 15 dias)</h3>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 12px;">Ações imediatas de baixo esforço e alto impacto</p>
        <ul class="roadmap-list">
          {{roadmap_phase1_html}}
        </ul>
      </div>
      <div class="roadmap-col" style="border-top: 4px solid var(--medium);">
        <h3 style="color: var(--medium);">Fase 2: Refatoração Estrutural (Sprints)</h3>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 12px;">Desacoplamento de camadas, Clean Arch e SOLID</p>
        <ul class="roadmap-list">
          {{roadmap_phase2_html}}
        </ul>
      </div>
      <div class="roadmap-col" style="border-top: 4px solid var(--accent-purple);">
        <h3 style="color: var(--accent-purple);">Fase 3: Escala & Resiliência (Estratégico)</h3>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 12px;">System Design distribuído, Outbox, SAGA e Observabilidade</p>
        <ul class="roadmap-list">
          {{roadmap_phase3_html}}
        </ul>
      </div>
    </div>

    <footer>
      Relatório gerado automaticamente pela Skill <strong>repo-gap-analyzer</strong> (Engenharia de Software, Clean Architecture e System Design).
    </footer>
  </div>
</body>
</html>
"""

def get_color_for_score(score: float) -> str:
    if score >= 8.0:
        return "var(--pass)"
    elif score >= 5.0:
        return "var(--medium)"
    else:
        return "var(--critical)"

def get_badge_class(severity: str) -> str:
    s = severity.upper()
    if "CRIT" in s:
        return "badge-critical"
    elif "HIGH" in s or "ALTA" in s:
        return "badge-high"
    elif "MED" in s:
        return "badge-medium"
    return "badge-pass"

def generate_html_from_data(data: dict) -> str:
    project_name = data.get("project_name", "Repositório Analisado")
    auditor = data.get("auditor", "Agente de IA (repo-gap-analyzer)")
    audit_date = data.get("audit_date", datetime.now().strftime("%Y-%m-%d"))
    tech_stack = data.get("tech_stack", "Multi-stack (.NET / C# / Web)")
    overall_score = float(data.get("overall_score", 5.0))
    status_verdict = data.get("status_verdict", "Débito Técnico Elevado")

    score_color = get_color_for_score(overall_score)

    dimensions = data.get("dimensions", [])
    gaps = data.get("gaps", [])
    missing_disciplines = data.get("missing_disciplines", [])
    roadmap = data.get("roadmap", {})

    total_gaps = len(gaps)
    critical_gaps = sum(1 for g in gaps if "CRIT" in str(g.get("severity", "")).upper())
    high_gaps = sum(1 for g in gaps if "HIGH" in str(g.get("severity", "")).upper() or "ALTA" in str(g.get("severity", "")).upper())
    missing_count = len(missing_disciplines)

    # Build Missing Disciplines HTML
    missing_html = []
    for item in missing_disciplines:
        title = item.get("discipline", "Disciplina Não Identificada")
        desc = item.get("impact", "Não encontrada implementação ou boas práticas no projeto.")
        missing_html.append(f"""
        <div class="missing-card">
          <div class="missing-title">{title}</div>
          <div class="missing-desc">{desc}</div>
        </div>
        """)
    if not missing_html:
        missing_html.append("""
        <div class="missing-card" style="border-left-color: var(--pass);">
          <div class="missing-title" style="color: var(--pass);">Todas as disciplinas essenciais estão presentes</div>
          <div class="missing-desc">O projeto possui estrutura representativa em todas as disciplinas avaliadas.</div>
        </div>
        """)

    # Build Dimensions Cards HTML
    dim_cards_html = []
    for dim in dimensions:
        num = dim.get("id", "")
        name = dim.get("name", "")
        score = float(dim.get("score", 0.0))
        notes = dim.get("notes", "")
        fill_pct = min(max(score * 10, 0), 100)
        bar_color = get_color_for_score(score)

        dim_cards_html.append(f"""
        <div class="dim-card">
          <div>
            <div class="dim-header">
              <span class="dim-name">{num}. {name}</span>
              <span style="font-weight:800; color:{bar_color};">{score:.1f}/10</span>
            </div>
            <div class="dim-bar-bg">
              <div class="dim-bar-fill" style="width: {fill_pct}%; background-color: {bar_color};"></div>
            </div>
          </div>
          <div class="dim-notes">{notes}</div>
        </div>
        """)

    # Build GAPs rows HTML
    gaps_rows = []
    for g in gaps:
        gid = g.get("id", "GAP")
        dim = g.get("dimension", "")
        desc = g.get("title", "")
        sev = g.get("severity", "MEDIUM")
        eff = g.get("effort", "MEDIUM")
        imp = g.get("impact", "")
        b_class = get_badge_class(sev)

        gaps_rows.append(f"""
        <tr>
          <td style="font-weight:800; color:#fff;">{gid}</td>
          <td>{dim}</td>
          <td>{desc}</td>
          <td><span class="badge {b_class}">{sev}</span></td>
          <td>{eff}</td>
          <td style="color:var(--text-muted);">{imp}</td>
        </tr>
        """)

    # Build Roadmap HTML
    def render_list(items):
        if not items:
            return "<li>Nenhuma ação pendente mapeada.</li>"
        return "".join([f"<li>{item}</li>" for item in items])

    r_p1 = render_list(roadmap.get("phase1", []))
    r_p2 = render_list(roadmap.get("phase2", []))
    r_p3 = render_list(roadmap.get("phase3", []))

    html = HTML_TEMPLATE
    html = html.replace("{{project_name}}", project_name)
    html = html.replace("{{auditor}}", auditor)
    html = html.replace("{{audit_date}}", str(audit_date))
    html = html.replace("{{tech_stack}}", tech_stack)
    html = html.replace("{{overall_score}}", f"{overall_score:.1f}")
    html = html.replace("{{score_color}}", score_color)
    html = html.replace("{{status_verdict}}", status_verdict)
    html = html.replace("{{total_gaps}}", str(total_gaps))
    html = html.replace("{{critical_gaps}}", str(critical_gaps))
    html = html.replace("{{high_gaps}}", str(high_gaps))
    html = html.replace("{{missing_count}}", str(missing_count))
    html = html.replace("{{missing_disciplines_html}}", "\n".join(missing_html))
    html = html.replace("{{dimensions_cards_html}}", "\n".join(dim_cards_html))
    html = html.replace("{{gaps_rows_html}}", "\n".join(gaps_rows))
    html = html.replace("{{roadmap_phase1_html}}", r_p1)
    html = html.replace("{{roadmap_phase2_html}}", r_p2)
    html = html.replace("{{roadmap_phase3_html}}", r_p3)

    return html

def get_demo_data() -> dict:
    return {
        "project_name": "Demo Core Banking & Payments Service",
        "auditor": "repo-gap-analyzer (AI Architecture Auditor)",
        "audit_date": datetime.now().strftime("%Y-%m-%d"),
        "tech_stack": ".NET 8 / C#, EF Core, PostgreSQL, RabbitMQ",
        "overall_score": 4.8,
        "status_verdict": "Alto Risco & Débito Técnico Crítico",
        "missing_disciplines": [
            {
                "discipline": "16. Observabilidade Distribuída (TraceId & CorrelationId)",
                "impact": "Logs gerados em formato texto plano sem identificador de correlação; ausência de rastreamento com OpenTelemetry."
            },
            {
                "discipline": "21. Cloud Readiness & Resiliência (Circuit Breakers)",
                "impact": "Chamadas HTTP e conexões externas sem políticas de Circuit Breaker (Polly), Timeouts explícitos ou Retries com Jitter."
            },
            {
                "discipline": "10. Gerenciamento de Memória (IDisposable & using)",
                "impact": "Streams e conexões com o banco instanciadas sem blocos using var / await using var, gerando risco de exaustão de pool."
            },
            {
                "discipline": "18. Testes Automatizados (Integração & Contrato)",
                "impact": "Repositório possui apenas alguns testes unitários pontuais; ausência total de testes de integração com Testcontainers ou validação de contratos."
            }
        ],
        "dimensions": [
            {"id": 1, "name": "Correção", "score": 6.5, "notes": "Caminho feliz funciona; falta validação de edge cases e tratamento de nulos."},
            {"id": 2, "name": "Legibilidade (Clean Code)", "score": 5.0, "notes": "Métodos com mais de 60 linhas e múltiplos níveis de aninhamento."},
            {"id": 3, "name": "Orientação a Objetos (OOP)", "score": 4.0, "notes": "Modelos anêmicos com lógica de negócio espalhada em controllers."},
            {"id": 4, "name": "SOLID", "score": 4.5, "notes": "Violações graves de SRP e acoplamento direto a implementações (DIP)."},
            {"id": 5, "name": "Princípios Gerais (DRY/KISS/YAGNI)", "score": 5.5, "notes": "Duplicação de regras de cálculo financeiro em múltiplos endpoints."},
            {"id": 6, "name": "Arquitetura", "score": 4.0, "notes": "Entidades de ORM vazadas no domínio; sem isolamento de portas e adaptadores."},
            {"id": 7, "name": "Design Patterns", "score": 5.0, "notes": "Uso tímido de padrões; ausência de Strategy para cálculo de tarifas."},
            {"id": 8, "name": "Tratamento de Erros", "score": 3.5, "notes": "Blocos catch vazios engolindo erros e rethrow com throw ex."},
            {"id": 9, "name": "Performance", "score": 4.0, "notes": "Queries N+1 no Entity Framework ao listar pedidos com itens."},
            {"id": 10, "name": "Gerenciamento de Memória", "score": 3.0, "notes": "Falta de using em conexões e buffers grandes alocados na LOH."},
            {"id": 11, "name": "Concorrência", "score": 5.0, "notes": "Lock bloqueante sincrônico utilizado em métodos assíncronos."},
            {"id": 12, "name": "Programação Assíncrona", "score": 2.5, "notes": "Uso de .Result e .Wait() com altíssimo risco de ThreadPool starvation."},
            {"id": 13, "name": "Banco de Dados", "score": 5.0, "notes": "Falta de paginação em listagens e índices em colunas de busca frequente."},
            {"id": 14, "name": "APIs", "score": 6.0, "notes": "Endpoints REST básicos; ausência de chaves de idempotência e rate limit."},
            {"id": 15, "name": "Segurança", "score": 5.5, "notes": "Queries parametrizadas corretas, mas faltam validações estritas de claims."},
            {"id": 16, "name": "Observabilidade", "score": 3.0, "notes": "Ausência de structured logging em JSON e sem correlation IDs."},
            {"id": 17, "name": "Testabilidade", "score": 4.5, "notes": "Classes acopladas diretamente a instâncias concretas sem interfaces."},
            {"id": 18, "name": "Testes", "score": 3.0, "notes": "Sem testes de integração; apenas testes unitários simples."},
            {"id": 19, "name": "Manutenibilidade", "score": 4.0, "notes": "Alta carga cognitiva e alto blast radius para adicionar novas regras."},
            {"id": 20, "name": "Escalabilidade", "score": 5.0, "notes": "Aplicação é stateless, mas depende de banco único sem réplicas de leitura."},
            {"id": 21, "name": "Cloud Readiness", "score": 3.5, "notes": "Falta de circuit breaker, retries com jitter e health checks dedicados."},
            {"id": 22, "name": "Domain Driven Design (DDD)", "score": 3.5, "notes": "Sem agregados nem Value Objects para proteção de invariantes monetárias."},
            {"id": 23, "name": "Qualidade de Dependências", "score": 7.0, "notes": "Pacotes NuGet relativamente atualizados; sem CVEs graves detectadas."},
            {"id": 24, "name": "DevOps", "score": 6.0, "notes": "Pipeline básico de build no GitHub Actions; falta análise de SonarQube."},
            {"id": 25, "name": "Métricas de Código", "score": 4.0, "notes": "Complexidade ciclomática elevada (>20) em classes de liquidação."}
        ],
        "gaps": [
            {
                "id": "GAP-01",
                "dimension": "12. Assincronismo (.NET)",
                "title": "Sync-over-async com .Result em chamada HTTP",
                "severity": "CRITICAL",
                "effort": "LOW",
                "impact": "Risco de ThreadPool Starvation e travamento sob concorrência"
            },
            {
                "id": "GAP-02",
                "dimension": "10. Memória (.NET)",
                "title": "IDisposable sem bloco using em conexões SQL",
                "severity": "CRITICAL",
                "effort": "LOW",
                "impact": "Esgotamento de pool de conexões do banco de dados"
            },
            {
                "id": "GAP-03",
                "dimension": "21. Cloud Readiness",
                "title": "Chamada a Gateway de Pagamento sem Circuit Breaker / Timeout",
                "severity": "HIGH",
                "effort": "LOW",
                "impact": "Falha em cascata e bloqueio de threads quando o gateway oscilar"
            },
            {
                "id": "GAP-04",
                "dimension": "13. Banco de Dados",
                "title": "Problema N+1 ao carregar Extratos e Lançamentos",
                "severity": "HIGH",
                "effort": "MEDIUM",
                "impact": "Degradação extrema de latência e sobrecarga no banco"
            },
            {
                "id": "GAP-05",
                "dimension": "6. Arquitetura",
                "title": "Tabelas de ORM utilizadas diretamente como modelos de domínio",
                "severity": "HIGH",
                "effort": "HIGH",
                "impact": "Acoplamento rígido ao schema físico do banco; inviabiliza testes limpos"
            }
        ],
        "roadmap": {
            "phase1": [
                "Substituir todos os `.Result` e `.Wait()` por `await` e repassar `CancellationToken`.",
                "Adicionar `using var` / `await using var` em todas as instâncias de `IDisposable`.",
                "Configurar Timeouts de 3000ms nos clientes HTTP.",
                "Eliminar blocos `catch` vazios e trocar `throw ex;` por `throw;`."
            ],
            "phase2": [
                "Isolar entidades de domínio do ORM utilizando DTOs e mappers dedicados.",
                "Resolver consultas N+1 com `.Include()` e paginação keyset.",
                "Implementar Circuit Breakers (Polly) com retentativas exponenciais e Jitter.",
                "Adicionar logging estruturado com pares chave/valor e `CorrelationId`."
            ],
            "phase3": [
                "Implementar Transactional Outbox Pattern para comunicação assíncrona com RabbitMQ.",
                "Introduzir Cache-Aside com Redis e mitigação de Cache Stampede.",
                "Instrumentar OpenTelemetry para rastreamento distribuído (Traces e Métricas RED).",
                "Criar suíte de testes de integração conteinerizada com Testcontainers."
            ]
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Generate visual executive HTML gap analysis report")
    parser.add_argument("--input", help="Path to JSON file with audit data")
    parser.add_argument("--out", default="gap-analysis-report.html", help="Path to output HTML file")
    parser.add_argument("--demo", action="store_true", help="Generate a demo report with sample findings")
    args = parser.parse_args()

    if args.demo:
        data = get_demo_data()
    elif args.input:
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found.")
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        print("Please provide --input <file.json> or --demo. Use --help for details.")
        sys.exit(1)

    html_content = generate_html_from_data(data)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"HTML Executive Report generated successfully: {args.out}")

if __name__ == "__main__":
    main()

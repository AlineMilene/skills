<#
.SYNOPSIS
    Script de instalação e distribuição da skill repo-gap-analyzer para Windows (PowerShell).

.DESCRIPTION
    Instala a skill repo-gap-analyzer em qualquer repositório local ou pasta de agente de IA (Cursor, Windsurf, Claude Code, ou genérico).

.PARAMETER TargetDir
    Caminho do repositório ou pasta de destino onde a skill será instalada. Padrão: diretório atual.

.PARAMETER Agent
    Tipo de estrutura de destino:
    - 'generic': Cria em <TargetDir>/skills/repo-gap-analyzer (Recomendado/Universal)
    - 'cursor': Cria em <TargetDir>/.cursor/skills/repo-gap-analyzer
    - 'windsurf': Cria em <TargetDir>/.windsurf/skills/repo-gap-analyzer
    - 'claude': Cria em <TargetDir>/.claude/skills/repo-gap-analyzer
    - 'all': Cria em todas as pastas compatíveis acima.

.PARAMETER Symlink
    Cria link simbólico em vez de cópia de arquivos (requer privilégios de Administrador ou Modo Desenvolvedor ativo).

.PARAMETER Force
    Sobrescreve a pasta de destino caso já exista.

.EXAMPLE
    .\install.ps1 -TargetDir "C:\Projetos\meu-microsservico" -Agent "generic"
    .\install.ps1 -TargetDir "C:\Projetos\meu-microsservico" -Agent "cursor"
    .\install.ps1 -TargetDir "C:\Projetos\meu-microsservico" -Agent "all" -Force
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$TargetDir = (Get-Location).Path,

    [Parameter(Position = 1)]
    [ValidateSet("generic", "cursor", "windsurf", "claude", "devin", "hive", "all")]
    [string]$Agent = "generic",

    [switch]$Symlink,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$SourceDir = Join-Path $PSScriptRoot "skills\repo-gap-analyzer"
if (-not (Test-Path $SourceDir)) {
    Write-Error "Pasta de origem da skill não encontrada em: $SourceDir"
    exit 1
}

$ResolvedTarget = [System.IO.Path]::GetFullPath($TargetDir)
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Instalador da Skill: repo-gap-analyzer (Por: Aline Milene)" -ForegroundColor Cyan
Write-Host "  Origem : $SourceDir" -ForegroundColor Gray
Write-Host "  Destino: $ResolvedTarget" -ForegroundColor Gray
Write-Host "  Modo   : $Agent" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

$Destinations = @()

switch ($Agent) {
    "generic" {
        $Destinations += (Join-Path $ResolvedTarget "skills\repo-gap-analyzer")
    }
    "cursor" {
        $Destinations += (Join-Path $ResolvedTarget ".cursor\skills\repo-gap-analyzer")
    }
    "windsurf" {
        $Destinations += (Join-Path $ResolvedTarget ".windsurf\skills\repo-gap-analyzer")
    }
    "claude" {
        $Destinations += (Join-Path $ResolvedTarget ".claude\skills\repo-gap-analyzer")
    }
    "devin" {
        $Destinations += (Join-Path $ResolvedTarget ".devin\skills\repo-gap-analyzer")
        $Destinations += (Join-Path $ResolvedTarget "skills\repo-gap-analyzer")
    }
    "hive" {
        $Destinations += (Join-Path $ResolvedTarget ".hive\skills\repo-gap-analyzer")
        $Destinations += (Join-Path $ResolvedTarget "skills\repo-gap-analyzer")
    }
    "all" {
        $Destinations += (Join-Path $ResolvedTarget "skills\repo-gap-analyzer")
        $Destinations += (Join-Path $ResolvedTarget ".cursor\skills\repo-gap-analyzer")
        $Destinations += (Join-Path $ResolvedTarget ".windsurf\skills\repo-gap-analyzer")
        $Destinations += (Join-Path $ResolvedTarget ".claude\skills\repo-gap-analyzer")
        $Destinations += (Join-Path $ResolvedTarget ".devin\skills\repo-gap-analyzer")
        $Destinations += (Join-Path $ResolvedTarget ".hive\skills\repo-gap-analyzer")
    }
}

foreach ($Dest in $Destinations) {
    if (Test-Path $Dest) {
        if ($Force) {
            Write-Host "[!] Removendo instalação existente em: $Dest" -ForegroundColor Yellow
            Remove-Item -Path $Dest -Recurse -Force
        } else {
            Write-Host "[!] Destino já existe: $Dest. Use -Force para sobrescrever." -ForegroundColor Yellow
            continue
        }
    }

    $ParentDir = Split-Path $Dest -Parent
    if (-not (Test-Path $ParentDir)) {
        New-Item -ItemType Directory -Path $ParentDir -Force | Out-Null
    }

    if ($Symlink) {
        Write-Host "[+] Criando link simbólico em: $Dest" -ForegroundColor Green
        New-Item -ItemType SymbolicLink -Path $Dest -Target $SourceDir | Out-Null
    } else {
        Write-Host "[+] Copiando arquivos para: $Dest" -ForegroundColor Green
        Copy-Item -Path $SourceDir -Destination $Dest -Recurse -Force
    }
}

Write-Host "`n[+] Instalação concluída com sucesso!" -ForegroundColor Green
Write-Host "Para utilizar, basta pedir ao assistente de IA:" -ForegroundColor Gray
Write-Host '  "Audite este repositório aplicando a skill repo-gap-analyzer e gere o relatório .html"' -ForegroundColor White

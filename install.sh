#!/usr/bin/env bash
# ==============================================================================
# Script de instalação e distribuição da skill repo-gap-analyzer para Linux/macOS
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$SCRIPT_DIR/skills/repo-gap-analyzer"

TARGET_DIR="$(pwd)"
AGENT="generic"
SYMLINK=false
FORCE=false

print_usage() {
  echo "Uso: ./install.sh [opções]"
  echo ""
  echo "Opções:"
  echo "  -t, --target <path>   Diretório de destino (padrão: diretório atual)"
  echo "  -a, --agent <type>    Tipo de destino: generic, cursor, windsurf, claude, devin, hive, all (padrão: generic)"
  echo "  -s, --symlink         Cria link simbólico em vez de cópia física"
  echo "  -f, --force           Sobrescreve a instalação se já existir"
  echo "  -h, --help            Exibe esta ajuda"
  echo ""
  echo "Exemplos:"
  echo "  ./install.sh --target /caminho/meu-repo --agent generic"
  echo "  ./install.sh --target /caminho/meu-repo --agent devin"
  echo "  ./install.sh --target /caminho/meu-repo --agent all"
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -t|--target) TARGET_DIR="$2"; shift ;;
    -a|--agent) AGENT="$2"; shift ;;
    -s|--symlink) SYMLINK=true ;;
    -f|--force) FORCE=true ;;
    -h|--help) print_usage; exit 0 ;;
    *) echo "Opção desconhecida: $1"; print_usage; exit 1 ;;
  esac
  shift
done

if [ ! -d "$SOURCE_DIR" ]; then
  echo "Erro: Pasta de origem da skill não encontrada em: $SOURCE_DIR" >&2
  exit 1
fi

TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd || echo "$TARGET_DIR")"

echo "=========================================================="
echo "  Instalador da Skill: repo-gap-analyzer (Por: Aline Milene)"
echo "  Origem : $SOURCE_DIR"
echo "  Destino: $TARGET_DIR"
echo "  Modo   : $AGENT"
echo "=========================================================="

DESTINATIONS=()

case $AGENT in
  generic)
    DESTINATIONS+=("$TARGET_DIR/skills/repo-gap-analyzer")
    ;;
  cursor)
    DESTINATIONS+=("$TARGET_DIR/.cursor/skills/repo-gap-analyzer")
    ;;
  windsurf)
    DESTINATIONS+=("$TARGET_DIR/.windsurf/skills/repo-gap-analyzer")
    ;;
  claude)
    DESTINATIONS+=("$TARGET_DIR/.claude/skills/repo-gap-analyzer")
    ;;
  devin)
    DESTINATIONS+=("$TARGET_DIR/.devin/skills/repo-gap-analyzer")
    DESTINATIONS+=("$TARGET_DIR/skills/repo-gap-analyzer")
    ;;
  hive)
    DESTINATIONS+=("$TARGET_DIR/.hive/skills/repo-gap-analyzer")
    DESTINATIONS+=("$TARGET_DIR/skills/repo-gap-analyzer")
    ;;
  all)
    DESTINATIONS+=("$TARGET_DIR/skills/repo-gap-analyzer")
    DESTINATIONS+=("$TARGET_DIR/.cursor/skills/repo-gap-analyzer")
    DESTINATIONS+=("$TARGET_DIR/.windsurf/skills/repo-gap-analyzer")
    DESTINATIONS+=("$TARGET_DIR/.claude/skills/repo-gap-analyzer")
    DESTINATIONS+=("$TARGET_DIR/.devin/skills/repo-gap-analyzer")
    DESTINATIONS+=("$TARGET_DIR/.hive/skills/repo-gap-analyzer")
    ;;
  *)
    echo "Erro: Tipo de agente desconhecido '$AGENT'. Escolha: generic, cursor, windsurf, claude, devin, hive, all." >&2
    exit 1
    ;;
esac

for DEST in "${DESTINATIONS[@]}"; do
  if [ -e "$DEST" ]; then
    if [ "$FORCE" = true ]; then
      echo "[!] Removendo instalação existente em: $DEST"
      rm -rf "$DEST"
    else
      echo "[!] Destino já existe: $DEST. Use --force para sobrescrever."
      continue
    fi
  fi

  PARENT_DIR="$(dirname "$DEST")"
  mkdir -p "$PARENT_DIR"

  if [ "$SYMLINK" = true ]; then
    echo "[+] Criando link simbólico em: $DEST"
    ln -s "$SOURCE_DIR" "$DEST"
  else
    echo "[+] Copiando arquivos para: $DEST"
    cp -R "$SOURCE_DIR" "$DEST"
  fi
done

echo ""
echo "[+] Instalação concluída com sucesso!"
echo "Para utilizar, basta pedir ao assistente de IA:"
echo '  "Audite este repositório aplicando a skill repo-gap-analyzer e gere o relatório .html"'

#!/bin/bash

# Este script é executado pela Vercel antes de cada build
# Retorna 1 para IGNORAR o build, 0 para PROSSEGUIR com o build

# Se não for a branch main ou master, ignora o build
if [[ "$VERCEL_GIT_COMMIT_REF" != "main" && "$VERCEL_GIT_COMMIT_REF" != "master" ]]; then
  echo "🔸 Branch '$VERCEL_GIT_COMMIT_REF' não é main/master. Build ignorado."
  exit 1
fi

# Verifica o status do último workflow do GitHub Actions
REPO="fenol64/teste-tecnico-seiwa"
COMMIT_SHA="$VERCEL_GIT_COMMIT_SHA"

echo "🔍 Verificando status dos testes no GitHub Actions..."
echo "📍 Commit: $COMMIT_SHA"

# Aguarda até 5 minutos para os testes completarem
MAX_ATTEMPTS=30
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  # Busca o status dos checks do commit
  STATUS=$(curl -s -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO/commits/$COMMIT_SHA/check-runs" | \
    grep -o '"conclusion":"[^"]*"' | head -1 | cut -d'"' -f4)

  if [ "$STATUS" = "success" ]; then
    echo "✅ Testes passaram! Prosseguindo com deploy..."
    exit 0
  elif [ "$STATUS" = "failure" ] || [ "$STATUS" = "cancelled" ]; then
    echo "❌ Testes falharam ou foram cancelados. Build ignorado."
    exit 1
  else
    echo "⏳ Aguardando conclusão dos testes... (tentativa $((ATTEMPT + 1))/$MAX_ATTEMPTS)"
    sleep 10
    ATTEMPT=$((ATTEMPT + 1))
  fi
done

echo "⏱️ Timeout aguardando testes. Build ignorado por segurança."
exit 1

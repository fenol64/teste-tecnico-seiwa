#!/bin/bash

# Este script é executado pela Vercel antes de cada build
# ATENÇÃO: Na Vercel, exit 0 = IGNORA build, exit 1 = PROSSEGUE com build
# (comportamento inverso do padrão)

# Se não for a branch main ou master, ignora o build
if [[ "$VERCEL_GIT_COMMIT_REF" != "main" && "$VERCEL_GIT_COMMIT_REF" != "master" ]]; then
  echo "🔸 Branch '$VERCEL_GIT_COMMIT_REF' não é main/master. Build ignorado."
  exit 0
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
  RESPONSE=$(curl -s -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/$REPO/commits/$COMMIT_SHA/check-runs")

  echo "📡 Resposta da API (tentativa $((ATTEMPT + 1))/$MAX_ATTEMPTS):"
  # Extrai o status e conclusion usando sed
  STATUS=$(echo "$RESPONSE" | sed -n 's/.*"status": *"\([^"]*\)".*/\1/p' | head -1)
  CONCLUSION=$(echo "$RESPONSE" | sed -n 's/.*"conclusion": *"\([^"]*\)".*/\1/p' | head -1)

  echo "📊 Status: $STATUS | Conclusion: $CONCLUSION"

  if [ "$STATUS" = "completed" ]; then
    if [ "$CONCLUSION" = "success" ]; then
      echo "✅ Testes passaram! Prosseguindo com deploy..."
      exit 1  # exit 1 = PROSSEGUIR com build na Vercel
    elif [ "$CONCLUSION" = "failure" ] || [ "$CONCLUSION" = "cancelled" ]; then
      echo "❌ Testes falharam ou foram cancelados. Build ignorado."
      exit 0  # exit 0 = IGNORAR build na Vercel
    fi
  fi

  echo "⏳ Aguardando conclusão dos testes..."
  sleep 10
  ATTEMPT=$((ATTEMPT + 1))
done

echo "⏱️ Timeout aguardando testes. Build ignorado por segurança."
exit 0  # exit 0 = IGNORAR build na Vercel

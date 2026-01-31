# Configuração de CI/CD

Este projeto usa GitHub Actions para executar testes automaticamente e a integração nativa da Vercel para deploy.

## Pipeline

O pipeline de CI/CD funciona da seguinte forma:

### 1. GitHub Actions - Test Job
- Executa em todas as branches quando há push ou pull request
- Configura PostgreSQL como service container
- Instala dependências Python
- Executa todos os testes com pytest
- Gera relatório de cobertura de código
- Envia cobertura para Codecov (opcional)

### 2. Vercel - Deploy Automático
- Integração nativa do GitHub com Vercel
- Vercel detecta automaticamente o push
- **Antes de fazer build**, executa `vercel-ignore-build.sh`
- O script verifica o status dos testes no GitHub Actions
- **Deploy só acontece se os testes passarem ✅**

## Como Funciona

1. **Push para branch** → GitHub Actions executa testes
2. **Vercel detecta push** → Aguarda conclusão dos testes
3. **Testes passam** → ✅ Vercel faz o build e deploy
4. **Testes falham** → ❌ Vercel ignora o build (sem deploy)

## Configuração na Vercel

A configuração está em [vercel.json](../vercel.json):

```json
{
  "ignoreCommand": "bash vercel-ignore-build.sh"
}
```

Este comando é executado antes de cada build. Se retornar `1`, o build é ignorado.

## Script de Verificação

O [vercel-ignore-build.sh](../vercel-ignore-build.sh) faz:

1. Verifica se a branch é `main` ou `master`
2. Consulta a API do GitHub para obter status dos checks
3. Aguarda até 5 minutos pela conclusão dos testes
4. Retorna sucesso (0) se testes passarem
5. Retorna falha (1) se testes falharem ou timeout

## Configuração Necessária

### No GitHub (Repositório)

Nenhuma configuração adicional necessária! Os testes rodam automaticamente via GitHub Actions.

### Na Vercel (Dashboard)

1. Acesse: [Vercel Dashboard](https://vercel.com/dashboard)
2. Selecione seu projeto
3. Vá em **Settings** → **Git**
4. Certifique-se de que a integração com GitHub está ativa
5. **Pronto!** O `vercel.json` já configura o resto

## Monitoramento

Antes de fazer push, você pode executar os mesmos testes localmente:

```bash
# Inicie o banco de dados
make up

# Execute os testes
make test

# Se os testes passarem, faça o push
git push
```

## Desabilitar Deploy Automático

Se quiser apenas rodar os testes sem fazer deploy, remova ou comente o job `deploy` no arquivo [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml).

## Monitoramento

- **GitHub Actions**: https://github.com/fenol64/teste-tecnico-seiwa/actions
- **Vercel Deployments**: https://vercel.com/dashboard
- **Codecov**: https://codecov.io/ (se configurado)

## Testando Localmente

Antes de fazer push, você pode executar os mesmos testes localmente:

```bash
# Inicie o banco de dados
make up

# Execute os testes
make test

# Se os testes passarem, faça o push
git push
```

## Logs e Debug

### Ver logs do build na Vercel
1. Acesse o [Dashboard da Vercel](https://vercel.com/dashboard)
2. Clique no seu projeto
3. Vá em **Deployments**
4. Clique no deployment específico

Se o build foi ignorado, você verá a mensagem do script `vercel-ignore-build.sh`.

### Ver status dos testes no GitHub
1. Acesse: https://github.com/fenol64/teste-tecnico-seiwa/actions
2. Clique no workflow específico
3. Veja os logs detalhados dos testes

## Troubleshooting

### Deploy não está acontecendo
- Verifique se os testes estão passando no GitHub Actions
- Verifique os logs do build na Vercel
- O script aguarda até 5 minutos pelos testes - pode haver delay

### Testes passam mas deploy é ignorado
- Verifique se a branch é `main` ou `master`
- Veja os logs do `vercel-ignore-build.sh` na Vercel
- Verifique se o script tem permissão de execução

### Build acontece mesmo com testes falhando
- Verifique a configuração `ignoreCommand` no `vercel.json`
- Certifique-se de que `vercel-ignore-build.sh` está executável
- Verifique os logs na Vercel para ver se o script está sendo executado

# Monitoramento com Prometheus e Grafana

Este projeto inclui monitoramento completo da API usando Prometheus e Grafana.

## Serviços de Monitoramento

### Prometheus
- **URL**: http://localhost:9090
- **Função**: Coleta métricas da API FastAPI
- **Scrape Interval**: 5 segundos

### Grafana
- **URL**: http://localhost:3000
- **Usuário**: admin
- **Senha**: admin
- **Função**: Visualização de métricas com dashboards

## Métricas Disponíveis

A API expõe as seguintes métricas no endpoint `/metrics`:

- **http_requests_total**: Total de requisições HTTP por método, endpoint e status
- **http_request_duration_seconds**: Latência das requisições (histograma)
- **http_requests_in_progress**: Número de requisições em andamento
- **process_cpu_seconds_total**: Tempo total de CPU do processo
- **process_resident_memory_bytes**: Memória residente do processo
- **python_gc_objects_collected_total**: Objetos coletados pelo garbage collector

## Como Usar

### 1. Iniciar os serviços

```bash
make up
```

Isso iniciará todos os serviços incluindo Prometheus e Grafana.

### 2. Acessar Prometheus

```bash
make prometheus
```

Ou acesse manualmente: http://localhost:9090

No Prometheus você pode:
- Consultar métricas usando PromQL
- Verificar targets (a API deve estar UP)
- Ver alertas configurados

### 3. Acessar Grafana

```bash
make grafana
```

Ou acesse manualmente: http://localhost:3000

**Login**: admin / admin

O Grafana já vem configurado com:
- Prometheus como datasource
- Dashboard "FastAPI Metrics" pré-configurado

### 4. Visualizar Dashboard

No Grafana, navegue até:
- **Dashboards** → **FastAPI Metrics**

O dashboard inclui:
- **Request Rate**: Taxa de requisições por segundo
- **Total Requests**: Total acumulado de requisições
- **Response Time Percentiles**: p50, p95, p99 de latência
- **Error Rate**: Taxa de erros 5xx
- **Requests by Endpoint**: Requisições por endpoint

## Queries Úteis no Prometheus

### Taxa de requisições por segundo
```promql
rate(http_requests_total[1m])
```

### Latência p95
```promql
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))
```

### Taxa de erros
```promql
rate(http_requests_total{status=~"5.."}[1m]) / rate(http_requests_total[1m]) * 100
```

### Requisições por endpoint
```promql
sum by (handler) (rate(http_requests_total[1m]))
```

## Estrutura de Arquivos

```
ops/
├── docker-compose.yml                      # Orquestração de serviços
├── prometheus.yml                          # Configuração do Prometheus
├── grafana/
│   ├── dashboards/
│   │   └── fastapi-dashboard.json         # Dashboard FastAPI
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml             # Datasource Prometheus
│       └── dashboards/
│           └── dashboard.yml              # Provider de dashboards
└── README.md                               # Documentação da pasta ops
```

## Personalizando o Dashboard

Para editar o dashboard no Grafana:

1. Acesse o dashboard
2. Clique em "Settings" (ícone de engrenagem)
3. Edite os painéis conforme necessário
4. Salve as alterações
5. Exporte o JSON atualizado para `ops/grafana/dashboards/fastapi-dashboard.json`

## Alertas (Opcional)

Para configurar alertas, edite `ops/prometheus.yml` e adicione regras de alerta:

```yaml
rule_files:
  - "alert_rules.yml"
```

Crie `ops/alert_rules.yml`:

```yaml
groups:
  - name: api_alerts
    interval: 10s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[1m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Alta taxa de erros na API"
```

## Troubleshooting

### Prometheus não encontra a API
- Verifique se o serviço `api` está rodando: `docker-compose ps`
- Verifique os logs: `docker-compose logs prometheus`
- Certifique-se de que `/metrics` está acessível: `curl http://localhost:8000/metrics`

### Dashboard vazio no Grafana
- Verifique se o Prometheus está coletando métricas
- Gere tráfego na API para popular as métricas
- Verifique a conexão do Grafana com o Prometheus em Configuration → Data Sources

### Métricas não aparecem
- Execute algumas requisições na API: `curl http://localhost:8000/health`
- Aguarde alguns segundos para o Prometheus coletar os dados
- Verifique os targets no Prometheus: http://localhost:9090/targets

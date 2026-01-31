# Ops - Infraestrutura e Monitoramento

Esta pasta contém todos os arquivos de infraestrutura e monitoramento do projeto.

## Estrutura

```
ops/
├── docker-compose.yml          # Orquestração de todos os serviços
├── prometheus.yml              # Configuração do Prometheus
└── grafana/                    # Configurações do Grafana
    ├── dashboards/             # Dashboards pré-configurados
    │   └── fastapi-dashboard.json
    └── provisioning/           # Provisionamento automático
        ├── datasources/        # Datasources (Prometheus)
        └── dashboards/         # Provider de dashboards
```

## Serviços

### API FastAPI
- **Porta**: 8000
- **Função**: Aplicação principal
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics

### PostgreSQL
- **Porta**: 5432
- **Usuário**: postgres
- **Senha**: postgres
- **Database**: seiwa_db

### pgAdmin
- **Porta**: 5050
- **Usuário**: admin@admin.com
- **Senha**: admin
- **Função**: Interface web para gerenciar PostgreSQL

### Prometheus
- **Porta**: 9090
- **Função**: Coleta e armazena métricas
- **Scrape Interval**: 5 segundos

### Grafana
- **Porta**: 3000
- **Usuário**: admin
- **Senha**: admin
- **Função**: Visualização de métricas

## Comandos

Todos os comandos devem ser executados a partir do diretório raiz do projeto:

```bash
# Iniciar todos os serviços
make up

# Parar todos os serviços
make down

# Ver logs
make logs

# Ver status dos serviços
make status

# Acessar shell do container da API
make shell

# Acessar Prometheus
make prometheus

# Acessar Grafana
make grafana

# Acessar pgAdmin
make pgadmin
```

## Volumes Persistentes

- **postgres_data**: Dados do PostgreSQL
- **prometheus_data**: Dados históricos do Prometheus
- **grafana_data**: Configurações e dashboards do Grafana

## Network

Todos os serviços estão conectados à rede `app-network` com driver host, permitindo comunicação entre containers.

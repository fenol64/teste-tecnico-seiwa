# Teste tecnico Seiwa

Este repositório contém o código-fonte para o teste técnico da Seiwa, incluindo a implementação de uma API RESTful para gerenciamento de repasses financeiros.

projeto foi desenvolvido utilizando Python com FastAPI, PostgreSQL como banco de dados, e Docker para containerização. Além disso, foram integradas ferramentas de monitoramento como Prometheus e Grafana.

url de produção: (https://api-seiwa.fenol64.com.br/docs)

### Contexto

A Seiwa integra dados financeiros de médicos a partir de sistemas hospitalares distintos. Um dos desafios é consolidar eventos financeiros, garantir consistência, performance e auditabilidade.

### Desafio

Você deverá desenvolver uma API para consolidar repasses e informações financeiras de médicos. A API deve permitir:

- Cadastrar médicos
- Registrar produções (valor, data, hospital)
- Registrar repasses (valor, data, hospital)
- Consultar saldo consolidado de um médico por período

Fique a vontade para usar uma linguagem/framework de sua escolha, bem como para complementar a entrega com documentos e informações adicionais, se julgar necessário. A ideia é que você faça um projeto de forma bem "livre", até porque não é só sua capacidade de desenvolvimento que queremos avaliar, fechado?

## Tecnologias Utilizadas
- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker & Docker Compose
- Prometheus & Grafana para monitoramento
- Pytest para testes automatizados

##  Arquitetura macro

![Desenho da Arquitetura](docs/img/arq-macro.png)

## Decisões de Projeto

- **Clean Architecture**: Para garantir separação de responsabilidades e facilitar a manutenção.
- **FastAPI**: Escolhida pela sua performance e velocidade de desenvolvimento.
- **SQLAlchemy + Alembic**: Para facilitar o mapeamento objeto-relacional e migrations.
- **Docker**: Para garantir que o ambiente de desenvolvimento seja consistente e fácil de configurar.
- **Pytest**: Para garantir a qualidade do código através de testes automatizados (unitários e de integração).
- **Prometheus & Grafana**: Para monitoramento e visualização de métricas da aplicação.

## pastas Importantes

- `api/`: Definição do WSGI para deploy na vercel
- `alembic/`: Migrations do banco de dados
- `docs/`: Documentação do projeto e arquivos auxiliares para IA pegar contexto
- `scripts/`: Scripts auxiliares como seeders
- `src/`: Código-fonte da aplicação
  - `bootstrap/`:  injeção de dependências e overrides
  - `controllers/`: handlers das rotas da API
  - `routes/`: Definição das rotas da API
  - `services/`: Serviços da aplicação
  - `domain/`: Entidades e regras de negócio
    - `application/`: Casos de uso e lógica de negócio
    - `infrastructure/`: Implementações específicas (banco de dados, etc)
    - `interfaces/`: Definições de interfaces e contratos
- `tests/`: Testes automatizados
- `ops/`: Configurações de infraestrutura (Docker, Prometheus, Grafana, etc)

## Como Rodar o Projeto

### Pré-requisitos
- Docker e Docker Compose instalados na sua máquina.
### Passos
1. Clone o repositório:
   ```bash
   git clone https://github.com/fenol64/teste-tec-seiwa.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd teste-tec-seiwa
   ```
3. Inicie os serviços com Docker Compose:
   ```bash
   make up
   ```
4. Acesse a API em `http://localhost:8000`. A documentação interativa estará disponível em `http://localhost:8000/docs`.




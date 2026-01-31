# Tests

Este diretório contém os testes do projeto.

## Estrutura

- **unit/**: Testes unitários
  - `usecases/`: Testes dos casos de uso
  - `repositories/`: Testes dos repositórios
  - `services/`: Testes dos serviços

- **integration/**: Testes de integração
  - Testes das rotas da API

## Executar os testes

```bash
# Instalar dependências de teste
pip install -r requirements.txt

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=src --cov-report=html

# Executar testes específicos
pytest tests/unit/
pytest tests/integration/

# Executar um arquivo específico
pytest tests/unit/usecases/test_doctor_usecase.py

# Executar com verbose
pytest -v

# Executar e parar no primeiro erro
pytest -x
```

## Cobertura de Código

Após executar os testes com cobertura, abra o relatório:

```bash
open htmlcov/index.html
```

## Principais Casos Testados

### Testes Unitários
- **Use Cases**: Validações de negócio, tratamento de erros
- **Repositories**: CRUD operations, queries específicas
- **Services**: Hash de senha, JWT token

### Testes de Integração
- **Authentication**: Signup, signin, proteção de rotas
- **Doctors**: CRUD, validações de CRM e email duplicados
- **Hospitals**: CRUD operations
- **Doctor-Hospital**: Vínculos entre médicos e hospitais
- **Productions**: CRUD, validações de FK
- **Repasses**: CRUD, validação de produção existente

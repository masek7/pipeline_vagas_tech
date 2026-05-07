# Pipeline ETL de Vagas com Python

## Descrição
Projeto de pipeline ETL desenvolvido em Python para consumir dados da The Muse Jobs API, transformar os registros com `pandas` e carregar o resultado em um banco PostgreSQL.

O objetivo é simular um mini ETL real, com separação por etapas, uso de POO, tratamento de dados, persistência em banco relacional e proteção contra duplicatas na reexecução.

---

## Objetivo do Projeto
Este projeto foi construído para praticar conceitos de Engenharia de Dados, incluindo:

- extração de dados via API pública;
- paginação de múltiplas páginas;
- transformação tabular com `pandas`;
- carga em PostgreSQL;
- separação de responsabilidades por classe;
- reexecução segura sem duplicação de registros.

---

## Tecnologias Utilizadas

- Python
- requests
- pandas
- PostgreSQL
- psycopg2
- SQLAlchemy
- python-dotenv

---

### Responsabilidade dos arquivos

- `main.py`: ponto de entrada e orquestração do pipeline.
- `client.py`: responsável pelas chamadas HTTP à API.
- `extract.py`: controla paginação, coleta e métricas de extração.
- `transform.py`: transforma os dados brutos em DataFrame final.
- `load.py`: cria tabela e realiza a carga no PostgreSQL.
- `create_table.sql`: script SQL de criação da tabela.
- `.env.example`: exemplo das variáveis de ambiente do banco.
- `api_key.example.json`: exemplo do formato esperado para a chave da API.

---

## Fonte dos Dados

Os dados são consumidos da **The Muse Jobs API**.

- API: The Muse Jobs API
- Endpoint utilizado: `/api/public/jobs`

O projeto usa `api_key` local para autenticação e controle de limite de requisições.

---

## Estrutura da Tabela Final

A tabela final no PostgreSQL é:

- `job_vacancies`

Colunas principais:

- `job_id`
- `job_name`
- `publication_date`
- `category`
- `levels`
- `company_id`
- `company_name`
- `location_name`
- `landing_page`

---

## Regras de Negócio Implementadas

- coleta de múltiplas páginas da API;
- paginação controlada pela aplicação;
- transformação dos dados em estrutura tabular;
- padronização de colunas;
- tratamento de nulos em campos textuais;
- conversão de tipos;
- remoção de duplicatas por `job_id`;
- criação da tabela no PostgreSQL;
- carga com proteção contra duplicatas no banco;
- geração de resumo da carga.

---

## Como Configurar o Ambiente

### 1. Criar e ativar ambiente virtual
```bash
# exemplo
python -m venv .venv
```

Ative o ambiente virtual de acordo com seu sistema operacional.

### 2. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 3. Criar o arquivo `.env`
Copie o arquivo `.env.example` e renomeie para `.env`.

Preencha com os dados do seu PostgreSQL local.

### 4. Criar o arquivo `api_key.json`
Copie o arquivo `api_key.example.json` e renomeie para `api_key.json`.

Preencha com sua chave da API.

---

## Variáveis de Ambiente

O arquivo `.env` deve conter as seguintes variáveis:

```env
DB_HOST=
DB_NAME=
DB_USER=
DB_PASS=
DB_PORT=
```

---

## Formato esperado para a API key

Exemplo de estrutura do arquivo `api_key.json`:

```json
{
  "api_key": "SUA_CHAVE_AQUI"
}
```
## Subindo o PostgreSQL com Docker e Portainer

O projeto pode ser executado com PostgreSQL local em container Docker.  
No meu ambiente, utilizei o Portainer para criar e gerenciar o container.

### Configuração utilizada

- **Container name:** `postgres-db`
- **Image:** `postgres:15`
- **Host port:** `5432`
- **Container port:** `5432`

### Variáveis de ambiente do container

- `POSTGRES_USER=admin`
- `POSTGRES_PASSWORD=senha123`
- `POSTGRES_DB=meu_banco`

### Persistência de dados 

Para evitar perda dos dados ao reiniciar ou recriar o container, foi configurado um volume apontando para:

```text
/var/lib/postgresql/data
```
### Fluxo resumido no Portainer

- `acessar o Portainer;`
- `criar um novo container com a imagem postgres:15;`
- `mapear a porta 5432:5432;`
- `configurar as variáveis de ambiente do PostgreSQL;`
- `configurar o volume para persistência dos dados;`
- `fazer o deploy do container.`

---
### Observação

Se você já tiver PostgreSQL instalado localmente, também pode usar sua instância local, desde que os dados de conexão no arquivo .env estejam corretos.
## Como Executar

Antes de executar, garanta que:

- o PostgreSQL esteja ativo;
- o banco de dados exista;
- o arquivo `.env` esteja preenchido;
- o arquivo `api_key.json` esteja configurado.

Depois, execute:

```bash
python main.py
```

---

## Fluxo do Pipeline

O pipeline executa as seguintes etapas:

1. coleta parâmetros de entrada;
2. consulta múltiplas páginas da API;
3. acumula os resultados brutos;
4. transforma os dados em DataFrame;
5. padroniza os campos;
6. remove duplicatas por `job_id`;
7. cria a tabela no PostgreSQL;
8. carrega os dados no banco;
9. apresenta resumo da execução.

---

## Exemplo de Resumo da Carga

```text
Rows received: X
Rows inserted: Y
Rows ignored: Z
```

---

## Possíveis Consultas no Banco

Após a carga, a tabela permite análises como:

- vagas por empresa;
- vagas por localização;
- vagas por data de publicação;
- categorias mais frequentes;
- níveis mais frequentes.

---

## Melhorias Futuras

- logging em arquivo;
- exportação adicional para CSV;
- CLI para parâmetros de execução;
- normalização de campos como `levels`;
- tratamento de erros mais granular;
- agendamento do pipeline.

---

## Observações

- arquivos sensíveis como `.env` e `api_key.json` não devem ser versionados;
- o projeto foi construído com foco em clareza arquitetural e separação de responsabilidades;
- a carga foi projetada para permitir reexecução sem duplicar registros.

---


# API de Imóveis

Esta é uma API desenvolvida em Flask que permite acessar informações de imóveis armazenados em um banco de dados PostgreSQL. A API oferece recursos de busca com base em data e inscrição, bem como paginação para facilitar a navegação pelos resultados.

## Funcionalidades

- **Busca por Data**: Permite recuperar dados de imóveis para uma data específica.
- **Busca por Inscrição**: Permite recuperar dados de imóveis baseados em uma inscrição específica.
- **Busca Geral**: Permite recuperar todos os dados de imóveis com suporte a paginação.
- **Paginação**: Os resultados são retornados em páginas de tamanho configurável.

## Pré-requisitos

- Python 3.7 ou superior
- PostgreSQL
- As bibliotecas Python listadas no arquivo `requirements.txt`

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate```
  # Para Linux/Mac
venv\Scripts\activate
# Para Windows
Instale as dependências:

```bash
pip install -r requirements.txt```
Configure as credenciais do banco de dados:

Certifique-se de que o arquivo credentials_PostgreSQL.enc esteja presente no diretório do projeto. Esse arquivo deve conter as credenciais de conexão ao banco de dados PostgreSQL.

(Opcional) Gere uma chave privada se ainda não tiver:

```bash
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048```
Execução
Para iniciar a API, execute o seguinte comando:

```bash
python app.py```
A API estará disponível em http://127.0.0.1:3600.

#Endpoints
1. Buscar por Data
URL: /get_view/data/<date_str>

Método: GET

Parâmetros:

date_str: Data no formato ddmmyyyy
page: (opcional) Número da página para paginação
Exemplo:

```bash
GET /get_view/data/21092024?page=1```

2. Buscar por Inscrição
URL: /get_view/inscricao/<inscricao>

Método: GET

Parâmetros:

inscricao: Inscrição do imóvel
page: (opcional) Número da página para paginação
Exemplo:

```bash
GET /get_view/inscricao/123456?page=1```

3. Buscar Todos os Imóveis
URL: /get_view/all

Método: GET

Parâmetros:

page: (opcional) Número da página para paginação
Exemplo:

```sql
GET /get_view/all?page=1```
Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

### Dicas para Uso

1. **Substitua** `seu-usuario` e `seu-repositorio` pelo seu nome de usuário e o nome do repositório no GitHub.
2. **Verifique** se todas as instruções e informações estão corretas e atualizadas com base no seu projeto.
3. **Adicione** uma seção para as dependências do seu projeto caso não tenha um arquivo `requir

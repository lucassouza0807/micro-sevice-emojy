# Emojify API

Esta documentação descreve a API Emojify, construída utilizando FastAPI. A API inclui dois endpoints principais: um para verificar o status do serviço e outro para transformar frases em versões enriquecidas com emojis.

---

## Instalação e Configuração

1. Clone o repositório para sua máquina local.
   ```bash
   git clone https://github.com/lucassouza0807/micro-sevice-emojy.git
   cd micro-sevice-emojy
   ```
3. Instale as dependências necessárias com:
   ```bash
   pip install -r requirements.txt
   ```
4. Crie o Ambiente Virtual (venv)
   ### Linux/Mac:
   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```
   ### Windows
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Inicie o servidor FastAPI com o comando:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints

### 1. **Ping Endpoint**
#### `GET /api/ping`
Este endpoint verifica o status da API.

#### **Resposta de Sucesso**
- **Status Code:** 200 OK
- **Exemplo de Resposta:**
  ```json
  {
    "message": "Ok"
  }
  ```

---

### 2. **Emojify Endpoint**
#### `POST /api/emojify`
Este endpoint transforma uma frase fornecida pelo usuário em uma versão com emojis.

#### **Requisição**
- **Cabeçalhos:**
  - `Content-Type: application/json`
- **Corpo:**
  ```json
  {
    "phrase": "gato"
  }
  ```
  - `phrase` (obrigatório): Uma string contendo a frase que será emojificada.

#### **Resposta de Sucesso**
- **Status Code:** 200 OK
- **Exemplo de Resposta:**
  ```json
  {
    "original_phrase": "gato",
    "emojified_phrase": "🐱"
  }
  ```

#### **Erros Possíveis**
1. **Campo Ausente**
   - **Status Code:** 400 Bad Request
   - **Exemplo de Resposta:**
     ```json
     {
       "detail": "O campo 'phrase' não foi encontrado no corpo da requisição."
     }
     ```

2. **Erro Interno no Servidor**
   - **Status Code:** 500 Internal Server Error
   - **Exemplo de Resposta:**
     ```json
     {
       "error": "An unexpected error occurred: <mensagem de erro>"
     }
     ```

---



## Notas Adicionais
- Certifique-se de que o serviço OpenIAservice esteja devidamente implementado e configurado no arquivo `src/services/OpenIAservice.py`.
- Adapte as origens permitidas em `origins` no middleware CORS, conforme necessário.

---

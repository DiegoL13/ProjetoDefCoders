# Portal Saúde - Documentação da API REST

## Visão Geral

A API REST do Portal Saúde fornece endpoints para gerenciamento completo de usuários, exames médicos e imagens, utilizando Django REST Framework.

## Base URL

```
http://127.0.0.1:8000/api/
```

## Autenticação

A API utiliza dois métodos de autenticação:

1. **Session Authentication** - Para uso com interface web
2. **Token Authentication** - Para aplicações mobile/third-party

### Headers necessários

```
Authorization: Token <seu_token_aqui>
Content-Type: application/json
```

## Endpoints

### 1. Usuários

#### Listar todos os usuários
```http
GET /api/usuarios/
```

#### Criar novo usuário
```http
POST /api/usuarios/
Content-Type: application/json

{
    "nome": "João Silva",
    "cpf": "12345678901",
    "data_nascimento": "1990-01-01",
    "sexo": "M",
    "contato": "(11) 1234-5678",
    "email": "joao@example.com",
    "password": "senha123"
}
```

#### Detalhes do usuário
```http
GET /api/usuarios/{id}/
```

#### Atualizar usuário
```http
PUT /api/usuarios/{id}/
PATCH /api/usuarios/{id}/
```

#### Deletar usuário
```http
DELETE /api/usuarios/{id}/
```

### 2. Pacientes

#### Listar pacientes
```http
GET /api/pacientes/
```

#### Criar paciente
```http
POST /api/pacientes/
Content-Type: application/json

{
    "nome": "Maria Santos",
    "cpf": "98765432109",
    "data_nascimento": "1985-05-15",
    "sexo": "F",
    "contato": "(11) 9876-5432",
    "email": "maria@example.com",
    "password": "senha123",
    "historico_medico": "Hipertensão controlada"
}
```

#### Pacientes específicos
```http
GET /api/pacientes/{id}/
PUT /api/pacientes/{id}/
DELETE /api/pacientes/{id}/
```

### 3. Médicos

#### Listar médicos
```http
GET /api/medicos/
```

#### Criar médico
```http
POST /api/medicos/
Content-Type: application/json

{
    "nome": "Dr. Pedro Costa",
    "cpf": "11122233344",
    "data_nascimento": "1975-03-20",
    "sexo": "M",
    "contato": "(11) 5555-6666",
    "email": "pedro@example.com",
    "password": "senha123",
    "crm": "CRM-SP 12345",
    "especialidade": "Radiologia"
}
```

#### Médicos específicos
```http
GET /api/medicos/{id}/
PUT /api/medicos/{id}/
DELETE /api/medicos/{id}/
```

### 4. Exames

#### Listar todos os exames
```http
GET /api/exames/
```

#### Criar novo exame
```http
POST /api/exames/
Content-Type: application/json

{
    "medico": 1,
    "paciente": 1,
    "descricao": "Exame de raio-X do tórax",
    "resultado_ia": "BENIGNO",
    "resultado_medico": "BENIGNO",
    "assinatura": "Dr. Pedro Costa",
    "disponibilidade": false
}
```

#### Detalhes do exame
```http
GET /api/exames/{id}/
```

#### Atualizar exame
```http
PUT /api/exames/{id}/
PATCH /api/exames/{id}/
```

#### Deletar exame
```http
DELETE /api/exames/{id}/
```

### 5. Imagens

#### Listar imagens
```http
GET /api/imagens/
```

#### Upload de imagem
```http
POST /api/imagens/
Content-Type: multipart/form-data

exame: 1
path: <arquivo_de_imagem>
```

#### Detalhes da imagem
```http
GET /api/imagens/{id}/
```

#### Deletar imagem
```http
DELETE /api/imagens/{id}/
```

### 6. Endpoints Especiais

#### Exames de um paciente específico
```http
GET /api/pacientes/{paciente_id}/exames/
```

#### Exames de um médico específico
```http
GET /api/medicos/{medico_id}/exames/
```

## Respostas da API

### Formato de resposta padrão

#### Sucesso (200 OK)
```json
{
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com",
    "created_at": "2026-01-24T15:30:00Z"
}
```

#### Erro de validação (400 Bad Request)
```json
{
    "email": [
        "Este campo é obrigatório."
    ],
    "cpf": [
        "CPF já cadastrado."
    ]
}
```

#### Não encontrado (404 Not Found)
```json
{
    "detail": "Não encontrado."
}
```

#### Não autorizado (401 Unauthorized)
```json
{
    "detail": "Credenciais de autenticação não foram fornecidas."
}
```

#### Proibido (403 Forbidden)
```json
{
    "detail": "Você não tem permissão para realizar esta ação."
}
```

## Filtros e Paginação

### Filtros disponíveis

Para exames:
```http
GET /api/exames/?paciente_id=1
GET /api/exames/?medico_id=1
GET /api/exames/?disponibilidade=true
GET /api/exames/?resultado_ia=BENIGNO
```

### Paginação

A API utiliza paginação padrão do Django REST Framework:

```http
GET /api/exames/?page=1
GET /api/exames/?page=2&page_size=20
```

Resposta paginada:
```json
{
    "count": 100,
    "next": "http://127.0.0.1:8000/api/exames/?page=3",
    "previous": "http://127.0.0.1:8000/api/exames/?page=1",
    "results": [...]
}
```

## Validações e Regras de Negócio

### Validações de CPF
- CPF deve ter 11 dígitos
- CPF deve ser válido (algoritmo de validação)
- CPF deve ser único no sistema

### Validações de Email
- Email deve ser único no sistema
- Formato de email válido obrigatório

### Validações de Exames
- Médico e paciente são obrigatórios
- Descrição limitada a 2000 caracteres
- Resultados devem pertencer às opções predefinidas

### Validações de Imagens
- Apenas arquivos de imagem permitidos
- Tamanho máximo: 10MB
- Formatos aceitos: JPEG, PNG, GIF

## Exemplos de Uso

### Python com requests

```python
import requests

# Login e obtenção de token
login_data = {
    'email': 'medico@example.com',
    'password': 'senha123'
}
response = requests.post('http://127.0.0.1:8000/api/login/', json=login_data)
token = response.json()['token']

# Headers de autenticação
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}

# Listar exames do médico
response = requests.get('http://127.0.0.1:8000/api/medicos/1/exames/', headers=headers)
exames = response.json()

# Criar novo exame
exame_data = {
    "paciente": 2,
    "descricao": "Exame de ultrassom abdominal",
    "resultado_ia": "SAUDÁVEL",
    "assinatura": "Dr. Teste"
}
response = requests.post('http://127.0.0.1:8000/api/exames/', json=exame_data, headers=headers)
```

### JavaScript com fetch

```javascript
// Login
const loginData = {
    email: 'medico@example.com',
    password: 'senha123'
};

fetch('http://127.0.0.1:8000/api/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(loginData)
})
.then(response => response.json())
.then(data => {
    const token = data.token;
    
    // Listar pacientes
    return fetch('http://127.0.0.1:8000/api/pacientes/', {
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    });
})
.then(response => response.json())
.then(pacientes => {
    console.log('Pacientes:', pacientes);
});
```

## Limitações da API

- Rate limiting: 100 requisições por minuto por usuário
- Upload de imagens: máximo 10MB por arquivo
- Tamanho máximo de request: 50MB
- Timeout: 30 segundos para requisições longas

## Ambiente de Teste

Para desenvolvimento, utilize:
- URL: `http://127.0.0.1:8000/api/`
- Credenciais de teste:
  - Médico: medico@example.com / medico123
  - Paciente: paciente@example.com / paciente123

## Suporte

Para dúvidas sobre a API:
- Documentation completa: `docs/API.md`
- Código fonte: `core/views.py`, `core/serializers.py`
- Testes: `core/tests.py` (em desenvolvimento)
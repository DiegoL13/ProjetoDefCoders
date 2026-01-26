# Portal Saúde - Sistema de Gerenciamento de Exames Médicos

## 📋 Visão Geral

O **Portal Saúde** é uma plataforma web desenvolvida em Django para gerenciamento de exames médicos, conectando médicos e pacientes com recursos de análise assistida por IA. O sistema possui autenticação customizada, upload de imagens, dashboard médico, visualização de exames por pacientes e API REST completa.

**Status do Projeto:** ✅ **Funcional e Pronto para Uso** (após refatoração completa)

## 🎯 Funcionalidades Principais

### ✅ Sistema de Autenticação Customizado
- Modelo `Usuario` com autenticação por email/senha
- Perfis específicos para Médicos e Pacientes
- Validação completa de CPF (11 dígitos com algoritmo verificador)
- Redirecionamento automático baseado em perfil

### ✅ Gestão de Exames Médicos
- Criação de exames com upload de múltiplas imagens
- Dashboard médico com lista de exames criados
- Processamento automático de "resultado IA" (simulado)
- Assinatura digital do médico
- Liberação de exames para pacientes

### ✅ API REST Completa
- Endpoints para todos os modelos (usuários, médicos, pacientes, exames, imagens)
- Autenticação por sessão ou token
- Filtros por médico/paciente específico
- Paginação e validações

### ✅ Interface Web Moderna
- Templates responsivos com Bootstrap 5 + Font Awesome
- Formulários com validação em tempo real
- Dashboard médico intuitivo
- Fluxo de trabalho otimizado

## 📁 Estrutura do Projeto

```
PortalSaude-Continuacao/
├── sistema/                    # Projeto Django principal
│   ├── core/                  # Aplicação principal
│   │   ├── forms.py          # Formulários com validação CPF completa
│   │   ├── models.py         # Modelos (Usuario, Medico, Paciente, Exame, Imagem)
│   │   ├── templates/        # Templates HTML (base, login, dashboard, etc.)
│   │   ├── views.py          # Views com lógica de negócio
│   │   ├── urls.py           # Rotas da aplicação
│   │   └── migrations/       # Migrações do banco de dados
│   ├── manage.py             # Script de gerenciamento Django
│   ├── settings.py           # Configurações do projeto
│   └── urls.py               # Rotas principais
├── imagens_exames/           # Diretório para upload de imagens (mídia)
├── static/                   # Arquivos estáticos fonte (CSS, JS, imagens)
├── docs/                     # Documentação
│   └── API.md               # Documentação completa da API REST
├── requirements.txt          # Dependências Python
├── start.bat                # Script de inicialização automática (Windows)
├── README.md                # Este arquivo
└── db.sqlite3               # Banco de dados SQLite com dados de teste
```

## 🚀 Como Executar o Projeto

### Pré-requisitos
- **Python 3.8 ou superior** instalado e no PATH
- **pip** (gerenciador de pacotes Python)

### Método 1: Script Automático (Windows)
1. Navegue até a pasta do projeto
2. Execute `start.bat` (clique duas vezes)
3. Aguarde a instalação das dependências e inicialização do servidor
4. Acesse http://127.0.0.1:8000/

### Método 2: Comandos Manuais (Windows/Linux/macOS)
```bash
# 1. Navegar até o projeto
cd "C:\Users\test\Desktop\folders\Development Projects\PortalSaude-Continuacao_FIX\PortalSaude-Continuacao"

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar migrações do banco de dados
cd sistema
python manage.py migrate

# 4. Coletar arquivos estáticos (opcional para desenvolvimento)
python manage.py collectstatic --noinput

# 5. Iniciar servidor de desenvolvimento
python manage.py runserver 127.0.0.1:8000
```

## 🔑 Credenciais de Teste

### Médicos Disponíveis:
- **Email:** doctor@example.com
- **Senha:** password
- **ID do médico:** 23
- **Dashboard:** http://127.0.0.1:8000/medicos/23/dashboard/

- **Email:** medico@example.com
- **Senha:** password
- **ID do médico:** 19
- **Dashboard:** http://127.0.0.1:8000/medicos/19/dashboard/

- **Email:** test.medico@example.com  
- **Senha:** password
- **CRM:** CRM-SP-55566677788

### Pacientes Disponíveis:
- **Email:** patient@example.com
- **Senha:** password
- **ID do paciente:** 24

- **Email:** paciente@example.com
- **Senha:** password
- **ID do paciente:** 20

- **Email:** test.paciente@example.com
- **Senha:** password
- **CPF:** 66677788899

## 🌐 Acessos Importantes

- **Página inicial:** http://127.0.0.1:8000/
- **Login:** http://127.0.0.1:8000/login/
- **Cadastro médico:** http://127.0.0.1:8000/cadastro/medico/
- **Cadastro paciente:** http://127.0.0.1:8000/cadastro/paciente/
- **Dashboard médico:** http://127.0.0.1:8000/medicos/23/dashboard/
- **Criar exame:** http://127.0.0.1:8000/medicos/23/novo-exame/
- **API REST:** http://127.0.0.1:8000/api/
- **Admin Django:** http://127.0.0.1:8000/admin/ (criar superusuário primeiro)

## 🔄 Fluxo de Trabalho Típico

1. **Médico faz login** → Redirecionado para dashboard
2. **No dashboard** → Visualiza exames existentes
3. **Clica em "Novo Exame"** → Seleciona paciente, descrição, anexa imagens
4. **Sistema processa** → Gera resultado IA simulado, salva no banco
5. **Paciente faz login** → Visualiza exames disponíveis

## 🛠️ Solução de Problemas Comuns

### Erro "ModuleNotFoundError: No module named 'django'"
```bash
pip install django==6.0.1
```

### Erro "Database is locked"
Delete o arquivo `db.sqlite3` e execute:
```bash
python manage.py migrate
```

### Erro "Static files not found"
O coletor de arquivos estáticos pode falhar no Windows. Como alternativa:

1. **Copiar manualmente** os arquivos estáticos:
```bash
cd PortalSaude-Continuacao
mkdir -p staticfiles
cp -r static/* staticfiles/
```

2. **Ou ignore o erro** - os templates usam estilos inline, então a funcionalidade não é afetada.

Se o erro persistir, o sistema funcionará normalmente sem arquivos estáticos externos.

### Criar Superusuário para Admin Django
```bash
python manage.py createsuperuser
```

### Porta 8000 já em uso
```bash
python manage.py runserver 127.0.0.1:8001  # Use outra porta
```

## 📝 Notas Técnicas

- **Banco de dados:** SQLite (desenvolvimento) - pronto para produção com PostgreSQL
- **Upload de imagens:** Salvas em `imagens_exames/` (configurável em `settings.py`)
- **Validação CPF:** Algoritmo completo com dígitos verificadores (forms.py)
- **Autenticação:** Sistema customizado com modelo `Usuario` (AUTH_USER_MODEL = 'core.Usuario')
- **Templates:** Bootstrap 5 + Font Awesome + CSS inline para facilidade de deploy
- **API:** Django REST Framework com serializers e viewset completos

## 📊 Status de Implementação

| Componente | Status | Detalhes |
|------------|--------|----------|
| Models | ✅ Completo | Usuario, Medico, Paciente, Exame, Imagem, LogExames |
| Views | ✅ Completo | Autenticação, dashboard, criação de exames, API |
| Templates | ✅ 95% | Todas as páginas principais funcionais |
| Forms | ✅ Completo | Validação CPF, registro médico/paciente |
| API REST | ✅ Completo | Endpoints para todos os modelos |
| Testes Automatizados | ⚠️ Parcial | Testes de registro implementados |
| Documentação | ✅ Suficiente | README + API.md |

## 🚀 Deploy para Produção

O projeto está configurado para deploy em produção com as seguintes opções:

### 📦 Dependências de Produção
Arquivo `requirements-prod.txt` inclui:
- Gunicorn (servidor WSGI)
- Whitenoise (servir arquivos estáticos)
- PostgreSQL adapter
- dj-database-url

### 🔧 Configuração
1. **Variáveis de ambiente**: Copie `.env.example` para `.env` e configure:
   - `SECRET_KEY`: Gere uma nova chave secreta
   - `DEBUG`: Defina como `False`
   - `ALLOWED_HOSTS`: Domínios permitidos
   - `DATABASE_URL`: URL do banco de dados PostgreSQL

2. **Banco de dados**: Use PostgreSQL em produção:
   ```sql
   CREATE DATABASE portal_saude;
   CREATE USER portal_user WITH PASSWORD 'senha_forte';
   GRANT ALL PRIVILEGES ON DATABASE portal_saude TO portal_user;
   ```

### 🐳 Docker (Recomendado)
```bash
# Build da imagem
docker build -t portal-saude .

# Ou com Docker Compose
docker-compose up -d
```

### 🖥️ Servidor Tradicional
Use o script de deploy automatizado:
```bash
chmod +x deploy.sh
sudo ./deploy.sh production
```

### 📄 Documentação Completa
Consulte `DEPLOY.md` para instruções detalhadas de deploy em diferentes ambientes.

## 🔧 Personalização e Extensão

### Adicionar Novos Tipos de Exame
Edite `core/choices.py` para adicionar novas opções ao campo `tipo_exame`.

### Configurar Email para Produção
Atualize as configurações de email em `sistema/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### Substituir Banco de Dados para Produção
Altere `DATABASES` em `settings.py` para PostgreSQL, MySQL, etc.

### Implementar IA Real
Substitua a lógica de "resultado IA simulado" em `CriarExameView` por integração com API de IA real.

## 📞 Suporte e Contribuição

Problemas com a execução? Verifique:
1. Python 3.8+ instalado e no PATH
2. Dependências instaladas (`requirements.txt`)
3. Permissões de escrita na pasta `imagens_exames/`
4. Porta 8000 disponível

**Documentação da API:** Consulte `docs/API.md` para detalhes completos dos endpoints REST.

O projeto está pronto para uso com todas as funcionalidades principais testadas e validadas! 🚀
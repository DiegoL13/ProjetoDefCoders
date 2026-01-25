
# **Sistema de Apoio ao Diagnóstico Histopatológico**
## Solução tecnológica para auxiliar médicos no diagnóstico de câncer via Inteligência Artificial, desenvolvida para o Grupo de Pesquisas em Computação Biomédica.




## **📑 Sumário**
Sobre o Projeto

Principais Funcionalidades

Estrutura de Dados

Como Instalar




## **🔬 Sobre o Projeto**
Este sistema permite que profissionais de saúde façam o upload de imagens de microscopia digital e recebam uma classificação automatizada da IA. O objetivo é validar protótipos de aprendizado de máquina e otimizar o fluxo de laudos médicos.

## **🛠️ Tecnologias Utilizadas**
**Backend:** Python 3.x, Django 5.x.

**API:** Django REST Framework.

**Banco de Dados:** SQLite (Desenvolvimento) / PostgreSQL (Produção).

**Autenticação:** Django Auth System.

## **📂 Estrutura de Arquivos Principal**
**models.py:** Define a estrutura de Usuario, Medico, Paciente, Exame e LogExames.

**views.py:** Contém a lógica de negócio, incluindo a simulação da IA e controle de acesso.

**serializers.py:** Transforma os modelos em JSON para a API.

**choices.py:** Centraliza as opções de resultados e ações do sistema.




## **✨ Principais Funcionalidades**

### **👨‍⚕️ Área do Médico**
Dashboard de Exames: Gestão centralizada de pacientes e diagnósticos.

Upload Inteligente: Suporte a múltiplas imagens por exame.

Validação de IA: Recebimento de prévia (Benigno/Maligno/Saudável) com opção de revisão manual.

### **👤 Área do Paciente**

Laudos Liberados: Acesso aos resultados apenas após a autorização do médico responsável.




## **📊 Estrutura de Dados**
O sistema utiliza os seguintes modelos principais:

Modelo - Descrição
Usuario - Base customizada com CPF e E-mail como identificadores únicos.
Medico - Extensão com CRM e Especialidade.
Paciente - Extensão com Histórico Médico.
Exame - "Vínculo entre médico/paciente, contendo a descrição e o resultado da IA."
Imagem - Armazena os caminhos das imagens histopatológicas.




## **Como Instalar**

### **Clone o repositório:**

git clone https://github.com/seu-usuario/projeto-diagnostico.git

### **Configure o ambiente:**

python -m venv .venv
source venv/bin/activate   (Linux/Mac)
venv\Scripts\activate      (Windows)

### **Instale as dependências:**

pip install django djangorestframework
pip -r requirements.txt

### **Migre o Banco de Dados:**

python manage.py migrate
python manage.py makemigrate
python manage.py createsuperuser

### **Inicie o servidor: python manage.py runserver.**

Acesse http://127.0.0.1:8000/

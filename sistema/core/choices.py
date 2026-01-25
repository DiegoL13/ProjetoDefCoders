# Aqui ficam as tabelas de opções de escolhas que são usadas nos Models em models.py

SEXO_BIOLOG_CHOICES = {
    'masculino': 'Masculino',
    'feminino': 'Feminino',
}

EXAME_ACTIONS = {
    'created': 'Criado',
    'updated': 'Atualizado',
    'deleted': 'Deletado',
    'viewed': 'Visualizado',
    'result_added': 'Resultado Adicionado',
}

RESULTADOS = (
      ('BENIGNO','Benigno'),
      ('MALIGNO', 'Maligno'),
      ('SAUDÁVEL', 'Saudável')
  )

EVENTOS_CHOICES = [
        ('Criação', 'Criação'),
        ('Disponibilização para o paciente', 'Disponibilização para o paciente'),
        ('Revisão por IA', 'Revisão por IA'),
        ('Revisão por médico', 'Revisão por médico'),
    ]
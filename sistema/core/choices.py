# Aqui ficam as tabelas de opções de escolhas que são usadas nos Models em models.py

SEXO_BIOLOG_CHOICES = {
    'masculino': 'Masculino',
    'feminino': 'Feminino',
}

  
resultados = (
      ('BENIGNO','Benigno'),
      ('MALIGNO', 'Maligno'),
      ('SAUDÁVEL', 'Saudável')
  )
  

STATUS_EXAME = [
    ('PENDENTE', 'Aguardando Análise'),
    ('IA', 'Em Análise pela IA'),
    ('REVISADO', 'Revisado pelo Médico'),
    ('LIBERADO', 'Liberado para o Paciente')
]
EXAME_ACTIONS = {
    'created': 'Criado',
    'updated': 'Atualizado',
    'deleted': 'Deletado',
    'viewed': 'Visualizado',
    'result_added': 'Resultado Adicionado',
}

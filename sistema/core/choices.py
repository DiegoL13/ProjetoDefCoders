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
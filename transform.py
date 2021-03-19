"""
    TRANSFORM
    Utilizando a biblioteca pandas transformamos o arquivo em um dataframe, desta forma conseguimos realizar diversas
    operações para o tratamento, dentre elas selecionar apenas dados referentes ao Brasil e manter somente 8 colunas.
"""
import pandas as pd
name_dataset_brasil = 'covid19_brasil.csv'
df = pd.read_csv(f'download/covid19.csv', sep=',', encoding='utf-8') # Abrindo arquivo

# Selecionando apenas dados referentes ao Brasil e realizando a tradução do valor do campo
df_brazil = df[df['location'] == 'Brazil'] # dataframe[dataframe[campo] == valor]
df_brazil = df_brazil.replace('Brazil', 'Brasil')  # objeto.substituir(Antigo, Novo)

# Mantendo apenas colunas referentes a casos, novos casos, mortes e novas mortes.
columns = ['location', 'date', 'total_cases', 'new_cases', 'total_deaths',
           'new_deaths', 'total_cases_per_million', 'new_cases_per_million']
df_brazil = df_brazil.filter(columns)

renomear_colunas = {'location': 'pais',
                        'date': 'data',
                 'total_cases': 'total_casos',
                   'new_cases': 'novos_casos',
                'total_deaths': 'total_obitos',
                  'new_deaths': 'novos_obitos',
     'total_cases_per_million': 'total_casos_por_milhao',
       'new_cases_per_million': 'novos_casos_por_milhao'}
df_brazil = df_brazil.rename(columns=renomear_colunas) # Renomeando as colunas, antigo nome: novo nome

# Salvando o resultado (dataframe) novamente em CSV, dispensando a coluna de index.
df_brazil.to_csv(name_dataset_brasil, sep=',', index=False)

"""
    EXTRACT
    Através de uma URL de download obtemos o arquivo e salvamos em formato csv
"""
import requests

name_dataset = 'covid19.csv'

# Fonte do dado
source_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

# Iniciando conexão para extrair arquivo da web
data = requests.get(source_url)

if data.status_code != 200:  # Verificando se a conexão teve algum problema
    print('Erro ao extrair!')

# Salvando dados em forma de texto dentro de um arquivo .csv
with open(f'download/{name_dataset}', 'w', encoding='utf-8') as f:
    f.write(data.text)
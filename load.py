"""
    LOAD
    Com a biblioteca sqlalchemy abrimos conexão com um banco de dados MySQL e inserimos os dados dentro de uma
    tabela neste banco, caso as tabelas/schema não existam nós criamos.
"""
from sqlalchemy import create_engine
import pandas as pd

# Dados de conexão local
conn = {'host': 'localhost', 'user': 'root', 'pass': '',
        'schema': 'estudo', 'tmp': 'tmp_coronavirus', 'rel': 'rel_coronavirus'}

# Criando conexão
engine = create_engine(f'mysql+pymysql://{conn["user"]}:{conn["pass"]}@{conn["host"]}/{conn["schema"]}')

# Cria tabela temporária caso não exista
create_tmp = f""" CREATE TABLE IF NOT EXISTS {conn["schema"]}.{conn["tmp"]} (
			 pais VARCHAR(100)
			,data DATE
			,total_casos BIGINT
			,novos_casos BIGINT
			,total_obitos BIGINT
			,novos_obitos BIGINT
			,total_casos_por_milhao FLOAT
			,novos_casos_por_milhao FLOAT );"""

engine.execute(create_tmp)


# Cria tabela relacional caso não exista
create_rel = f"""CREATE TABLE IF NOT EXISTS {conn["schema"]}.{conn["rel"]} (
         id INT NOT NULL AUTO_INCREMENT
		 ,pais VARCHAR(100)
		 ,data DATE
		 ,total_casos BIGINT
		 ,novos_casos BIGINT
		 ,total_obitos BIGINT
		 ,novos_obitos BIGINT
		 ,total_casos_por_milhao FLOAT
		 ,novos_casos_por_milhao FLOAT
		 ,horario_insercao TIMESTAMP
		 ,horario_alteracao TIMESTAMP
		 ,PRIMARY KEY(id));"""

engine.execute(create_rel)

# Abrindo arquivo de dados transformados
data_corona = pd.read_csv('covid19_brasil.csv', sep=',', encoding='utf-8', index_col=False)

# Limpa a tabela temporária (stage) e insere os dados
engine.execute(f'TRUNCATE TABLE {conn["schema"]}.{conn["tmp"]};')
data_corona.to_sql(name=conn["tmp"], con=engine, schema=conn["schema"], if_exists='append', index=False)

# Insere os novos dados na tabela permanente (relacional)
query = f"""INSERT INTO {conn["schema"]}.{conn["rel"]}
                (pais, data, total_casos, novos_casos, total_obitos, novos_obitos, total_casos_por_milhao, novos_casos_por_milhao, horario_insercao)
            SELECT             
                pais, data, total_casos, novos_casos, total_obitos, novos_obitos, total_casos_por_milhao, novos_casos_por_milhao, CURRENT_TIMESTAMP
            FROM {conn["schema"]}.{conn["tmp"]} AS tmp_corona
            WHERE tmp_corona.data NOT IN (SELECT data FROM {conn["schema"]}.{conn["rel"]});
"""
engine.execute(query)


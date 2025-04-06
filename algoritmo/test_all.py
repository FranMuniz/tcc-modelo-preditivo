import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente 
load_dotenv()

# Configuração do Banco de Dados 
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Cria a conexão com o Banco de Dados com sqlalchemy 
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine_conexao = create_engine(DATABASE_URL)

# Path para os arquivos excel 
path = r'C:\Users\Francieli Muniz\OneDrive\Área de Trabalho\Área de Trabalho\Francieli dos Santos Muniz\Docs\Faculdade\8 - TCC I e II\Ingestion'

# Lê os arquivos excel
predicao = pd.read_excel(f'{path}\predicoes_vendas_2024.xlsx')

# Remover as vírgulas e converter os valores para float
predicao = predicao.replace({',': ''}, regex=True)  # Remove todas as vírgulas
predicao = predicao.apply(pd.to_numeric, errors='ignore')  # Converte colunas numéricas para float

# Insere os dados nas tabelas
def insert_data(table_name, dataframe):
    dataframe.to_sql(table_name, engine_conexao, if_exists='append', index=False)

# Insere os dados nas tabelas
insert_data('predicao', predicao)

print("Dados carregados com sucesso!")

""" Projeto: Trabalho de Conclusão de Curso UNIP
Descrição: Carregamento dos dados
Autores: André Maldonado, Caio Teixeira, Francieli Muniz, Gabriel Aparecido, João Soares e Lais Falcochio
(c) """
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente 
load_dotenv()

# Configuração do Banco de Dados 
# os.getenv pega os valores das variáveis de ambiente
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Cria a conexão com o Banco de Dados com sqlalchemy 
# Cria o engine de conexão para interagir com o banco e fazer consultas. 
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine_conexao = create_engine(DATABASE_URL)

# Path para os arquivos excel 
path = r'C:\Users\Francieli Muniz\OneDrive\Área de Trabalho\Área de Trabalho\Francieli dos Santos Muniz\Docs\Faculdade\8 - TCC I e II\Ingestion'

# Lê os arquivos excel
pedido = pd.read_excel(f'{path}\pedido.xlsx')
item_pedido = pd.read_excel(f'{path}\item_pedido.xlsx')
pagamento = pd.read_excel(f'{path}\pagamento.xlsx')
cliente = pd.read_excel(f'{path}\cliente.xlsx')
fornecedor = pd.read_excel(f'{path}\fornecedor.xlsx')
pessoa_fisica = pd.read_excel(f'{path}\pessoa_fisica.xlsx')
produto = pd.read_excel(f'{path}\produto.xlsx')

# Insere os dados nas tabelas
def insert_data(table_name, dataframe):
    dataframe.to_sql(table_name, engine_conexao, if_exists='append', index=False)

# Insere os dados nas tabelas, para não ter problemas com as PK e FK
insert_data('cliente', cliente)
insert_data('fornecedor', fornecedor)
insert_data('pessoa_fisica', pessoa_fisica)
insert_data('produto', produto)
insert_data('pedido', pedido)
insert_data('item_pedido', item_pedido)
insert_data('pagamento', pagamento)

print("Dados carregados com sucesso!")









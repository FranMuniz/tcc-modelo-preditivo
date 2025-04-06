""" Projeto: Trabalho de Conclusão de Curso UNIP
Descrição: RDS connection 
Autores: André Maldonado, Caio Teixeira, Francieli Muniz, Gabriel Aparecido, João Soares e Lais Falcochio
(c) """
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text

# Carrega as variáveis de ambiente 
load_dotenv()

# Cria a URL de conexão com sqlalchemy 
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Cria o engine de conexão para interagir com o banco e fazer consultas.
engine_conexao = create_engine(DATABASE_URL)

# Função para extrair os dados e armazenar em um DataFrame
def get_data(query, engine):
    
    # Usa a conexão com o engine
    with engine.connect() as conexao:
        df = pd.read_sql(text(query), conexao)
    return df 

# Conecta com o banco, extrai os dados e apresenta uma amostra
try:
    consulta = 'SELECT * FROM pagamento'
    data = get_data(consulta, engine_conexao)
    print(data.head())
    
    # Salva o DataFrame em um arquivo .pkl
    data.to_pickle("dados_vendas.pkl")
    print("Arquivo dados_vendas.pkl criado com sucesso")
except Exception as excecao:
    print("Erro ao conectar ao banco de dados:", excecao)




""" Projeto: Trabalho de Conclusão de Curso UNIP
Descrição: Algoritmo de Predição
Autores: André Maldonado, Caio Teixeira, Francieli Muniz, Gabriel Aparecido, João Soares e Lais Falcochio
(c) """
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Carrega o DataFrame criado no connection_rds.py
data = pd.read_pickle("dados_vendas.pkl")

# Converte a coluna 'data_pagamento' em formato datetime
data['data_pagamento'] = pd.to_datetime(data['data_pagamento'], errors='coerce')

# Filtra pagamentos com status 'Sucesso'
data_sucesso = data[data['status'] == 'Sucesso']

# Inicializa as listas para armazenagem dos dados
meses = list(range(1, 13))
vendas_2019 = []
vendas_2020 = []
vendas_2021 = []
vendas_2022 = []
vendas_2023 = []
previsoes_2024 = []

# Itera em cada mês
for mes in meses:
    # Filtra o respectivo mês de 2019 a 2023 
    meses_19 = data_sucesso[(data_sucesso['data_pagamento'].dt.year == 2019) & (data_sucesso['data_pagamento'].dt.month == mes)]
    meses_20 = data_sucesso[(data_sucesso['data_pagamento'].dt.year == 2020) & (data_sucesso['data_pagamento'].dt.month == mes)]
    meses_21 = data_sucesso[(data_sucesso['data_pagamento'].dt.year == 2021) & (data_sucesso['data_pagamento'].dt.month == mes)]
    meses_22 = data_sucesso[(data_sucesso['data_pagamento'].dt.year == 2022) & (data_sucesso['data_pagamento'].dt.month == mes)]
    meses_23 = data_sucesso[(data_sucesso['data_pagamento'].dt.year == 2023) & (data_sucesso['data_pagamento'].dt.month == mes)]
    
    # Calcula a soma de vendas para cada mês, de cada ano
    meses_19_vendas = meses_19['valor_pedido'].sum()
    meses_20_vendas = meses_20['valor_pedido'].sum()
    meses_21_vendas = meses_21['valor_pedido'].sum()
    meses_22_vendas = meses_22['valor_pedido'].sum()
    meses_23_vendas = meses_23['valor_pedido'].sum()

    # Armazena os dados de 2019 a 2023
    vendas_2019.append(meses_19_vendas)
    vendas_2020.append(meses_20_vendas)
    vendas_2021.append(meses_21_vendas)
    vendas_2022.append(meses_22_vendas)
    vendas_2023.append(meses_23_vendas)

    # Cria um DataFrame com os dados de vendas de todos os meses, todos os anos
    dados_vendas = pd.DataFrame({
        'ano': [2019, 2020, 2021, 2022, 2023],
        'vendas': [meses_19_vendas, meses_20_vendas, meses_21_vendas, meses_22_vendas, meses_23_vendas]
    })

    # Modelo de Regressão Linear
    X = dados_vendas[['ano']] # Variável Independente
    y = dados_vendas['vendas'] # Variável Dependente

    model = LinearRegression()
    model.fit(X, y)

    # Predição de vendas para o respectivo mês em 2024 
    meses_2024_vendas_predicao = model.predict(np.array([[2024]]))

    # Armazena as predições
    previsoes_2024.append(meses_2024_vendas_predicao[0])

    # Cria o gráfico de dispersão para o respectivo mês
    plt.figure(figsize=(10, 6))

    # Plota os pontos de dados reais
    plt.scatter(X, y, color='blue', label='Dados Reais')

    # Plota a linha de regressão
    plt.plot(X, model.predict(X), color='red', label='Linha de Regressão')

    # Adiciona o ponto previsto para 2024
    plt.scatter([2024], meses_2024_vendas_predicao, color='green', label='Previsão 2024')

    # Configurações do gráfico
    plt.title(f'Regressão Linear - Mês: {mes:02d}')
    plt.xlabel('Ano')
    plt.ylabel('Vendas')
    plt.legend()
    plt.grid(True)

    # Exibe o gráfico
    plt.show()

# Formata os valores com duas casas decimais e separadores de milhar
vendas_2019 = [f'{valor:,.2f}' for valor in vendas_2019]
vendas_2020 = [f'{valor:,.2f}' for valor in vendas_2020]
vendas_2021 = [f'{valor:,.2f}' for valor in vendas_2021]
vendas_2022 = [f'{valor:,.2f}' for valor in vendas_2022]
vendas_2023 = [f'{valor:,.2f}' for valor in vendas_2023]
previsoes_2024 = [f'{prev:,.2f}' for prev in previsoes_2024]

# Converte os meses para strings
meses_str = [f'{mes:02d}' for mes in meses]

# Cria a figura do eixo do gráfico
fig, ax = plt.subplots(figsize=(14, 6))

# Plota no gráfico as vendas de 2019
ax.scatter(meses, [float(valor.replace(',', '')) for valor in vendas_2019], color='orange', label='Vendas 2019')
ax.plot(meses, [float(valor.replace(',', '')) for valor in vendas_2019], color='orange')

# Plota no gráfico as vendas de 2020
ax.scatter(meses, [float(valor.replace(',', '')) for valor in vendas_2020], color='purple', label='Vendas 2020')
ax.plot(meses, [float(valor.replace(',', '')) for valor in vendas_2020], color='purple')

# Plota no gráfico as vendas de 2021 
ax.scatter(meses, [float(valor.replace(',', '')) for valor in vendas_2021], color='grey', label='Vendas 2021')
ax.plot(meses, [float(valor.replace(',', '')) for valor in vendas_2021], color='grey')

# Plota no gráfico as vendas de 2022
ax.scatter(meses, [float(valor.replace(',', '')) for valor in vendas_2022], color='red', label='Vendas 2022')
ax.plot(meses, [float(valor.replace(',', '')) for valor in vendas_2022], color='red')

# Plota no gráfico as vendas de 2023
ax.scatter(meses, [float(valor.replace(',', '')) for valor in vendas_2023], color='green', label='Vendas 2023')
ax.plot(meses, [float(valor.replace(',', '')) for valor in vendas_2023], color='green')

# Plota as previsões para 2024
ax.scatter(meses, [float(prev.replace(',', '')) for prev in previsoes_2024], color='blue', label='Previsões 2024')
ax.plot(meses, [float(prev.replace(',', '')) for prev in previsoes_2024], color='blue')

# Títulos
ax.set_title('Vendas de 2019 a 2023 vs Previsões de Vendas para 2024')
ax.set_xlabel('Mês')
ax.set_ylabel('Vendas')
ax.set_xticks(meses)
ax.set_xticklabels(meses_str, rotation=45)
ax.grid(True)
ax.legend()

# Cria a tabela com os dados do gráfico
tabela_dados = pd.DataFrame({
    'Mês': meses_str,
    'Vendas 2019': vendas_2019,
    'Vendas 2020': vendas_2020,
    'Vendas 2021': vendas_2021,
    'Vendas 2022': vendas_2022,
    'Vendas 2023': vendas_2023,
    'Previsão 2024': previsoes_2024
})

# Cria a figura para a tabela
fig_table, ax_table = plt.subplots(figsize=(10, 6))

# Plota a tabela
ax_table.axis('off')
tabela = ax_table.table(cellText=tabela_dados.values,
                      colLabels=tabela_dados.columns,
                      cellLoc='center',
                      loc='center',
                      colColours=["lightpink"] * len(tabela_dados.columns))

# Ajusta o layout para evitar sobreposição
plt.subplots_adjust(left=0.1, right=0.7, wspace=0.5)

# Exibe o gráfico e a tabela
plt.show()

# Salva as vendas em um arquivo .pkl para uso no código de validação
pd.to_pickle({'vendas_2019': vendas_2019, 'vendas_2020': vendas_2020, 'vendas_2021': vendas_2021, 'vendas_2022': vendas_2022, 'vendas_2023': vendas_2023, 'previsoes_2024': previsoes_2024}, 'dados_para_validacao.pkl')

""" Projeto: Trabalho de Conclusão de Curso UNIP
Descrição: Validação do Algoritmo de Predição
Autores: André Maldonado, Caio Teixeira, Francieli Muniz, Gabriel Aparecido, João Soares e Lais Falcochio
(c) """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression

# Carrega as vendas e previsões geradas no sales_algotithm.py
resultados = pd.read_pickle('dados_para_validacao.pkl')

# Converte as vendas e previsões para formato numérico 
meses = list(range(1, 13))
vendas_2019 = [float(venda.replace(',', '')) for venda in resultados['vendas_2019']]
vendas_2020 = [float(venda.replace(',', '')) for venda in resultados['vendas_2020']]
vendas_2021 = [float(venda.replace(',', '')) for venda in resultados['vendas_2021']]
vendas_2022 = [float(venda.replace(',', '')) for venda in resultados['vendas_2022']]
vendas_2023 = [float(venda.replace(',', '')) for venda in resultados['vendas_2023']]
previsoes_2024 = [float(prev.replace(',', '')) for prev in resultados['previsoes_2024']]

# Prepara os dados para o modelo
dados_venda = pd.DataFrame({
    'ano': [2019, 2020, 2021, 2022, 2023],
    'vendas': [np.mean(vendas_2019), np.mean(vendas_2020), np.mean(vendas_2021), np.mean(vendas_2022), np.mean(vendas_2023)]
})

# Modelo de regressão linear
X = dados_venda[['ano']]
y = dados_venda['vendas']

model = LinearRegression()
model.fit(X, y)

# Adiciona as previsões do DataFrame original para fazer a análise de resíduos
dados_venda['previsoes'] = model.predict(X)
dados_venda['residuos'] = dados_venda['vendas'] - dados_venda['previsoes']

# Plota o gráfico de resíduos
plt.figure(figsize=(10, 6))
sns.scatterplot(x=dados_venda['previsoes'], y=dados_venda['residuos'])
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Previsões')
plt.ylabel('Resíduos')
plt.title('Resíduos vs Previsões')
plt.show()

# Normalidade dos resíduos
fig = plt.figure(figsize=(10, 6))
stats.probplot(dados_venda['residuos'], dist="norm", plot=plt)
plt.title('Gráfico Q-Q dos Resíduos')
plt.show()

# Calcula as métricas de validação
mae = mean_absolute_error(dados_venda['vendas'], dados_venda['previsoes'])
mse = mean_squared_error(dados_venda['vendas'], dados_venda['previsoes'])
rmse = np.sqrt(mse)
r2 = model.score(X, y)

# Formatação dos valores das métricas para incluir separadores de milhar e exibição dos valores
print(f'R²: {r2:.3f}')
print(f'MAE: {mae:,.2f}')
print(f'MSE: {mse:,.2f}')
print(f'RMSE: {rmse:,.2f}')

# Calcula a média dos valores reais 
vendas_media = dados_venda['vendas'].mean()

# Percentual do MAE (Erro Médio Absoluto) e RMSE (Raiz do Erro Quadrático Médio)
percentual_mae = (mae / vendas_media) * 100
percentual_rmse = (rmse / vendas_media) * 100

print(f'Percentual de erro MAE: {percentual_mae:.2f}%')
print(f'Percentual de erro RMSE: {percentual_rmse:.2f}%')

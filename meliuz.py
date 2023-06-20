import pandas as pd
import matplotlib.pyplot as plt

database = pd.read_excel('database.xlsx')

#contagem de categorias e lojas sem repetição
categorias = len(database['Categoria'].unique())
lojas = len(database['Parceiro'].unique())
#resultados no terminal
print(f'Quantidade de categorias: {categorias} \nQuantidade de lojas: {lojas}')

### TAXA DE CONVERSÃO ###
#calcula a taxa de conversão agrupando por parceiro e filtrando por mes
vendas = database.groupby(['Parceiro', pd.Grouper(key='Data', freq='M')])['Nº de vendas'].sum()
acessos = database.groupby(['Parceiro', pd.Grouper(key='Data', freq='M')])['Qtd de acessos'].sum()
conversao = vendas/acessos

#criando gráfico do tipo barras
plt.figure(figsize=(10, 6))
conversao.unstack(level=0).plot(kind='bar')
plt.xlabel('Mês')
plt.ylabel('Taxa de Conversão')
plt.legend(title='Loja')
#substituir numeros por nome dos meses
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio']
plt.xticks(range(len(meses)), meses)
#posição da legenda
plt.legend(title='Loja', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()


### TAXA DE CONFIRMAÇÃO ###
#calcula a taxa de confirmação agrupando confirmadas por parcerio e mês(utiliza variável vendas do cálculo anterior)
confirmadas = database.groupby(['Parceiro', pd.Grouper(key='Data', freq='M')])['Nº de vendas confirmadas'].sum()
confirmacao = confirmadas/vendas
#lista para substituir numeros por nome dos meses
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio']


#criando gráfico do tipo barras
plt.figure(figsize=(10, 6))
confirmacao.unstack(level=0).plot(kind='bar')
plt.xlabel('Mês')
plt.ylabel('Taxa de Confirmação')
plt.legend(title='Loja')
plt.xticks(range(len(meses)), meses)
#posição da legenda
plt.legend(title='Loja', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()


### REPRESENTATIVIDADE EM VENDAS POR LOJA E GMV POR CATEGORIA ###
#exportando para excel os dados necessários
representatividade = database.groupby(['Parceiro', pd.Grouper(key='Data', freq='M')])['GMV'].sum()

GMV_por_categoria = database.groupby(['Categoria', pd.Grouper(key='Data', freq='M')])['GMV'].sum().unstack().fillna(0)
#inclui cabeçalho dos meses
GMV_por_categoria.columns = meses
#salvar em excel
GMV_por_categoria.to_excel('GMV por categoria ao mês.xlsx')

### PICO DE VENDAS POR LOJA ###
#agrupando os dados por loja e iterando os valores de cada uma
lojas = database.groupby('Parceiro')
for loja, data in lojas:
  #seleciona índice da linha com a maior quantidade de vendas e obtém a data
  mais_vendas = data['Nº de vendas'].idxmax()
  pico = data.loc[mais_vendas, 'Data']
  data_formatada = pico.strftime("%d-%m-%y")
  print(f"Pico do {loja} em: {data_formatada}.")

#agruda por categoria e parceiro, depois itera
categorias = database.groupby(['Categoria'])
for categoria, data in categorias:
    GMV_por_loja = data.groupby(['Parceiro'])['GMV'].sum()
    #seleciona o maior e menor valor GMV de cada grupo
    melhor = GMV_por_loja.idxmax()
    pior = GMV_por_loja.idxmin()
    print(f"Em '{categoria}' - melhor desempenho:'{melhor}' / pior desempenho: '{pior}'.")

parceiros_por_categoria = database.groupby('Categoria')['Parceiro'].unique()
parceiros_por_categoria.to_excel('parceiros_por_categoria.xlsx')

### PARTICIPANTES DE PERÍODO PROMOCIONAL ###
#agrupa lojas que participaram do período promocional e compara diferença do ticket médio diário
participantes = database.loc[database['Tipo'] == 'Promocional']
lojas_participantes = participantes['Parceiro'].unique()

print(' ')

for loja in lojas_participantes:
  loja_padrao = database.loc[(database['Parceiro'] == loja) & (database['Tipo'] == 'Padrão')]
  diario = loja_padrao['GMV'].sum()
  ticket_diario = diario / loja_padrao['Nº de vendas'].sum()
  loja_promocional = database.loc[(database['Parceiro'] == loja) & (database['Tipo'] == 'Promocional')]
  promocional = loja_promocional['GMV'].sum()
  ticket_promocional = promocional / loja_promocional['Nº de vendas'].sum()

  print(f"Ticket médio diário do {loja}: {ticket_diario:.2f}")
  print(f">>>>>>>>> Em dias promocionais ficou: {ticket_promocional:.2f} \n")


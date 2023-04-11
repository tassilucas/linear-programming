from datetime import date
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

import stock_data

from tkinter import *
import tkinter.font as font

def printLogResults(m):
    # Para usar na interface grafica
    toBuy = ''

    if m.status == GRB.OPTIMAL:
        print("\n-------\nValor obtido: {}".format(m.ObjVal))
        print("Comprar:")

        for variable in m.getVars():
            if variable.X > 0 and 'peso' in variable.VarName:
                # Gambiarra para imprimir bonito
                name = variable.VarName.split('[')[1][:-1]
                toBuy += name + ' -> ' + str(variable.X) + '\n'
                print("{} -> {}".format(variable.VarName.split('[')[1][:-1], variable.X))

    return toBuy

# # CRIAR MODELO
def buildModel(stock, n, max_variance, min_peso, max_peso):
    tickers, rent = gp.multidict(dict(zip(stock.ticker, stock.rentabilidade)))
    tickers_variancia = dict(zip(stock.ticker, stock.variancia))

    m = gp.Model("carteira")

    # Criando variaveis
    buy = m.addVars(tickers, name="buy", vtype=gp.GRB.BINARY)
    peso = m.addVars(tickers, name="peso")

    # Definindo função objetivo
    m.setObjective(peso.prod(rent), GRB.MAXIMIZE)

    # Adicionando restrição de limite de ações na carteira
    m.addConstr(gp.quicksum(buy[t] for t in tickers) <= n, "_")

    # Adicionando restrição de variancia maxima
    m.addConstr(gp.quicksum(tickers_variancia[t] * buy[t] for t in tickers) <= gp.quicksum(buy[t] for t in tickers)*max_variance, "_")

    # Adicionando restrição de peso
    for t in tickers:
        m.addConstr(peso[t] <= max_peso * buy[t], "_")
        m.addConstr(peso[t] >= min_peso * buy[t], "_")

    # Adicionando restrição proporção peso
    m.addConstr(gp.quicksum(peso[t] for t in tickers) <= 1, "_")

    return m

# # SOLVE
def solveModel(m):
    m.optimize()
    for var in m.getVars():
        print(var)
    txt = printLogResults(m)

    # Retorna string com nome de acoes a serem compradas e valor otimo
    return m.ObjVal, txt

# # EXPORTAR PARA ARQUIVO
def writeToFile(n, max_variance, min_year, min_peso, max_peso, sol, content):
    filename = date.today().isoformat() + '.txt'
    output_file = open('solutions/' + filename, 'w+')
    output_file.write('n: {}, max variance: {}, min_year: {}, min_peso: {}, max_peso: {}\n'.format(n, max_variance, min_year, min_peso, max_peso))
    output_file.write('solution: {}\n'.format(sol))
    output_file.write('acoes: \n{}'.format(content))

def printDataFrame(stock_data, max_variance):
    print(stock_data.query('variancia < @max_variance').sort_values(by=['rentabilidade'], ascending = False))

# # EXIBIR RESULTADOS E EXPORTAR PARA ARQUIVO
def update_display():
    n = int(input_n.get("1.0", "end-1c"))
    max_variance = int(input_variance.get("1.0", "end-1c"))
    min_year = int(input_year.get("1.0", "end-1c"))
    min_peso = float(input_min_peso.get("1.0", "end-1c"))
    max_peso = float(input_max_peso.get("1.0", "end-1c"))
    print("Obtendo dados do mercado (n = {}, max var = {})".format(n, max_variance))
    stock = stock_data.read_stock_data()
    stock = stock.query('year < @min_year')
    printDataFrame(stock, max_variance)
    print("\n------\nDados do mercado obtido. Criando modelo:\n")

    m = buildModel(stock, n, max_variance, min_peso, max_peso)
    sol, content = solveModel(m)

    output.insert(END, content)
    sol_label = Label(text = "Solucao obtida: {}".format(sol))
    sol_label['font'] = myFont
    sol_label.pack()

    writeToFile(n, max_variance, min_year, min_peso, max_peso, sol, content)

app = Tk()
app.geometry("600x570")
app.title("Carteira de Investimentos")

myFont = font.Font(size=20, family='Helvetica')

n_label = Label(text = "Numero maximo de acoes na carteira")
n_label['font'] = myFont
input_n = Text(app, height = 1, width = 25)
input_n['font'] = myFont
variance_label = Label(text = "Media maxima de variancia")
variance_label['font'] = myFont
input_variance = Text(app, height = 1, width = 25)
input_variance['font'] = myFont
year_label = Label(text = "Numero minimo de ano")
year_label['font'] = myFont
input_year = Text(app, height = 1, width = 25)
input_year['font'] = myFont

min_peso_label = Label(text = "Minimo de peso (ex: 0.1)")
min_peso_label['font'] = myFont
input_min_peso = Text(app, height = 1, width = 25)
input_min_peso['font'] = myFont

max_peso_label = Label(text = "Maximo de peso (ex: 0.5)")
max_peso_label['font'] = myFont
input_max_peso = Text(app, height = 1, width = 25)
input_max_peso['font'] = myFont

output = Text(app, height = 5, width = 35)
output['font'] = myFont

sol_button = Button(app, height = 2, width = 20, text="Encontrar solucao",
        command = lambda:update_display())
sol_button['font'] = myFont

n_label.pack()
input_n.pack()
variance_label.pack()
input_variance.pack()
year_label.pack()
input_year.pack()
min_peso_label.pack()
input_min_peso.pack()
max_peso_label.pack()
input_max_peso.pack()
sol_button.pack()
output.pack()

mainloop()

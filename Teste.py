from tabulate import tabulate
import time
import mysql.connector
from Color_Console import *

# CONEXÃO COM O BANCO DE DADOS
db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projetointegrador1"
)
print(db)

# TESTES COM BANCO DE DADOS
cursor = db.cursor()
cursor.execute("SELECT nomeProduto FROM produto")  # QUERY 
resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado)  # EXIBE O RESULTADO DO QUERY
    print()

def decisao_sim_nao(questao):
    while True:
        resposta = input(f"{questao} (S/N): ").strip().lower()
        if resposta in ["s", "n"]:
            return resposta == "s"
        else:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")

def visualizarProdutos():
    cursor.execute("SELECT * FROM produto")  # QUERY 
    resultados = cursor.fetchall()
    for resultado in resultados:
        print(resultado)  # EXIBE O RESULTADO DO QUERY
        print()

# Adicione a função de calculadora de preços
def calculadoraPreco():
    CA = float(input("Digite o custo do produto: "))  # CUSTO AQUISIÇÃO
    CF = float(input("Digite o custo fixo do produto: "))  # CUSTO FIXO
    CV = float(input("Digite a comissão de vendas do produto: "))  # COMISSÃO DE VENDAS
    IV = float(input("Digite os impostos do produto: "))  # IMPOSTOS SOBRE PRODUTO
    ML = float(input("Digite a margem de lucro do produto: "))  # MARGEM DE LUCRO
    PV = CA / (1 - (CF + CV + IV + ML) / 100)  # PREÇO DE VENDA
    RB = PV - CA  # RECEITA BRUTA
    OC = PV * (CF + CV + IV) / 100  # OUTROS CUSTOS (CF + CV + IV)
    RT = RB - OC  # RENTABILIDADE

    # Retorne todas as variáveis importantes para uso posterior
    return CA, CF, CV, IV, ML, PV, RB, OC, RT

def gerarTabelaResultado(PV, CA, RB, OC, RT, CF, CV, IV):
    tabelaResultados = [
        ["A. Preço de Venda", f"R${round(PV,2)}", "100.0%"],
        ["B. Custo de aquisição", f"R${round(CA,2)}", f"{round(CA / PV * 100,3)}%"],
        ["C. Receita Bruta", f"R${round(PV - CA,2)}", f"{round((PV - CA) / PV * 100,3)}%"],
        ["D. Custo Fixo/Administrativo", f"{round(CF,3)}%", f"{round(CF * PV / 100,2)}"],
        ["E. Comissão de Vendas", f"{round(CV,3)}%", f"{round(CV * PV / 100,2)}"],
        ["F. Impostos", f"{round(IV,3)}%", f"{round(IV * PV / 100,2)}"],
        ["G. Outros Custos", f"{round(OC / PV * 100,3)}%", f"{round(OC,2)}"],
        ["H. Rentabilidade", f"{round(RT / PV * 100,3)}%", f"{round(RT,2)}"],
    ]

    print("\n\nTABELA DE RESULTADOS:")
    print(tabulate(tabelaResultados, headers=["Descrição", "Porcentagem", "Valor"]))

def gerarRentabilidade(RT, PV):
    print("\n\nCLASSIFICAÇÃO DE RENTABILIDADE:")
    rentabilidade = (RT / PV) * 100
    
    if rentabilidade > 20:
        print(f"Rentabilidade alta, com uma porcentagem de lucro de {rentabilidade:.2f}%")
    elif 10 < rentabilidade <= 20:
        print(f"Rentabilidade média, com uma porcentagem de lucro de {rentabilidade:.2f}%")
    elif 0 < rentabilidade <= 10:
        print(f"Rentabilidade baixa, com uma porcentagem de lucro de {rentabilidade:.2f}%")
    elif rentabilidade == 0:
        print("Sem lucro")
    elif rentabilidade < 0:
        print("Prejuízo")
    
    print()

def menu():
    while True:  # Mantém o menu em loop para permitir várias seleções
        print("-- MENU do Controle de Estoque --")
        print("Selecione uma função para prosseguir:")
        
        tabelaFuncoes = [
            ["1. ", "Visualizar produtos"],
            ["2. ", "Adicionar produtos"],
            ["3. ", "Calcular preços"],
            ["4. ", "Sair"],  # Opção para sair do loop
        ]
        print(tabulate(tabelaFuncoes, headers=["Entrada:", "Função:"]))

        print()

        opc = int(input("Selecione a função a ser executada: "))

        if opc == 1:
            visualizarProdutos()
        elif opc == 2:
            print("Adicionar produtos ainda não está implementado.")
        elif opc == 3:
            CA, CF, CV, IV, ML, PV, RB, OC, RT = calculadoraPreco()

            question = "Deseja exibir os resultados?"
            resposta = decisao_sim_nao(question)  # Captura a resposta

            if resposta:
                gerarTabelaResultado(PV, CA, RB, OC, RT, CF, CV, IV)  # Passe os argumentos corretos
                gerarRentabilidade(RT, PV)  # Passe as variáveis certas
            else:
                print("A função de exibição de resultados não será executada.")
        elif opc == 4:
            print("O programa encerrará em 10 segundos.")
            time.sleep(10)
            break  # Sai do loop e encerra o programa
        
        print()  # Adiciona um espaço para melhor formatação do menu

menu()

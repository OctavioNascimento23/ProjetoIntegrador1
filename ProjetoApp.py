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
cursor.execute("SELECT nomeProduto FROM produto") # QUERY 
resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado) # EXIBE O RESULTADO DO QUERY
    print()

#CP_BD
#CF_BD
#CV_BD
#IV_BD
#ML_BD

def decisao_sim_nao(questao):
    while True:
        resposta = input(f"{questao} (S/N): ").strip().lower()  # obtém a resposta do usuário e converte para minúsculas
        if resposta in ["s", "n"]:  # verifica se a resposta é 's' ou 'n'
            return resposta == "s"  # retorna True para 's', False para 'n'
        else:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")

def visualizarProdutos():
    cursor = db.cursor()
cursor.execute("SELECT * FROM produto") # QUERY 
resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado) # EXIBE O RESULTADO DO QUERY
    print()

def calculadoraPreco():
    CP = float(input("Digite o custo do produto: ")) # CUSTO PRODUTO
    CF = float(input("Digite o custo fixo do produto: ")) # CUSTO FIXO
    CV = float(input("Digite a comissão de vendas do produto: ")) # COMISSÃO DE VENDAS
    IV = float(input("Digite os impostos do produto: ")) # IMPOSTOS SOBRE PRODUTO
    ML = float(input("Digite a margem de lucro do produto: ")) # MARGEM DE LUCRO
    PV = CP / (1 - (CF + CV + IV + ML) / 100) # PREÇO DE VENDA
    RB = PV-CP # RECEITA BRUTA
    OC = PV*(CF+CV+IV)/100 # OUTROS CUSTOS (CF + CV + IV)
    RT = RB-OC # RENTABILIDADE

def gerarTabelaResultado():
    tabelaResultados = [
            ["A. Preço de Venda",f"R${round(PV,2)}","100.0%"],
            ["B. Custo de aquisição",f"R${round(CP,2)}",f"{round(CP/PV*100,3)}"+"%"],
            ["C. Receita Bruta",f"R${round(PV-CP,2)}",f"{round((PV-CP)/PV*100,3)}"+"%"],
            ["D. Custo Fixo/Administrativo",f"R${round(CF*PV/100,2)}",f"{round(CF,3)}"+"%"],
            ["E. Comissão de Vendas",f"R${round(CV*PV/100,2)}",f"{round(CV,3)}"+"%"],
            ["F. Impostos",f"R${round(IV*PV/100,2)}",f"{round(IV,3)}"+"%"],
            ["G. Outros Custos",f"R${round(OC,2)}",f"{round(OC/PV*100,3)}"+"%"],
            ["H. Rentabilidade",f"R${round(RT,2)}",f"{round(RT/PV*100,3)}"+"%"]]

    print("\n\n TABELA DE RESULTADOS: \n")
    print(tabulate(tabelaResultados,headers=["Descrição","Valor","%"]))

def gerarRentabilidade():
    print("\n\n CLASSIFICAÇÃO DE RENTABILIDADE: \n")
    if ((RT/PV)*100)>20:
        print(f"Seu produto possui uma rentabilidade alta, a porcentagem de lucro será de {(round(RT/PV,2)*100)}"+"%")
    elif ((RT/PV)*100)<20 and ((RT/PV)*100)>10 or ((RT/PV)*100)==20:
        print(f"Seu produto possui uma rentabilidade média, a porcentagem de lucro será de {(round(RT/PV,2)*100)}"+"%")
    elif ((RT/PV)*100)<10 and ((RT/PV)*100)>0 and ((RT/PV)*100)!=0 and ML!=0:
        print(f"Seu produto possui uma rentabilidade baixa, a porcentagem de lucro será de {(round(RT/PV,2)*100)}"+"%")
    elif ((RT/PV)*100)==0 or ML==0:
        print(f"Seu produto não irá gerar lucro")
    elif ((RT/PV)*100)<0:
        print(f"Seu produto acarretará em prejuízos de {(round(RT/PV,2)*100)}"+"%")
    else:
        print("ERRO, TENTE NOVAMENTE!")
    print()

def menu():
    print("-- MENU do Controle de Estoque --")
    print()
    #time.sleep(2)
    print("Funções do programa: ")
    print()
    tabelaFuncoes = [
        ["1. ","Visualizar produtos"],
        ["2. ","Adicionar produtos"]]
    print(tabulate(tabelaFuncoes, headers=["Entrada:","Função:"]))
    print()
    opc = int(input(print("Selecione a função a ser executada: ")))
    if opc == 1:
        calculadoraPreco()
    elif opc == 2:
        visualizarProdutos()
    elif opc == 3: 
        calculadoraPreco()
        question = "Deseja exibir os resultados?"
        decisao_sim_nao(question)
        if resposta:
            gerarTabelaResultado()
        else:
            print("A função não será executada.")

menu()
    


print("O programa irá encerrar em 10 segundos.")

time.sleep(10)


from tabulate import tabulate
import time
import mysql.connector
from Color_Console import *

# CONEXÃO COM O BANCO DE DADOS
db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projetointegrador1" # Nome do BD
)
print(db)

# TESTES COM BANCO DE DADOS
cursor = db.cursor()
queryProdutos = "SELECT nomeProduto FROM produto"
cursor.execute("SELECT nomeProduto FROM produto")  # Query 
resultados = cursor.fetchall()
for resultado in resultados:
    print(resultado)  # Exibindo o query
    print()

def decisao_sim_nao(questao):
    while True:
        resposta = input(f"{questao} (S/N): ").strip().lower()
        if resposta in ["s", "n"]:
            return resposta == "s" # Enquanto aqui tiver "SIM" o loop será True
        else:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")

def visualizarProdutos(cursor):
    cursor.execute("SELECT * FROM produto")  # Query 
    resultados = cursor.fetchall()  # Obtendo todos os resultados

    # Cabeçalho para tabela de visualização de produtinhos
    CabecalhoProdutos = ["ID", "Nome do Produto", "Descrição", "Custo de aquisição", "Imposto sobre produto", "Custo fixo", "Comissão", "Rentabilidade"] 

    # Tabulando dados do BD
    print("\n\nTABELA DE PRODUTOS:")
    print()
    print(tabulate(resultados, headers=CabecalhoProdutos, tablefmt="grid"))

    cursor.execute("SELECT idProduto, nomeProduto, precoProduto, impostoProduto, custoProduto, custoFixo, comissaoVendas, rentabilidadeProduto FROM produto")
    produtos = cursor.fetchall()

    DecisaoTabelaProduto = "Deseja exibir os cálculos para os produtos?"
    resposta = decisao_sim_nao(DecisaoTabelaProduto)
    if resposta:

        for produto in produtos:

            idProduto, nomeProduto, PV, IV, CA, CF, CV, ML = produto
            
            # Calcular preço de venda e rentabilidade usando a função calculadoraPreco

            PV = CA / (1 - (CF + CV + IV + ML) / 100)  # PREÇO DE VENDA
            RB = PV - CA  # RECEITA BRUTA
            OC = PV * (CF + CV + IV) / 100  # OUTROS CUSTOS (CF + CV + IV)
            RT = RB - OC  # RENTABILIDADE

            # Informações do produto
            print(f"Produto: {nomeProduto}")
            print(f"ID do Produto: {idProduto}")

            # Gerar tabela de resultados
            gerarTabelaResultado(PV, CA, RB, OC, RT, CF, CV, IV)

            # Gerar classificação de rentabilidade
            gerarRentabilidade(RT, PV)


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

    # Retornando para usar nas próximas funções. 
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
    print()
    print(tabulate(tabelaResultados, headers=["Descrição", "Porcentagem", "Valor"]))

def gerarRentabilidade(RT, PV):
    print("\n\nCLASSIFICAÇÃO DE RENTABILIDADE:")
    print()
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
    
def adicionarProduto():
    cod=int(input("Digite o código do produto: "))
    nome=input("Digite o nome do produto: ")
    descricao=input("Digite a descrição do produto: ")
    PR=float(input("Digite o preço do produto: "))
    IV = float(input("Digite os impostos do produto: "))  # IMPOSTOS SOBRE PRODUTO
    CA=float(input("Digite o custo do produto: "))
    CF = float(input("Digite o custo fixo do produto: "))  # CUSTO FIXO
    CV = float(input("Digite a comissão de vendas do produto: "))  # COMISSÃO DE VENDAS
    ML = float(input("Digite a margem de lucro do produto: "))  # MARGEM DE LUCRO

    query = "INSERT INTO produto (idProduto, nomeProduto, descProduto, precoProduto,impostoProduto,custoProduto, custoFixo, comissaoVendas, rentabilidadeProduto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
    values = (cod, nome, descricao,PR,IV,CA, CF, CV, ML)

    try:
        cursor.execute(query, values)
        db.commit()  # Confirmar a transação no banco de dados
        print("Produto adicionado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao adicionar o produto:", err)

def excluirProduto():
    cod = int(input("Digite o código do produto a ser excluído: "))

    cursor.execute("SELECT * FROM produto WHERE idProduto = %s", (cod,))
    produto = cursor.fetchone()

    if produto:
        idProduto, nomeProduto, descricaoProduto, precoProduto, impostoProduto, custoProduto, custoFixo, comissaoVendas, rentabilidadeProduto = produto

        print("\nProduto encontrado:")
        print(f"ID: {idProduto}")
        print(f"Nome: {nomeProduto}")
        print(f"Descrição: {descricaoProduto}")
        print(f"Preço: R${precoProduto}")
        print(f"Imposto: {impostoProduto}%")
        print(f"Custo: R${custoProduto}")
        print(f"Custo Fixo: {custoFixo}%")
        print(f"Comissão de Vendas: {comissaoVendas}%")
        print(f"Rentabilidade: {rentabilidadeProduto}%")
           
        questao = input("Deseja mesmo excluir o produto? (S/N): ").strip().lower()
        if questao=='s':
            cursor.execute("DELETE FROM produto WHERE idProduto = %s", (cod,))
            db.commit()
            print("Produto excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
    else:
        print("Produto não encontrado.")

    

def menu():
    while True: 
        print("MENU do Controle de Estoque")
        print()
        print("Selecione uma função para prosseguir:")
        print()
        
        tabelaFuncoes = [
            ["1. ", "Visualizar produtos"],
            ["2. ", "Adicionar produtos"],
            ["3. ", "Calcular preços"],
            ["4. ","Alterar produto"],
            ["5. ","Excluir produto"],
            ["6. ","Sair"],  
        ]
        print(tabulate(tabelaFuncoes, headers=["Entrada", "Função"]))
        print()

        opc = int(input("Selecione a função a ser executada: "))
        print()
        if opc == 1:
            visualizarProdutos(cursor)
        elif opc == 2:
            adicionarProduto()
        elif opc == 3:
            CA, CF, CV, IV, ML, PV, RB, OC, RT = calculadoraPreco()

            DecisaoExibirTabela = "Deseja exibir os resultados?"
            resposta = decisao_sim_nao(DecisaoExibirTabela) 

            if resposta:
                gerarTabelaResultado(PV, CA, RB, OC, RT, CF, CV, IV) 
                gerarRentabilidade(RT, PV) 
            else:
                print("A função de exibição de resultados não será executada.")

        elif opc==4:
            print("Em breve")

        elif opc==5:
            excluirProduto()

        elif opc == 6:
            print("O programa encerrará em 10 segundos.")
            time.sleep(10)
            break  # Sai do loop e encerra o programa
        
        print()
        input("Aperte -Enter- para voltar ao início: ")
        #print("\033c", end='') apaga o código
        print()
        print("########################") # Melhor formatação do menu
        print("######## INÍCIO ########") # Melhor formatação do menu
        print("########################") # Melhor formatação do menu
        print()

menu()

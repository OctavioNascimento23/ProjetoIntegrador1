from tabulate import tabulate
import time
import mysql.connector
from Color_Console import *

# CONEXÃO COM O BANCO DE DADOS, JÁ MODULADA
db = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projeto"
)
print(db)

# TESTES COM BANCO DE DADOS
cursor = db.cursor()

def decisao_sim_nao(questao):
    while True:
        resposta = input(f"{questao} (S/N): ").strip().lower()
        if resposta in ["s", "n"]:
            return resposta == "s" # Enquanto aqui tiver "SIM" o loop será True
        else:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")

def visualizarProdutos():
    cursor.execute("SELECT `idProduto`, `nomeProduto`, `descProduto`, `precoVenda`, `custoAquisicao`, `impostoProduto`, `custoFixo`, `comissaoVendas`, `rentabilidadeProduto` FROM `produto`")  # Query (TEM QUE ESTAR DE ACORDO COM O BANCO DE DADOS)
    resultados = cursor.fetchall()  # Obtendo todos os resultados

    # Cabeçalho para tabela de visualização de produtinhos
    CabecalhoProdutos = ["ID", "Nome do Produto", "Descrição", "Preço de Venda", "Imposto sobre produto", "Custo de aquisição", "Custo fixo", "Comissão", "Rentabilidade"] # TEM QUE ESTAR DE ACORDO COM QUERY

    # Tabulando dados do BD
    print("\n\nTABELA DE PRODUTOS:")
    print()
    print(tabulate(resultados, headers=CabecalhoProdutos, tablefmt="grid"))

    cursor.execute("SELECT idProduto, nomeProduto, precoVenda, impostoProduto, custoAquisicao, custoFixo, comissaoVendas, rentabilidadeProduto FROM produto")
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

            print()
            print("========================================")
            print()

            # Informações do produto
            print(f"Produto: {nomeProduto}")
            print(f"ID do Produto: {idProduto}")

            # Gerar tabela de resultados
            gerarTabelaResultado(CA, CF, CV, IV, ML, PV, RB, OC, RT)

            # Gerar classificação de rentabilidade
            gerarRentabilidade(RT, PV)
    else: 
        print()


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

def gerarTabelaResultado(CA, CF, CV, IV, ML, PV, RB, OC, RT):

    tabelaResultados = [
        ["A. Preço de Venda",f"R${round(PV,2)}","100.0%"],
        ["B. Custo de aquisição",f"R${round(CA,2)}",f"{round(CA/PV*100,3)}"+"%"],
        ["C.  Receita Bruta",f"R${round(PV-CA,2)}",f"{round((PV-CA)/PV*100,3)}"+"%"],
        ["D. Custo Fixo/Administrativo",f"R${round(CF*PV/100,2)}",f"{round(CF,3)}"+"%"],
        ["E. Comissão de Vendas",f"R${round(CV*PV/100,2)}",f"{round(CV,3)}"+"%"],
        ["F. Impostos",f"R${round(IV*PV/100,2)}",f"{round(IV,3)}"+"%"],
        ["G. Outros Custos",f"R${round(OC,2)}",f"{round(OC/PV*100,3)}"+"%"],
        ["H. Rentabilidade",f"R${round(RT,2)}",f"{round(RT/PV*100,3)}"+"%"]]

    print("\n\nTABELA DE RESULTADOS:")
    print()
    print(tabulate(tabelaResultados, headers=["Descrição", "Porcentagem", "Valor"]))

def gerarRentabilidade(RT, PV):
    print("\n\nCLASSIFICAÇÃO DE RENTABILIDADE:")
    print()
    rentabilidade = (RT / PV) * 100
    
    if rentabilidade > 20:
        print(f"Rentabilidade alta, com uma porcentagem de lucro de {rentabilidade}%")
    elif 10 < rentabilidade <= 20:
        print(f"Rentabilidade média, com uma porcentagem de lucro de {rentabilidade}%")
    elif 0 < rentabilidade <= 10:
        print(f"Rentabilidade baixa, com uma porcentagem de lucro de {rentabilidade}%")
    elif rentabilidade == 0:
        print("Sem lucro")
    elif rentabilidade < 0:
        print(f"Prejuízo de {rentabilidade}%")
    
    print()
    
def adicionarProduto():

    cod=int(input("Digite o código do produto: "))
    nome=input("Digite o nome do produto: ")
    descricao=input("Digite a descrição do produto: ")
    PV=float(input("Digite o valor de preço de venda (R$): "))
    CA=float(input("Digite o custo de aquisição (R$): "))
    IV = float(input("Digite os impostos do produto (%): "))  # IMPOSTOS SOBRE PRODUTO
    CF = float(input("Digite o custo fixo do produto (%): "))  # CUSTO FIXO
    CV = float(input("Digite a comissão de vendas do produto (%): "))  # COMISSÃO DE VENDAS
    ML = float(input("Digite a margem de lucro do produto (%): "))  # MARGEM DE LUCRO

    query = "INSERT INTO produto (idProduto, nomeProduto, descProduto, precoVenda, custoAquisicao, impostoProduto,custoFixo, comissaoVendas, rentabilidadeProduto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (cod, nome, descricao,PV,CA,IV, CF, CV, ML)

    try:
        cursor.execute(query, values)
        db.commit()  # Confirmar a transação no banco de dados
        print()
        print("Produto adicionado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao adicionar o produto:", err)

def excluirProduto():
    DecisaoExibir = "Deseja exibir os produtos antes de excluir?"
    resposta = decisao_sim_nao(DecisaoExibir)

    if resposta:
        visualizarProdutos()
    cod = int(input("Digite o código do produto a ser excluído: "))

    cursor.execute("SELECT * FROM produto WHERE idProduto = %s", (cod,))
    produto = cursor.fetchone()

    if produto:
        idProduto, nomeProduto, descricaoProduto, custoAquisicao, impostoProduto, precoVenda, custoFixo, comissaoVendas, rentabilidadeProduto = produto

        print("\nProduto encontrado:")
        print(f"ID: {idProduto}")
        print(f"Nome: {nomeProduto}")
        print(f"Descrição: {descricaoProduto}")
        print(f"Preço: R${precoVenda}")
        print(f"Imposto: {impostoProduto}%")
        print(f"Custo: R${custoAquisicao}")
        print(f"Custo Fixo: {custoFixo}%")
        print(f"Comissão de Vendas: {comissaoVendas}%")
        print(f"Rentabilidade: {rentabilidadeProduto}%")
        
        DecisaoExcluirPrdouto = "\nDeseja excluir o produto?\n"
        resposta = decisao_sim_nao(DecisaoExcluirPrdouto)

        if resposta:
            cursor.execute("DELETE FROM produto WHERE idProduto = %s", (cod,))
            db.commit()
            print("Produto excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
    else:
        print("Produto não encontrado.")

    

def atualizarProduto():
    cod = int(input("Deseja modificar um produto com qual código? "))
    
    # Verifica se o produto com o código fornecido existe no banco de dados
    cursor.execute("SELECT * FROM produto WHERE idProduto = %s", (cod,)) #Seleciona o produto que possui o id digitado
    produto = cursor.fetchone()
    
    if produto:
        print("Produto encontrado:")
        print("Cod:", produto[0])
        print("Nome:", produto[1])
        print("Descrição:", produto[2])
        print("Preço:", produto[3])
        print("Impostos - IV ", produto[4])
        print("Custos - CA", produto[5])
        print("Custo Fixo - CF", produto[6])
        print("Comissão de Vendas - CV", produto[7])
        print("Margem de Lucro - ML", produto[8])
        print()


        print("Opções de modificação:")
        print("[1] Código")
        print("[2] Nome")
        print("[3] Descrição")
        print("[4] Preço")
        print("[5] Impostos/IV")
        print("[6] Custo/CA")
        print("[7] Custo Fixo/CF")
        print("[8] Comissão de Vendas/CV")
        print("[9] Margem de Lucro/ML")
        print()

        opcao = int(input("Escolha o número da opção que você gostaria de modificar: "))
        print()
        if opcao == 1:
            novo_cod = int(input("Digite o novo código do produto: "))
            print()
            cursor.execute("UPDATE produto SET idProduto = %s WHERE idProduto = %s", (novo_cod, cod))
            db.commit()
            print("Código do produto atualizado com sucesso!")
        elif opcao == 2:
            novo_nome = input("Digite o novo nome do produto: ")
            print()
            cursor.execute("UPDATE produto SET nomeProduto = %s WHERE idProduto = %s", (novo_nome, cod))
            db.commit()
            print("Nome do produto atualizado com sucesso!")
        elif opcao == 3:
            nova_descricao = input("Digite a nova descrição do produto: ")
            print()
            cursor.execute("UPDATE produto SET descProduto = %s WHERE idProduto = %s", (nova_descricao, cod))
            db.commit()
            print("Descrição do produto atualizada com sucesso!")
        elif opcao == 4:
            novo_preco = float(input("Digite o novo preço do produto: "))
            print()
            cursor.execute("UPDATE produto SET precoVenda = %s WHERE idProduto = %s", (novo_preco, cod))
            db.commit()
            print("Preço do produto atualizado com sucesso!")
        elif opcao == 5:
            novos_impostos = float(input("Digite os novos impostos do produto: "))
            print()
            cursor.execute("UPDATE produto SET impostoProduto = %s WHERE idProduto = %s", (novos_impostos, cod))
            db.commit()
            print("Impostos do produto atualizados com sucesso!")
        elif opcao == 6:
            novo_custo = float(input("Digite o novo custo do produto: "))
            print()
            cursor.execute("UPDATE produto SET custoAquisicao = %s WHERE idProduto = %s", (novo_custo, cod))
            db.commit()
            print("Custo do produto atualizado com sucesso!")
        elif opcao == 7:
            novo_custo_fixo = float(input("Digite o novo custo fixo do produto: "))
            print()
            cursor.execute("UPDATE produto SET custoFixo = %s WHERE idProduto = %s", (novo_custo_fixo, cod))
            db.commit()
            print("Custo fixo do produto atualizado com sucesso!")
        elif opcao == 8:
            nova_comissao_vendas = float(input("Digite a nova comissão de vendas do produto: "))
            print()
            cursor.execute("UPDATE produto SET comissaoVendas = %s WHERE idProduto = %s", (nova_comissao_vendas, cod))
            db.commit()
            print("Comissão de vendas do produto atualizada com sucesso!")
        elif opcao == 9:
            nova_margem_lucro = float(input("Digite a nova margem de lucro do produto: "))
            print()
            cursor.execute("UPDATE produto SET rentabilidadeProduto = %s WHERE idProduto = %s", (nova_margem_lucro, cod))
            db.commit()
            print("Margem de lucro do produto atualizada com sucesso!")
        else:
            print("Opção inválida.")
    else:
        print("Produto com código", cod, "não encontrado.")

def menu():
        while True: 
            print("MENU DO CONTROLE DE ESTOQUE")
            print()
            print("Selecione uma função para prosseguir:")
            print()

            tabelaFuncoes = [
            ["1. ", "Visualizar produtos"],
            ["2. ", "Adicionar produtos"],
            ["3. ","Atualizar produto"],
            ["4. ","Excluir produto"],
            ["5. ", "Calcular preços"],
            ["6. ","Sair"],  
            ]
            print(tabulate(tabelaFuncoes, headers=["Opção", "Descrição"]))
            print()

            opc = int(input("Selecione a opção a ser executada: "))
            print()
            if opc == 1:
                visualizarProdutos()
            elif opc == 2:
                adicionarProduto()
            elif opc == 3:
                atualizarProduto()
            elif opc == 4:
                excluirProduto()
            elif opc == 5:
                CA, CF, CV, IV, ML, PV, RB, OC, RT = calculadoraPreco()
                DecisaoExibirTabela = "Deseja exibir os resultados?"
                resposta = decisao_sim_nao(DecisaoExibirTabela) 

                if resposta:
                    gerarTabelaResultado(PV, CA, OC, RT, CF, CV, IV,ML,RB) 
                    gerarRentabilidade(RT, PV) 
                else:
                    print("A função de exibição de resultados não será executada.")

            elif opc == 6:
                DecisaoEncerrar = "Deseja realmente sair?"
                resposta = decisao_sim_nao(DecisaoEncerrar)
                if resposta:
                    print("O programa encerrará em 10 segundos.")
                    time.sleep(10)
                    break 
                else:
                    menu() 

        input("Aperte -Enter- para voltar ao início: ")
        #print("\033c", end='') apaga o código
        print()
        print("########################") # Melhor formatação do menu
        print("######## INÍCIO ########") # Melhor formatação do menu
        print("########################") # Melhor formatação do menu
        print()

menu()

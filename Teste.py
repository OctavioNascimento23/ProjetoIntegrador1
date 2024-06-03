from tabulate import tabulate
import mysql.connector
from colorama import init, Fore, Back
import sys

init()  # Iniciando o colorama

def connectBD():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            database="projeto"
        )
        cursor = db.cursor()
        print(Fore.LIGHTGREEN_EX + "\n\nConexão com o banco de dados estabelecida com sucesso.")
        return db, cursor
    except mysql.connector.Error as err:
        print(Fore.LIGHTRED_EX + f"Erro ao conectar ao banco de dados: {err}")
        sys.exit(1)

def closeBD(db, cursor):
    cursor.close()
    db.close()
    print(Fore.LIGHTGREEN_EX + "Conexão com o banco de dados fechada.")

db, cursor = connectBD()

def decisao_sim_nao(questao):  # Função para decisões de "Sim ou não"
    while True:
        resposta = input(Fore.RESET + f"{questao} (S/N): ").strip().lower()
        if resposta in ["s", "n"]:
            return resposta == "s" 
        else:
            print(Fore.LIGHTRED_EX + "Resposta inválida. Por favor, responda com 'S' ou 'N'.")

def visualizarProdutos():  # Função para visualização dos produtos
    try:
        cursor.execute("SELECT idProduto, nomeProduto, descProduto, precoVenda, custoAquisicao, impostoProduto, custoFixo, comissaoVendas, rentabilidadeProduto FROM produto")
        resultados = cursor.fetchall()

        CabecalhoProdutos = [Fore.RESET + "ID", "Nome do Produto", "Descrição", "Preço de Venda", "Custo de Aquisição", "Imposto sobre Produto", "Custo fixo", "Comissão", "Rentabilidade"]

        print(Fore.LIGHTCYAN_EX + "\nTabela de produtos:")
        print(Fore.RESET + tabulate(resultados, headers=CabecalhoProdutos, tablefmt="grid"))

        cursor.execute("SELECT idProduto, nomeProduto, precoVenda, impostoProduto, custoAquisicao, custoFixo, comissaoVendas, rentabilidadeProduto FROM produto")
        produtos = cursor.fetchall()

        DecisaoTabelaProduto = Fore.RESET + "Deseja exibir os cálculos para os produtos?"
        resposta = decisao_sim_nao(DecisaoTabelaProduto)
        if resposta:
            for produto in produtos:
                idProduto, nomeProduto, PV, IV, CA, CF, CV, ML = produto

                # Informações do produto
                print(Fore.LIGHTYELLOW_EX + "\n" + "="*40)
                print(Fore.LIGHTMAGENTA_EX + f"\nProduto: {nomeProduto}")
                print(Fore.LIGHTMAGENTA_EX + f"ID do Produto: {idProduto}\n")

                PV, RB, OC, RT = gerarTabelaResultado(idProduto, CA, CF, CV, IV, ML)  # Modificação aqui
                gerarRentabilidade(RT, PV)

            print()
    except mysql.connector.Error as err:
        print(Fore.LIGHTRED_EX + f"Erro ao consultar produtos: {err}\n")

def gerarTabelaResultado(idProduto, CA, CF, CV, IV, ML):
    PV = CA / (1 - (CF + CV + IV + ML) / 100)
    RB = PV - CA
    OC = PV * (CF + CV + IV) / 100
    RT = RB - OC
    
    tabelaResultados = [
        ["A. Preço de Venda", f"R${round(PV, 2)}", "100.0%"],
        ["B. Custo de aquisição", f"R${round(CA, 2)}", f"{round(CA/PV*100, 4)}%"],
        ["C. Receita Bruta", f"R${round(RB, 2)}", f"{round((RB)/PV*100, 4)}%"],
        ["D. Custo Fixo/Administrativo", f"R${round(OC, 2)}", f"{round(OC/PV*100, 4)}%"],
        ["E. Comissão de Vendas", f"R${round(CV*PV/100, 2)}", f"{round(CV, 4)}%"],
        ["F. Impostos", f"R${round(IV*PV/100, 2)}", f"{round(IV, 4)}%"],
        ["G. Outros Custos", f"R${round(OC, 2)}", f"{round(OC/PV*100, 4)}%"],
        ["H. Rentabilidade", f"R${round(RT, 2)}", f"{round(RT/PV*100, 4)}%"]
    ]

    print(Fore.LIGHTCYAN_EX + "\nTabela de resultados:")
    print(Fore.RESET + tabulate(tabelaResultados, headers=["Descrição", "Valor", "Porcentagem"]))

    return PV, RB, OC, RT

def gerarRentabilidade(RT, PV):  # Função para gerar tabela de rentabilidade dos produtos
    print(Fore.LIGHTCYAN_EX + "\nClassificação de rentabilidade:")
    rentabilidade = (RT / PV) * 100

    if rentabilidade > 20:
        print(Fore.LIGHTGREEN_EX + f"Rentabilidade alta, com uma porcentagem de lucro de {round(rentabilidade,2)}%")
    elif 10 < rentabilidade <= 20:
        print(Fore.LIGHTYELLOW_EX + f"Rentabilidade média, com uma porcentagem de lucro de {round(rentabilidade,2)}%")
    elif 0 < rentabilidade <= 10:
        print(Fore.LIGHTRED_EX + f"Rentabilidade baixa, com uma porcentagem de lucro de {round(rentabilidade,2)}%")
    elif rentabilidade == 0:
        print(Fore.LIGHTRED_EX + "Sem lucro")
    else:
        print(Fore.LIGHTRED_EX + f"Prejuízo de {round(rentabilidade,2)}%\n")

def adicionarProduto():  # Função para adição dos produtos no banco de dados
    try:
        cod = int(input(Fore.RESET + "\nDigite o código do produto: "))
        nome = input("Digite o nome do produto: ")
        descricao = input("Digite a descrição do produto: ")
        CA = float(input("Digite o custo de aquisição (R$): "))
        IV = float(input("Digite os impostos do produto (%): "))
        CF = float(input("Digite o custo fixo do produto (%): "))
        CV = float(input("Digite a comissão de vendas do produto (%): "))
        ML = float(input("Digite a margem de lucro do produto (%): "))

        PV = CA / (1 - (CF + CV + IV + ML) / 100)

        query = "INSERT INTO produto (idProduto, nomeProduto, descProduto, precoVenda, custoAquisicao, impostoProduto, custoFixo, comissaoVendas, rentabilidadeProduto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (cod, nome, descricao, PV, CA, IV, CF, CV, ML)

        cursor.execute(query, values)
        db.commit()
        print(Fore.LIGHTGREEN_EX + "\nProduto adicionado com sucesso!\n")
    except mysql.connector.Error as err:
        print(Fore.LIGHTRED_EX + f"Erro ao adicionar o produto: {err}")
    except ValueError:
        print(Fore.LIGHTRED_EX + "Entrada inválida. Por favor, insira valores corretos.")

def excluirProduto():  # Função para exclusão dos produtos no banco de dados
    resposta = decisao_sim_nao(Fore.RESET + "\nDeseja exibir os produtos antes de excluir?")
    if resposta:
        visualizarProdutos()

    try:
        cod = int(input("\nDigite o código do produto a ser excluído: "))
        cursor.execute("SELECT idProduto, nomeProduto, descProduto, precoVenda, impostoProduto, custoAquisicao, custoFixo, comissaoVendas, rentabilidadeProduto FROM produto WHERE idProduto = %s", (cod,))
        produto = cursor.fetchone()

        if produto:
            idProduto, nomeProduto, descProduto, precoVenda, impostoProduto, custoAquisicao, custoFixo, comissaoVendas, rentabilidadeProduto = produto

            print(Fore.LIGHTGREEN_EX + "\nProduto encontrado:")
            print(Fore.LIGHTMAGENTA_EX + f"ID: {idProduto}")
            print(Fore.RESET + f"Nome: {nomeProduto}")
            print(f"Descrição: {descProduto}")
            print(f"Preço: R${precoVenda}")
            print(f"Imposto: {impostoProduto}%")
            print(f"Custo: R${custoAquisicao}")
            print(f"Custo Fixo: {custoFixo}%")
            print(f"Comissão de Vendas: {comissaoVendas}%")
            print(f"Rentabilidade: {rentabilidadeProduto}%")

            resposta = decisao_sim_nao("\nDeseja excluir o produto?")
            if resposta:
                cursor.execute("DELETE FROM produto WHERE idProduto = %s", (cod,))
                db.commit()
                print(Fore.LIGHTGREEN_EX + "Produto excluído com sucesso!")
            else:
                print(Fore.RESET + "Exclusão cancelada.")
        else:
            print(Fore.LIGHTRED_EX + "Produto não encontrado.")
    except mysql.connector.Error as err:
        print(Fore.LIGHTRED_EX + f"Erro ao excluir o produto: {err}")
    except ValueError:
        print(Fore.LIGHTRED_EX + "Código inválido. Por favor, insira um código numérico.")

def atualizarProduto():  # Função para atualização dos produtos no banco de dados
    try:
        visualizarProdutos()
        cod = int(input(Fore.RESET + "\nDeseja modificar um produto com qual código? "))
        
        cursor.execute("SELECT idProduto, nomeProduto, descProduto, precoVenda, custoAquisicao, impostoProduto, custoFixo, comissaoVendas, rentabilidadeProduto FROM produto WHERE idProduto = %s", (cod,))
        produto = cursor.fetchone()

        if produto:
            idProduto, nomeProduto, descProduto, precoVenda, custoAquisicao, impostoProduto, custoFixo, comissaoVendas, rentabilidadeProduto = produto

            print(Fore.LIGHTGREEN_EX + "\nProduto encontrado:")
            print(Fore.LIGHTMAGENTA_EX + f"ID: {idProduto}")
            print(Fore.RESET + f"Nome: {nomeProduto}")
            print(f"Descrição: {descProduto}")
            print(f"Preço: R${precoVenda}")
            print(f"Custo: R${custoAquisicao}")
            print(f"Imposto: {impostoProduto}%")
            print(f"Custo Fixo: {custoFixo}%")
            print(f"Comissão de Vendas: {comissaoVendas}%")
            print(f"Rentabilidade: {rentabilidadeProduto}%")

            nome = input("Digite o novo nome do produto (deixe em branco para não alterar): ") or nomeProduto
            descricao = input("Digite a nova descrição do produto (deixe em branco para não alterar): ") or descProduto
            CA = input(f"Digite o novo custo de aquisição (R$) (atual: {custoAquisicao}): ")
            IV = input(f"Digite os novos impostos do produto (%) (atual: {impostoProduto}): ")
            CF = input(f"Digite o novo custo fixo do produto (%) (atual: {custoFixo}): ")
            CV = input(f"Digite a nova comissão de vendas do produto (%) (atual: {comissaoVendas}): ")
            ML = input(f"Digite a nova margem de lucro do produto (%) (atual: {rentabilidadeProduto}): ")

            CA = float(CA) if CA else custoAquisicao
            IV = float(IV) if IV else impostoProduto
            CF = float(CF) if CF else custoFixo
            CV = float(CV) if CV else comissaoVendas
            ML = float(ML) if ML else rentabilidadeProduto

            PV = CA / (1 - (CF + CV + IV + ML) / 100) # Recalculando o preço de venda

            query = "UPDATE produto SET nomeProduto = %s, descProduto = %s, precoVenda = %s, custoAquisicao = %s, impostoProduto = %s, custoFixo = %s, comissaoVendas = %s, rentabilidadeProduto = %s WHERE idProduto = %s"
            values = (nome, descricao, PV, CA, IV, CF, CV, ML, cod)

            cursor.execute(query, values)
            db.commit()
            print(Fore.LIGHTGREEN_EX + "Produto atualizado com sucesso!")
        else:
            print(Fore.LIGHTRED_EX + "Produto não encontrado.")
    except mysql.connector.Error as err:
        print(Fore.LIGHTRED_EX + f"Erro ao atualizar o produto: {err}")
    except ValueError:
        print(Fore.LIGHTRED_EX + "Entrada inválida. Por favor, insira valores numéricos.")

def menu():  # Função responsável pela navegação do app
    while True:
        input(Fore.RESET + "\n\nAperte -Enter- para continuar: ")
        print("\033c", end='')  # Apaga o código acima
        print()
        print("########################")  # Melhor formatação do menu
        print("######## INÍCIO ########")  # Melhor formatação do menu
        print("########################")  # Melhor formatação do menu
        print()
        print(Fore.LIGHTCYAN_EX + "MENU DO CONTROLE DE ESTOQUE")
        print(Fore.LIGHTYELLOW_EX + "", "="*40)
        print(Fore.RESET + "Escolha uma das seguintes opções:")
        print("1 - Visualizar todos os produtos")
        print("2 - Adicionar um novo produto")
        print("3 - Excluir um produto")
        print("4 - Atualizar um produto")
        print("5 - Sair")
        print(Fore.LIGHTYELLOW_EX + "="*40)

        try:
            opcao = int(input(Fore.RESET + "Digite o número da opção desejada: "))
            if opcao == 1:
                visualizarProdutos()
            elif opcao == 2:
                adicionarProduto()
            elif opcao == 3:
                excluirProduto()
            elif opcao == 4:
                atualizarProduto()
            elif opcao == 5:
                print("Saindo do programa...")
                closeBD(db, cursor)  # Fecha a conexão com o banco de dados
                break
            else:
                print(Fore.LIGHTRED_EX + "Opção inválida. Tente novamente.")
        except ValueError:
            print(Fore.LIGHTRED_EX + "Entrada inválida. Por favor, digite um número.")
        except Exception as e:
            print(Fore.LIGHTRED_EX + f"Ocorreu um erro inesperado: {e}")

menu()
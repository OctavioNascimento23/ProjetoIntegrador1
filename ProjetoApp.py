# executar no terminal: pip install tabulate

from tabulate import tabulate
import time # Biblioteca ainda não usada

CP = float(input("Digite o custo do produto: ")) # CUSTO PRODUTO
CF = float(input("Digite o custo fixo do produto: ")) # CUSTO FIXO
CV = float(input("Digite a comissão de vendas do produto: ")) # COMISSÃO DE VENDAS
IV = float(input("Digite os impostos do produto: ")) # IMPOSTOS SOBRE PRODUTO
ML = float(input("Digite a margem de lucro do produto: ")) # MARGEM DE LUCRO
PV = CP / (1 - (CF + CV + IV + ML) / 100) # PREÇO DE VENDA
RB = PV-CP # RECEITA BRUTA
OC = PV*(CF+CV+IV)/100 # OUTROS CUSTOS (CF + CV + IV)
RT = RB-OC # RENTABILIDADE

tabelaResultados = [["Descrição","Valor","%"],
          ["A. Preço de Venda",f"R${round(PV,2)}","100.0%"],
          ["B. Custo de aquisição",f"R${round(CP,2)}",f"{round(CP/PV*100,3)}"+"%"],
          ["C. Receita Bruta",f"R${round(PV-CP,2)}",f"{round((PV-CP)/PV*100,3)}"+"%"],
          ["D. Custo Fixo/Administrativo",f"R${round(CF*PV/100,2)}",f"{round(CF,3)}"+"%"],
          ["E. Comissão de Vendas",f"R${round(CV*PV/100,2)}",f"{round(CV,3)}"+"%"],
          ["F. Impostos",f"R${round(IV*PV/100,2)}",f"{round(IV,3)}"+"%"],
          ["G. Outros Custos",f"R${round(OC,2)}",f"{round(OC/PV*100,3)}"+"%"],
          ["H. Rentabilidade",f"R${round(RT,2)}",f"{round(RT/PV*100,3)}"+"%"]]

print("\n\n TABELA DE RESULTADOS: \n")
print(tabulate(tabelaResultados))
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
print("O programa irá encerrar em 10 segundos.")
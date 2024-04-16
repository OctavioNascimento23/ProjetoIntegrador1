# executar no terminal: pip install tabulate

from tabulate import tabulate
import time

CP = 36.0 # CUSTO PRODUTO
CF = 15.0 # CUSTO FIXO / ADMINISTRATIVO
CV = 5.0 # COMISSÃO DE VENDAS
IV = 12.0 # IMPOSTO SOBRE VENDA
ML = 20.0 # MARGEM DE LUCRO
PV = CP / (1 - (CF + CV + IV + ML) / 100) # PREÇO DE VENDA
RB = PV-CP # RECEITA BRUTA
OC = PV*(CF+CV+IV)/100 # OUTROS CUSTOS (CF + CV + IV)
RT = RB-OC # RENTABILIDADE

tabelaResultados = [["Descrição","Valor","%"],
          ["Preço de Venda",PV,"100.0%"],
          ["Custo de aquisição",CP,f"{(CP/PV)*100}"+"%"],
          ["Receita Bruta",PV-CP,f"{((PV-CP)/PV)*100}"+"%"],
          ["Custo Fixo/Administrativo",(CF*PV)/100,f"{CF}"+"%"],
          ["Comissão de Vendas",(CV*PV)/100,f"{CV}"+"%"],
          ["Impostos",(IV*PV)/100,f"{IV}"+"%"],
          ["Outros Custos",OC,f"{(OC/PV)*100}"+"%"],
          ["Rentabilidade",RT,f"{(RT/PV)*100}"+"%"]]

print("\n\n TABELA DE RESULTADOS: \n")
print(tabulate(tabelaResultados))
print("\n\n CLASSIFICAÇÃO DE RENTABILIDADE: \n")
if ((RT/PV)*100)>20:
    print(f"Seu produto possui uma rentabilidade alta, a porcentagem de lucro será de {((RT/PV)*100)}"+"%")
elif ((RT/PV)*100)<=20>10:
    print(f"Seu produto possui uma rentabilidade média, a porcentagem de lucro será de {((RT/PV)*100)}"+"%")
elif ((RT/PV)*100)<=10>0:
    print(f"Seu produto possui uma rentabilidade baixa, a porcentagem de lucro será de {((RT/PV)*100)}"+"%")
elif ((RT/PV)*100)==0:
    print(f"Seu produto não irá gerar lucro")
elif ((RT/PV)*100)==0:
    print(f"Seu produto acarretará em prejuízos de {((RT/PV)*100)}"+"%")
else:
    print("ERRO, TENTE NOVAMENTE!")
print()
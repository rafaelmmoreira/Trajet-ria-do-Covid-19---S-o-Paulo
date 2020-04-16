import csv
import matplotlib.pyplot as plt
import requests
import os

def salvaCSV(texto, data):
    nome = 'Dados-covid-19-estado-{}.csv'.format(ultimadata)
    arq = open(nome, 'w')
    arq.write(texto.replace('\r', ''))
    arq.close()
    print('Dados salvos em', os.getcwd() + '\\' + nome)

planilha = requests.get('http://www.seade.gov.br/wp-content/uploads/2020/04/Dados-covid-19-estado.csv', verify=False)

if planilha.status_code == 200:
    totais = []
    novos = []
    datas = []
    
    leitor = csv.reader(planilha.text.splitlines(), delimiter=';', lineterminator='\n')
    primeiro = True
    for linha in leitor:
        if not primeiro and linha[0] != '':
            datas.append(linha[0])
            totais.append(int(linha[1]))
            novos.append(int(linha[2]))
        else:
            primeiro = False

    while (len(totais)) % 7 != 0:
        totais.insert(0, 0)
        novos.insert(0, 0)
        datas.insert(0, '')
    totais.insert(0, 0)
    novos.insert(0, 0)
    datas.insert(0, '')

    totaissem = []
    novossem = []
    ultimadata = ''
    n = 0
    
    for i in range(len(totais)):
        if i % 7 == 0:
            ultimadata = datas[i]
            totaissem.append(totais[i])
            novossem.append(n)
            n = 0
        n += novos[i]

    plt.plot(totaissem, novossem, 'ro')
    plt.xlabel('Total de casos confirmados (até {})'.format(ultimadata))
    plt.ylabel('Total de novos casos (por semana)')
    plt.title('Trajetória dos casos de COVID-19 no Estado de São Paulo')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True)
    plt.show()
    salvar = input('Deseja salvar planilha? S/N: ')
    if salvar[0].upper() == 'S':
        salvaCSV(planilha.text, ultimadata)
    
else:
    print('Erro:', planilha.status_code)
        

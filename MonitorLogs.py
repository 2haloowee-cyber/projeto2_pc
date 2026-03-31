import random
import datetime

def menu():
    nome_arq = 'log.txt'
    while True:
        print('Monitor Logpy')
        print('1 - Gerar Logs')
        print('2 - Analisar Logs')
        print('3 - Gerar e Analisar Logs')
        print('4 - Sair')
        opcao = input('Escolha uma opção: ')
        if opcao == '1':
            try:
                qtd = int(input('Quantidade de Logs'))
                gerarArquivo(nome_arq, qtd)
            except:
                print('Qtd incorreta')
        elif opcao == '2':
            analisarLog(nome_arq)
        elif opcao == '3':
            try:
                qtd = int(input('Qualidade Logs'))
                gerarArquivo(nome_arq, qtd)
                analisarLog(nome_arq)
            except:
                print('Qtd Incorreta')
        elif opcao == '4':
            print('Até mas')
            break
        else:
            print('opcao errada')

def gerarArquivo(nome_arq, qtd):
    with open(nome_arq, 'w', encoding='UTF-8') as arq:
              for i in range(qtd):
                arq.white(montarLog(i) + '\n')
                print('Logs gerados')
            
def montarLog(i):
    data = gerarDataHora(i)
    ip = gerarIp(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i)
    tempo = gerarTempo(i)
    agente = gerarAgente(i)
    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - 500mb - HTTP/1.1 -{agente} - /home'

def gerarDataHora(i):
    base = datetime.datetime(2026, 3, 30, 22,8,0)
    data = datetime.timedelta(seconds=i * random.randint(5,20))
    return (base + data.strftime('%d/%m/%Y %H:%M:%S'))

def gerarIP(i):
    r = random.randint(1, 6)
    
    if i >= 20 and i <= 30:
        return '200.0.111.345'
    
    if r == 1:
        return '192.168.5.6'
    elif r == 2:
       return '192.168.5.7'  
    elif r == 3:
       return '192.168.5.8'
    elif r == 4:
       return '192.168.5.9' 
    elif r == 5:
       return '193.169.3.2' 
    elif r == 6:
       return '182.173.2.1' 
    else:
       return '192.558.39.76'
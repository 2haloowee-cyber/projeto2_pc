import random
import datetime

# ================= MENU =================
def menu():
    nome_arq = 'log.txt'

    while True:
        print('\n=== MONITOR LOGPY ===')
        print('1 - Gerar Logs')
        print('2 - Analisar Logs')
        print('3 - Gerar e Analisar')
        print('4 - Sair')

        opcao = input('Escolha: ')

        if opcao == '1':
            qtd = input('Quantidade: ')
            if qtd.isdigit():
                gerar_arquivo_logs(nome_arq, int(qtd))
            else:
                print('Valor inválido')

        elif opcao == '2':
            analisar_arquivo_logs(nome_arq)

        elif opcao == '3':
            qtd = input('Quantidade: ')
            if qtd.isdigit():
                gerar_arquivo_logs(nome_arq, int(qtd))
                analisar_arquivo_logs(nome_arq)
            else:
                print('Valor inválido')

        elif opcao == '4':
            print('Encerrando...')
            break

        else:
            print('Opção inválida')

# ================= GERAÇÃO =================
def gerar_arquivo_logs(nome_arquivo, quantidade):
    with open(nome_arquivo, 'w', encoding='utf-8') as arq:
        for i in range(quantidade):
            arq.write(montarLog(i) + '\n')
    print('Logs gerados com sucesso')

def montarLog(i):
    data = gerarDataHora(i)
    ip = gerarIP(i)
    recurso = gerarRecurso(i)
    metodo = gerarMetodo(i)
    status = gerarStatus(i, metodo)
    tempo = gerarTempo(i, status)
    tamanho = gerarTamanho(status)
    protocolo = gerarProtocolo(i)
    agente = gerarAgente(i)
    referer = gerarReferer(recurso)

    return f'[{data}] {ip} - {metodo} - {status} - {recurso} - {tempo}ms - {tamanho}B - {protocolo} - {agente} - {referer}'

def gerarDataHora(i):
    base = datetime.datetime(2026, 3, 30, 22, 8, 0)
    data = datetime.timedelta(seconds=i * random.randint(5, 20))
    return (base + data).strftime('%d/%m/%Y %H:%M:%S')

def gerarIP(i):
    r = random.randint(1, 6)

    if 20 <= i <= 30:
        return '200.0.111.245'

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
    else:
        return '182.173.2.1'

def gerarMetodo(i):
    if i % 5 == 0:
        return 'POST'
    return 'GET'

def gerarRecurso(i):
    if 15 <= i <= 18:
        return '/admin'
    elif 40 <= i <= 45:
        return '/login'
    elif i % 7 == 0:
        return '/produtos'
    elif i % 9 == 0:
        return '/carrinho'
    else:
        return '/home'

def gerarStatus(i, metodo):
    if 15 <= i <= 18:
        return 403
    if 40 <= i <= 45:
        return 403
    if 60 <= i <= 65:
        return 500
    if i % 10 == 0:
        return 404
    return 200

def gerarTempo(i, status):
    if 70 <= i <= 75:
        return 200 + (i * 50)
    if status == 500:
        return random.randint(800, 1500)
    if status == 403:
        return random.randint(300, 900)
    return random.randint(50, 400)

def gerarTamanho(status):
    if status == 500:
        return random.randint(100, 300)
    return random.randint(400, 2000)

def gerarProtocolo(i):
    if i % 3 == 0:
        return 'HTTP/1.0'
    elif i % 3 == 1:
        return 'HTTP/1.1'
    else:
        return 'HTTP/2'

def gerarAgente(i):
    if 50 <= i <= 55:
        return 'GoogleBot'

    if i % 4 == 0:
        return 'Chrome'
    elif i % 4 == 1:
        return 'Firefox'
    elif i % 4 == 2:
        return 'Edge'
    else:
        return 'Safari'

def gerarReferer(recurso):
    if recurso == '/login':
        return '/home'
    elif recurso == '/admin':
        return '/login'
    elif recurso == '/carrinho':
        return '/produtos'
    else:
        return '/home'

# ================= AUXILIARES =================
def limpar_espacos(texto):
    return texto.strip()

def classificar_tempo(tempo):
    if tempo < 200:
        return 0
    elif tempo < 800:
        return 1
    else:
        return 2

def extrair_campos_linha(linha):
    i = 0
    campo = ""
    contador = 0

    data_hora = ""
    ip = ""
    metodo = ""
    status = ""
    recurso = ""
    tempo = ""
    tamanho = ""
    protocolo = ""
    user_agent = ""
    referer = ""

    while i < len(linha):
        if linha[i] == '[':
            i += 1
            while linha[i] != ']':
                data_hora += linha[i]
                i += 1

        elif linha[i] == ' ' and linha[i+1] == '-':
            contador += 1
            i += 3
            campo = ""

            while i < len(linha) and linha[i] != '-':
                campo += linha[i]
                i += 1

            campo = campo.strip()

            if contador == 1:
                metodo = campo
            elif contador == 2:
                status = campo
            elif contador == 3:
                recurso = campo
            elif contador == 4:
                tempo = campo.replace("ms", "")
            elif contador == 5:
                tamanho = campo.replace("B", "")
            elif contador == 6:
                protocolo = campo
            elif contador == 7:
                user_agent = campo

        i += 1

    inicio_ip = linha.find(']') + 2
    fim_ip = linha.find(' -')
    ip = linha[inicio_ip:fim_ip]

    ultimo_traco = linha.rfind('-')
    referer = linha[ultimo_traco + 1:].strip()

    return data_hora, ip, metodo, status, recurso, tempo, tamanho, protocolo, user_agent, referer

# ================= ANÁLISE =================
def analisar_arquivo_logs(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:

        total_acessos = 0
        total_sucessos = 0
        total_erros = 0
        total_500 = 0

        soma_tempo = 0
        maior_tempo = 0
        menor_tempo = float('inf')

        rapidos = 0
        normais = 0
        lentos = 0

        status_200 = 0
        status_403 = 0
        status_404 = 0
        status_500 = 0

        acessos_admin_indevidos = 0
        eventos_forca_bruta = 0
        ultimo_ip_forca_bruta = ""

        eventos_degradacao = 0
        eventos_falha_critica = 0

        suspeitas_bot = 0
        ultimo_ip_bot = ""

        acessos_rotas_sensiveis = 0
        falhas_rotas_sensiveis = 0

        ip_anterior = ""
        contador_ip = 0

        contador_403_login = 0
        ip_forca_bruta_atual = ""

        contador_500_seq = 0

        tempo_anterior = -1
        contador_aumento = 0

        ip_controle = ""
        ip_controle_qtd = 0
        ip_mais_ativo = ""
        ip_mais_qtd = 0

        ip_erro_controle = ""
        ip_erro_qtd = 0
        ip_mais_erro = ""
        ip_mais_erro_qtd = 0

        while True:
            linha = arquivo.readline()
            if linha == "":
                break

            linha = limpar_espacos(linha)
            if linha == "":
                continue

            total_acessos += 1

            (data_hora, ip, metodo, status, recurso,
             tempo, tamanho, protocolo, user_agent, referer) = extrair_campos_linha(linha)

            tempo = int(tempo)
            status = int(status)

            if status == 200:
                total_sucessos += 1
                status_200 += 1
            else:
                total_erros += 1
                if status == 403:
                    status_403 += 1
                elif status == 404:
                    status_404 += 1
                elif status == 500:
                    status_500 += 1
                    total_500 += 1

            soma_tempo += tempo

            if tempo > maior_tempo:
                maior_tempo = tempo
            if tempo < menor_tempo:
                menor_tempo = tempo

            tipo = classificar_tempo(tempo)
            if tipo == 0:
                rapidos += 1
            elif tipo == 1:
                normais += 1
            else:
                lentos += 1

            if recurso == '/admin' and status != 200:
                acessos_admin_indevidos += 1

            if recurso == '/login' and status == 403:
                if ip == ip_forca_bruta_atual:
                    contador_403_login += 1
                else:
                    contador_403_login = 1
                    ip_forca_bruta_atual = ip

                if contador_403_login == 3:
                    eventos_forca_bruta += 1
                    ultimo_ip_forca_bruta = ip
            else:
                contador_403_login = 0

            if status == 500:
                contador_500_seq += 1
                if contador_500_seq == 3:
                    eventos_falha_critica += 1
            else:
                contador_500_seq = 0

            if tempo_anterior != -1 and tempo > tempo_anterior:
                contador_aumento += 1
                if contador_aumento == 3:
                    eventos_degradacao += 1
            else:
                contador_aumento = 0

            tempo_anterior = tempo

            if ip == ip_anterior:
                contador_ip += 1
            else:
                contador_ip = 1
                ip_anterior = ip

            if contador_ip == 5:
                suspeitas_bot += 1
                ultimo_ip_bot = ip

            if ("Bot" in user_agent):
                suspeitas_bot += 1
                ultimo_ip_bot = ip

            if recurso == '/admin' or recurso == '/backup' or recurso == '/config' or recurso == '/private':
                acessos_rotas_sensiveis += 1
                if status != 200:
                    falhas_rotas_sensiveis += 1

            if ip == ip_controle:
                ip_controle_qtd += 1
            else:
                if ip_controle_qtd > ip_mais_qtd:
                    ip_mais_qtd = ip_controle_qtd
                    ip_mais_ativo = ip_controle
                ip_controle = ip
                ip_controle_qtd = 1

            if status != 200:
                if ip == ip_erro_controle:
                    ip_erro_qtd += 1
                else:
                    if ip_erro_qtd > ip_mais_erro_qtd:
                        ip_mais_erro_qtd = ip_erro_qtd
                        ip_mais_erro = ip_erro_controle
                    ip_erro_controle = ip
                    ip_erro_qtd = 1

        if ip_controle_qtd > ip_mais_qtd:
            ip_mais_ativo = ip_controle

        if ip_erro_qtd > ip_mais_erro_qtd:
            ip_mais_erro = ip_erro_controle

        disponibilidade = (total_sucessos / total_acessos) * 100 if total_acessos > 0 else 0
        taxa_erro = (total_erros / total_acessos) * 100 if total_acessos > 0 else 0
        tempo_medio = soma_tempo / total_acessos if total_acessos > 0 else 0

        estado = 'SAUDÁVEL'

        if eventos_falha_critica > 0 or disponibilidade < 70:
            estado = 'CRÍTICO'
        elif disponibilidade < 85 or lentos > rapidos:
            estado = 'INSTÁVEL'
        elif disponibilidade < 95 or suspeitas_bot > 0:
            estado = 'ATENÇÃO'

        print("\n===== RELATÓRIO FINAL =====")
        print("Total acessos:", total_acessos)
        print("Sucessos:", total_sucessos)
        print("Erros:", total_erros)
        print("Erros críticos:", total_500)
        print("Disponibilidade:", disponibilidade)
        print("Taxa erro:", taxa_erro)
        print("Tempo médio:", tempo_medio)
        print("Maior tempo:", maior_tempo)
        print("Menor tempo:", menor_tempo)
        print("Rápidos:", rapidos)
        print("Normais:", normais)
        print("Lentos:", lentos)
        print("Status 200:", status_200)
        print("Status 403:", status_403)
        print("Status 404:", status_404)
        print("Status 500:", status_500)
        print("IP mais ativo:", ip_mais_ativo)
        print("IP com mais erros:", ip_mais_erro)
        print("Força bruta:", eventos_forca_bruta)
        print("Último IP força bruta:", ultimo_ip_forca_bruta)
        print("Acessos indevidos /admin:", acessos_admin_indevidos)
        print("Degradação:", eventos_degradacao)
        print("Falhas críticas:", eventos_falha_critica)
        print("Suspeitas de bot:", suspeitas_bot)
        print("Último IP bot:", ultimo_ip_bot)
        print("Rotas sensíveis:", acessos_rotas_sensiveis)
        print("Falhas rotas sensíveis:", falhas_rotas_sensiveis)
        print("Estado final:", estado)

        return estado
    
menu()
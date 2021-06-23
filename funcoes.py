import sqlite3
from tabulate import tabulate
import menu
import app_aux
from datetime import datetime

verm = "\033[1;31m"
red = "\033[1;32;40m"  # <--- cor vermelho
reset_color = "\033[0;0m"  # <--- cor preto
blue = "\033[1;34m"

data = datetime.now()
data_hora = data.strftime("%d/%m/%y %H:%M")


def criar_conta_corrente():
    app_aux.titulo('    GERAR CONTA-CORRENTE   ')
    global data_hora, valor_deposito, id_cliente, value
    transacao = 'dep_inicial'
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    sql = c.execute('''SELECT cl.id, cl.nome, cl.cidade
                    FROM cliente cl
                    LEFT JOIN conta co ON co.cod_cliente = cl.id
                    WHERE co.cod_cliente is NULL''')
    consulta = sql.fetchall()
    print('  CLIENTES SEM CONTA CORRENTE ')
    head = [col[0] for col in sql.description]
    print(tabulate(consulta, headers=head, tablefmt="grid"))
    #################################################
    # verifica o ID correto, digitar entra em um loop
    #################################################
    for id_cliente in consulta:
        value = {id_cliente[0]}

    id_ = int(input(blue + 'INFORME O ID DO CLIENTE: ' + reset_color))
    if id_ not in value:
        print(verm + 'CLIENTE NÃO LOCALIZADO, INFORME O ID DO CLIENTE: ' + reset_color)
    else:
        valor_dep = float(input(blue + 'INFORME O VALOR DO DEPOSITO: '))  # valor_deposito

    app_aux.insert_deposito(id_cliente, valor_dep, data_hora, transacao)
    print(f'Conta-Corrente criada com sucesso para o cliente {app_aux.qry_cliente_saldo(id_cliente)[0]}\n '
          f'Valor depositado R${valor_deposito}')


def novo_cliente():
    app_aux.titulo('     CADASTRO DE CLIENTE     ')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    nome = input('NOME DO CLIENTE__: ').upper()
    cidade = input('CIDADE___________: ').upper()
    telefone = input('TELEFONE_________: ').upper()
    c.execute('''INSERT INTO cliente (nome, cidade, telefone)
                 VALUES(?, ?, ?)''', (nome, cidade, telefone))
    conn.commit()
    print('{} Cadastrado com Sucesso'.format(nome))
    conn.close()
    print('')
    input("Pressione ENTER para Continuar.")
    menu.monta_menu(menu.menu_principal)


def consulta_todos_clientes():
    app_aux.titulo('    CONSULTA TODOS CLIENTES   ')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    sql = c.execute('''SELECT * FROM cliente''')
    consulta = sql.fetchall()
    if consulta:
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        print('Quantidade de Clientes: {}'.format(len(consulta)))
        print('')
        conn.close()
        input("Pressione ENTER para Continuar.")
        menu.monta_menu(menu.menu_principal)
    else:
        print('Nenhum cliente encontrado')
        conn.close()


def consulta_cliente_id():
    app_aux.titulo('   CONSULTA CLIENTE: ID    ')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    id = int(input('Informe o numero do ID_Cliente: '))
    print('')
    sql = c.execute('''SELECT id, nome, cidade, telefone FROM cliente WHERE id=?''', (id,))
    consulta = sql.fetchall()
    if consulta:
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        input('Pressione ENTER para Continuar')
        menu.monta_menu(menu.menu_principal)
    else:
        print(f'ID numero {id} não localizado.')
        print('')
        consulta_cliente_id()
        print('')
    conn.close()


def consulta_cliente_nome():
    app_aux.titulo('  CONSULTA CLIENTE: NOME   ')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    nome = input('Informe o nome do cliente: ')
    sql = c.execute("SELECT * FROM cliente WHERE nome LIKE '%'||?||'%'", (nome,))
    print('')
    consulta = sql.fetchall()
    if consulta:
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        input('Pressione ENTER para Continuar')
        menu.monta_menu(menu.menu_principal)
    else:
        print(f'Cliente {nome} não localizado(a).')
        print('')
        consulta_cliente_nome()
        print('')

    conn.close()


def consulta_cliente_cidade():
    app_aux.titulo(' CONSULTA CLIENTE: CIDADE  ')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    cidade = input('Informe a Cidade do Cliente: ')
    sql = c.execute("SELECT * FROM cliente WHERE cidade LIKE '%'||?||'%'", (cidade,))
    consulta = sql.fetchall()
    if cidade:
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        conn.close()
        input('Pressione ENTER para Continuar')
        menu.monta_menu(menu.menu_principal)
    else:
        print(f' Cidade {cidade} não foi localizado.')
        print('')
        conn.close()


def transDeposito():
    app_aux.titulo('         DEPOSITO        ')
    global data_hora
    transacao = 'deposito'
    print('')
    id_1 = int(input('Sua Identificação: Informe o seu ID: '))
    valor_deposito = float(input(f'Seja bem vindo(a): {app_aux.qry_cliente_saldo(id_1)[0]}\n '
                                 f'     Saldo Atual: R${app_aux.qry_cliente_saldo(id_1)[1]}\n'
                                 f'Valor do Depósito: R$ '))
    app_aux.insert_deposito(id_1, valor_deposito, data_hora, transacao)
    input('Pressione ENTER para Continuar')
    print('')
    print(f'* {app_aux.qry_cliente_saldo(id_1)[0]} Depósito realizado com sucesso!'
          f' saldo atual: R${app_aux.qry_cliente_saldo(id_1)[1]}')
    menu.monta_menu(menu.menu_principal)


def transSaque():
    app_aux.titulo('         SAQUE          ')
    global data_hora
    transacao = 'saque'
    print('')
    id_1 = int(input('Sua Identificação: Informe o seu ID: '))
    valor_saque = float(input(f'Seja bem vindo(a): {app_aux.qry_cliente_saldo(id_1)[0]}\n '
                              f'     Saldo Atual: R${app_aux.qry_cliente_saldo(id_1)[1]}\n'
                              f'   Valor do Saque: R$ '))
    if valor_saque > app_aux.qry_cliente_saldo(id_1)[1]:
        print(f'O saldo atual é de R${app_aux.qry_cliente_saldo(id_1)[1]}, '
              f'não há limite disponivel para o saque de R${valor_saque}')
        input('PRESSIONE ENTER: ')
        transSaque()
    else:
        app_aux.insert_saque(id_1, valor_saque, data_hora, transacao)
        input('Pressione ENTER para Continuar')
        print(f'{app_aux.qry_cliente_saldo(id_1)[0]} Saque realizado com sucesso!'
              f' saldo atual: R${app_aux.qry_cliente_saldo(id_1)[1]}')
        menu.monta_menu(menu.menu_principal)


def transFerencia():
    app_aux.titulo('    TRANSFERENCIA     ')
    global data_hora
    print()
    # #####################################
    # Identifica quem Transfere
    # #####################################
    while True:
        id_1 = int(input('Sua Identificação: \nInforme o seu ID: '))
        if app_aux.consulta_cliente(id_1):
            valor_transf = float(input(f'Seja bem vindo(a): {app_aux.qry_cliente_saldo(id_1)[0]} \n     '
                                       f' Saldo Atual: R${app_aux.qry_cliente_saldo(id_1)[1]} '
                                       f'\n    Transferencia: R$'))
            break
        else:
            print(verm + '\nCliente Não localizado, tente novamente:\n' + reset_color)
    ###################################################
    # Identifica Favorecido e confirma a transferencia
    ###################################################
    print()
    while True:
        id_2 = int(input('    ID_FAVORECIDO: '))
        if app_aux.consulta_cliente(id_2):
            input(f'        CLIENTE__: {app_aux.qry_cliente_saldo(id_2)[0]} \nPrescione ENTER para CONFIRMAR')
            break
        else:
            print(verm + '\nCliente Não localizado, tente novamente:\n' + reset_color)
    # #####################################
    # Faz o depósito na conta do favorecido
    # #####################################
    transSaida = 'tr_saque'
    transEntrada = 'tr_entrada'
    app_aux.insert_saque(id_1, valor_transf, data_hora, transSaida)  # realizada saque do cliente
    app_aux.insert_deposito(id_2, valor_transf, data_hora, transEntrada)  # deposita para o favorecido
    input(blue+'\nTransação realizada com SUCESSO!'+reset_color)
    # #####################################
    # Consulta saldo atual dos clientes
    # #####################################
    print(f'\n{app_aux.qry_cliente_saldo(id_1)[0]}\nSaldo atual: R${app_aux.qry_cliente_saldo(id_1)[1]}')
    input('Pressione ENTER para Continuar')
    menu.monta_menu(menu.menu_principal)


def extrato():
    app_aux.titulo('       EXTRATO       ')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    print()
    try:
        id_1 = int(input('Sua Identificação: Informe o seu ID: '))
        cliente = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_1,))
        cliente1 = cliente.fetchone()[0]
        print(f'{cliente1} extrato para simples conferência.')
        sql = c.execute('''SELECT c.data, c.entrada, c.saida, c.transacao
                                        FROM conta C
                                        LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                        WHERE c.cod_cliente = ?
                                        ORDER BY c.id ASC''', (id_1,))  # <------consulta conta cliente
        consulta = sql.fetchall()
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        print(f'TOTAL ENTRADA: R${app_aux.qry_cliente_saldo(id_1)[2]}')
        print(f'TOTAL   SAÍDA: R${app_aux.qry_cliente_saldo(id_1)[3]}')
        print(f'SALDO   ATUAL: R${app_aux.qry_cliente_saldo(id_1)[1]}')
        input("Prescione ENTER para sair.")
        menu.monta_menu(menu.menu_principal)
    except TypeError:
        print('Cliente Não Existe no Banco de Dados')
        extrato()

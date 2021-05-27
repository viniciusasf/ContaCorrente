import sqlite3
from tabulate import tabulate
import sys
from time import sleep
import menu


def titulo(texto):
    reset_color = "\033[0m"  # <--- cor preto
    red = "\033[1;32;40m"  # <--- cor vermelho
    print('-=' * 15)
    print(red + texto + reset_color)
    print('-=' * 15)


def sair():
    print('Encerrando o sistema. \nAguarde...\nGravando Dados no Bando de Dados...')
    contagem()
    print('Sistema Encerrado')
    sys.exit()


def contagem():
    for cont in range(3, -1, -1):
        print(cont, '... ', end='')
        sleep(1)


def criar_conta_corrente():
    titulo('CONTA - CORRENTE')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    sql = c.execute('''SELECT * FROM cliente''')
    consulta = sql.fetchall()
    head = [col[0] for col in sql.description]
    print(tabulate(consulta, headers=head, tablefmt="grid"))

    id_cliente = int(input('INFORME O ID DO CLIENTE: '))
    valor_deposito = float(input('INFORME O VALOR DO DEPOSITO: '))

    c.execute('''INSERT INTO conta (cod_cliente, entrada)
                    VALUES(?, ?)''', (id_cliente, valor_deposito))

    consulta_cliente = c.execute('''SELECT nome
                                   FROM cliente
                                   WHERE id = ?''', (id_cliente,))
    cliente = consulta_cliente.fetchone()[0]
    print(f'Conta-Corrente Gerada com sucesso para o cliente {cliente} com o valor de deposito de {valor_deposito}')
    conn.commit()
    conn.close()


def novo_cliente():
    titulo('CADASTRO DE CLIENTE')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    nome = input('NOME DO CLIENTE: ')
    cidade = input('CIDADE: ')
    telefone = input('TELEFONE: ')
    c.execute('''INSERT INTO cliente (nome, cidade, telefone)
                 VALUES(?, ?, ?)''', (nome, cidade, telefone))
    conn.commit()
    print('{} Cadastrado com Sucesso'.format(nome))
    conn.close()
    print('{} Cadastrado com Sucesso'.format(nome))
    print('')
    opcao = input("Deseja Criar a Conta Corrente Agora: 1 - SIM / 2 - NÃO")
    if opcao == '1':
        criar_conta_corrente()
    else:
        menu.monta_menu(menu.menu_principal)


def consulta_todos_clientes():
    titulo('CONSULTA TODOS CLIENTES')
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
        input("Prescione ENTER para sair.")
    else:
        print('Nenhum cliente encontrado')
        conn.close()


def consulta_cliente_id():
    titulo('CONSULTA CLIENTE POR ID')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    id = int(input('Informe o numero do ID_Cliente: '))
    print('')
    sql = c.execute('''SELECT id, nome, cidade, telefone FROM cliente WHERE id=?''', (id,))
    consulta = sql.fetchall()
    if consulta:
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        input("Prescione ENTER para sair.")
    else:
        print(f'ID numero {id} não localizado.')
        print('')
        consulta_cliente_id()
        print('')
    conn.close()


def consulta_cliente_nome():
    titulo('CONSULTA CLIENTE POR NOME')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    nome = input('Informe o nome do cliente: ')
    sql = c.execute("SELECT * FROM cliente WHERE nome LIKE '%'||?||'%'", (nome,))
    print('')
    consulta = sql.fetchall()
    if consulta:
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        input("Prescione ENTER para sair.")
    else:
        print(f'Cliente {nome} não localizado(a).')
        print('')
        consulta_cliente_nome()
        print('')

    conn.close()


def consulta_cliente_cidade():
    titulo('CONSULTA CLIENTE POR CIDADE')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    cidade = input('Informe a Cidade do Cliente: ')
    sql = c.execute("SELECT * FROM cliente WHERE cidade LIKE '%'||?||'%'", (cidade,))
    consulta = sql.fetchall()
    if cidade:
        head = [col[0] for col in sql.description]
        print(tabulate(consulta, headers=head, tablefmt="grid"))
        conn.close()
        input("Prescione ENTER para sair.")
    else:
        print(f' Cidade {cidade} não foi localizado.')
        print('')
        conn.close()


def transDeposito():
    titulo('DEPOSITO')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    print('')
    id_1 = int(input('Sua Identificação: Informe o seu ID: '))
    print('')
    cliente1 = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_1,))
    cliente = cliente1.fetchone()[0]
    print('')
    valor_depositado = float(input(f'Seja bem vindo(a) {cliente} informe o valor do deposito: '))
    c.execute('''INSERT INTO conta (cod_cliente, entrada) VALUES(?, ?)''', (id_1, valor_depositado))
    conn.commit()
    consulta_saldo = c.execute('''SELECT sum(c.entrada) - sum(c.saida)     
                                FROM conta c
                                LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                WHERE c.cod_cliente = ?''', (id_1,))  # <------consulta saldo conta-corrente
    consulta_saldos = consulta_saldo.fetchone()[0]
    print('')
    print(f'{cliente} depositou {valor_depositado} o saldo de sua conta é de: R${consulta_saldos}')
    conn.close()


def transSaque():
    titulo('SAQUE')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    print('')
    id_1 = int(input('Sua Identificação: Informe o seu ID: '))
    print('')
    cliente1 = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_1,))
    cliente = cliente1.fetchone()[0]
    print('')
    valor_saque = float(input(f'Seja bem vindo(a) {cliente} informe o valor do saque: '))
    c.execute('''INSERT INTO conta (cod_cliente, saida) VALUES(?, ?)''', (id_1, valor_saque))
    conn.commit()
    consulta_saldo = c.execute('''SELECT sum(c.entrada) - sum(c.saida)     
                                    FROM conta c
                                    LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                    WHERE c.cod_cliente = ?''', (id_1,))  # <------consulta saldo conta-corrente
    consulta_saldos = consulta_saldo.fetchone()[0]
    print('')
    print(f'{cliente} depositou {valor_saque} o saldo de sua conta é de: R${consulta_saldos}')
    conn.close()


def transFerencia():
    titulo('TRANSFERENCIA')
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    print()
    # identifica cliente 1
    id_1 = int(input('Sua Identificação: Informe o seu ID: '))
    cliente1 = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_1,))
    cliente_1 = cliente1.fetchone()[0]
    valor_transf = float(input(f'Seja bem vindo(a) {cliente_1} informe o valor da Transferencia: '))
    # faz a retirada da conta
    c.execute('''INSERT INTO conta (cod_cliente, saida) VALUES(?, ?)''', (id_1, valor_transf))

    print()
    # identifica cliente 2
    id_2 = int(input('Informe o ID do Favorecido que irá receber a Transferencia: '))
    cliente2 = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_2,))
    cliente_2 = cliente2.fetchone()[0]
    print()
    input(f'{cliente_1} irá transferir o valor de R${valor_transf} para o cliente {cliente_2} \nprescione ENTER '
          f'para continuar')
    # faz o deposito na conta do favorecido
    c.execute('''INSERT INTO conta (cod_cliente, entrada) VALUES(?, ?)''', (id_2, valor_transf))
    conn.commit()
    print('valor transferido com sucesso')

    # consulta o saldo atual dos clientes
    saldo_cli1 = c.execute('''SELECT sum(c.entrada) - sum(c.saida)     
                                        FROM conta c
                                        LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                        WHERE c.cod_cliente = ?''', (id_1,))  # <------consulta saldo conta-corrente
    consulta_saldoc1 = saldo_cli1.fetchone()[0]
    saldo_cli2 = c.execute('''SELECT sum(c.entrada) - sum(c.saida)     
                                            FROM conta c
                                            LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                            WHERE c.cod_cliente = ?''', (id_2,))  # <------consulta saldo conta-corrente
    consulta_saldoc2 = saldo_cli2.fetchone()[0]
    print(f'{cliente_1} saldo atual é de: R${consulta_saldoc1} \n '
          f'{cliente_2} saldo atual é de: R${consulta_saldoc2} ')
    # print(f'{cliente} depositou {valor_saque} o saldo de sua conta é de: R${consulta_saldos}')
    conn.close()#


def pagamentos():
    pass


def extrato():
    pass
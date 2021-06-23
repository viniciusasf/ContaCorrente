import sqlite3
from time import sleep
import sys


verm = "\033[1;31m"
green = "\033[1;32;40m"  #
reset_color = "\033[0;0m"  # <--- cor preto
blue = "\033[1;34m"


def consulta_cliente(id_):
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    consulta = c.execute('select id from cliente where id=?', (id_,))
    return consulta.fetchall()


def titulo(texto) -> object:
    print('-=' * 15)
    print(green + texto + reset_color)
    print('-=' * 15)


def sair():
    print(verm + 'Encerrando o sistema... Aguarde...\nGravando Dados no Bando de Dados...' + reset_color)
    contagem()
    print('\n\nSistema Encerrado' + reset_color)
    sys.exit()


def contagem():
    for cont in range(3, -1, -1):
        print(cont, '... ', end='')
        sleep(1)


def qry_cliente_saldo(id_):
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    saldo = c.execute('''SELECT cli.nome, sum(c.entrada) - sum(c.saida), sum(c.entrada), sum(c.saida)  
                                                  FROM conta c
                                                  LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                                  WHERE c.cod_cliente = ?''', (id_,))
    return saldo.fetchall()[0]


def insert_saque(id_1, valor_saque, data_hora, transacao):
    valor_entrada = 0.0
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    c.execute('''INSERT INTO conta (cod_cliente, entrada, saida, data, transacao)
            VALUES(?, ?, ?, ?, ?)''', (id_1, valor_entrada, valor_saque, data_hora, transacao))
    conn.commit()
    conn.close()


def insert_deposito(id_1, valor_entrada, data_hora, transacao) -> object:
    valor_saque = 0.0
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    c.execute('''INSERT INTO conta (cod_cliente, entrada, saida, data, transacao)
                VALUES(?, ?, ?, ?, ?)''', (id_1, valor_entrada, valor_saque, data_hora, transacao))
    conn.commit()
    conn.close()



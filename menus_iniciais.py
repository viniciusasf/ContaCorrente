import sqlite3
from tabulate import tabulate


def extrato():
    conn = sqlite3.connect('contacorente.db')
    c = conn.cursor()
    print()
    id_1 = int(input('Sua Identificação: Informe o seu ID: '))
    cliente = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_1,))
    cliente1 = cliente.fetchone()[0]
    print('')
    print(f'{cliente1} extrato para simples conferência.')
    # sql = c.execute('''SELECT cli.nome, c.data, c.entrada, c.saida
    #                             FROM conta C
    #                             LEFT JOIN cliente cli on cli.id = c.cod_cliente
    #                             WHERE c.cod_cliente = ?
    #                             ORDER BY c.data''', (id_1,))  # <------consulta conta cliente
    sql = c.execute('''SELECT c.data, c.entrada, c.saida
                                FROM conta C
                                LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                WHERE c.cod_cliente = ?
                                ORDER BY c.data''', (id_1,))  # <------consulta conta cliente
    consulta = sql.fetchall()
    head = [col[0] for col in sql.description]
    print(tabulate(consulta, headers=head, tablefmt="grid"))

    ent = c.execute('''SELECT sum(c.entrada)     
                                    FROM conta c
                                    LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                    WHERE c.cod_cliente = ?''', (id_1,))
    entrada = ent.fetchone()[0]
    sai = c.execute('''SELECT sum(c.saida)     
                                        FROM conta c
                                        LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                        WHERE c.cod_cliente = ?''', (id_1,))
    saida = sai.fetchone()[0]
    sal = c.execute('''SELECT sum(c.entrada) - sum(c.saida)     
                                        FROM conta c
                                        LEFT JOIN cliente cli on cli.id = c.cod_cliente
                                        WHERE c.cod_cliente = ?''', (id_1,))  # <------consulta saldo conta-corrente
    saldo = sal.fetchone()[0]
    print(f'TOTAL ENTRADA: R${entrada}')
    print(f'TOTAL   SAÍDA: R${saida}')
    print(f'SALDO ATUAL  : R${saldo}')
    input("Prescione ENTER para sair.")
    conn.close()

extrato()



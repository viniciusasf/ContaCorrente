import sqlite3

conn = sqlite3.connect('contacorente.db')
c = conn.cursor()
print()
#identifica cliente 1
id_1 = int(input('Sua Identificação: Informe o seu ID: '))
cliente1 = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_1,))
cliente_1 = cliente1.fetchone()[0]
valor_transf = float(input(f'Seja bem vindo(a) {cliente_1} informe o valor da Transferencia: '))
#faz a retirada da conta
c.execute('''INSERT INTO conta (cod_cliente, saida) VALUES(?, ?)''', (id_1, valor_transf))

print()
#identifica cliente 2
id_2 = int(input('Informe o ID do cliente que irá receber a Transferencia: '))
cliente2 = c.execute('''SELECT nome FROM cliente WHERE id = ?''', (id_2,))
cliente_2 = cliente2.fetchone()[0]
print()
input(f'{cliente_1} irá transferir o valor de R${valor_transf} para o cliente {cliente_2} \nprescione ENTER '
      f'para continuar')
#faz o deposito na conta
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
conn.close()
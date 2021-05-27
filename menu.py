import funcoes

menu_consulta = {
    '1': ('- Consulta por ID', funcoes.consulta_cliente_id),
    '2': ('- Consulta por Cidade', funcoes.consulta_cliente_cidade),
    '3': ('- Consulta por Nome', funcoes.consulta_cliente_nome),
    '4': ('- Consulta Todos Clientes', funcoes.consulta_todos_clientes),
    '9': ('- Deslogar', funcoes.sair),
}
menu_cadastro = {
    '1': ('- Cadastro de Cliente', funcoes.novo_cliente),
    '2': ('- Cadastro de Conta-Corrente', funcoes.criar_conta_corrente),
    '9': ('- Deslogar', funcoes.sair),
}
menu_trans = {
    '1': ('- Depósito', funcoes.transDeposito),
    '2': ('- Saque', funcoes.transSaque),
    '3': ('- Transferência', funcoes.transFerencia),
    '4': ('- Pagamentos', funcoes.pagamentos),
    '5': ('- Extrato', funcoes.extrato),
    '9': ('- Voltar', menu_cadastro),
}
menu_principal = {
    '1': ('- Cadastros', menu_cadastro),
    '2': ('- Consultas', menu_consulta),
    '3': ('- Transações - Em desenvolvimento', menu_trans),
    '9': ('- Deslogar - Em desenvolvimento', funcoes.sair),
}


def monta_menu(menu) -> object:
    funcoes.titulo('BEM VINDO AO SISTEMA')
    for k, v in menu.items():
        texto, _ = v
        print(k, texto)
    print('')
    opcao = input('Digite a Opçao Desejada:    ')
    print('')
    try:
        escolhido = menu[opcao]
        _, funcao = escolhido
        if isinstance(funcao, dict):
            monta_menu(funcao)
        else:
            funcao()
    except KeyError:
        print()
        monta_menu(menu_principal)

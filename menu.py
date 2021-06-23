import funcoes

bold = "\033[;1m"


menu_consulta = {
    '1': ('- Extrato', funcoes.extrato),
    '2': ('- Consulta por ID', funcoes.consulta_cliente_id),
    '3': ('- Consulta por Cidade', funcoes.consulta_cliente_cidade),
    '4': ('- Consulta por Nome', funcoes.consulta_cliente_nome),
    '5': ('- Consulta Todos Clientes', funcoes.consulta_todos_clientes),
    '9': ('- Deslogar', funcoes.app_aux.sair),
}
menu_cadastro = {
    '1': ('- Cadastro de Cliente', funcoes.novo_cliente),
    '2': ('- Cadastro de Conta-Corrente', funcoes.criar_conta_corrente),
    '9': ('- Sair', funcoes.app_aux.sair),
}
menu_trans = {
    '1': ('- Depósito', funcoes.transDeposito),
    '2': ('- Saque', funcoes.transSaque),
    '3': ('- Transferência', funcoes.transFerencia),
    '9': ('- Voltar', menu_cadastro),
}
menu_principal = {
    '1': ('- Cadastros', menu_cadastro),
    '2': ('- Consultas', menu_consulta),
    '3': ('- Transações', menu_trans),
    '9': ('- Sair ', funcoes.app_aux.sair),
}


def monta_menu(menu) -> object:
    funcoes.app_aux.titulo('     BEM VINDO AO SISTEMA     ')
    for k, v in menu.items():
        texto, _ = v
        print(k, bold+texto)
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






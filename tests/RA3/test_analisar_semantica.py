from src.RA3.functions.python.analisador_tipos import analisarSemantica
from src.RA3.functions.python.gramatica_atributos import definirGramaticaAtributos, inicializar_sistema_semantico


def test_assignment_stores_type():
    gramatica, tabela = inicializar_sistema_semantico()
    ast = {
        'linhas': [
            {'numero_linha': 1, 'filhos': [{'elementos': [{'subtipo': 'numero_real', 'valor': '5'}, {'subtipo': 'variavel', 'valor': 'A'}], 'operador': None}]}
        ]
    }
    res = analisarSemantica(ast, gramatica, tabela)
    assert res['sucesso']
    # A should be in table
    assert tabela.existe('A')
    assert tabela.obter_tipo('A') in ('int', 'real')


def test_division_requires_int():
    gramatica, tabela = inicializar_sistema_semantico()
    ast = {
        'linhas': [
            {'numero_linha': 1, 'filhos': [{'elementos': [{'subtipo': 'numero_real', 'valor': '3.5'}, {'subtipo': 'numero_real', 'valor': '2.0'}], 'operador': '/'}]}
        ]
    }
    res = analisarSemantica(ast, gramatica, tabela)
    assert not res['sucesso']
    assert any('requer operandos inteiros' in e['erro'].lower() or 'inteiros' in e['erro'].lower() for e in res['erros'])


def test_power_exponent_int_requirement():
    gramatica, tabela = inicializar_sistema_semantico()
    ast = {
        'linhas': [
            {'numero_linha': 1, 'filhos': [{'elementos': [{'subtipo': 'numero_real', 'valor': '2'}, {'subtipo': 'numero_real', 'valor': '2.5'}], 'operador': '^'}]}
        ]
    }
    res = analisarSemantica(ast, gramatica, tabela)
    assert not res['sucesso']
    assert any('expoente' in e['erro'].lower() for e in res['erros'])


def test_uninitialized_variable_error():
    gramatica, tabela = inicializar_sistema_semantico()
    # Pre-declare variable X as uninitialized so we test the "sem inicialização" error
    tabela.adicionarSimbolo('X', 'int', inicializada=False, linha=0)
    ast = {
        'linhas': [
            {'numero_linha': 1, 'filhos': [{'elementos': [{'subtipo': 'variavel', 'valor': 'X'}], 'operador': None}]}
        ]
    }
    res = analisarSemantica(ast, gramatica, tabela)
    assert not res['sucesso']
    assert any('sem inicialização' in e['erro'].lower() for e in res['erros'])

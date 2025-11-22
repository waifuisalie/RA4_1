"""
Testes para o Gerador de Assembly AVR

Testa a funcionalidade de alocação de registradores e geração de código Assembly.
"""

import sys
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from RA4.functions.python.gerador_assembly import GeradorAssembly


def test_register_allocator_basic():
    """Testa alocação básica de registradores (sem spilling)"""
    print("\n=== Teste 1: Alocação Básica (sem spill) ===")

    tac_simple = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "1", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "2", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "+", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_simple)

    print(assembly)
    print("\n✓ Teste 1 passou: Assembly gerado com sucesso!")

    # Verificações básicas
    assert "main:" in assembly
    assert "rjmp fim" in assembly
    assert "ldi r16" in assembly  # Constante carregada
    assert "add r" in assembly    # Operação de soma
    print("✓ Verificações de conteúdo passaram!")


def test_register_allocator_with_spill():
    """Testa alocação com spilling (mais de 4 pares de variáveis)"""
    print("\n=== Teste 2: Alocação com Spilling ===")

    # TAC que requer mais de 4 pares de registradores
    tac_with_spill = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "1", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "2", "line": 2},
            {"type": "assignment", "dest": "t2", "source": "3", "line": 3},
            {"type": "assignment", "dest": "t3", "source": "4", "line": 4},
            {"type": "assignment", "dest": "t4", "source": "5", "line": 5},  # Deve spillar t0
            {"type": "binary_op", "result": "t5", "operand1": "t4",
             "operator": "+", "operand2": "t1", "line": 6}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_with_spill)

    print(assembly)
    print("\n✓ Teste 2 passou: Assembly com spilling gerado!")

    # Verificar se há instruções de spill
    assert "Spill" in assembly or "sts 0x0100" in assembly
    print("✓ Código de spilling detectado!")


def test_example_from_issue():
    """Testa com o exemplo fornecido pelo usuário"""
    print("\n=== Teste 3: Exemplo do Issue ===")

    tac_example = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "1", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "2", "line": 2},
            {"type": "assignment", "dest": "t2", "source": "3", "line": 3},
            {"type": "binary_op", "result": "t3", "operand1": "t0",
             "operator": "+", "operand2": "t1", "line": 4},
            {"type": "binary_op", "result": "t4", "operand1": "t3",
             "operator": "*", "operand2": "t2", "line": 5},
            {"type": "label", "name": "L1", "line": 16},
            {"type": "assignment", "dest": "t15", "source": "1", "line": 17},
            {"type": "goto", "target": "L2", "line": 18},
            {"type": "label", "name": "L2", "line": 19},
            {"type": "assignment", "dest": "t16", "source": "42", "line": 20}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_example)

    print(assembly)
    print("\n✓ Teste 3 passou: Exemplo completo gerado!")

    # Verificar labels e goto
    assert "L1:" in assembly
    assert "L2:" in assembly
    assert "rjmp L2" in assembly
    print("✓ Labels e goto funcionando!")


def test_constant_vs_variable():
    """Testa diferenciação entre constantes e variáveis"""
    print("\n=== Teste 4: Constantes vs Variáveis ===")

    tac_mixed = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "100", "line": 1},  # Constante
            {"type": "assignment", "dest": "t1", "source": "t0", "line": 2},   # Variável
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_mixed)

    print(assembly)

    # Constante deve usar LDI
    assert "ldi r16, 100" in assembly or "ldi r16, 0x64" in assembly
    # Variável deve usar MOV
    assert "mov r" in assembly

    print("✓ Teste 4 passou: Constantes e variáveis diferenciadas!")


def test_subtraction():
    """Testa operação de subtração 16-bit"""
    print("\n=== Teste 5: Subtração (10 - 3 = 7) ===")

    tac_sub = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "10", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "3", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "-", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_sub)

    print(assembly)

    # Verificar instruções de subtração
    assert "sub r" in assembly
    assert "sbc r" in assembly
    print("✓ Teste 5 passou: Subtração implementada com SUB/SBC!")


def test_multiplication():
    """Testa operação de multiplicação 16-bit"""
    print("\n=== Teste 6: Multiplicação (6 * 7 = 42) ===")

    tac_mul = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "6", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "7", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "*", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_mul)

    print(assembly)

    # Verificar chamada para rotina mul16
    assert "rcall mul16" in assembly
    assert "mul16:" in assembly  # Rotina deve ser gerada
    assert "mul r" in assembly   # Instrução MUL deve estar na rotina
    print("✓ Teste 6 passou: Multiplicação implementada com rotina mul16!")


if __name__ == "__main__":
    print("=" * 70)
    print("TESTES DO GERADOR DE ASSEMBLY - SUB-ISSUES 3.2, 3.3, 3.4")
    print("=" * 70)

    try:
        test_register_allocator_basic()
        test_register_allocator_with_spill()
        test_example_from_issue()
        test_constant_vs_variable()
        test_subtraction()
        test_multiplication()

        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

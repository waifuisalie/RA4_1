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


def test_division():
    """Testa operação de divisão 16-bit (100 / 7 = 14)"""
    print("\n=== Teste 7: Divisão (100 / 7 = 14) ===")

    tac_div = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "100", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "7", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "/", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_div)

    print(assembly)

    # Verificar chamada para rotina div16
    assert "rcall div16" in assembly
    assert "div16:" in assembly  # Rotina deve ser gerada
    assert "mov r18" in assembly  # Parameter setup (dividend)
    assert "mov r20" in assembly  # Parameter setup (divisor)
    assert "mov r24" in assembly or "r24" in assembly  # Result (quotient)
    print("✓ Teste 7 passou: Divisão implementada com rotina div16!")


def test_modulo():
    """Testa operação de módulo 16-bit (100 % 7 = 2)"""
    print("\n=== Teste 8: Módulo (100 % 7 = 2) ===")

    tac_mod = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "100", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "7", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "%", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_mod)

    print(assembly)

    # Verificar chamada para rotina div16 (mesma rotina!)
    assert "rcall div16" in assembly
    assert "div16:" in assembly  # Rotina deve ser gerada
    assert "mov r18" in assembly  # Parameter setup (dividend)
    assert "mov r20" in assembly  # Parameter setup (divisor)
    assert "r22" in assembly  # Result (remainder, not quotient!)
    print("✓ Teste 8 passou: Módulo implementado usando rotina div16 (retorna resto)!")


def test_comparison_eq():
    """Testa comparação de igualdade (100 == 100 = 1, 100 == 99 = 0)"""
    print("\n=== Teste 9: Comparação == (Equal) ===")

    tac_eq = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "100", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "100", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "==", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_eq)

    print(assembly)

    # Verificar instruções de comparação
    assert "cp r" in assembly      # Compare instruction
    assert "cpc r" in assembly     # Compare with carry
    assert "brne skip_eq_3" in assembly  # Branch if not equal
    assert "skip_eq_3:" in assembly
    print("✓ Teste 9 passou: Comparação == implementada!")


def test_comparison_ne():
    """Testa comparação de desigualdade (100 != 99 = 1, 100 != 100 = 0)"""
    print("\n=== Teste 10: Comparação != (Not Equal) ===")

    tac_ne = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "100", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "99", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "!=", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_ne)

    print(assembly)

    # Verificar instruções de comparação
    assert "cp r" in assembly
    assert "cpc r" in assembly
    assert "breq skip_ne_3" in assembly  # Branch if equal (inverted logic)
    assert "skip_ne_3:" in assembly
    print("✓ Teste 10 passou: Comparação != implementada!")


def test_comparison_lt():
    """Testa comparação menor que (50 < 100 = 1, 100 < 50 = 0)"""
    print("\n=== Teste 11: Comparação < (Less Than) ===")

    tac_lt = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "50", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "100", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "<", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_lt)

    print(assembly)

    # Verificar instruções de comparação
    assert "cp r" in assembly
    assert "cpc r" in assembly
    assert "brsh skip_lt_3" in assembly  # Branch if same or higher (A >= B)
    assert "skip_lt_3:" in assembly
    print("✓ Teste 11 passou: Comparação < implementada!")


def test_comparison_ge():
    """Testa comparação maior ou igual (100 >= 50 = 1, 50 >= 100 = 0)"""
    print("\n=== Teste 12: Comparação >= (Greater or Equal) ===")

    tac_ge = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "100", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "50", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": ">=", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_ge)

    print(assembly)

    # Verificar instruções de comparação
    assert "cp r" in assembly
    assert "cpc r" in assembly
    assert "brlo skip_ge_3" in assembly  # Branch if lower (A < B)
    assert "skip_ge_3:" in assembly
    print("✓ Teste 12 passou: Comparação >= implementada!")


def test_comparison_gt():
    """Testa comparação maior que (100 > 50 = 1, 50 > 100 = 0)"""
    print("\n=== Teste 13: Comparação > (Greater Than) ===")

    tac_gt = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "100", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "50", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": ">", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_gt)

    print(assembly)

    # Verificar instruções de comparação (operandos trocados!)
    assert "cp r" in assembly
    assert "cpc r" in assembly
    assert "brsh skip_gt_3" in assembly  # B >= A (swapped)
    assert "skip_gt_3:" in assembly
    print("✓ Teste 13 passou: Comparação > implementada (com swap de operandos)!")


def test_comparison_le():
    """Testa comparação menor ou igual (50 <= 100 = 1, 100 <= 50 = 0)"""
    print("\n=== Teste 14: Comparação <= (Less or Equal) ===")

    tac_le = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "50", "line": 1},
            {"type": "assignment", "dest": "t1", "source": "100", "line": 2},
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "<=", "operand2": "t1", "line": 3}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_le)

    print(assembly)

    # Verificar instruções de comparação (operandos trocados!)
    assert "cp r" in assembly
    assert "cpc r" in assembly
    assert "brlo skip_le_3" in assembly  # B < A (swapped)
    assert "skip_le_3:" in assembly
    print("✓ Teste 14 passou: Comparação <= implementada (com swap de operandos)!")


def test_if_goto():
    """Testa salto condicional if_goto (jump if TRUE)"""
    print("\n=== Teste 15: Salto Condicional if_goto ===")

    tac_if_goto = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "1", "line": 1},
            {"type": "if_goto", "condition": "t0", "target": "L2", "line": 2},
            {"type": "assignment", "dest": "t1", "source": "100", "line": 3},
            {"type": "label", "name": "L2", "line": 4}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_if_goto)

    print(assembly)

    # Verificar instruções de salto condicional
    assert "cp r" in assembly       # Compare instruction
    assert "cpc r" in assembly      # Compare with carry
    assert "brne L2" in assembly    # Branch if not equal (true)
    assert "L2:" in assembly        # Target label
    print("✓ Teste 15 passou: if_goto implementado (brne)!")


def test_if_false_goto():
    """Testa salto condicional if_false_goto (jump if FALSE)"""
    print("\n=== Teste 16: Salto Condicional if_false_goto ===")

    tac_if_false_goto = {
        "instructions": [
            {"type": "assignment", "dest": "t0", "source": "0", "line": 1},
            {"type": "if_false_goto", "condition": "t0", "target": "L1", "line": 2},
            {"type": "assignment", "dest": "t1", "source": "100", "line": 3},
            {"type": "label", "name": "L1", "line": 4}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_if_false_goto)

    print(assembly)

    # Verificar instruções de salto condicional
    assert "cp r" in assembly       # Compare instruction
    assert "cpc r" in assembly      # Compare with carry
    assert "breq L1" in assembly    # Branch if equal (false)
    assert "L1:" in assembly        # Target label
    print("✓ Teste 16 passou: if_false_goto implementado (breq)!")


def test_simple_while_loop():
    """Testa estrutura completa de WHILE loop"""
    print("\n=== Teste 17: WHILE Loop Completo ===")

    # Simple WHILE loop structure without actual loop (just structure test)
    tac_while = {
        "instructions": [
            # Initialize value
            {"type": "assignment", "dest": "t0", "source": "5", "line": 1},

            # Loop start
            {"type": "label", "name": "L0", "line": 2},

            # Condition check (t0 < 10)
            {"type": "binary_op", "result": "t1", "operand1": "t0",
             "operator": "<", "operand2": "10", "line": 2},
            {"type": "if_false_goto", "condition": "t1", "target": "L1", "line": 2},

            # Loop body - just increment
            {"type": "binary_op", "result": "t2", "operand1": "t0",
             "operator": "+", "operand2": "1", "line": 2},

            # Loop back
            {"type": "goto", "target": "L0", "line": 2},

            # Loop exit
            {"type": "label", "name": "L1", "line": 2}
        ]
    }

    gerador = GeradorAssembly()
    assembly = gerador.gerarAssembly(tac_while)

    print(assembly)

    # Verify loop structure
    assert "L0:" in assembly         # Loop start label
    assert "L1:" in assembly         # Loop exit label
    assert "breq L1" in assembly     # ifFalse exit
    assert "rjmp L0" in assembly     # goto loop start
    assert "brsh skip_lt_2" in assembly  # Comparison branch
    print("✓ Teste 17 passou: WHILE loop completo funciona!")


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
        test_division()
        test_modulo()
        test_comparison_eq()
        test_comparison_ne()
        test_comparison_lt()
        test_comparison_ge()
        test_comparison_gt()
        test_comparison_le()
        test_if_goto()
        test_if_false_goto()
        test_simple_while_loop()

        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

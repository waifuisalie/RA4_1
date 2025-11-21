#!/usr/bin/env python3
"""
Test script for TAC optimization placeholders

This script loads the TAC placeholder files and shows the optimization
opportunities available in each test case.
"""

import json
import os
from pathlib import Path


def load_tac_json(file_path: str) -> dict:
    """Load TAC JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_tac_opportunities(tac_data: dict, filename: str):
    """Analyze TAC instructions for optimization opportunities."""
    instructions = tac_data['instructions']

    print(f"\n{'='*60}")
    print(f"ANÁLISE DE OPORTUNIDADES DE OTIMIZAÇÃO - {filename}")
    print(f"{'='*60}")

    print(f"Total de instruções: {len(instructions)}")

    # Count different instruction types
    types_count = {}
    constants_used = set()
    temps_defined = set()
    temps_used = set()

    for inst in instructions:
        inst_type = inst['type']
        types_count[inst_type] = types_count.get(inst_type, 0) + 1

        # Track constants
        if inst_type in ['assignment', 'copy']:
            source = inst.get('source', '')
            if source.replace('.', '').replace('-', '').isdigit():
                constants_used.add(source)

        # Track temporaries
        if 'dest' in inst and inst['dest'].startswith('t'):
            temps_defined.add(inst['dest'])
        if 'result' in inst and inst['result'].startswith('t'):
            temps_defined.add(inst['result'])

        # Track variable usage
        for key in ['source', 'operand1', 'operand2', 'condition']:
            if key in inst and inst[key].startswith('t'):
                temps_used.add(inst[key])

    print(f"Tipos de instrução: {types_count}")
    print(f"Constantes encontradas: {sorted(constants_used)}")
    print(f"Temporários definidos: {len(temps_defined)}")
    print(f"Temporários usados: {len(temps_used)}")

    # Identify optimization opportunities
    opportunities = []

    # Constant folding opportunities
    binary_ops = [i for i in instructions if i['type'] == 'binary_op']
    constant_folding_ops = 0
    for op in binary_ops:
        op1_const = op.get('operand1', '').replace('.', '').replace('-', '').isdigit()
        op2_const = op.get('operand2', '').replace('.', '').replace('-', '').isdigit()
        if op1_const and op2_const:
            constant_folding_ops += 1
            opportunities.append(f"Constant folding: {op['operand1']} {op['operator']} {op['operand2']}")

    # Dead code opportunities (temporaries defined but not used)
    dead_temps = temps_defined - temps_used
    if dead_temps:
        opportunities.append(f"Dead code: {len(dead_temps)} temporários não utilizados")

    # Jump optimization opportunities
    labels = [i for i in instructions if i['type'] == 'label']
    gotos = [i for i in instructions if i['type'] == 'goto']
    if labels and gotos:
        opportunities.append(f"Jump optimization: {len(gotos)} gotos, {len(labels)} labels")

    print(f"\nRESUMO DE OPORTUNIDADES:")
    print(f"  • {len(instructions)} instruções totais")
    print(f"  • {len(constants_used)} constantes encontradas")
    print(f"  • {len(dead_temps)} temporários não utilizados (dead code)")
    print(f"  • {len(gotos)} gotos e {len(labels)} labels (jump optimization)")
    print(f"  • {constant_folding_ops} operações binárias com constantes (folding)")


def main():
    """Main function to analyze all TAC placeholders."""
    placeholder_dir = Path("/Users/thaismonteiro/Documents/RA4_1/tests/RA4/test_data_for_vac_optimization/tac_placeholders")

    if not placeholder_dir.exists():
        print(f"Diretório de placeholders não encontrado: {placeholder_dir}")
        return

    test_files = [
        "fatorial_tac.json",
        "fibonacci_tac.json",
        "taylor_tac.json"
    ]

    print("ANÁLISE DOS PLACEHOLDERS TAC PARA OTIMIZAÇÃO")
    print("=" * 60)

    for filename in test_files:
        file_path = placeholder_dir / filename
        if file_path.exists():
            try:
                tac_data = load_tac_json(str(file_path))
                analyze_tac_opportunities(tac_data, filename)
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")
        else:
            print(f"Arquivo não encontrado: {filename}")


if __name__ == "__main__":
    main()
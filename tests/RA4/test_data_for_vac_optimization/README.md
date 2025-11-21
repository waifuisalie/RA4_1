# TAC Optimization Placeholders

Este diretório contém placeholders JSON para desenvolvimento e teste da otimização TAC durante a Fase 4.

## Arquivos de Placeholder

### `fatorial_tac.json`
- **Programa**: Cálculo de fatorial
- **Características**: Operações aritméticas, constantes, controle de fluxo
- **Oportunidades de otimização**:
  - Dead code: 5 temporários não utilizados
  - Jump optimization: 1 goto + 2 labels
  - Constant folding: operações com constantes

### `fibonacci_tac.json`
- **Programa**: Sequência de Fibonacci
- **Características**: Sequências numéricas, operações iterativas
- **Oportunidades de otimização**:
  - Dead code: 8 temporários não utilizados
  - Jump optimization: 1 goto + 1 label
  - Constant propagation: cadeias de constantes

### `taylor_tac.json`
- **Programa**: Série de Taylor para cos(x)
- **Características**: Operações em ponto flutuante, constantes reais, expressões matemáticas
- **Oportunidades de otimização**:
  - Dead code: 8 temporários não utilizados
  - Jump optimization: 1 goto + 2 labels
  - Constant folding: operações reais (divisão `|`)

## Formato JSON

Todos os arquivos seguem o formato especificado na interface:

```json
{
  "instructions": [
    {
      "type": "assignment|binary_op|unary_op|label|goto|if_goto|...",
      "dest|result": "t0|t1|...",
      "source|operand1|operand2": "value|variable",
      "operator": "+|-|*|/|||%|...",
      "line": 1
    }
  ]
}
```

## Como Usar

1. **Desenvolvimento**: Use estes arquivos para testar cada técnica de otimização
2. **Validação**: Verifique se as otimizações produzem o resultado esperado
3. **Benchmarking**: Meça reduções de instruções e temporários

## Comando para Análise

```bash
cd /Users/thaismonteiro/Documents/RA4_1
python3 test_data/analyze_placeholders.py
```

Este comando mostra estatísticas e oportunidades de otimização em cada placeholder.

## Próximos Passos

1. Implementar parser TAC (#11)
2. Implementar técnicas de otimização (#12-#15)
3. Testar com estes placeholders
4. Integrar com pipeline real quando TAC generation estiver pronto
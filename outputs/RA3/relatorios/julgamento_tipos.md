# Julgamento de Tipos

**Gerado em:** 2025-11-25 14:16:58

**Total de expressões analisadas:** 4

---

## Linha 1: `(1.0 X_VAL)`

### Análise de Tipos:
- **Operando 1:** `1.0` → tipo: `real`
- **Operando 2:** `X_VAL` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 2: `(1.0 TERM1)`

### Análise de Tipos:
- **Operando 1:** `1.0` → tipo: `real`
- **Operando 2:** `TERM1` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 3: `(1 COUNTER)`

### Análise de Tipos:
- **Operando 1:** `1` → tipo: `int`
- **Operando 2:** `COUNTER` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 4: `((COUNTER 1 <=) (X_VAL X_VAL *) (2.0) (X_SQUARE FACT_2 |) (0.0 TEMP2 -) (X_SQUARE X_SQUARE *) (4.0 3.0 *) (TEMP4A 2.0 *) (TEMP4B 1.0 *) (X_FOURTH FACT_4 |) (X_FOURTH X_SQUARE *) (6.0 5.0 *) (TEMP6A 4.0 *) (TEMP6B 3.0 *) (TEMP6C 2.0 *) (TEMP6D 1.0 *) (X_SIXTH FACT_6 |) (0.0 TEMP8 -) (TERM1 TERM2 +) (SUM12 TERM3 +) (SUM123 TERM4 +) (RESULT_COS) (COUNTER 1 +) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(COUNTER 1 <=)` → tipo: `boolean`
    - `COUNTER` : `int`
    - `1` : `int`
    - Operador: `<=`
    - Resultado: `boolean`
- **Operando 2:** `(X_VAL X_VAL *)` → tipo: `real`
- **Operando 3:** `(2.0)` → tipo: `real`
- **Operando 4:** `(X_SQUARE FACT_2 |)` → tipo: `None`
    - `X_SQUARE` : `N/A`
    - `FACT_2` : `N/A`
    - Operador: `|`
- **Operando 5:** `(0.0 TEMP2 -)` → tipo: `real`
- **Operando 6:** `(X_SQUARE X_SQUARE *)` → tipo: `None`
    - `X_SQUARE` : `N/A`
    - `X_SQUARE` : `N/A`
    - Operador: `*`
- **Operando 7:** `(4.0 3.0 *)` → tipo: `real`
- **Operando 8:** `(TEMP4A 2.0 *)` → tipo: `real`
- **Operando 9:** `(TEMP4B 1.0 *)` → tipo: `real`
- **Operando 10:** `(X_FOURTH FACT_4 |)` → tipo: `None`
    - `X_FOURTH` : `N/A`
    - `FACT_4` : `N/A`
    - Operador: `|`
- **Operando 11:** `(X_FOURTH X_SQUARE *)` → tipo: `None`
    - `X_FOURTH` : `N/A`
    - `X_SQUARE` : `N/A`
    - Operador: `*`
- **Operando 12:** `(6.0 5.0 *)` → tipo: `real`
- **Operando 13:** `(TEMP6A 4.0 *)` → tipo: `real`
- **Operando 14:** `(TEMP6B 3.0 *)` → tipo: `real`
- **Operando 15:** `(TEMP6C 2.0 *)` → tipo: `real`
- **Operando 16:** `(TEMP6D 1.0 *)` → tipo: `real`
- **Operando 17:** `(X_SIXTH FACT_6 |)` → tipo: `None`
    - `X_SIXTH` : `N/A`
    - `FACT_6` : `N/A`
    - Operador: `|`
- **Operando 18:** `(0.0 TEMP8 -)` → tipo: `real`
- **Operando 19:** `(TERM1 TERM2 +)` → tipo: `real`
- **Operando 20:** `(SUM12 TERM3 +)` → tipo: `None`
    - `SUM12` : `N/A`
    - `TERM3` : `N/A`
    - Operador: `+`
- **Operando 21:** `(SUM123 TERM4 +)` → tipo: `None`
    - `SUM123` : `N/A`
    - `TERM4` : `N/A`
    - Operador: `+`
- **Operando 22:** `(RESULT_COS)` → tipo: `None`
    - `RESULT_COS` : `N/A`
    - `FINAL_COS` : `N/A`
- **Operando 23:** `(COUNTER 1 +)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ bloco : T
──────────────────────────────────────────────────
         Γ ⊢ (cond bloco WHILE) : T
```

### Tipo Resultante: `real`

### Observação:
Tipo promovido de `int` para `real` devido a operando `real`.

---

## Resumo de Tipos

### Estatísticas
- **Total de expressões:** 4
- **Com tipo definido:** 4
- **Sem tipo definido:** 0
- **Promoções de tipo:** 1

### Distribuição de Tipos
- `int`: 1 expressões (25.0%)
- `real`: 3 expressões (75.0%)

### Tipos Utilizados
- `int`
- `real`

---
*Relatório gerado automaticamente pelo Compilador RA3_1*

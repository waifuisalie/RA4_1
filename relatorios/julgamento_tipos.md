# Julgamento de Tipos

**Gerado em:** 2025-11-25 01:39:53

**Total de expressões analisadas:** 15

---

## Linha 1: `(0.5 X_VAL)`

### Análise de Tipos:
- **Operando 1:** `0.5` → tipo: `real`
- **Operando 2:** `X_VAL` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 2: `(1.0 TERM1)`

### Análise de Tipos:
- **Operando 1:** `1.0` → tipo: `real`
- **Operando 2:** `TERM1` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 3: `((X_VAL X_VAL *) TEMP1)`

### Análise de Tipos:
- **Operando 1:** `(X_VAL X_VAL *)` → tipo: `real`
    - `X_VAL` : `real`
    - `X_VAL` : `real`
    - Operador: `*`
    - Resultado: `real`
- **Operando 2:** `TEMP1` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 4: `((TEMP1 2.0 |) TEMP2)`

### Análise de Tipos:
- **Operando 1:** `(TEMP1 2.0 |)` → tipo: `real`
    - `TEMP1` : `real`
    - `2.0` : `real`
    - Operador: `|`
    - Resultado: `real`
- **Operando 2:** `TEMP2` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 5: `((0 TEMP2 -) TERM2)`

### Análise de Tipos:
- **Operando 1:** `(0 TEMP2 -)` → tipo: `real`
    - `0` : `int`
    - `TEMP2` : `real`
    - Operador: `-`
    - Resultado: `real`
- **Operando 2:** `TERM2` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 6: `((X_VAL X_VAL *) TEMP3)`

### Análise de Tipos:
- **Operando 1:** `(X_VAL X_VAL *)` → tipo: `real`
    - `X_VAL` : `real`
    - `X_VAL` : `real`
    - Operador: `*`
    - Resultado: `real`
- **Operando 2:** `TEMP3` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 7: `(((TEMP3 X_VAL X_VAL *) *) TEMP4)`

### Análise de Tipos:
- **Operando 1:** `((TEMP3 X_VAL X_VAL *) *)` → tipo: `real`
    - Operador: `*`
    - Resultado: `real`
- **Operando 2:** `TEMP4` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 8: `((TEMP4 24.0 |) TERM3)`

### Análise de Tipos:
- **Operando 1:** `(TEMP4 24.0 |)` → tipo: `real`
    - `TEMP4` : `real`
    - `24.0` : `real`
    - Operador: `|`
    - Resultado: `real`
- **Operando 2:** `TERM3` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 9: `((X_VAL X_VAL *) TEMP5)`

### Análise de Tipos:
- **Operando 1:** `(X_VAL X_VAL *)` → tipo: `real`
    - `X_VAL` : `real`
    - `X_VAL` : `real`
    - Operador: `*`
    - Resultado: `real`
- **Operando 2:** `TEMP5` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 10: `(((TEMP5 X_VAL X_VAL *) *) TEMP6)`

### Análise de Tipos:
- **Operando 1:** `((TEMP5 X_VAL X_VAL *) *)` → tipo: `real`
    - Operador: `*`
    - Resultado: `real`
- **Operando 2:** `TEMP6` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 11: `(((TEMP6 X_VAL X_VAL *) *) TEMP7)`

### Análise de Tipos:
- **Operando 1:** `((TEMP6 X_VAL X_VAL *) *)` → tipo: `real`
    - Operador: `*`
    - Resultado: `real`
- **Operando 2:** `TEMP7` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 12: `((TEMP7 720.0 |) TEMP8)`

### Análise de Tipos:
- **Operando 1:** `(TEMP7 720.0 |)` → tipo: `real`
    - `TEMP7` : `real`
    - `720.0` : `real`
    - Operador: `|`
    - Resultado: `real`
- **Operando 2:** `TEMP8` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 13: `((0 TEMP8 -) TERM4)`

### Análise de Tipos:
- **Operando 1:** `(0 TEMP8 -)` → tipo: `real`
    - `0` : `int`
    - `TEMP8` : `real`
    - Operador: `-`
    - Resultado: `real`
- **Operando 2:** `TERM4` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 14: `((((TERM1 TERM2 +) TERM3 +) TERM3 +) RESULT_COS)`

### Análise de Tipos:
- **Operando 1:** `(((TERM1 TERM2 +) TERM3 +) TERM3 +)` → tipo: `real`
    - `((TERM1 TERM2 +) TERM3 +)` : `real`
      - `TERM1` : `real`
      - `TERM2` : `real`
      - Operador: `+`
      - Resultado: `real`
    - `TERM3` : `real`
    - Operador: `+`
    - Resultado: `real`
- **Operando 2:** `RESULT_COS` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 15: `(RESULT_COS FINAL_COS)`

### Análise de Tipos:
- **Operando 1:** `RESULT_COS` → tipo: `real`
- **Operando 2:** `FINAL_COS` → tipo: `real`

### Tipo Resultante: `real`

---

## Resumo de Tipos

### Estatísticas
- **Total de expressões:** 15
- **Com tipo definido:** 15
- **Sem tipo definido:** 0
- **Promoções de tipo:** 0

### Distribuição de Tipos
- `real`: 15 expressões (100.0%)

### Tipos Utilizados
- `real`

---
*Relatório gerado automaticamente pelo Compilador RA3_1*

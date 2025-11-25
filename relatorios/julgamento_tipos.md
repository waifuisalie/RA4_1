# Julgamento de Tipos

**Gerado em:** 2025-11-24 23:40:48

**Total de expressões analisadas:** 7

---

## Linha 1: `(0 CONTADOR)`

### Análise de Tipos:
- **Operando 1:** `0` → tipo: `int`
- **Operando 2:** `CONTADOR` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 2: `(5 LIMITE)`

### Análise de Tipos:
- **Operando 1:** `5` → tipo: `int`
- **Operando 2:** `LIMITE` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 3: `(10 X)`

### Análise de Tipos:
- **Operando 1:** `10` → tipo: `int`
- **Operando 2:** `X` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 4: `(20 Y)`

### Análise de Tipos:
- **Operando 1:** `20` → tipo: `int`
- **Operando 2:** `Y` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 5: `((CONTADOR LIMITE <) ((X 1 +) X) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(CONTADOR LIMITE <)` → tipo: `boolean`
    - `CONTADOR` : `int`
    - `LIMITE` : `int`
    - Operador: `<`
    - Resultado: `boolean`
- **Operando 2:** `((X 1 +) X)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```

### Tipo Resultante: `int`

---

## Linha 6: `(X RESULT_X)`

### Análise de Tipos:
- **Operando 1:** `X` → tipo: `int`
- **Operando 2:** `RESULT_X` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 7: `(Y RESULT_Y)`

### Análise de Tipos:
- **Operando 1:** `Y` → tipo: `int`
- **Operando 2:** `RESULT_Y` → tipo: `int`

### Tipo Resultante: `int`

---

## Resumo de Tipos

### Estatísticas
- **Total de expressões:** 7
- **Com tipo definido:** 7
- **Sem tipo definido:** 0
- **Promoções de tipo:** 0

### Distribuição de Tipos
- `int`: 7 expressões (100.0%)

### Tipos Utilizados
- `int`

---
*Relatório gerado automaticamente pelo Compilador RA3_1*

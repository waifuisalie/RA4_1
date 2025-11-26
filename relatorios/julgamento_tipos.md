# Julgamento de Tipos

**Gerado em:** 2025-11-25 22:38:52

**Total de expressões analisadas:** 6

---

## Linha 1: `(1 COUNTER)`

### Análise de Tipos:
- **Operando 1:** `1` → tipo: `int`
- **Operando 2:** `COUNTER` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 2: `(1 RESULT)`

### Análise de Tipos:
- **Operando 1:** `1` → tipo: `int`
- **Operando 2:** `RESULT` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 3: `(8 LIMIT)`

### Análise de Tipos:
- **Operando 1:** `8` → tipo: `int`
- **Operando 2:** `LIMIT` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 4: `((COUNTER LIMIT <=) ((RESULT COUNTER *) RESULT) (COUNTER 1 +) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(COUNTER LIMIT <=)` → tipo: `boolean`
    - `COUNTER` : `int`
    - `LIMIT` : `int`
    - Operador: `<=`
    - Resultado: `boolean`
- **Operando 2:** `((RESULT COUNTER *) RESULT)` → tipo: `int`
- **Operando 3:** `(COUNTER 1 +)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ bloco : T
──────────────────────────────────────────────────
         Γ ⊢ (cond bloco WHILE) : T
```

### Tipo Resultante: `int`

---

## Linha 5: `(RESULT FINAL_RESULT)`

### Análise de Tipos:
- **Operando 1:** `RESULT` → tipo: `int`
- **Operando 2:** `FINAL_RESULT` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 6: `(RESULT FINAL_RESULT)`

### Análise de Tipos:
- **Operando 1:** `RESULT` → tipo: `int`
- **Operando 2:** `FINAL_RESULT` → tipo: `int`

### Tipo Resultante: `int`

---

## Resumo de Tipos

### Estatísticas
- **Total de expressões:** 6
- **Com tipo definido:** 6
- **Sem tipo definido:** 0
- **Promoções de tipo:** 0

### Distribuição de Tipos
- `int`: 6 expressões (100.0%)

### Tipos Utilizados
- `int`

---
*Relatório gerado automaticamente pelo Compilador RA3_1*

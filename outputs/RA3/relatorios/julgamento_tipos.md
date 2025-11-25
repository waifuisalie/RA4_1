# Julgamento de Tipos

**Gerado em:** 2025-11-25 12:24:39

**Total de expressões analisadas:** 6

---

## Linha 1: `(0 FIB_0)`

### Análise de Tipos:
- **Operando 1:** `0` → tipo: `int`
- **Operando 2:** `FIB_0` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 2: `(1 FIB_1)`

### Análise de Tipos:
- **Operando 1:** `1` → tipo: `int`
- **Operando 2:** `FIB_1` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 3: `(2 COUNTER)`

### Análise de Tipos:
- **Operando 1:** `2` → tipo: `int`
- **Operando 2:** `COUNTER` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 4: `(24 LIMIT)`

### Análise de Tipos:
- **Operando 1:** `24` → tipo: `int`
- **Operando 2:** `LIMIT` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 5: `((COUNTER LIMIT <=) (FIB_0 FIB_1 +) (FIB_1) (FIB_NEXT) (COUNTER 1 +) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(COUNTER LIMIT <=)` → tipo: `boolean`
    - `COUNTER` : `int`
    - `LIMIT` : `int`
    - Operador: `<=`
    - Resultado: `boolean`
- **Operando 2:** `(FIB_0 FIB_1 +)` → tipo: `int`
- **Operando 3:** `(FIB_1)` → tipo: `int`
- **Operando 4:** `(FIB_NEXT)` → tipo: `int`
- **Operando 5:** `(COUNTER 1 +)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ bloco : T
──────────────────────────────────────────────────
         Γ ⊢ (cond bloco WHILE) : T
```

### Tipo Resultante: `int`

---

## Linha 6: `(FIB_NEXT RESULT)`

### Análise de Tipos:
- **Operando 1:** `FIB_NEXT` → tipo: `None`
- **Operando 2:** `RESULT` → tipo: `None`

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

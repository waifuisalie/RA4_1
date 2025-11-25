# Julgamento de Tipos

**Gerado em:** 2025-11-24 23:26:07

**Total de expressões analisadas:** 7

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

## Linha 3: `(2 INICIO)`

### Análise de Tipos:
- **Operando 1:** `2` → tipo: `int`
- **Operando 2:** `INICIO` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 4: `(24 FIM)`

### Análise de Tipos:
- **Operando 1:** `24` → tipo: `int`
- **Operando 2:** `FIM` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 5: `(1 PASSO)`

### Análise de Tipos:
- **Operando 1:** `1` → tipo: `int`
- **Operando 2:** `PASSO` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 6: `(INICIO FIM PASSO ((FIB_0 FIB_1 +) FIB_NEXT) FOR)`

### Análise de Tipos:
- **Operando 1:** `INICIO` → tipo: `int`
    - `INICIO` : `int`
- **Operando 2:** `FIM` → tipo: `int`
    - `FIM` : `int`
- **Operando 3:** `PASSO` → tipo: `int`
    - `PASSO` : `int`
- **Operando 4:** `((FIB_0 FIB_1 +) FIB_NEXT)` → tipo: `int`
- **Operador:** `FOR`

### Regra Aplicada:

```
Γ ⊢ init : int    Γ ⊢ end : int    Γ ⊢ step : int    Γ ⊢ corpo : T
────────────────────────────────────────────────────────────────
              Γ ⊢ (init end step corpo FOR) : T
```

### Tipo Resultante: `int`

---

## Linha 7: `(FIB_NEXT RESULT)`

### Análise de Tipos:
- **Operando 1:** `FIB_NEXT` → tipo: `None`
- **Operando 2:** `RESULT` → tipo: `None`

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

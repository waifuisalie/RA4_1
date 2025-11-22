# Julgamento de Tipos

**Gerado em:** 2025-11-22 14:28:51

**Total de expressões analisadas:** 23

---

## Linha 1: `(5 3 +)`

### Análise de Tipos:
- **Operando 1:** `5` → tipo: `int`
    - `5` : `int`
- **Operando 2:** `3` → tipo: `int`
    - `3` : `int`
- **Operador:** `+`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(int, int)
```

### Tipo Resultante: `int`

---

## Linha 2: `(10.5 2.0 *)`

### Análise de Tipos:
- **Operando 1:** `10.5` → tipo: `real`
    - `10.5` : `real`
- **Operando 2:** `2.0` → tipo: `real`
    - `2.0` : `real`
- **Operador:** `*`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : real    (real, real ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ *) : promover_tipo(real, real)
```

### Tipo Resultante: `real`

---

## Linha 3: `(100 50 +)`

### Análise de Tipos:
- **Operando 1:** `100` → tipo: `int`
    - `100` : `int`
- **Operando 2:** `50` → tipo: `int`
    - `50` : `int`
- **Operador:** `+`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(int, int)
```

### Tipo Resultante: `int`

---

## Linha 4: `(15 7 /)`

### Análise de Tipos:
- **Operando 1:** `15` → tipo: `int`
    - `15` : `int`
- **Operando 2:** `7` → tipo: `int`
    - `7` : `int`
- **Operador:** `/`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
    Γ ⊢ (e₁ e₂ /) : int
```

### Tipo Resultante: `int`

### Observação:
Divisão inteira: ambos operandos devem ser `int`, resultado é `int`.

---

## Linha 5: `(23 6 %)`

### Análise de Tipos:
- **Operando 1:** `23` → tipo: `int`
    - `23` : `int`
- **Operando 2:** `6` → tipo: `int`
    - `6` : `int`
- **Operador:** `%`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
    Γ ⊢ (e₁ e₂ %) : int
```

### Tipo Resultante: `int`

### Observação:
Resto da divisão: ambos operandos devem ser `int`, resultado é `int`.

---

## Linha 6: `(2.5 3 ^)`

### Análise de Tipos:
- **Operando 1:** `2.5` → tipo: `real`
    - `2.5` : `real`
- **Operando 2:** `3` → tipo: `int`
    - `3` : `int`
- **Operador:** `^`

### Regra Aplicada:

```
Γ ⊢ e₁ : T    Γ ⊢ e₂ : int    e₂ > 0    (T ∈ {int, real})
──────────────────────────────────────────────────────────
               Γ ⊢ (e₁ e₂ ^) : T
```

### Tipo Resultante: `real`

### Observação:
Tipo promovido de `int` para `real` devido a operando `real`.

### Observação:
Potenciação: expoente deve ser `int` positivo, resultado tem tipo da base.

---

## Linha 7: `(5.5 3.2 >)`

### Análise de Tipos:
- **Operando 1:** `5.5` → tipo: `real`
    - `5.5` : `real`
- **Operando 2:** `3.2` → tipo: `real`
    - `3.2` : `real`
- **Operador:** `>`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : real    (real, real ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ >) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 8: `(3 !)`

### Análise de Tipos:
- **Operando 1:** `3` → tipo: `int`
    - `3` : `int`
- **Operador:** `!`

### Regra Aplicada:

```
Γ ⊢ e : int    (int ∈ {int, real, boolean})
───────────────────────────────────────
       Γ ⊢ (e !) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador lógico: resultado sempre `boolean`. Modo permissivo aceita conversão via truthiness.

---

## Linha 9: `((5 3 >) (2 1 <) &&)`

### Análise de Tipos:
- **Operando 1:** `(5 3 >)` → tipo: `boolean`
    - `5` : `int`
    - `3` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operando 2:** `(2 1 <)` → tipo: `boolean`
    - `2` : `int`
    - `1` : `int`
    - Operador: `<`
    - Resultado: `boolean`
- **Operador:** `&&`

### Regra Aplicada:

```
Γ ⊢ e₁ : boolean    Γ ⊢ e₂ : boolean    (boolean, boolean ∈ {int, real, boolean})
──────────────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ &&) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador lógico: resultado sempre `boolean`. Modo permissivo aceita conversão via truthiness.

---

## Linha 10: `(10 X)`

### Análise de Tipos:
- **Operando 1:** `10` → tipo: `int`
- **Operando 2:** `X` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 11: `(20 A)`

### Análise de Tipos:
- **Operando 1:** `20` → tipo: `int`
- **Operando 2:** `A` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 12: `(10 I)`

### Análise de Tipos:
- **Operando 1:** `10` → tipo: `int`
- **Operando 2:** `I` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 13: `(0 COUNTER)`

### Análise de Tipos:
- **Operando 1:** `0` → tipo: `int`
- **Operando 2:** `COUNTER` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 14: `((X 5 +) Y)`

### Análise de Tipos:
- **Operando 1:** `(X 5 +)` → tipo: `int`
    - `X` : `int`
    - `5` : `int`
    - Operador: `+`
    - Resultado: `int`
- **Operando 2:** `Y` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 15: `((A X -) B)`

### Análise de Tipos:
- **Operando 1:** `(A X -)` → tipo: `int`
    - `A` : `int`
    - `X` : `int`
    - Operador: `-`
    - Resultado: `int`
- **Operando 2:** `B` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 16: `(1)`

### Análise de Tipos:
- **Operando 1:** `1` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 17: `(2)`

### Análise de Tipos:
- **Operando 1:** `2` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 18: `((COUNTER 5 <) ((COUNTER 1 +) COUNTER) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(COUNTER 5 <)` → tipo: `boolean`
    - `COUNTER` : `int`
    - `5` : `int`
    - Operador: `<`
    - Resultado: `boolean`
- **Operando 2:** `((COUNTER 1 +) COUNTER)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```

### Tipo Resultante: `int`

---

## Linha 19: `((B 0 >) ((B 1 -) B) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(B 0 >)` → tipo: `boolean`
    - `B` : `int`
    - `0` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operando 2:** `((B 1 -) B)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```

### Tipo Resultante: `int`

---

## Linha 20: `((1) (10) (1) (I 2 *) FOR)`

### Análise de Tipos:
- **Operando 1:** `(1)` → tipo: `int`
- **Operando 2:** `(10)` → tipo: `int`
- **Operando 3:** `(1)` → tipo: `int`
- **Operando 4:** `(I 2 *)` → tipo: `int`
    - `I` : `int`
    - `2` : `int`
    - Operador: `*`
    - Resultado: `int`
- **Operador:** `FOR`

### Regra Aplicada:

```
Γ ⊢ init : int    Γ ⊢ end : int    Γ ⊢ step : int    Γ ⊢ corpo : T
────────────────────────────────────────────────────────────────
              Γ ⊢ (init end step corpo FOR) : T
```

### Tipo Resultante: `int`

---

## Linha 21: `((X 15 >) (100) (200) IFELSE)`

### Análise de Tipos:
- **Operando 1:** `(X 15 >)` → tipo: `boolean`
    - `X` : `int`
    - `15` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operando 2:** `(100)` → tipo: `int`
- **Operando 3:** `(200)` → tipo: `int`
- **Operador:** `IFELSE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

### Tipo Resultante: `int`

---

## Linha 22: `(((A 10 >) (Y 5 >) &&) ((A Y +) 2.0 |) (A Y *) IFELSE)`

### Análise de Tipos:
- **Operando 1:** `((A 10 >) (Y 5 >) &&)` → tipo: `boolean`
    - Operador: `&&`
    - Resultado: `boolean`
- **Operando 2:** `((A Y +) 2.0 |)` → tipo: `real`
- **Operando 3:** `(A Y *)` → tipo: `int`
- **Operador:** `IFELSE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

### Tipo Resultante: `real`

### Observação:
Tipo promovido de `int` para `real` devido a operando `real`.

---

## Linha 23: `((5 3 +) (2 4 *) *)`

### Análise de Tipos:
- **Operando 1:** `(5 3 +)` → tipo: `int`
    - `5` : `int`
    - `3` : `int`
    - Operador: `+`
    - Resultado: `int`
- **Operando 2:** `(2 4 *)` → tipo: `int`
    - `2` : `int`
    - `4` : `int`
    - Operador: `*`
    - Resultado: `int`
- **Operador:** `*`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ *) : promover_tipo(int, int)
```

### Tipo Resultante: `int`

---

## Resumo de Tipos

### Estatísticas
- **Total de expressões:** 23
- **Com tipo definido:** 23
- **Sem tipo definido:** 0
- **Promoções de tipo:** 2

### Distribuição de Tipos
- `boolean`: 3 expressões (13.0%)
- `int`: 17 expressões (73.9%)
- `real`: 3 expressões (13.0%)

### Tipos Utilizados
- `boolean`
- `int`
- `real`

---
*Relatório gerado automaticamente pelo Compilador RA3_1*

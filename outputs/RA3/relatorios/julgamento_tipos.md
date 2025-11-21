# Julgamento de Tipos

**Gerado em:** 2025-11-21 19:19:06

**Total de expressões analisadas:** 40

---

## Linha 1: `(10 A)`

### Análise de Tipos:
- **Operando 1:** `10` → tipo: `int`
- **Operando 2:** `A` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 2: `(20 B)`

### Análise de Tipos:
- **Operando 1:** `20` → tipo: `int`
- **Operando 2:** `B` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 3: `(5.5 X)`

### Análise de Tipos:
- **Operando 1:** `5.5` → tipo: `real`
- **Operando 2:** `X` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 4: `(3.14 Y)`

### Análise de Tipos:
- **Operando 1:** `3.14` → tipo: `real`
- **Operando 2:** `Y` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 5: `(A B +)`

### Análise de Tipos:
- **Operando 1:** `A` → tipo: `int`
    - `A` : `int`
- **Operando 2:** `B` → tipo: `int`
    - `B` : `int`
- **Operador:** `+`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(int, int)
```

### Tipo Resultante: `int`

---

## Linha 6: `(X Y *)`

### Análise de Tipos:
- **Operando 1:** `X` → tipo: `real`
    - `X` : `real`
- **Operando 2:** `Y` → tipo: `real`
    - `Y` : `real`
- **Operador:** `*`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : real    (real, real ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ *) : promover_tipo(real, real)
```

### Tipo Resultante: `real`

---

## Linha 7: `(A 2 -)`

### Análise de Tipos:
- **Operando 1:** `A` → tipo: `int`
    - `A` : `int`
- **Operando 2:** `2` → tipo: `int`
    - `2` : `int`
- **Operador:** `-`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ -) : promover_tipo(int, int)
```

### Tipo Resultante: `int`

---

## Linha 8: `(B 3 /)`

### Análise de Tipos:
- **Operando 1:** `B` → tipo: `int`
    - `B` : `int`
- **Operando 2:** `3` → tipo: `int`
    - `3` : `int`
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

## Linha 9: `(X 2.0 |)`

### Análise de Tipos:
- **Operando 1:** `X` → tipo: `real`
    - `X` : `real`
- **Operando 2:** `2.0` → tipo: `real`
    - `2.0` : `real`
- **Operador:** `|`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : real    (real, real ∈ {int, real})
───────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ |) : real
```

### Tipo Resultante: `real`

### Observação:
Divisão real: resultado sempre `real`, independente dos tipos dos operandos.

---

## Linha 10: `(10 5.5 +)`

### Análise de Tipos:
- **Operando 1:** `10` → tipo: `int`
    - `10` : `int`
- **Operando 2:** `5.5` → tipo: `real`
    - `5.5` : `real`
- **Operador:** `+`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : real    (int, real ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(int, real)
```

### Tipo Resultante: `real`

### Observação:
Tipo promovido de `int` para `real` devido a operando `real`.

---

## Linha 11: `(3.14 2 *)`

### Análise de Tipos:
- **Operando 1:** `3.14` → tipo: `real`
    - `3.14` : `real`
- **Operando 2:** `2` → tipo: `int`
    - `2` : `int`
- **Operador:** `*`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : int    (real, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ *) : promover_tipo(real, int)
```

### Tipo Resultante: `real`

### Observação:
Tipo promovido de `int` para `real` devido a operando `real`.

---

## Linha 12: `(50.0 10 -)`

### Análise de Tipos:
- **Operando 1:** `50.0` → tipo: `real`
    - `50.0` : `real`
- **Operando 2:** `10` → tipo: `int`
    - `10` : `int`
- **Operador:** `-`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : int    (real, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ -) : promover_tipo(real, int)
```

### Tipo Resultante: `real`

### Observação:
Tipo promovido de `int` para `real` devido a operando `real`.

---

## Linha 13: `(A B >)`

### Análise de Tipos:
- **Operando 1:** `A` → tipo: `int`
    - `A` : `int`
- **Operando 2:** `B` → tipo: `int`
    - `B` : `int`
- **Operador:** `>`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ >) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 14: `(X Y <)`

### Análise de Tipos:
- **Operando 1:** `X` → tipo: `real`
    - `X` : `real`
- **Operando 2:** `Y` → tipo: `real`
    - `Y` : `real`
- **Operador:** `<`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : real    (real, real ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ <) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 15: `(A 10 ==)`

### Análise de Tipos:
- **Operando 1:** `A` → tipo: `int`
    - `A` : `int`
- **Operando 2:** `10` → tipo: `int`
    - `10` : `int`
- **Operador:** `==`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ ==) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 16: `(B 20 >=)`

### Análise de Tipos:
- **Operando 1:** `B` → tipo: `int`
    - `B` : `int`
- **Operando 2:** `20` → tipo: `int`
    - `20` : `int`
- **Operador:** `>=`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ >=) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 17: `(X 5.0 <=)`

### Análise de Tipos:
- **Operando 1:** `X` → tipo: `real`
    - `X` : `real`
- **Operando 2:** `5.0` → tipo: `real`
    - `5.0` : `real`
- **Operador:** `<=`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : real    (real, real ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ <=) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 18: `((A B >) (X Y <) &&)`

### Análise de Tipos:
- **Operando 1:** `(A B >)` → tipo: `boolean`
    - `A` : `int`
    - `B` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operando 2:** `(X Y <)` → tipo: `boolean`
    - `X` : `real`
    - `Y` : `real`
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

## Linha 19: `((A 10 ==) (B 20 >) ||)`

### Análise de Tipos:
- **Operando 1:** `(A 10 ==)` → tipo: `boolean`
    - `A` : `int`
    - `10` : `int`
    - Operador: `==`
    - Resultado: `boolean`
- **Operando 2:** `(B 20 >)` → tipo: `boolean`
    - `B` : `int`
    - `20` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operador:** `||`

### Regra Aplicada:

```
Γ ⊢ e₁ : boolean    Γ ⊢ e₂ : boolean    (boolean, boolean ∈ {int, real, boolean})
──────────────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ ||) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador lógico: resultado sempre `boolean`. Modo permissivo aceita conversão via truthiness.

---

## Linha 20: `((X 5.0 >) !)`

### Análise de Tipos:
- **Operando 1:** `(X 5.0 >)` → tipo: `boolean`
    - `X` : `real`
    - `5.0` : `real`
    - Operador: `>`
    - Resultado: `boolean`
- **Operador:** `!`

### Regra Aplicada:

```
Γ ⊢ e : boolean    (boolean ∈ {int, real, boolean})
───────────────────────────────────────
       Γ ⊢ (e !) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador lógico: resultado sempre `boolean`. Modo permissivo aceita conversão via truthiness.

---

## Linha 21: `((A B <) (X Y >=) &&)`

### Análise de Tipos:
- **Operando 1:** `(A B <)` → tipo: `boolean`
    - `A` : `int`
    - `B` : `int`
    - Operador: `<`
    - Resultado: `boolean`
- **Operando 2:** `(X Y >=)` → tipo: `boolean`
    - `X` : `real`
    - `Y` : `real`
    - Operador: `>=`
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

## Linha 22: `((10 5 >) (3.14 2.0 <) ||)`

### Análise de Tipos:
- **Operando 1:** `(10 5 >)` → tipo: `boolean`
    - `10` : `int`
    - `5` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operando 2:** `(3.14 2.0 <)` → tipo: `boolean`
    - `3.14` : `real`
    - `2.0` : `real`
    - Operador: `<`
    - Resultado: `boolean`
- **Operador:** `||`

### Regra Aplicada:

```
Γ ⊢ e₁ : boolean    Γ ⊢ e₂ : boolean    (boolean, boolean ∈ {int, real, boolean})
──────────────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ ||) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador lógico: resultado sempre `boolean`. Modo permissivo aceita conversão via truthiness.

---

## Linha 23: `((A B +) SUM)`

### Análise de Tipos:
- **Operando 1:** `(A B +)` → tipo: `int`
    - `A` : `int`
    - `B` : `int`
    - Operador: `+`
    - Resultado: `int`
- **Operando 2:** `SUM` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 24: `((X Y *) PRODUCT)`

### Análise de Tipos:
- **Operando 1:** `(X Y *)` → tipo: `real`
    - `X` : `real`
    - `Y` : `real`
    - Operador: `*`
    - Resultado: `real`
- **Operando 2:** `PRODUCT` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 25: `(SUM)`

### Análise de Tipos:
- **Operando 1:** `SUM` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 26: `(PRODUCT)`

### Análise de Tipos:
- **Operando 1:** `PRODUCT` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 27: `((SUM 10 +) RESULT)`

### Análise de Tipos:
- **Operando 1:** `(SUM 10 +)` → tipo: `int`
    - `SUM` : `int`
    - `10` : `int`
    - Operador: `+`
    - Resultado: `int`
- **Operando 2:** `RESULT` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 28: `(RESULT)`

### Análise de Tipos:
- **Operando 1:** `RESULT` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 29: `(100 COUNTER)`

### Análise de Tipos:
- **Operando 1:** `100` → tipo: `int`
- **Operando 2:** `COUNTER` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 30: `(0 INDEX)`

### Análise de Tipos:
- **Operando 1:** `0` → tipo: `int`
- **Operando 2:** `INDEX` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 31: `((A B >) (100) (200) IFELSE)`

### Análise de Tipos:
- **Operando 1:** `(A B >)` → tipo: `boolean`
    - `A` : `int`
    - `B` : `int`
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

## Linha 32: `((X 5.0 <) (10) (20) IFELSE)`

### Análise de Tipos:
- **Operando 1:** `(X 5.0 <)` → tipo: `boolean`
    - `X` : `real`
    - `5.0` : `real`
    - Operador: `<`
    - Resultado: `boolean`
- **Operando 2:** `(10)` → tipo: `int`
- **Operando 3:** `(20)` → tipo: `int`
- **Operador:** `IFELSE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

### Tipo Resultante: `int`

---

## Linha 33: `((SUM 100 >=) (SUM 10 -) (SUM 10 +) IFELSE)`

### Análise de Tipos:
- **Operando 1:** `(SUM 100 >=)` → tipo: `boolean`
    - `SUM` : `int`
    - `100` : `int`
    - Operador: `>=`
    - Resultado: `boolean`
- **Operando 2:** `(SUM 10 -)` → tipo: `int`
- **Operando 3:** `(SUM 10 +)` → tipo: `int`
- **Operador:** `IFELSE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

### Tipo Resultante: `int`

---

## Linha 34: `((COUNTER 50 >) (1) (0) IFELSE)`

### Análise de Tipos:
- **Operando 1:** `(COUNTER 50 >)` → tipo: `boolean`
    - `COUNTER` : `int`
    - `50` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operando 2:** `(1)` → tipo: `int`
- **Operando 3:** `(0)` → tipo: `int`
- **Operador:** `IFELSE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

### Tipo Resultante: `int`

---

## Linha 35: `((COUNTER 100 <) ((COUNTER 1 +) COUNTER) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(COUNTER 100 <)` → tipo: `boolean`
    - `COUNTER` : `int`
    - `100` : `int`
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

## Linha 36: `((INDEX 50 <) ((INDEX 2 +) INDEX) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(INDEX 50 <)` → tipo: `boolean`
    - `INDEX` : `int`
    - `50` : `int`
    - Operador: `<`
    - Resultado: `boolean`
- **Operando 2:** `((INDEX 2 +) INDEX)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```

### Tipo Resultante: `int`

---

## Linha 37: `((A 200 <) ((A 5 +) A) WHILE)`

### Análise de Tipos:
- **Operando 1:** `(A 200 <)` → tipo: `boolean`
    - `A` : `int`
    - `200` : `int`
    - Operador: `<`
    - Resultado: `boolean`
- **Operando 2:** `((A 5 +) A)` → tipo: `int`
- **Operador:** `WHILE`

### Regra Aplicada:

```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```

### Tipo Resultante: `int`

---

## Linha 38: `((1) (10) (1) ((I 1 +) I) FOR)`

### Análise de Tipos:
- **Operando 1:** `(1)` → tipo: `int`
- **Operando 2:** `(10)` → tipo: `int`
- **Operando 3:** `(1)` → tipo: `int`
- **Operando 4:** `((I 1 +) I)` → tipo: `int`
- **Operador:** `FOR`

### Tipo Resultante: `N/A`

---

## Linha 39: `((0) (20) (2) ((J 2 *) J) FOR)`

### Análise de Tipos:
- **Operando 1:** `(0)` → tipo: `int`
- **Operando 2:** `(20)` → tipo: `int`
- **Operando 3:** `(2)` → tipo: `int`
- **Operando 4:** `((J 2 *) J)` → tipo: `int`
- **Operador:** `FOR`

### Tipo Resultante: `N/A`

---

## Linha 40: `((1) (5) (1) ((SUM K +) SUM) FOR)`

### Análise de Tipos:
- **Operando 1:** `(1)` → tipo: `int`
- **Operando 2:** `(5)` → tipo: `int`
- **Operando 3:** `(1)` → tipo: `int`
- **Operando 4:** `((SUM K +) SUM)` → tipo: `int`
- **Operador:** `FOR`

### Tipo Resultante: `N/A`

---

## Resumo de Tipos

### Estatísticas
- **Total de expressões:** 40
- **Com tipo definido:** 37
- **Sem tipo definido:** 3
- **Promoções de tipo:** 3

### Distribuição de Tipos
- `boolean`: 10 expressões (25.0%)
- `int`: 18 expressões (45.0%)
- `real`: 9 expressões (22.5%)

### Tipos Utilizados
- `boolean`
- `int`
- `real`

---
*Relatório gerado automaticamente pelo Compilador RA3_1*

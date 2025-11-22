# Julgamento de Tipos

**Gerado em:** 2025-11-22 16:26:31

**Total de expressões analisadas:** 35

---

## Linha 1: `(5 3.0 +)`

### Análise de Tipos:
- **Operando 1:** `5` → tipo: `int`
    - `5` : `int`
- **Operando 2:** `3.0` → tipo: `real`
    - `3.0` : `real`
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

## Linha 3: `(15 4 -)`

### Análise de Tipos:
- **Operando 1:** `15` → tipo: `int`
    - `15` : `int`
- **Operando 2:** `4` → tipo: `int`
    - `4` : `int`
- **Operador:** `-`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ -) : promover_tipo(int, int)
```

### Tipo Resultante: `int`

---

## Linha 4: `(8.0 2.0 |)`

### Análise de Tipos:
- **Operando 1:** `8.0` → tipo: `real`
    - `8.0` : `real`
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

## Linha 5: `(20 3 /)`

### Análise de Tipos:
- **Operando 1:** `20` → tipo: `int`
    - `20` : `int`
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

## Linha 6: `(17 5 %)`

### Análise de Tipos:
- **Operando 1:** `17` → tipo: `int`
    - `17` : `int`
- **Operando 2:** `5` → tipo: `int`
    - `5` : `int`
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

## Linha 7: `(2 3 ^)`

### Análise de Tipos:
- **Operando 1:** `2` → tipo: `int`
    - `2` : `int`
- **Operando 2:** `3` → tipo: `int`
    - `3` : `int`
- **Operador:** `^`

### Regra Aplicada:

```
Γ ⊢ e₁ : T    Γ ⊢ e₂ : int    e₂ > 0    (T ∈ {int, real})
──────────────────────────────────────────────────────────
               Γ ⊢ (e₁ e₂ ^) : T
```

### Tipo Resultante: `int`

### Observação:
Potenciação: expoente deve ser `int` positivo, resultado tem tipo da base.

---

## Linha 8: `(100 50 +)`

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

## Linha 9: `(5 2 /)`

### Análise de Tipos:
- **Operando 1:** `5` → tipo: `int`
    - `5` : `int`
- **Operando 2:** `2` → tipo: `int`
    - `2` : `int`
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

## Linha 10: `(10 3 %)`

### Análise de Tipos:
- **Operando 1:** `10` → tipo: `int`
    - `10` : `int`
- **Operando 2:** `3` → tipo: `int`
    - `3` : `int`
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

## Linha 11: `(2 3 ^)`

### Análise de Tipos:
- **Operando 1:** `2` → tipo: `int`
    - `2` : `int`
- **Operando 2:** `3` → tipo: `int`
    - `3` : `int`
- **Operador:** `^`

### Regra Aplicada:

```
Γ ⊢ e₁ : T    Γ ⊢ e₂ : int    e₂ > 0    (T ∈ {int, real})
──────────────────────────────────────────────────────────
               Γ ⊢ (e₁ e₂ ^) : T
```

### Tipo Resultante: `int`

### Observação:
Potenciação: expoente deve ser `int` positivo, resultado tem tipo da base.

---

## Linha 12: `(42 X)`

### Análise de Tipos:
- **Operando 1:** `42` → tipo: `int`
- **Operando 2:** `X` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 13: `(3.14 PI)`

### Análise de Tipos:
- **Operando 1:** `3.14` → tipo: `real`
- **Operando 2:** `PI` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 14: `(1 FLAG)`

### Análise de Tipos:
- **Operando 1:** `1` → tipo: `int`
- **Operando 2:** `FLAG` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 15: `(100 COUNTER)`

### Análise de Tipos:
- **Operando 1:** `100` → tipo: `int`
- **Operando 2:** `COUNTER` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 16: `(0 SUM)`

### Análise de Tipos:
- **Operando 1:** `0` → tipo: `int`
- **Operando 2:** `SUM` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 17: `(200 Y)`

### Análise de Tipos:
- **Operando 1:** `200` → tipo: `int`
- **Operando 2:** `Y` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 18: `(300 Z)`

### Análise de Tipos:
- **Operando 1:** `300` → tipo: `int`
- **Operando 2:** `Z` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 19: `(X)`

### Análise de Tipos:
- **Operando 1:** `X` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 20: `(PI)`

### Análise de Tipos:
- **Operando 1:** `PI` → tipo: `real`

### Tipo Resultante: `real`

---

## Linha 21: `(FLAG)`

### Análise de Tipos:
- **Operando 1:** `FLAG` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 22: `(COUNTER)`

### Análise de Tipos:
- **Operando 1:** `COUNTER` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 23: `(SUM)`

### Análise de Tipos:
- **Operando 1:** `SUM` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 24: `(Y)`

### Análise de Tipos:
- **Operando 1:** `Y` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 25: `(Z)`

### Análise de Tipos:
- **Operando 1:** `Z` → tipo: `int`

### Tipo Resultante: `int`

---

## Linha 26: `(5 3 >)`

### Análise de Tipos:
- **Operando 1:** `5` → tipo: `int`
    - `5` : `int`
- **Operando 2:** `3` → tipo: `int`
    - `3` : `int`
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

## Linha 27: `(10.5 2.0 <)`

### Análise de Tipos:
- **Operando 1:** `10.5` → tipo: `real`
    - `10.5` : `real`
- **Operando 2:** `2.0` → tipo: `real`
    - `2.0` : `real`
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

## Linha 28: `(15 15 ==)`

### Análise de Tipos:
- **Operando 1:** `15` → tipo: `int`
    - `15` : `int`
- **Operando 2:** `15` → tipo: `int`
    - `15` : `int`
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

## Linha 29: `(8.0 9.0 !=)`

### Análise de Tipos:
- **Operando 1:** `8.0` → tipo: `real`
    - `8.0` : `real`
- **Operando 2:** `9.0` → tipo: `real`
    - `9.0` : `real`
- **Operador:** `!=`

### Regra Aplicada:

```
Γ ⊢ e₁ : real    Γ ⊢ e₂ : real    (real, real ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ !=) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 30: `(20 10 >=)`

### Análise de Tipos:
- **Operando 1:** `20` → tipo: `int`
    - `20` : `int`
- **Operando 2:** `10` → tipo: `int`
    - `10` : `int`
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

## Linha 31: `(5 7 <=)`

### Análise de Tipos:
- **Operando 1:** `5` → tipo: `int`
    - `5` : `int`
- **Operando 2:** `7` → tipo: `int`
    - `7` : `int`
- **Operador:** `<=`

### Regra Aplicada:

```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int    (int, int ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ <=) : boolean
```

### Tipo Resultante: `boolean`

### Observação:
Operador de comparação: resultado sempre `boolean`.

---

## Linha 32: `((5 3 >) (10 5 <) &&)`

### Análise de Tipos:
- **Operando 1:** `(5 3 >)` → tipo: `boolean`
    - `5` : `int`
    - `3` : `int`
    - Operador: `>`
    - Resultado: `boolean`
- **Operando 2:** `(10 5 <)` → tipo: `boolean`
    - `10` : `int`
    - `5` : `int`
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

## Linha 33: `((2 4 ==) (8 3 >) ||)`

### Análise de Tipos:
- **Operando 1:** `(2 4 ==)` → tipo: `boolean`
    - `2` : `int`
    - `4` : `int`
    - Operador: `==`
    - Resultado: `boolean`
- **Operando 2:** `(8 3 >)` → tipo: `boolean`
    - `8` : `int`
    - `3` : `int`
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

## Linha 34: `((10 0 >) !)`

### Análise de Tipos:
- **Operando 1:** `(10 0 >)` → tipo: `boolean`
    - `10` : `int`
    - `0` : `int`
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

## Linha 35: `(((5 3 +) 2 +))`

### Análise de Tipos:
- **Operando 1:** `((5 3 +) 2 +)` → tipo: `int`
    - `(5 3 +)` : `int`
      - `5` : `int`
      - `3` : `int`
      - Operador: `+`
      - Resultado: `int`
    - `2` : `int`
    - Operador: `+`
    - Resultado: `int`

### Tipo Resultante: `int`

---

## Resumo de Tipos

### Estatísticas
- **Total de expressões:** 35
- **Com tipo definido:** 35
- **Sem tipo definido:** 0
- **Promoções de tipo:** 1

### Distribuição de Tipos
- `boolean`: 9 expressões (25.7%)
- `int`: 21 expressões (60.0%)
- `real`: 5 expressões (14.3%)

### Tipos Utilizados
- `boolean`
- `int`
- `real`

---
*Relatório gerado automaticamente pelo Compilador RA3_1*

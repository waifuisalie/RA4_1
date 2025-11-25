# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-25 01:39:53

## Resumo

- **Total de linhas:** 15
- **Linhas com tipo definido:** 15
- **Linhas sem tipo definido:** 0

## Detalhes da Árvore Atribuída por Linha

### Linha 1

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    LINHA : real [0.5] {numero_real}
    LINHA : real [X_VAL] {variavel}
```

### Linha 2

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    LINHA : real [1.0] {numero_real}
    LINHA : real [TERM1] {variavel}
```

### Linha 3

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (*) : real
      LINHA : real [X_VAL] {variavel}
      LINHA : real [X_VAL] {variavel}
    LINHA : real [TEMP1] {variavel}
```

### Linha 4

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (|) : real
      LINHA : real [TEMP1] {variavel}
      LINHA : real [2.0] {numero_real}
    LINHA : real [TEMP2] {variavel}
```

### Linha 5

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (-) : real
      LINHA : int [0] {numero_inteiro}
      LINHA : real [TEMP2] {variavel}
    LINHA : real [TERM2] {variavel}
```

### Linha 6

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (*) : real
      LINHA : real [X_VAL] {variavel}
      LINHA : real [X_VAL] {variavel}
    LINHA : real [TEMP3] {variavel}
```

### Linha 7

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (*) : real
      ARITH_OP (*) : real
        LINHA : real [TEMP3] {variavel}
        LINHA : real [X_VAL] {variavel}
        LINHA : real [X_VAL] {variavel}
    LINHA : real [TEMP4] {variavel}
```

### Linha 8

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (|) : real
      LINHA : real [TEMP4] {variavel}
      LINHA : real [24.0] {numero_real}
    LINHA : real [TERM3] {variavel}
```

### Linha 9

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (*) : real
      LINHA : real [X_VAL] {variavel}
      LINHA : real [X_VAL] {variavel}
    LINHA : real [TEMP5] {variavel}
```

### Linha 10

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (*) : real
      ARITH_OP (*) : real
        LINHA : real [TEMP5] {variavel}
        LINHA : real [X_VAL] {variavel}
        LINHA : real [X_VAL] {variavel}
    LINHA : real [TEMP6] {variavel}
```

### Linha 11

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (*) : real
      ARITH_OP (*) : real
        LINHA : real [TEMP6] {variavel}
        LINHA : real [X_VAL] {variavel}
        LINHA : real [X_VAL] {variavel}
    LINHA : real [TEMP7] {variavel}
```

### Linha 12

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (|) : real
      LINHA : real [TEMP7] {variavel}
      LINHA : real [720.0] {numero_real}
    LINHA : real [TEMP8] {variavel}
```

### Linha 13

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (-) : real
      LINHA : int [0] {numero_inteiro}
      LINHA : real [TEMP8] {variavel}
    LINHA : real [TERM4] {variavel}
```

### Linha 14

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (+) : real
      ARITH_OP (+) : real
        ARITH_OP (+) : real
          LINHA : real [TERM1] {variavel}
          LINHA : real [TERM2] {variavel}
        LINHA : real [TERM3] {variavel}
      LINHA : real [TERM3] {variavel}
    LINHA : real [RESULT_COS] {variavel}
```

### Linha 15

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    LINHA : real [RESULT_COS] {variavel}
    LINHA : real [FINAL_COS] {variavel}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*
# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-21 18:24:03

## Resumo

- **Total de linhas:** 22
- **Linhas com tipo definido:** 22
- **Linhas sem tipo definido:** 0

## Detalhes da Árvore Atribuída por Linha

### Linha 1

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (+) : int
    LINHA : int [5] {numero_inteiro}
    LINHA : int [3] {numero_inteiro}
```

### Linha 2

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (*) : real
    LINHA : real [10.5] {numero_real}
    LINHA : real [2.0] {numero_real}
```

### Linha 3

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (+) : int
    LINHA : int [100] {numero_inteiro}
    LINHA : int [50] {numero_inteiro}
```

### Linha 4

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (/) : int
    LINHA : int [15] {numero_inteiro}
    LINHA : int [7] {numero_inteiro}
```

### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (%) : int
    LINHA : int [23] {numero_inteiro}
    LINHA : int [6] {numero_inteiro}
```

### Linha 6

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (^) : real
    LINHA : real [2.5] {numero_real}
    LINHA : int [3] {numero_inteiro}
```

### Linha 7

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  COMP_OP (>) : boolean
    LINHA : real [5.5] {numero_real}
    LINHA : real [3.2] {numero_real}
```

### Linha 8

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  LOGIC_OP (&&) : boolean
    COMP_OP (>) : boolean
      LINHA : int [5] {numero_inteiro}
      LINHA : int [3] {numero_inteiro}
    COMP_OP (<) : boolean
      LINHA : int [2] {numero_inteiro}
      LINHA : int [1] {numero_inteiro}
```

### Linha 9

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [10] {numero_inteiro}
    LINHA : int [X] {variavel}
```

### Linha 10

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [20] {numero_inteiro}
    LINHA : int [A] {variavel}
```

### Linha 11

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [10] {numero_inteiro}
    LINHA : int [I] {variavel}
```

### Linha 12

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [0] {numero_inteiro}
    LINHA : int [COUNTER] {variavel}
```

### Linha 13

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    ARITH_OP (+) : int
      LINHA : int [X] {variavel}
      LINHA : int [5] {numero_inteiro}
    LINHA : int [Y] {variavel}
```

### Linha 14

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    ARITH_OP (-) : int
      LINHA : int [A] {variavel}
      LINHA : int [X] {variavel}
    LINHA : int [B] {variavel}
```

### Linha 15

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [1] {numero_inteiro_res}
```

### Linha 16

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [2] {numero_inteiro_res}
```

### Linha 17

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<) : boolean
      LINHA : int [COUNTER] {variavel}
      LINHA : int [5] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA : int [COUNTER] {variavel}
          LINHA : int [1] {numero_inteiro}
        LINHA : int [COUNTER] {variavel}
```

### Linha 18

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (>) : boolean
      LINHA : int [B] {variavel}
      LINHA : int [0] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (-) : int
          LINHA : int [B] {variavel}
          LINHA : int [1] {numero_inteiro}
        LINHA : int [B] {variavel}
```

### Linha 19

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (FOR)
    LINHA
      LINHA : int [1] {numero_inteiro}
    LINHA
      LINHA : int [10] {numero_inteiro}
    LINHA
      LINHA : int [1] {numero_inteiro}
    ARITH_OP (*) : int
      LINHA : int [I] {variavel}
      LINHA : int [2] {numero_inteiro}
```

### Linha 20

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (IFELSE)
    COMP_OP (>) : boolean
      LINHA : int [X] {variavel}
      LINHA : int [15] {numero_inteiro}
    LINHA
      LINHA : int [100] {numero_inteiro}
    LINHA
      LINHA : int [200] {numero_inteiro}
```

### Linha 21

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  CONTROL_OP (IFELSE)
    LOGIC_OP (&&) : boolean
      COMP_OP (>) : boolean
        LINHA : int [A] {variavel}
        LINHA : int [10] {numero_inteiro}
      COMP_OP (>) : boolean
        LINHA : int [Y] {variavel}
        LINHA : int [5] {numero_inteiro}
    LINHA
      ARITH_OP (|) : real
        ARITH_OP (+) : int
          LINHA : int [A] {variavel}
          LINHA : int [Y] {variavel}
        LINHA : real [2.0] {numero_real}
    LINHA
      ARITH_OP (*) : int
        LINHA : int [A] {variavel}
        LINHA : int [Y] {variavel}
```

### Linha 22

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (*) : int
    ARITH_OP (+) : int
      LINHA : int [5] {numero_inteiro}
      LINHA : int [3] {numero_inteiro}
    ARITH_OP (*) : int
      LINHA : int [2] {numero_inteiro}
      LINHA : int [4] {numero_inteiro}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*
# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-21 19:19:06

## Resumo

- **Total de linhas:** 40
- **Linhas com tipo definido:** 37
- **Linhas sem tipo definido:** 3

## Detalhes da Árvore Atribuída por Linha

### Linha 1

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [10] {numero_inteiro}
    LINHA : int [A] {variavel}
```

### Linha 2

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [20] {numero_inteiro}
    LINHA : int [B] {variavel}
```

### Linha 3

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    LINHA : real [5.5] {numero_real}
    LINHA : real [X] {variavel}
```

### Linha 4

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    LINHA : real [3.14] {numero_real}
    LINHA : real [Y] {variavel}
```

### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (+) : int
    LINHA : int [A] {variavel}
    LINHA : int [B] {variavel}
```

### Linha 6

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (*) : real
    LINHA : real [X] {variavel}
    LINHA : real [Y] {variavel}
```

### Linha 7

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (-) : int
    LINHA : int [A] {variavel}
    LINHA : int [2] {numero_inteiro}
```

### Linha 8

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  ARITH_OP (/) : int
    LINHA : int [B] {variavel}
    LINHA : int [3] {numero_inteiro}
```

### Linha 9

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (|) : real
    LINHA : real [X] {variavel}
    LINHA : real [2.0] {numero_real}
```

### Linha 10

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (+) : real
    LINHA : int [10] {numero_inteiro}
    LINHA : real [5.5] {numero_real}
```

### Linha 11

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (*) : real
    LINHA : real [3.14] {numero_real}
    LINHA : int [2] {numero_inteiro}
```

### Linha 12

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  ARITH_OP (-) : real
    LINHA : real [50.0] {numero_real}
    LINHA : int [10] {numero_inteiro}
```

### Linha 13

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  COMP_OP (>) : boolean
    LINHA : int [A] {variavel}
    LINHA : int [B] {variavel}
```

### Linha 14

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  COMP_OP (<) : boolean
    LINHA : real [X] {variavel}
    LINHA : real [Y] {variavel}
```

### Linha 15

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  COMP_OP (==) : boolean
    LINHA : int [A] {variavel}
    LINHA : int [10] {numero_inteiro}
```

### Linha 16

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  COMP_OP (>=) : boolean
    LINHA : int [B] {variavel}
    LINHA : int [20] {numero_inteiro}
```

### Linha 17

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  COMP_OP (<=) : boolean
    LINHA : real [X] {variavel}
    LINHA : real [5.0] {numero_real}
```

### Linha 18

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  LOGIC_OP (&&) : boolean
    COMP_OP (>) : boolean
      LINHA : int [A] {variavel}
      LINHA : int [B] {variavel}
    COMP_OP (<) : boolean
      LINHA : real [X] {variavel}
      LINHA : real [Y] {variavel}
```

### Linha 19

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  LOGIC_OP (||) : boolean
    COMP_OP (==) : boolean
      LINHA : int [A] {variavel}
      LINHA : int [10] {numero_inteiro}
    COMP_OP (>) : boolean
      LINHA : int [B] {variavel}
      LINHA : int [20] {numero_inteiro}
```

### Linha 20

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  LOGIC_OP (!) : boolean
    COMP_OP (>) : boolean
      LINHA : real [X] {variavel}
      LINHA : real [5.0] {numero_real}
```

### Linha 21

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  LOGIC_OP (&&) : boolean
    COMP_OP (<) : boolean
      LINHA : int [A] {variavel}
      LINHA : int [B] {variavel}
    COMP_OP (>=) : boolean
      LINHA : real [X] {variavel}
      LINHA : real [Y] {variavel}
```

### Linha 22

**Tipo Resultado:** `boolean`

**Estrutura da Árvore:**

```
LINHA : boolean
  LOGIC_OP (||) : boolean
    COMP_OP (>) : boolean
      LINHA : int [10] {numero_inteiro}
      LINHA : int [5] {numero_inteiro}
    COMP_OP (<) : boolean
      LINHA : real [3.14] {numero_real}
      LINHA : real [2.0] {numero_real}
```

### Linha 23

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    ARITH_OP (+) : int
      LINHA : int [A] {variavel}
      LINHA : int [B] {variavel}
    LINHA : int [SUM] {variavel}
```

### Linha 24

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    ARITH_OP (*) : real
      LINHA : real [X] {variavel}
      LINHA : real [Y] {variavel}
    LINHA : real [PRODUCT] {variavel}
```

### Linha 25

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [SUM] {variavel}
```

### Linha 26

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    LINHA : real [PRODUCT] {variavel}
```

### Linha 27

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    ARITH_OP (+) : int
      LINHA : int [SUM] {variavel}
      LINHA : int [10] {numero_inteiro}
    LINHA : int [RESULT] {variavel}
```

### Linha 28

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [RESULT] {variavel}
```

### Linha 29

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [100] {numero_inteiro}
    LINHA : int [COUNTER] {variavel}
```

### Linha 30

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [0] {numero_inteiro}
    LINHA : int [INDEX] {variavel}
```

### Linha 31

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (IFELSE)
    COMP_OP (>) : boolean
      LINHA : int [A] {variavel}
      LINHA : int [B] {variavel}
    LINHA
      LINHA : int [100] {numero_inteiro}
    LINHA
      LINHA : int [200] {numero_inteiro}
```

### Linha 32

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (IFELSE)
    COMP_OP (<) : boolean
      LINHA : real [X] {variavel}
      LINHA : real [5.0] {numero_real}
    LINHA
      LINHA : int [10] {numero_inteiro}
    LINHA
      LINHA : int [20] {numero_inteiro}
```

### Linha 33

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (IFELSE)
    COMP_OP (>=) : boolean
      LINHA : int [SUM] {variavel}
      LINHA : int [100] {numero_inteiro}
    LINHA
      ARITH_OP (-) : int
        LINHA : int [SUM] {variavel}
        LINHA : int [10] {numero_inteiro}
    LINHA
      ARITH_OP (+) : int
        LINHA : int [SUM] {variavel}
        LINHA : int [10] {numero_inteiro}
```

### Linha 34

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (IFELSE)
    COMP_OP (>) : boolean
      LINHA : int [COUNTER] {variavel}
      LINHA : int [50] {numero_inteiro}
    LINHA
      LINHA : int [1] {numero_inteiro}
    LINHA
      LINHA : int [0] {numero_inteiro}
```

### Linha 35

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<) : boolean
      LINHA : int [COUNTER] {variavel}
      LINHA : int [100] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA : int [COUNTER] {variavel}
          LINHA : int [1] {numero_inteiro}
        LINHA : int [COUNTER] {variavel}
```

### Linha 36

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<) : boolean
      LINHA : int [INDEX] {variavel}
      LINHA : int [50] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA : int [INDEX] {variavel}
          LINHA : int [2] {numero_inteiro}
        LINHA : int [INDEX] {variavel}
```

### Linha 37

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<) : boolean
      LINHA : int [A] {variavel}
      LINHA : int [200] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA : int [A] {variavel}
          LINHA : int [5] {numero_inteiro}
        LINHA : int [A] {variavel}
```

### Linha 38

**Tipo Resultado:** `None`

**Estrutura da Árvore:**

```
LINHA
  CONTROL_OP (FOR)
    LINHA
      LINHA : int [1] {numero_inteiro}
    LINHA
      LINHA : int [10] {numero_inteiro}
    LINHA
      LINHA : int [1] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA [I] {variavel}
          LINHA : int [1] {numero_inteiro}
        LINHA [I] {variavel}
```

### Linha 39

**Tipo Resultado:** `None`

**Estrutura da Árvore:**

```
LINHA
  CONTROL_OP (FOR)
    LINHA
      LINHA : int [0] {numero_inteiro}
    LINHA
      LINHA : int [20] {numero_inteiro}
    LINHA
      LINHA : int [2] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (*) : int
          LINHA [J] {variavel}
          LINHA : int [2] {numero_inteiro}
        LINHA [J] {variavel}
```

### Linha 40

**Tipo Resultado:** `None`

**Estrutura da Árvore:**

```
LINHA
  CONTROL_OP (FOR)
    LINHA
      LINHA : int [1] {numero_inteiro}
    LINHA
      LINHA : int [5] {numero_inteiro}
    LINHA
      LINHA : int [1] {numero_inteiro}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA : int [SUM] {variavel}
          LINHA [K] {variavel}
        LINHA : int [SUM] {variavel}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*
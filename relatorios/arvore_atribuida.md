# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-24 23:40:48

## Resumo

- **Total de linhas:** 7
- **Linhas com tipo definido:** 7
- **Linhas sem tipo definido:** 0

## Detalhes da Árvore Atribuída por Linha

### Linha 1

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [0] {numero_inteiro}
    LINHA : int [CONTADOR] {variavel}
```

### Linha 2

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [5] {numero_inteiro}
    LINHA : int [LIMITE] {variavel}
```

### Linha 3

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [10] {numero_inteiro}
    LINHA : int [X] {variavel}
```

### Linha 4

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [20] {numero_inteiro}
    LINHA : int [Y] {variavel}
```

### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<) : boolean
      LINHA : int [CONTADOR] {variavel}
      LINHA : int [LIMITE] {variavel}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA : int [X] {variavel}
          LINHA : int [1] {numero_inteiro}
        LINHA : int [X] {variavel}
      LINHA
        ARITH_OP (+) : int
          LINHA : int [X] {variavel}
          LINHA : int [(] {numero_inteiro}
        LINHA [(] {variavel}
      LINHA
        ARITH_OP (+) : int
          LINHA : int [Y] {variavel}
          LINHA : int [2] {numero_inteiro}
        LINHA : int [Y] {variavel}
```

### Linha 6

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [X] {variavel}
    LINHA : int [RESULT_X] {variavel}
```

### Linha 7

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [Y] {variavel}
    LINHA : int [RESULT_Y] {variavel}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*
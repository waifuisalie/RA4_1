# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-25 22:57:40

## Resumo

- **Total de linhas:** 6
- **Linhas com tipo definido:** 6
- **Linhas sem tipo definido:** 0

## Detalhes da Árvore Atribuída por Linha

### Linha 1

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [0] {numero_inteiro}
    LINHA : int [FIB_0] {variavel}
```

### Linha 2

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [1] {numero_inteiro}
    LINHA : int [FIB_1] {variavel}
```

### Linha 3

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [2] {numero_inteiro}
    LINHA : int [COUNTER] {variavel}
```

### Linha 4

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [24] {numero_inteiro}
    LINHA : int [LIMIT] {variavel}
```

### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<=) : boolean
      LINHA : int [COUNTER] {variavel}
      LINHA : int [LIMIT] {variavel}
    LINHA
      ARITH_OP (+) : int
        LINHA : int [FIB_0] {variavel}
        LINHA : int [FIB_1] {variavel}
      LINHA [FIB_NEXT] {variavel}
    LINHA
      LINHA : int [FIB_1] {variavel}
      LINHA : int [FIB_0] {variavel}
    LINHA
      LINHA [FIB_NEXT] {variavel}
      LINHA : int [FIB_1] {variavel}
    LINHA
      ARITH_OP (+) : int
        LINHA : int [COUNTER] {variavel}
        LINHA : int [1] {numero_inteiro}
      LINHA : int [COUNTER] {variavel}
```

### Linha 6

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA [FIB_NEXT] {variavel}
    LINHA [RESULT] {variavel}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*
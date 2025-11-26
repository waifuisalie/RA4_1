# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-25 22:38:52

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
    LINHA : int [1] {numero_inteiro}
    LINHA : int [COUNTER] {variavel}
```

### Linha 2

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [1] {numero_inteiro}
    LINHA : int [RESULT] {variavel}
```

### Linha 3

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [8] {numero_inteiro}
    LINHA : int [LIMIT] {variavel}
```

### Linha 4

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (WHILE)
    COMP_OP (<=) : boolean
      LINHA : int [COUNTER] {variavel}
      LINHA : int [LIMIT] {variavel}
    LINHA
      LINHA
        ARITH_OP (*) : int
          LINHA : int [RESULT] {variavel}
          LINHA : int [COUNTER] {variavel}
        LINHA : int [RESULT] {variavel}
    LINHA
      ARITH_OP (+) : int
        LINHA : int [COUNTER] {variavel}
        LINHA : int [1] {numero_inteiro}
      LINHA : int [COUNTER] {variavel}
```

### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [RESULT] {variavel}
    LINHA : int [FINAL_RESULT] {variavel}
```

### Linha 6

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [RESULT] {variavel}
    LINHA : int [FINAL_RESULT] {variavel}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*
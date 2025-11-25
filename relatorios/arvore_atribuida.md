# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-25 14:16:58

## Resumo

- **Total de linhas:** 4
- **Linhas com tipo definido:** 4
- **Linhas sem tipo definido:** 0

## Detalhes da Árvore Atribuída por Linha

### Linha 1

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  LINHA
    LINHA : real [1.0] {numero_real}
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

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [1] {numero_inteiro}
    LINHA : int [COUNTER] {variavel}
```

### Linha 4

**Tipo Resultado:** `real`

**Estrutura da Árvore:**

```
LINHA : real
  CONTROL_OP (WHILE)
    COMP_OP (<=) : boolean
      LINHA : int [COUNTER] {variavel}
      LINHA : int [1] {numero_inteiro}
    LINHA
      ARITH_OP (*) : real
        LINHA : real [X_VAL] {variavel}
        LINHA : real [X_VAL] {variavel}
      LINHA [X_SQUARE] {variavel}
    LINHA
      LINHA : real [2.0] {numero_real}
      LINHA [FACT_2] {variavel}
    LINHA
      ARITH_OP (|)
        LINHA [X_SQUARE] {variavel}
        LINHA [FACT_2] {variavel}
      LINHA [TEMP2] {variavel}
    LINHA
      ARITH_OP (-) : real
        LINHA : real [0.0] {numero_real}
        LINHA [TEMP2] {variavel}
      LINHA [TERM2] {variavel}
    LINHA
      ARITH_OP (*)
        LINHA [X_SQUARE] {variavel}
        LINHA [X_SQUARE] {variavel}
      LINHA [X_FOURTH] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA : real [4.0] {numero_real}
        LINHA : real [3.0] {numero_real}
      LINHA [TEMP4A] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA [TEMP4A] {variavel}
        LINHA : real [2.0] {numero_real}
      LINHA [TEMP4B] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA [TEMP4B] {variavel}
        LINHA : real [1.0] {numero_real}
      LINHA [FACT_4] {variavel}
    LINHA
      ARITH_OP (|)
        LINHA [X_FOURTH] {variavel}
        LINHA [FACT_4] {variavel}
      LINHA [TERM3] {variavel}
    LINHA
      ARITH_OP (*)
        LINHA [X_FOURTH] {variavel}
        LINHA [X_SQUARE] {variavel}
      LINHA [X_SIXTH] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA : real [6.0] {numero_real}
        LINHA : real [5.0] {numero_real}
      LINHA [TEMP6A] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA [TEMP6A] {variavel}
        LINHA : real [4.0] {numero_real}
      LINHA [TEMP6B] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA [TEMP6B] {variavel}
        LINHA : real [3.0] {numero_real}
      LINHA [TEMP6C] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA [TEMP6C] {variavel}
        LINHA : real [2.0] {numero_real}
      LINHA [TEMP6D] {variavel}
    LINHA
      ARITH_OP (*) : real
        LINHA [TEMP6D] {variavel}
        LINHA : real [1.0] {numero_real}
      LINHA [FACT_6] {variavel}
    LINHA
      ARITH_OP (|)
        LINHA [X_SIXTH] {variavel}
        LINHA [FACT_6] {variavel}
      LINHA [TEMP8] {variavel}
    LINHA
      ARITH_OP (-) : real
        LINHA : real [0.0] {numero_real}
        LINHA [TEMP8] {variavel}
      LINHA [TERM4] {variavel}
    LINHA
      ARITH_OP (+) : real
        LINHA : real [TERM1] {variavel}
        LINHA [TERM2] {variavel}
      LINHA [SUM12] {variavel}
    LINHA
      ARITH_OP (+)
        LINHA [SUM12] {variavel}
        LINHA [TERM3] {variavel}
      LINHA [SUM123] {variavel}
    LINHA
      ARITH_OP (+)
        LINHA [SUM123] {variavel}
        LINHA [TERM4] {variavel}
      LINHA [RESULT_COS] {variavel}
    LINHA
      LINHA [RESULT_COS] {variavel}
      LINHA [FINAL_COS] {variavel}
    LINHA
      ARITH_OP (+) : int
        LINHA : int [COUNTER] {variavel}
        LINHA : int [1] {numero_inteiro}
      LINHA : int [COUNTER] {variavel}
```


---
*Relatório gerado automaticamente pelo Compilador RA3_1*
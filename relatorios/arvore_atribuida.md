# Árvore Sintática Abstrata Atribuída

**Gerado em:** 2025-11-24 23:26:07

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
    LINHA : int [INICIO] {variavel}
```

### Linha 4

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [24] {numero_inteiro}
    LINHA : int [FIM] {variavel}
```

### Linha 5

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  LINHA
    LINHA : int [1] {numero_inteiro}
    LINHA : int [PASSO] {variavel}
```

### Linha 6

**Tipo Resultado:** `int`

**Estrutura da Árvore:**

```
LINHA : int
  CONTROL_OP (FOR)
    LINHA : int [INICIO] {variavel}
    LINHA : int [FIM] {variavel}
    LINHA : int [PASSO] {variavel}
    LINHA
      LINHA
        ARITH_OP (+) : int
          LINHA : int [FIB_0] {variavel}
          LINHA : int [FIB_1] {variavel}
        LINHA [FIB_NEXT] {variavel}
      LINHA
        LINHA [FIB_NEXT] {variavel}
        LINHA : int [FIB_1] {variavel}
      LINHA
        LINHA : int [FIB_1] {variavel}
        LINHA : int [FIB_0] {variavel}
```

### Linha 7

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
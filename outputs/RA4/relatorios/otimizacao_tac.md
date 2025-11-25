# Relatório de Otimizações TAC

## 1. Resumo Executivo
- Instruções antes: 21
- Instruções depois: 20
- Redução: 4.8%
- Temporários eliminados: 1

## 2. Técnicas Implementadas

### 2.1 Constant Folding
**Descrição:** Avalia operações constantes em tempo de compilação, substituindo expressões por seus valores calculados.

**Exemplo:**
Antes:
```
t0 = 2

t1 = 3

t2 = t0 + t1
```
Depois:
```
t2 = 5
```

**Impacto:** 0

### 2.2 Constant Propagation
**Descrição:** Propaga constantes conhecidas, substituindo referências a variáveis constantes por seus valores.

**Exemplo:**
Antes:
```
t0 = 5

t1 = t0 + 3

t2 = t0 * 2
```
Depois:
```
t0 = 5

t1 = 8

t2 = 10
```

**Impacto:** 1

### 2.3 Dead Code Elimination
**Descrição:** Remove instruções que não afetam o resultado final do programa.

**Exemplo:**
Antes:
```
t0 = x + y

t1 = t0 * 2

result = t0 + 1
```
Depois:
```
t0 = x + y

result = t0 + 1
```

**Impacto:** 1

### 2.4 Eliminação de Saltos Redundantes
**Descrição:** Remove saltos desnecessários e rótulos não utilizados.

**Exemplo:**
Antes:
```
goto L1

L1:

t0 = 5
```
Depois:
```
t0 = 5
```

**Impacto:** 0

## 3. Estatísticas Detalhadas
- Número de instruções TAC antes: 21
- Número de instruções TAC depois: 20
- Número de temporários eliminados: 1
- Redução percentual: 4.8%
- Número de iterações até convergência: 2

## 4. Análise do Impacto no Código Assembly Gerado
[Análise pendente - aguardando implementação da geração de Assembly]

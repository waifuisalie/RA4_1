# Gramática de Atributos - Linguagem RPN

**Projeto:** Analisador Semântico - Fase 3
**Grupo:** RA3_1
**Instituição:** PUCPR
**Data de Geração:** 2025-01-19

---

## Índice

1. [Visão Geral](#visão-geral)
2. [Sistema de Tipos](#sistema-de-tipos)
3. [Operadores Aritméticos](#operadores-aritméticos)
4. [Operadores de Comparação](#operadores-de-comparação)
5. [Operadores Lógicos](#operadores-lógicos)
6. [Estruturas de Controle](#estruturas-de-controle)
7. [Comandos Especiais](#comandos-especiais)
8. [Exemplos Completos](#exemplos-completos)

---

## Visão Geral

Esta gramática de atributos define as regras semânticas para a linguagem RPN (Reverse Polish Notation) utilizada no projeto de compiladores. A gramática especifica:

- **Verificação de tipos** para todos os operadores
- **Inferência de tipos** para expressões compostas
- **Coerção automática** de tipos (int → real)
- **Validação de restrições** semânticas
- **Regras de escopo** e inicialização de variáveis

### Notação Utilizada

```
Γ ⊢ e : T
```

- **Γ** (Gamma): Contexto de tipagem (tabela de símbolos)
- **⊢** (turnstile): Relação de derivação semântica
- **e**: Expressão
- **T**: Tipo da expressão

### Tipos Primitivos

| Tipo | Descrição | Pode ser armazenado em MEM? |
|------|-----------|----------------------------|
| `int` | Números inteiros | ✅ Sim |
| `real` | Números de ponto flutuante | ✅ Sim |
| `boolean` | Valores booleanos | ❌ **Não** |

### Hierarquia de Tipos

```
int < real  (int pode ser promovido para real)
boolean     (separado, sem promoção)
```

---

## Atributos da Gramática

Esta gramática utiliza **atributos sintetizados** e **atributos herdados** para realizar a análise semântica durante o parsing.

### Atributos Sintetizados (Bottom-Up)

Calculados **das folhas para a raiz** da árvore sintática:

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `tipo` | string | Tipo inferido da expressão (int, real, boolean) |
| `valor` | any | Valor calculado (quando aplicável, ex: literais) |
| `inicializada` | boolean | Status de inicialização de variável |

**Fluxo:** Operandos → Operadores → Resultado

**Exemplo:**
```
(5 3 +)
  └─ 5: tipo=int, valor=5
  └─ 3: tipo=int, valor=3
  └─ +: tipo=promover_tipo(int,int)=int
```

### Atributos Herdados (Top-Down)

Propagados **da raiz para as folhas** da árvore:

| Atributo | Tipo | Descrição |
|----------|------|-----------|
| `escopo` | Γ (Gamma) | Contexto de tipagem (tabela de símbolos) |
| `linha_atual` | int | Número da linha sendo processada (para RES) |
| `historico_tipos` | dict | Tipos das linhas anteriores (para validar RES) |

**Fluxo:** Contexto Global → Subexpressões → Folhas

**Exemplo:**
```
Linha 1: (5 X)              # X recebe tipo int
Linha 2: (X 3 +)            # Consulta Γ para obter tipo de X
         └─ X: tipo = Γ(X) = int
```

### Funções Auxiliares

**`promover_tipo(T₁, T₂) → T`**
- Retorna o tipo mais abrangente entre T₁ e T₂
- Implementa coerção automática (int → real)

**`truthy(T) → boolean`**
- Converte tipos numéricos para boolean
- 0/0.0 → false, outros → true

**`verificar_inicializacao(var, Γ) → boolean`**
- Valida se variável foi inicializada antes do uso
- Previne erros de "variável não inicializada"

---

## Sistema de Tipos

### Promoção de Tipos

**Função:** `promover_tipo(T₁, T₂) → T`

| T₁ | T₂ | Resultado |
|----|----|-----------|
| int | int | int |
| int | real | real |
| real | int | real |
| real | real | real |

### Conversão Truthiness (Modo Permissivo)

Para operadores lógicos e estruturas de controle:

| Tipo | Valor | Boolean Equivalente |
|------|-------|---------------------|
| int | 0 | false |
| int | ≠ 0 | true |
| real | 0.0 | false |
| real | ≠ 0.0 | true |
| boolean | valor | valor |

---

## Operadores Aritméticos

### 1. Adição (+)

**Sintaxe:** `(A B +)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(T₁, T₂)
```

**Exemplos:**
```
(5 3 +) → tipo: int (5+3=8)
(5.0 3 +) → tipo: real (5.0+3.0=8.0)
(2 3.14 +) → tipo: real (2.0+3.14=5.14)
```

---

### 2. Subtração (-)

**Sintaxe:** `(A B -)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ -) : promover_tipo(T₁, T₂)
```

---

### 3. Multiplicação (*)

**Sintaxe:** `(A B *)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ *) : promover_tipo(T₁, T₂)
```

---

### 4. Divisão Real (|)

**Sintaxe:** `(A B |)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ |) : real
```

**⚠️ Importante:** Resultado é **SEMPRE real**, mesmo se ambos operandos são int.

**Exemplos:**
```
(6 2 |) → tipo: real (resultado: 3.0)
(5 2 |) → tipo: real (resultado: 2.5)
(5.0 2.0 |) → tipo: real (resultado: 2.5)
```

---

### 5. Divisão Inteira (/)

**Sintaxe:** `(A B /)`

**Regra Semântica:**
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
    Γ ⊢ (e₁ e₂ /) : int
```

**⚠️ Restrição Crítica:** AMBOS operandos DEVEM ser int.

**Exemplos Válidos:**
```
(7 2 /) → tipo: int (resultado: 3)
(10 3 /) → tipo: int (resultado: 3)
```

**Erros Semânticos:**
```
(7.0 2 /) → ERRO: operando 1 deve ser int
(7 2.0 /) → ERRO: operando 2 deve ser int
```

---

### 6. Resto da Divisão (%)

**Sintaxe:** `(A B %)`

**Regra Semântica:**
```
Γ ⊢ e₁ : int    Γ ⊢ e₂ : int
─────────────────────────────
    Γ ⊢ (e₁ e₂ %) : int
```

**⚠️ Restrição Crítica:** AMBOS operandos DEVEM ser int.

**Exemplos:**
```
(7 3 %) → tipo: int (resultado: 1)
(10 3 %) → tipo: int (resultado: 1)
```

---

### 7. Potenciação (^)

**Sintaxe:** `(A B ^)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T    Γ ⊢ e₂ : int    e₂ > 0    (T ∈ {int, real})
──────────────────────────────────────────────────────────
               Γ ⊢ (e₁ e₂ ^) : T
```

**Regras:**
- **Base (A):** Pode ser int ou real
- **Expoente (B):** DEVE ser int E positivo (> 0)
- **Resultado:** Mesmo tipo da base

**Exemplos Válidos:**
```
(2 3 ^) → tipo: int (2³ = 8)
(2.5 3 ^) → tipo: real (2.5³ = 15.625)
```

**Erros Semânticos:**
```
(2 3.5 ^) → ERRO: expoente deve ser int
(2 -1 ^) → ERRO: expoente deve ser positivo
(2 0 ^) → ERRO: expoente deve ser positivo
```

---

## Operadores de Comparação

**Operadores:** `>`, `<`, `>=`, `<=`, `==`, `!=`

### Regra Semântica Geral

**Sintaxe:** `(A B op)` onde op ∈ {>, <, >=, <=, ==, !=}

```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
─────────────────────────────────────────────────────
          Γ ⊢ (e₁ e₂ op) : boolean
```

**⚠️ Importante:** Resultado é **SEMPRE boolean**.

### Exemplos

| Expressão | Tipo Resultado | Semântica |
|-----------|---------------|-----------|
| `(5 3 >)` | boolean | 5 > 3 (true) |
| `(5.0 3 <)` | boolean | 5.0 < 3 (false) |
| `(2 2.0 ==)` | boolean | 2 == 2.0 (true) |
| `(x 0 >)` | boolean | x > 0 |

---

## Operadores Lógicos

### Modo Permissivo

Os operadores lógicos aceitam **int, real ou boolean** como operandos.
Valores numéricos são convertidos via **truthiness**.

### 1. AND (&&)

**Sintaxe:** `(A B &&)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real, boolean})
──────────────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ &&) : boolean
```

**Exemplos:**
```
((5 3 >) (x 0 >) &&) → boolean && boolean
(5 3 &&) → truthy(5) && truthy(3) = true && true = true
(0 5 &&) → truthy(0) && truthy(5) = false && true = false
```

---

### 2. OR (||)

**Sintaxe:** `(A B ||)`

**Regra Semântica:**
```
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real, boolean})
──────────────────────────────────────────────────────────────
           Γ ⊢ (e₁ e₂ ||) : boolean
```

**Exemplos:**
```
(0 5 ||) → false || true = true
(0 0 ||) → false || false = false
```

---

### 3. NOT (!)

**Sintaxe:** `(A !)` (unário postfix)

**Regra Semântica:**
```
Γ ⊢ e : T    (T ∈ {int, real, boolean})
───────────────────────────────────────
       Γ ⊢ (e !) : boolean
```

**Exemplos:**
```
((5 3 >) !) → !(true) = false
(5 !) → !(true) = false
(0 !) → !(false) = true
```

---

## Estruturas de Controle

### 1. IFELSE

**Sintaxe:** `(condição blocoTrue blocoFalse IFELSE)`

**Regra Semântica:**
```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
```

**Regras:**
- Condição: Qualquer tipo conversível para boolean
- **Ambos os ramos devem ter o MESMO tipo T**
- Resultado: tipo T

**Exemplos Válidos:**
```
((x 0 >) (x 2 *) (x) IFELSE)
  cond: boolean
  true: int
  false: int
  resultado: int

((5) (3.14) (2.71) IFELSE)
  cond: int (truthy = true)
  true: real
  false: real
  resultado: real
```

**Erro Semântico:**
```
((x 0 >) (5) (3.14) IFELSE)
  ERRO: ramos devem ter o mesmo tipo (int vs real)
```

---

### 2. WHILE

**Sintaxe:** `(condição corpo WHILE)`

**Regra Semântica:**
```
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ corpo : T
──────────────────────────────────────────────────
         Γ ⊢ (cond corpo WHILE) : T
```

**Regras:**
- Condição: Qualquer tipo conversível para boolean
- Corpo: Qualquer tipo T
- **Resultado: tipo da última expressão do corpo**

**Exemplo:**
```
((i 10 <) ((i 1 + i MEM)) WHILE)
  cond: boolean (i < 10)
  corpo: int (resultado do MEM)
  resultado: int
```

---

### 3. FOR

**Sintaxe:** `(inicio fim passo corpo FOR)`

**Regra Semântica:**
```
Γ ⊢ init : int    Γ ⊢ end : int    Γ ⊢ step : int    Γ ⊢ corpo : T
────────────────────────────────────────────────────────────────
              Γ ⊢ (init end step corpo FOR) : T
```

**Regras:**
- **Inicio, fim, passo: DEVEM ser int**
- Corpo: Qualquer tipo T
- **Resultado: tipo da última expressão do corpo**

**Exemplo:**
```
(0 10 1 ((i i +)) FOR)
  init: 0 (int)
  end: 10 (int)
  step: 1 (int)
  corpo: int
  resultado: int
```

**Erro Semântico:**
```
(0.0 10 1 (CORPO) FOR)
  ERRO: inicio deve ser int
```

---

## Comandos Especiais

### 1. Armazenamento em Memória (MEM)

**Sintaxe:** `(valor VARIAVEL)`

**Regra Semântica:**
```
Γ ⊢ e : T    T ∈ {int, real}    Γ[x ↦ (T, initialized)] ⊢ ...
───────────────────────────────────────────────────────────
            Γ ⊢ (e x) : T
```

**⚠️ Restrição Crítica:** Apenas `int` e `real` podem ser armazenados.
**Boolean NÃO pode ser armazenado!**

**Exemplos Válidos:**
```
(5 CONTADOR) → Armazena int 5 em CONTADOR
(3.14 PI) → Armazena real 3.14 em PI
```

**Erro Semântico:**
```
((5 3 >) RESULT) → ERRO: boolean não pode ser armazenado
```

---

### 2. Recuperação de Memória (MEM)

**Sintaxe:** `(VARIAVEL)`

**Regra Semântica:**
```
Γ(x) = (T, initialized)
───────────────────────
    Γ ⊢ (x) : T
```

**⚠️ Restrição Crítica:** Variável DEVE estar inicializada.

**Exemplo Válido:**
```
Linha 1: (5 VAR)     # Inicializa VAR com int 5
Linha 2: (VAR 3 +)   # OK: VAR é int, resultado int
```

**Erro Semântico:**
```
Linha 1: (MEM 3 +)   # ERRO: MEM não foi inicializada
```

---

### 3. Referência a Resultado (RES)

**Sintaxe:**
- `(N RES)` onde N é um **literal inteiro** representando número de linhas atrás
- `(VAR RES)` onde VAR é uma **variável** contendo o offset de linhas

**Regra Semântica (Literal):**
```
Γ ⊢ N : int    N ≥ 0    linha_atual - N ≥ 1    tipo_linha(atual - N) = T
──────────────────────────────────────────────────────────────────────────
                      Γ ⊢ (N RES) : T
```

**Regra Semântica (Variável):**
```
Γ(VAR) = (int, initialized)    VAR ≥ 0    linha_atual - VAR ≥ 1    tipo_linha(atual - VAR) = T
───────────────────────────────────────────────────────────────────────────────────────────────
                               Γ ⊢ (VAR RES) : T
```

**⚠️ Diferença de MEM:** RES **PODE** referenciar resultados boolean.

**Exemplos (Literal):**
```
Linha 1: (5 3 +)        # Resultado: int 8
Linha 2: (1 RES 2 *)    # OK: referencia int literal 1 linha atrás, resultado int 16

Linha 1: (5 3 >)        # Resultado: boolean true
Linha 2: (1 RES !)      # OK: referencia boolean, resultado boolean false
Linha 3: (2 RES 5 +)    # ERRO: boolean + int (incompatível)
```

**Exemplos (Variável):**
```
Linha 1: (5 3 +)           # Resultado: int 8
Linha 2: (1 OFFSET)        # Armazena 1 em OFFSET
Linha 3: (OFFSET RES 2 *)  # OK: OFFSET=1, referencia linha 2 (int 8), resultado int 16

Linha 1: (10 20 +)         # Resultado: int 30
Linha 2: (2 LINHAS_ATRAS)  # Armazena 2 em LINHAS_ATRAS
Linha 3: (50 60 +)         # Resultado: int 110
Linha 4: (LINHAS_ATRAS RES)  # OK: Referencia linha 2 (int 30)
```

---

### 4. Expressão de Identidade (Epsilon)

**Sintaxe:** `(valor)`

**Regra Semântica:**
```
Γ ⊢ e : T
─────────────
 Γ ⊢ (e) : T
```

**Descrição:** Parênteses podem envolver um único valor sem operador. O tipo é preservado inalterado (função identidade). Esta é uma regra especial que permite expressões com um único operando.

---

#### Casos de Uso Detalhados

##### 1. Carga de Memória (Uso Principal)
**Propósito:** Recuperar valor armazenado em variável sem aplicar operação.

```
Linha 1: (10 CONTADOR)      # Armazena 10
Linha 2: (CONTADOR)         # Carrega 10 (via epsilon)
Linha 3: (CONTADOR 5 +)     # Usa valor carregado: 10 + 5 = 15
```

**Análise Semântica:**
- Linha 2: `Γ ⊢ (CONTADOR) : Γ(CONTADOR) = int`
- Epsilon permite acessar variável como expressão completa

##### 2. Agrupamento Explícito de Subexpressões
**Propósito:** Organizar código hierarquicamente sem alterar semântica.

```
Linha 1: (5 3 +)           # Resultado: int 8
Linha 2: ((5 3 +))         # Idêntico via epsilon
Linha 3: ((1 RES) 2 *)     # Epsilon agrupa RES: (8) * 2 = 16
```

**Diferença conceitual:**
- Sem epsilon: `(5 3 +)` → expressão com operador `+`
- Com epsilon: `((5 3 +))` → expressão aninhada dentro de epsilon

##### 3. Literal Direto (Raramente Usado)
**Propósito:** Retornar literal sem operação (válido mas redundante).

```
(5)           # Válido: epsilon retorna int 5
(3.14)        # Válido: epsilon retorna real 3.14
```

**Nota:** Na prática, raramente necessário, mas semanticamente correto.

---

#### Comparação com Outras Construções

| Construção | Sintaxe | Resultado | Usa Epsilon? |
|------------|---------|-----------|--------------|
| Literal puro | `5` | Erro sintático (sem parênteses) | ❌ |
| Epsilon + literal | `(5)` | `int 5` | ✅ |
| Memória + operador | `(X 3 +)` | Depende de X | ❌ |
| Epsilon + memória | `(X)` | Tipo de X | ✅ |
| Expressão completa | `(5 3 +)` | `int 8` | ❌ |
| Epsilon + expressão | `((5 3 +))` | `int 8` | ✅ |

---

#### Exemplos Práticos

**Exemplo 1: Referência indireta via epsilon**
```
Linha 1: (10 X)             # X = 10
Linha 2: (X)                # Carrega X (epsilon)
Linha 3: (2 RES 5 +)        # Usa linha 2: 10 + 5 = 15
```

**Exemplo 2: Estruturas de controle**
```
Linha 1: (5 FLAG)           # FLAG = 5
Linha 2: ((FLAG 0 >) (100) (200) IFELSE)
         # Condição usa epsilon: (FLAG) expandido para FLAG 0 >
```

**Exemplo 3: Compatibilidade com RES**
```
Linha 1: (42)               # Epsilon: literal 42
Linha 2: (1 RES 10 +)       # RES referencia linha 1: 42 + 10 = 52
```

---

#### Distinção: EPSILON vs MEM_LOAD

| Aspecto | EPSILON `(VAR)` | MEM_LOAD Implícito |
|---------|-----------------|---------------------|
| Sintaxe | `(VAR)` como linha completa | `VAR` dentro de expressão `(VAR 3 +)` |
| Semântica | Expressão standalone que retorna valor | Operando de uma expressão maior |
| Tipo | `Γ ⊢ (VAR) : T` | `VAR` contribui tipo T para operador |
| Uso | Linha independente ou em estruturas | Sempre parte de operação |

**Exemplo comparativo:**
```
# EPSILON (expressão completa)
(X)                 # Linha standalone que retorna valor de X

# MEM_LOAD implícito (parte de expressão)
(X 5 +)             # X é operando carregado, não epsilon
```

---

#### Observações Importantes

1. **Necessidade:** Epsilon é essencial para permitir linhas que apenas carregam valores
2. **Validação:** Tipo do operando é preservado (função identidade)
3. **Aninhamento:** Suporta expressões arbitrariamente aninhadas `((((X))))`
4. **Performance:** Semanticamente neutro, sem overhead em runtime

---

## Exemplos Completos

### Exemplo 1: Cálculo com Promoção de Tipos

```
Linha 1: (5 3 +)           # int + int = int (8)
Linha 2: (1 RES 2.5 *)     # int * real = real (20.0)
Linha 3: (2 RES RESULTADO MEM)  # Armazena real 20.0
```

**Análise de Tipos:**
1. Linha 1: `int + int → int`
2. Linha 2: `int * real → real` (promoção)
3. Linha 3: `MEM(real)` ✅ válido

---

### Exemplo 2: Estrutura Condicional

```
Linha 1: (10 X MEM)             # Armazena 10 em X
Linha 2: ((X 0 >) (X 2 *) (X !) IFELSE)
```

**Análise:**
- Condição: `(X 0 >)` → boolean
- Ramo true: `(X 2 *)` → int (10 * 2 = 20)
- Ramo false: `(X !)` → boolean
- ❌ **ERRO:** ramos têm tipos diferentes (int vs boolean)

**Correção:**
```
((X 0 >) (X 2 *) (0) IFELSE)  # Ambos ramos são int
```

---

### Exemplo 3: Loop com Contador

```
Linha 1: (0 SOMA MEM)           # Inicializa SOMA = 0
Linha 2: (0 10 1 ((SOMA 1 RES + SOMA MEM)) FOR)
```

**Análise:**
- Linha 2:
  - Init: 0 (int) ✅
  - End: 10 (int) ✅
  - Step: 1 (int) ✅
  - Corpo: `(SOMA 1 RES + SOMA MEM)`
    - `SOMA + 1 RES` → int + int = int
    - Armazena em SOMA → tipo int
  - Resultado do FOR: int

---

### Exemplo 4: Erro - Boolean em MEM

```
Linha 1: (5 3 >)                # Resultado: boolean
Linha 2: (1 RES CONDICAO MEM)   # ❌ ERRO!
```

**Erro Semântico:**
```
ERRO SEMÂNTICO [Linha 2]: Tipo 'boolean' não pode ser armazenado em memória
Contexto: (1 RES CONDICAO MEM)
```

**Correção - Usar RES ao invés de MEM:**
```
Linha 1: (5 3 >)           # Resultado: boolean
Linha 2: (1 RES !)         # OK: referencia boolean via RES
```

---

### Exemplo 5: Expressão de Identidade (Epsilon)

```
Linha 1: (10 CONTADOR)      # Armazena 10 em CONTADOR
Linha 2: (CONTADOR)         # Acessa CONTADOR sem operação
Linha 3: (5)                # Literal solto (semanticamente neutro)
Linha 4: ((2 3 +))          # Expressão aninhada sem operador externo
```

**Análise de Tipos:**
1. Linha 1: `MEM(int)` → armazena int 10 em CONTADOR ✅
2. Linha 2: `(CONTADOR)` → tipo: int, valor: 10 (carga de memória via epsilon)
3. Linha 3: `(5)` → tipo: int, valor: 5 (literal direto, função identidade)
4. Linha 4: `((2 3 +))` → tipo: int, valor: 5 (aninhamento sem operador)

**Observação:**
- Linha 2 demonstra o uso principal da expressão epsilon: **carregar memória sem operação**
- Linha 3 é tecnicamente válida mas raramente útil (retorna o próprio literal)
- Linha 4 mostra agrupamento explícito de subexpressão

---

## Sumário de Restrições Semânticas

| Operador/Comando | Restrição | Exemplo Inválido |
|------------------|-----------|------------------|
| `/`, `%` | Ambos operandos int | `(5.0 2 /)` |
| `^` | Expoente int > 0 | `(2 3.5 ^)`, `(2 -1 ^)` |
| IFELSE | Ramos mesmo tipo | `((c) (5) (3.14) IFELSE)` |
| FOR | Init/end/step int | `(0.5 10 1 corpo FOR)` |
| MEM Store | Apenas int/real | `((5 3 >) VAR)` |
| MEM Load | Deve estar inicializada | `(UNINIT 3 +)` |

---

## Estatísticas

- **Total de Regras Semânticas:** 23
- **Operadores Aritméticos:** 7
- **Operadores de Comparação:** 6
- **Operadores Lógicos:** 3
- **Estruturas de Controle:** 3
- **Comandos Especiais:** 4 (MEM_STORE, MEM_LOAD, RES, EPSILON)

---

## Estrutura Computacional

Esta gramática de atributos é implementada computacionalmente em Python através do módulo `gramatica_atributos.py`, que define um **dicionário de regras semânticas** organizado por categoria.

### Estrutura do Dicionário de Regras

Cada regra semântica é representada por um dicionário Python com a seguinte estrutura:

```python
{
    'categoria': str,              # 'aritmetico', 'comparacao', 'logico', 'controle', 'comando'
    'operador': str,               # Símbolo do operador ('+', '-', '>', 'IFELSE', etc.)
    'nome': str,                   # Nome descritivo ('soma', 'comparacao_maior', etc.)
    'aridade': int,                # Número de operandos (1 para unário, 2 para binário, etc.)
    'tipos_operandos': list,       # Lista de tipos aceitos para cada operando
    'tipo_resultado': callable,    # Função que calcula o tipo do resultado
    'restricoes': list,            # Lista de restrições semânticas
    'acao_semantica': callable,    # Função que aplica a regra semântica
    'descricao': str,              # Descrição legível da regra
    'regra_formal': str            # Notação formal (Γ ⊢ e : T)
}
```

---

### Exemplo: Regra de Adição

```python
'+': {
    'categoria': 'aritmetico',
    'operador': '+',
    'nome': 'soma',
    'aridade': 2,
    'tipos_operandos': [
        {'int', 'real'},  # Operando 1: int ou real
        {'int', 'real'}   # Operando 2: int ou real
    ],
    'tipo_resultado': lambda op1, op2: promover_tipo(op1['tipo'], op2['tipo']),
    'restricoes': [
        'Ambos operandos devem ser numéricos (int ou real)',
        'Resultado promovido para real se qualquer operando é real'
    ],
    'acao_semantica': lambda op1, op2, tabela: {
        'tipo': promover_tipo(op1['tipo'], op2['tipo']),
        'valor': None,  # Calculado em runtime
        'operandos': [op1, op2]
    },
    'descricao': 'Operador soma com promoção de tipos',
    'regra_formal': '''
Γ ⊢ e₁ : T₁    Γ ⊢ e₂ : T₂    (T₁, T₂ ∈ {int, real})
───────────────────────────────────────────────────────
    Γ ⊢ (e₁ e₂ +) : promover_tipo(T₁, T₂)
    '''
}
```

---

### Exemplo: Regra IFELSE

```python
'IFELSE': {
    'categoria': 'controle',
    'operador': 'IFELSE',
    'nome': 'ifelse',
    'aridade': 3,
    'tipos_operandos': [
        {'int', 'real', 'boolean'},  # Condição (qualquer tipo truthy)
        None,                         # BlocoTrue (qualquer tipo T)
        None                          # BlocoFalse (qualquer tipo T)
    ],
    'tipo_resultado': lambda cond, true_b, false_b:
        true_b['tipo'] if true_b['tipo'] == false_b['tipo'] else 'ERROR',
    'restricoes': [
        'Condição deve ser convertível para boolean (modo permissivo)',
        'Ambos os ramos (true e false) DEVEM ter o MESMO tipo',
        'Resultado tem o tipo dos ramos'
    ],
    'acao_semantica': lambda cond, true_branch, false_branch, tabela: {
        'tipo': true_branch['tipo'] if true_branch['tipo'] == false_branch['tipo'] else None,
        'erro': None if true_branch['tipo'] == false_branch['tipo']
                else 'Ramos do IFELSE devem ter o mesmo tipo',
        'valor': None,
        'operandos': [cond, true_branch, false_branch]
    },
    'descricao': 'Estrutura condicional IFELSE - ramos devem ter mesmo tipo',
    'regra_formal': '''
Γ ⊢ cond : Tcond    truthy(Tcond)    Γ ⊢ true : T    Γ ⊢ false : T
────────────────────────────────────────────────────────────────
           Γ ⊢ (cond true false IFELSE) : T
    '''
}
```

---

### Organização por Categoria

A gramática completa é organizada em 5 categorias principais:

```python
gramatica = {
    'aritmetico': {
        '+': <regra_soma>,
        '-': <regra_subtracao>,
        '*': <regra_multiplicacao>,
        '|': <regra_divisao_real>,
        '/': <regra_divisao_inteira>,
        '%': <regra_resto>,
        '^': <regra_potencia>
    },
    'comparacao': {
        '>': <regra_maior>,
        '<': <regra_menor>,
        '>=': <regra_maior_igual>,
        '<=': <regra_menor_igual>,
        '==': <regra_igual>,
        '!=': <regra_diferente>
    },
    'logico': {
        '&&': <regra_and>,
        '||': <regra_or>,
        '!': <regra_not>
    },
    'controle': {
        'IFELSE': <regra_ifelse>,
        'WHILE': <regra_while>,
        'FOR': <regra_for>
    },
    'comando': {
        'MEM_STORE': <regra_mem_store>,
        'MEM_LOAD': <regra_mem_load>,
        'RES': <regra_res>,
        'EPSILON': <regra_epsilon>
    }
}
```

---

### Estatísticas da Implementação

Ao executar `python gramatica_atributos.py`, obtemos:

```
======================================================================
GRAMÁTICA DE ATRIBUTOS - ESTATÍSTICAS
======================================================================

ARITMETICO: 7 regras
  - +          (soma                 ) - 2 operandos
  - -          (subtracao            ) - 2 operandos
  - *          (multiplicacao        ) - 2 operandos
  - |          (divisao_real         ) - 2 operandos
  - /          (divisao_inteira      ) - 2 operandos
  - %          (resto                ) - 2 operandos
  - ^          (potencia             ) - 2 operandos

COMPARACAO: 6 regras
  - >          (maior                ) - 2 operandos
  - <          (menor                ) - 2 operandos
  - >=         (maior_igual          ) - 2 operandos
  - <=         (menor_igual          ) - 2 operandos
  - ==         (igual                ) - 2 operandos
  - !=         (diferente            ) - 2 operandos

LOGICO: 3 regras
  - &&         (and                  ) - 2 operandos
  - ||         (or                   ) - 2 operandos
  - !          (not                  ) - 1 operandos

CONTROLE: 3 regras
  - IFELSE     (ifelse               ) - 3 operandos
  - WHILE      (while                ) - 2 operandos
  - FOR        (for                  ) - 4 operandos

COMANDO: 4 regras
  - MEM_STORE  (mem_store            ) - 2 operandos
  - MEM_LOAD   (mem_load             ) - 1 operandos
  - RES        (res                  ) - 1 operandos
  - EPSILON    (identidade           ) - 1 operandos

======================================================================
TOTAL: 23 regras semânticas definidas
======================================================================
```

---

### Funções Principais da API

**`definirGramaticaAtributos() → Dict`**
- Retorna o dicionário completo de regras semânticas
- Combina todas as categorias (aritmetico, comparacao, logico, controle, comando)

**`obter_regra(operador: str, categoria: Optional[str]) → RegraSemantica`**
- Busca a regra semântica de um operador específico
- Retorna None se operador não encontrado

**`inicializar_sistema_semantico() → tuple[Dict, TabelaSimbolos]`**
- Inicializa gramática + tabela de símbolos
- Retorna tupla (gramatica, tabela)

---

## Integração com Sistema Semântico

A gramática de atributos é o **núcleo teórico** do analisador semântico, integrando-se com os demais módulos do compilador.

### Pipeline Completo do Compilador

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: ANÁLISE LÉXICA (RA1)                                    │
│ Input: arquivo.txt                                              │
│ Output: tokens_gerados.txt                                      │
│ Módulo: src/RA1/functions/python/rpn_calc.py                   │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: ANÁLISE SINTÁTICA (RA2)                                 │
│ Input: tokens_gerados.txt                                       │
│ Output: arvore_sintatica.json                                   │
│ Módulo: src/RA2/functions/python/parsear.py                    │
│ Gramática: LL(1) com 37 produções                              │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: ANÁLISE SEMÂNTICA (RA3) ← GRAMÁTICA DE ATRIBUTOS       │
│ Input: arvore_sintatica.json                                    │
│ Output: arvore_atribuida.json + 4 relatórios .md               │
│ Módulo: src/RA3/functions/python/analisador_semantico.py       │
│                                                                  │
│ Sub-fases:                                                      │
│   1. Análise de Tipos (aplica regras desta gramática)          │
│   2. Análise de Memória (valida MEM/RES)                       │
│   3. Análise de Controle (valida IFELSE/WHILE/FOR)             │
│                                                                  │
│ Utiliza: gramatica_atributos.py (este documento)               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ GERAÇÃO DE RELATÓRIOS                                           │
│ Módulo: src/RA3/functions/python/gerador_arvore_atribuida.py   │
│                                                                  │
│ Saídas geradas:                                                 │
│   • arvore_atribuida.md - AST com tipos anotados               │
│   • julgamento_tipos.md - Tipos inferidos por linha            │
│   • erros_sematicos.md - Erros encontrados                     │
│   • tabela_simbolos.md - Variáveis e seus tipos                │
│   • gramatica_atributos.md - Este documento (manual)           │
└─────────────────────────────────────────────────────────────────┘
```

---

### Como as Regras São Aplicadas

**Exemplo: Linha `(5 3 +)` sendo analisada**

1. **Parser (RA2)** gera AST:
```json
{
  "tipo": "LINHA",
  "filhos": [
    {"tipo": "OPERANDO", "valor": 5},
    {"tipo": "OPERANDO", "valor": 3},
    {"tipo": "ARITH_OP", "operador": "+"}
  ]
}
```

2. **Analisador Semântico (RA3)** aplica regras:
```python
# Busca regra para operador '+'
regra = obter_regra('+', 'aritmetico')

# Infere tipo dos operandos
op1 = {'tipo': 'int', 'valor': 5}
op2 = {'tipo': 'int', 'valor': 3}

# Aplica acao_semantica da regra
resultado = regra['acao_semantica'](op1, op2, tabela_simbolos)
# resultado = {'tipo': 'int', 'valor': None, 'operandos': [op1, op2]}
```

3. **Gerador de Relatórios** documenta:
```markdown
Linha 1: (5 3 +)
Tipo Inferido: int
Regra Aplicada: ADIÇÃO (promover_tipo(int, int) = int)
```

---

### Relação com Outros Relatórios

| Relatório | Utiliza Gramática? | Descrição |
|-----------|-------------------|-----------|
| `arvore_atribuida.md` | ✅ Sim | Mostra AST com tipos inferidos usando as regras |
| `julgamento_tipos.md` | ✅ Sim | Lista tipos por linha (resultado da aplicação das regras) |
| `erros_sematicos.md` | ✅ Sim | Erros quando regras são violadas |
| `tabela_simbolos.md` | 🔄 Parcial | Atualizada por MEM_STORE (regra 'comando') |
| `gramatica_atributos.md` | ➖ Base | **Este documento** - define as regras |

---

### Fluxo de Dados Simplificado

```
AST (RA2)
   │
   ├──> Operando 1 ──┐
   ├──> Operando 2 ──┼──> obter_regra(operador)
   └──> Operador ────┘            │
                                   ▼
                          aplica 'acao_semantica'
                                   │
                     ┌─────────────┴────────────┐
                     ▼                          ▼
            infere 'tipo_resultado'    valida 'restricoes'
                     │                          │
                     ▼                          ▼
              Árvore Atribuída            Erros Semânticos
                     │                          │
                     └──────────┬───────────────┘
                                ▼
                          Relatórios .md
```

---

### Referências Cruzadas

- **Implementação completa:** `src/RA3/functions/python/gramatica_atributos.py`
- **Aplicação das regras:** `src/RA3/functions/python/analisador_semantico.py`
- **Sistema de tipos:** `src/RA3/functions/python/tipos.py`
- **Tabela de símbolos:** `src/RA3/functions/python/tabela_simbolos.py`
- **Resultados da análise:** `outputs/RA3/relatorios/julgamento_tipos.md`

---

**Documento gerado automaticamente a partir de:** `gramatica_atributos.py`
**Copyright © 2025 Grupo RA3_1 - PUCPR**

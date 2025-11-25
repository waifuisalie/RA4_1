# Compilador RA4 - Geração e Otimização de TAC EM DESENVOLVIMENTO

## Informações Institucionais

**Disciplina:** Compiladores
**Fase:** RA4 - Geração de Código Intermediário e Otimização
**Instituição:** PUCPR

### Integrantes do Grupo (Ordem Alfabética)

- **Breno Rossi Duarte** - [@breno-rossi](https://github.com/breno-rossi)
- **Francisco Bley Ruthes** - [@fbleyruthes](https://github.com/fbleyruthes)
- **Rafael Olivare Piveta** - [@RafaPiveta](https://github.com/RafaPiveta)
- **Stefan Benjamim Seixas Lourenço Rodrigues** - [@waifuisalie](https://github.com/waifuisalie)

**Nome do Grupo no Canvas:** RA4_1

---

## Visão Geral do Projeto

Este projeto implementa um compilador completo com 4 fases principais:

1. **RA1 - Análise Léxica:** Tokenização de expressões
2. **RA2 - Análise Sintática:** Parser LL(1) com geração de AST
3. **RA3 - Análise Semântica:** Verificação de tipos, memória e controle de fluxo
4. **RA4 - Geração e Otimização de TAC:** Código intermediário otimizado (Three Address Code)

O compilador processa uma linguagem baseada em notação prefixada com parênteses e gera código TAC otimizado, preparando-se para futura geração de código Assembly AVR para Arduino Uno.

---

## Estrutura do Projeto

```
RA4_1/
├── compilador.py              # Orquestrador principal do compilador
├── src/
│   ├── RA1/                   # Análise Léxica
│   │   └── functions/python/
│   │       ├── io_utils.py
│   │       ├── rpn_calc.py
│   │       └── tokens.py
│   ├── RA2/                   # Análise Sintática
│   │   └── functions/python/
│   │       ├── construirGramatica.py
│   │       ├── construirTabelaLL1.py
│   │       ├── gerarArvore.py
│   │       ├── lerTokens.py
│   │       └── parsear.py
│   ├── RA3/                   # Análise Semântica
│   │   └── functions/python/
│   │       ├── analisador_semantico.py
│   │       ├── analisador_tipos.py
│   │       └── gerador_arvore_atribuida.py
│   └── RA4/                   # Geração e Otimização de TAC
│       └── functions/python/
│           ├── gerador_tac.py          # Geração de TAC
│           ├── otimizador_tac.py       # Otimizações
│           ├── ast_traverser.py        # Travessia pós-ordem da AST
│           ├── tac_manager.py          # Gerenciamento de temps e labels
│           └── tac_instructions.py     # Definição de instruções TAC
├── inputs/RA4/                # Arquivos de teste
│   ├── fatorial.txt
│   ├── fibonacci.txt
│   ├── fibonacci_desenrolado.txt
│   └── taylor.txt
├── outputs/                   # Saídas de cada fase
│   ├── RA1/tokens/
│   ├── RA2/
│   ├── RA3/relatorios/
│   └── RA4/
│       ├── tac_instructions.json
│       ├── tac_output.md
│       ├── tac_otimizado.json
│       ├── tac_otimizado.md
│       └── relatorios/
│           └── otimizacao_tac.md
└── docs/                      # Documentação técnica
```

---

## Requisitos do Sistema

### Dependências

- **Python 3.8+**
- **Bibliotecas Python:**
  - `json` (built-in)
  - `pathlib` (built-in)
  - `typing` (built-in)


---

## Instruções de Compilação e Execução

### 1. Execução Completa (Todas as Fases)

O compilador executa automaticamente as 4 fases em sequência:

```bash
python compilador.py <arquivo_de_entrada>
```

**Exemplo:**
```bash
python compilador.py inputs/RA4/fatorial.txt
```

### 2. Fluxo de Execução

Quando você executa o comando acima, o compilador realiza:

#### **Fase 1: Tokenização (RA1)**
- Entrada: Arquivo `.txt` com expressões
- Saída: `outputs/RA1/tokens/tokens_gerados.txt`
- Ação: Converte código fonte em tokens

#### **Fase 2: Análise Sintática (RA2)**
- Entrada: Tokens do RA1
- Saída: `outputs/RA2/arvore_sintatica.json`
- Ações:
  - Valida tokens
  - Constrói gramática LL(1)
  - Gera tabela de parsing
  - Cria AST (Árvore Sintática Abstrata)

#### **Fase 3: Análise Semântica (RA3)**
- Entrada: AST do RA2
- Saída: `outputs/RA3/arvore_atribuida.json` + Relatórios
- Ações:
  - Verifica tipos (type checking)
  - Valida acesso à memória
  - Verifica estruturas de controle
  - Gera árvore atribuída com anotações de tipo

Relatórios gerados:
- `arvore_atribuida.md` - Árvore com tipos inferidos
- `julgamento_tipos.md` - Decisões de tipagem
- `erros_sematicos.md` - Erros encontrados
- `tabela_simbolos.md` - Variáveis e tipos

#### **Fase 4: Geração de TAC (RA4)**
- Entrada: Árvore atribuída do RA3
- Saída: `outputs/RA4/tac_instructions.json` e `tac_output.md`
- Ação: Gera código TAC (Three Address Code)

#### **Fase 5: Otimização de TAC (RA4)**
- Entrada: TAC gerado
- Saída: `outputs/RA4/tac_otimizado.json`, `tac_otimizado.md` e relatórios
- Ação: Aplica 4 técnicas de otimização

### 3. Saída do Compilador

O programa exibe um resumo de cada fase:

```
Arquivo de teste: fatorial.txt

--- TOKENIZAÇÃO (RA1 Lexical Analysis - Input for RA2/RA3) ---
  [OK] 6 linha(s) tokenizadas
  [OK] Tokens salvos em: outputs\RA1\tokens\tokens_gerados.txt

--- PROCESSAMENTO DE TOKENS PARA RA2 ---
Tokens processados: 41 tokens
Validação dos tokens: SUCESSO

--- ANALISE SINTATICA - GRAMATICA ---
[Gramática LL(1) exibida...]

--- RA3: ANÁLISE SEMÂNTICA ---
    [OK] Análise semântica concluída com sucesso sem nenhum erro

--- RA4: GERAÇÃO DE TAC ---
    [OK] 17 instruções TAC geradas
    [OK] Arquivos salvos em: outputs\RA4

--- RA4: OTIMIZAÇÃO DE TAC ---
    [OK] TAC otimizado com sucesso
    [OK] Instruções originais: 17
    [OK] Instruções otimizadas: 12
    [OK] Redução: 29.4%
```

### 4. Arquivos de Saída Importantes


1. **TAC Original:** `outputs/RA4/tac_output.md`
2. **TAC Otimizado:** `outputs/RA4/tac_otimizado.md`
3. **Relatório de Otimização:** `outputs/RA4/relatorios/otimizacao_tac.md`
4. **Árvore Atribuída:** `outputs/RA3/relatorios/arvore_atribuida.md`

---

## Técnicas de Otimização Implementadas

O otimizador TAC (`otimizador_tac.py`) implementa **4 técnicas clássicas de otimização** aplicadas em **múltiplas passadas** até atingir um ponto fixo (convergência).

### Algoritmo Multi-Pass

```
iteração = 0
mudou = True

while mudou and iteração < 100:
    iteração++
    mudou = False

    if constant_folding():        mudou = True
    if constant_propagation():    mudou = True
    if dead_code_elimination():   mudou = True
    if jump_elimination():        mudou = True
```

### 1. Constant Folding (Dobramento de Constantes)

**Descrição:** Avalia expressões constantes em tempo de compilação.

**Exemplo:**
```
Antes:
  t0 = 5
  t1 = 3
  t2 = t0 + t1    # Ambos operandos são constantes

Depois:
  t0 = 5
  t1 = 3
  t2 = 8          # Expressão avaliada
```

**Operações suportadas:**
- Aritméticas: `+`, `-`, `*`, `/` (divisão inteira), `%` (resto), `^` (potência)
- Comparação: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Lógicas: `&&` (AND), `||` (OR), `!` (NOT)

**Benefícios:**
- Reduz número de operações em runtime
- Elimina temporários desnecessários
- Melhora desempenho de loops com constantes

### 2. Constant Propagation (Propagação de Constantes)

**Descrição:** Substitui referências a variáveis constantes por seus valores literais.

**Exemplo:**
```
Antes:
  t1 = 5
  t2 = t1 + 3     # t1 é constante conhecida
  t3 = t1 * 2     # t1 é constante conhecida

Depois:
  t1 = 5
  t2 = 5 + 3      # t1 substituído por 5
  t3 = 5 * 2      # t1 substituído por 5
```

**Combinação com Constant Folding:**
```
Pass 1 (Propagation):
  t2 = 5 + 3
  t3 = 5 * 2

Pass 2 (Folding):
  t2 = 8          # 5 + 3 avaliado
  t3 = 10         # 5 * 2 avaliado
```

**Benefícios:**
- Cria oportunidades para constant folding
- Simplifica expressões complexas
- Reduz dependências entre instruções

### 3. Dead Code Elimination (Eliminação de Código Morto)

**Descrição:** Remove instruções cujo resultado nunca é usado.

**Algoritmo:**
1. Marca todas as instruções como "mortas"
2. Percorre código para trás (backward pass)
3. Marca como "vivas" variáveis usadas
4. Remove instruções não marcadas

**Exemplo:**
```
Antes:
  t0 = 5          # t0 nunca é usado
  t1 = 3
  t2 = t1 + 10
  RESULT = t2

Depois:
  t1 = 3          # t0 removido
  t2 = t1 + 10
  RESULT = t2
```

**Casos especiais (não remove):**
- Atribuições a variáveis do usuário (ex: `RESULT`, `X`, `FIB_NEXT`)
- Labels (rótulos de fluxo de controle)
- Instruções de salto (`goto`, `ifFalse goto`)

**Benefícios:**
- Reduz tamanho do código
- Elimina temporários intermediários
- Melhora cache de instruções

### 4. Jump Elimination (Eliminação de Saltos)

**Descrição:** Remove saltos redundantes e labels não utilizados.

**Otimizações aplicadas:**

#### 4.1 Remoção de Saltos para Próxima Instrução
```
Antes:
  goto L1
  L1:             # Label logo após o goto

Depois:
  L1:             # goto removido
```

#### 4.2 Remoção de Labels Não Referenciados
```
Antes:
  L0:             # Usado
    x = 5
  L1:             # Nunca referenciado
    y = 10
  goto L0

Depois:
  L0:
    x = 5
    y = 10        # L1 removido
  goto L0
```

#### 4.3 Encadeamento de Saltos
```
Antes:
  goto L1
  ...
  L1:
    goto L2

Depois:
  goto L2         # Pula direto para L2
  ...
  L1:
    goto L2
```

**Benefícios:**
- Reduz overhead de saltos
- Melhora pipeline de CPU
- Simplifica fluxo de controle

### Estatísticas de Otimização

Para cada arquivo de teste, o otimizador gera relatório detalhado:

**Exemplo (`fatorial.txt`):**
```markdown
## Estatísticas Gerais

- **Instruções originais:** 17
- **Instruções otimizadas:** 12
- **Redução:** 29.4%
- **Iterações:** 2

```

### Convergência Multi-Pass

O otimizador itera até que **nenhuma otimização produza mudanças** (ponto fixo):

**Exemplo de convergência (3 iterações):**
```
Iteração 1: 17 → 14 instruções (folding: 2, propagation: 1)
Iteração 2: 14 → 12 instruções (dead code: 2)
Iteração 3: 12 → 12 instruções (nenhuma mudança) → FIM
```

---

## Convenções de Registradores AVR

### Visão Geral

O compilador segue convenções padrão AVR para ATmega328P (Arduino Uno), preparando-se para futura geração de código Assembly.

### Mapa de Alocação de Registradores

| Registrador(es) | Uso | Descrição |
|----------------|-----|-----------|
| **R0-R1** | Reservado | Resultado de multiplicação (`mul`) |
| **R2-R15** | Salvos | Preservados entre chamadas de função |
| **R16-R23** | Temporários | Variáveis temporárias e computação geral |
| **R24-R25** | Parâmetros/Retorno | Parâmetros de função e valores de retorno (16-bit) |
| **R26-R27 (X)** | Ponteiro | Acesso à memória (load/store) |
| **R28-R29 (Y)** | Frame Pointer | Acesso a variáveis locais no stack frame |
| **R30-R31 (Z)** | Stack Pointer | Ponteiro de pilha (gerenciado pelo sistema) |

### Exemplo de Uso

**TAC:**
```
t0 = 5
t1 = 3
t2 = t0 + t1
RESULT = t2
```

**Assembly AVR:**
```asm
    ; TAC: t0 = 5
    ldi r16, 5          ; t0 → R16

    ; TAC: t1 = 3
    ldi r17, 3          ; t1 → R17

    ; TAC: t2 = t0 + t1
    add r16, r17        ; t2 → R16 (reutiliza)

    ; TAC: RESULT = t2
    sts RESULT, r16     ; Store to memory
```

### Operações de Memória

**Load (ler da memória):**
```asm
    ldi r26, lo8(VARIABLE)    ; X pointer low byte
    ldi r27, hi8(VARIABLE)    ; X pointer high byte
    ld r16, X                 ; Load from [X] to r16
```

**Store (escrever na memória):**
```asm
    ldi r26, lo8(VARIABLE)    ; X pointer low byte
    ldi r27, hi8(VARIABLE)    ; X pointer high byte
    st X, r16                 ; Store r16 to [X]
```

### Limitações e Spilling

Quando os 8 registradores temporários (R16-R23) são insuficientes:

1. **Identificar variável menos usada** (heurística: variável não usada no bloco atual)
2. **Spill para memória:** `st X, rN`
3. **Liberar registrador** para nova variável
4. **Reload quando necessário:** `ld rN, X`

---

## Exemplos de Uso e Resultados Esperados

### Exemplo 1: Fatorial (fatorial.txt)

**Entrada:**
```
# Inicializar contador = 1
(1 COUNTER)
# Inicializar resultado = 1
(1 RESULT)
# Inicializar limite = 12
(12 LIMIT)

# Laço WHILE: enquanto COUNTER <= LIMIT
# Corpo: RESULT = RESULT * COUNTER, COUNTER = COUNTER + 1
((COUNTER LIMIT <=) (((RESULT COUNTER *) RESULT)) ((COUNTER 1 +) COUNTER) WHILE)
```

**Descrição:** Calcula 12! (fatorial de 12) usando loop WHILE com múltiplas instruções no corpo.

**Algoritmo:**
- COUNTER = 1, RESULT = 1, LIMIT = 12 (inicialização)
- Loop WHILE enquanto COUNTER ≤ LIMIT:
  1. RESULT = RESULT * COUNTER (multiplicação acumulada)
  2. COUNTER = COUNTER + 1 (incremento)
- Resultado final: 12! = 479,001,600

**Execução:**
```bash
python compilador.py inputs/RA4/fatorial.txt
```

**Estrutura do TAC Gerado:**
```
Line 1: COUNTER = 1
Line 2: RESULT = 1
Line 3: LIMIT = 12
Line 4: L0:                        # Início do loop
Line 4: t3 = COUNTER <= LIMIT      # Testa condição
Line 4: ifFalse t3 goto L1         # Sai se falso
Line 4: t4 = RESULT * COUNTER      # Multiplicação
Line 4: RESULT = t4
Line 4: t6 = COUNTER + 1           # Incremento
Line 4: COUNTER = t6
Line 4: goto L0                    # Volta ao início
Line 4: L1:                        # Fim do loop
```

**Estatísticas:**
- Instruções TAC: **16**
- Temporários gerados: **7** (t0-t6)
- Labels gerados: **2** (L0, L1)
- Iterações executadas: **12**

**Valor Final:** `RESULT = 479,001,600` (12! correto) 

---

### Exemplo 2: Fibonacci (fibonacci.txt)

**Entrada:**
```
(0 FIB_0)
(1 FIB_1)
(2 COUNTER)
(24 LIMIT)
((COUNTER LIMIT <=) ((FIB_0 FIB_1 +) FIB_NEXT) (FIB_1 FIB_0) (FIB_NEXT FIB_1) ((COUNTER 1 +) COUNTER) WHILE)
(FIB_NEXT RESULT)
```

**Descrição:** Sequência de Fibonacci até F(24) usando loop WHILE com janela deslizante.

**Algoritmo:**
- FIB_0 = 0, FIB_1 = 1, COUNTER = 2, LIMIT = 24 (inicialização)
- Loop WHILE enquanto COUNTER ≤ LIMIT (23 iterações):
  1. FIB_NEXT = FIB_0 + FIB_1 (calcula próximo termo)
  2. FIB_0 = FIB_1 (desloca janela)
  3. FIB_1 = FIB_NEXT (desloca janela)
  4. COUNTER = COUNTER + 1 (incremento)
- RESULT = FIB_NEXT (armazena resultado final)

**Execução:**
```bash
python compilador.py inputs/RA4/fibonacci.txt
```

**Estrutura do TAC Gerado:**
```
Line 1: FIB_0 = 0
Line 2: FIB_1 = 1
Line 3: COUNTER = 2
Line 4: LIMIT = 24
Line 5: L0:                           # Início do loop
Line 5: t4 = COUNTER <= LIMIT         # Testa condição
Line 5: ifFalse t4 goto L1            # Sai se falso
Line 5: t5 = FIB_0 + FIB_1            # Soma
Line 5: FIB_NEXT = t5
Line 5: FIB_0 = FIB_1                 # Desloca janela
Line 5: FIB_1 = FIB_NEXT              # Desloca janela
Line 5: t7 = COUNTER + 1              # Incremento
Line 5: COUNTER = t7
Line 5: goto L0                       # Volta ao início
Line 5: L1:                           # Fim do loop
Line 6: RESULT = FIB_NEXT             # Resultado final
```

**Estatísticas:**
- Instruções TAC: **21**
- Temporários gerados: **8** (t0-t7)
- Labels gerados: **2** (L0, L1)
- Iterações executadas: **23** (de F(2) até F(24))

**Sequência gerada:** F(0)=0, F(1)=1, F(2)=1, F(3)=2, ..., F(24)=75,025

**Valor Final:** `RESULT = 75,025` (F(24) correto) 

---

### Exemplo 3: Taylor (taylor.txt)

**Descrição:** Cálculo da série de Taylor para **cos(x)** com x=1.0 radiano usando loop WHILE.

**Fórmula:** cos(x) ≈ 1 - x²/2! + x⁴/4! - x⁶/6!

**Entrada (estrutura do WHILE):**
```
(1.0 X_VAL)
(1.0 TERM1)
(1 COUNTER)
((COUNTER 1 <=)
  ((X_VAL X_VAL *) X_SQUARE)
  (2.0 FACT_2)
  ((X_SQUARE FACT_2 |) TEMP2)
  ((0.0 TEMP2 -) TERM2)
  ((X_SQUARE X_SQUARE *) X_FOURTH)
  ((4.0 3.0 *) TEMP4A)
  ((TEMP4A 2.0 *) TEMP4B)
  ((TEMP4B 1.0 *) FACT_4)
  ((X_FOURTH FACT_4 |) TERM3)
  ((X_FOURTH X_SQUARE *) X_SIXTH)
  ((6.0 5.0 *) TEMP6A)
  ((TEMP6A 4.0 *) TEMP6B)
  ((TEMP6B 3.0 *) TEMP6C)
  ((TEMP6C 2.0 *) TEMP6D)
  ((TEMP6D 1.0 *) FACT_6)
  ((X_SIXTH FACT_6 |) TEMP8)
  ((0.0 TEMP8 -) TERM4)
  ((TERM1 TERM2 +) SUM12)
  ((SUM12 TERM3 +) SUM123)
  ((SUM123 TERM4 +) RESULT_COS)
  (RESULT_COS FINAL_COS)
  ((COUNTER 1 +) COUNTER)
WHILE)
```

**Algoritmo:**
- X_VAL = 1.0, TERM1 = 1.0, COUNTER = 1
- Loop WHILE (executa 1 vez, COUNTER ≤ 1):
  - **TERMO 2:** TERM2 = -(X_VAL²) / 2! = -0.5
  - **TERMO 3:** TERM3 = (X_VAL⁴) / 4! ≈ 0.041667
  - **TERMO 4:** TERM4 = -(X_VAL⁶) / 6! ≈ -0.001389
  - **SOMA:** RESULT_COS = TERM1 + TERM2 + TERM3 + TERM4 ≈ 0.540278
  - FINAL_COS = RESULT_COS
  - COUNTER = COUNTER + 1 (= 2, sai do loop)

**Execução:**
```bash
python compilador.py inputs/RA4/taylor.txt
```

**Estatísticas:**
- Instruções TAC: **68**
- Temporários gerados: **39** (t0-t38)
- Labels gerados: **2** (L0, L1)
- Tipos: Todas operações aritméticas são `[type: real]`

**Cálculos intermediários:**
```
X_SQUARE = 1.0² = 1.0
X_FOURTH = 1.0⁴ = 1.0
X_SIXTH = 1.0⁶ = 1.0

FACT_2 = 2.0
FACT_4 = 4×3×2×1 = 24.0
FACT_6 = 6×5×4×3×2×1 = 720.0

TERM1 = 1.0
TERM2 = -1.0/2.0 = -0.5
TERM3 = 1.0/24.0 ≈ 0.041667
TERM4 = -1.0/720.0 ≈ -0.001389
```

**Valor Final:** `FINAL_COS ≈ 0.540278`

**Valor matemático exato:** cos(1.0) = 0.540302... (erro < 0.003%) 

---

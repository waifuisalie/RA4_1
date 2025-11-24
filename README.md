# Compilador RA4 - Geração e Otimização de TAC

## Informações Institucionais

**Disciplina:** Compiladores
**Fase:** RA4 - Geração de Código Intermediário e Otimização
**Instituição:** [Nome da Instituição]
**Semestre:** [Semestre/Ano]

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

### Ferramentas Opcionais (Fase 5 - Futuro)

Para geração de código Assembly AVR (planejado para próximas iterações):
- `avr-gcc` - Compilador AVR
- `avrdude` - Ferramenta de upload para Arduino
- `Arduino IDE` ou `PlatformIO`

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

Após a execução, consulte:

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

## Aplicações por Técnica

- Constant Folding: 5 aplicações
- Constant Propagation: 3 aplicações
- Dead Code Elimination: 2 aplicações
- Jump Elimination: 0 aplicações
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

### Justificativa das Escolhas

1. **R16-R23 (Temporários):**
   - AVR permite operações imediatas (`ldi`, `cpi`) apenas em R16-R31
   - Permite alocação de até 8 temporários simultaneamente
   - Ideal para variáveis TAC temporárias (`t0`, `t1`, `t2`, ...)

2. **R24-R25 (Parâmetros):**
   - Convenção padrão AVR-GCC
   - Suporta valores de 16-bit (inteiros grandes)
   - Compatível com funções de biblioteca

3. **R26-R27 (X), R28-R29 (Y):**
   - Registradores de ponteiro permitem endereçamento indireto
   - Necessários para acesso a arrays e variáveis em memória
   - X usado para acesso geral, Y para stack frame

4. **R30-R31 (Z):**
   - Ponteiro de pilha gerenciado automaticamente
   - Usado por `call`, `ret`, `push`, `pop`

### Estratégia de Alocação

1. **Fase 1:** Alocar variáveis frequentes em R16-R23
2. **Fase 2:** Usar R24-R25 para cálculos intermediários
3. **Fase 3:** Spill para memória quando registradores esgotarem
4. **Fase 4:** Liberar registradores após último uso

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

## Instruções para Compilar e Carregar Código no Arduino

### Compilação de Assembly para Arduino

**Nota:** A geração de código Assembly AVR está planejada para uma fase futura. As instruções abaixo são um guia para quando essa funcionalidade for implementada.

### 1. Compilar Assembly para Binário

```bash
# Compilar .s para .elf
avr-gcc -mmcu=atmega328p -o program.elf program.s

# Gerar arquivo .hex para upload
avr-objcopy -O ihex -R .eeprom program.elf program.hex
```

### 2. Verificar Tamanho do Programa

```bash
avr-size --format=avr --mcu=atmega328p program.elf
```

**Exemplo de saída:**
```
Program:    1024 bytes (3.1% Full)
Data:        128 bytes (6.3% Full)
```

### 3. Upload para Arduino Uno

**Usando avrdude (Linux/Mac):**
```bash
avrdude -c arduino -p atmega328p -P /dev/ttyACM0 -b 115200 -U flash:w:program.hex:i
```

**No Windows:**
```bash
avrdude -c arduino -p atmega328p -P COM3 -b 115200 -U flash:w:program.hex:i
```

**Identificar porta COM:**
- Windows: Device Manager → Ports (COM & LPT)
- Linux: `ls /dev/ttyACM*` ou `ls /dev/ttyUSB*`
- Mac: `ls /dev/tty.usbmodem*`

### 4. Upload via Arduino IDE

1. Salvar `program.hex` em pasta do projeto
2. Arduino IDE → Ferramentas → Programador → "AVR ISP"
3. Sketch → Upload Using Programmer
4. Ou usar ferramenta externa: Ferramentas → Queimar Bootloader

### 5. Depuração

**Serial Monitor (se programa usar UART):**
```cpp
// Adicionar no Assembly:
.section .text
call uart_init
call print_result
```

**LED de Debug (pino 13):**
```asm
; Configurar LED como saída
sbi DDRB, 5      ; Bit 5 do PORTB = pino 13

; Ligar LED
sbi PORTB, 5

; Desligar LED
cbi PORTB, 5
```

### 6. Simulação (Alternativa)

Antes de carregar no Arduino real, simule com:

- **SimulIDE:** Simulador gráfico de Arduino
- **Wokwi:** Simulador online (https://wokwi.com)
- **Proteus:** Simulação profissional

---

## Exemplos de Uso e Resultados Esperados

### Exemplo 1: Fatorial (fatorial.txt)

**Entrada:**
```
(1 RESULT)
(1 INICIO)
(8 FIM)
(1 PASSO)
(INICIO FIM PASSO (((RESULT INICIO *) RESULT)) FOR)
```

**Descrição:** Calcula 8! (fatorial de 8) usando loop FOR.

**Algoritmo:**
- RESULT = 1 (inicial)
- Loop de INICIO=1 até FIM=8, incrementando PASSO=1
- Cada iteração: RESULT = RESULT * INICIO
- Resultado final: 8! = 40320

**Execução:**
```bash
python compilador.py inputs/RA4/fatorial.txt
```

**Estatísticas:**
- Instruções TAC originais: **17**
- Instruções TAC otimizadas: **12**
- Redução: **29.4%**
- Técnicas aplicadas:
  - Constant Folding: 5 aplicações
  - Dead Code Elimination: 0 aplicações
  - Constant Propagation: 0 aplicações
  - Jump Elimination: 0 aplicações

**Valor Final:** `RESULT = 40320` (8! correto)

---

### Exemplo 2: Fibonacci (fibonacci_desenrolado.txt)

**Descrição:** Sequência de Fibonacci até F(24), com loop manualmente desenrolado.

**Estrutura (trecho):**
```
(0 FIB_0)
(1 FIB_1)

# Iteração 1: F(2) = F(0) + F(1) = 0 + 1 = 1
(((FIB_0 FIB_1 +) FIB_NEXT))
(FIB_1 FIB_0)
(FIB_NEXT FIB_1)

# ... repetir 23 vezes ...

(FIB_NEXT RESULT)
```

**Algoritmo:**
- FIB_0 = 0, FIB_1 = 1 (casos base)
- 23 iterações:
  1. FIB_NEXT = FIB_0 + FIB_1
  2. FIB_0 = FIB_1
  3. FIB_1 = FIB_NEXT
- Resultado final: F(24) = 46368

**Execução:**
```bash
python compilador.py fibonacci_desenrolado.txt
```

**Estatísticas:**
- Linhas de código: 72
- Instruções TAC originais: **97**
- Instruções TAC otimizadas: **95**
- Redução: **2.1%** (pequena, pois código já é simples)

**Valor Final:** `RESULT = 46368` (F(24) correto)

**Observação:** A baixa taxa de otimização ocorre porque:
- Código não contém constantes para dobrar
- Cada variável é usada, não há código morto
- Fluxo linear (sem saltos redundantes)

---

### Exemplo 3: Taylor (taylor.txt)

**Descrição:** Cálculo da série de Taylor para cos(x) com x=1.0.

**Fórmula:** cos(x) ≈ 1 - x²/2! + x⁴/4! - x⁶/6!

**Código (simplificado):**
```
(1.0 X_VAL)
(1.0 TERM1)                      # termo1 = 1.0
((X_VAL X_VAL *) TEMP1)          # x^2
((TEMP1 2.0 |) TEMP2)            # x^2 / 2
((0 TEMP2 -) TERM2)              # - (x^2 / 2)
((TEMP1 TEMP1 *) TEMP4)          # x^4
((TEMP4 24.0 |) TERM3)           # x^4 / 24
((TEMP4 TEMP1 *) TEMP7)          # x^6
((TEMP7 720.0 |) TEMP8)          # x^6 / 720
((0 TEMP8 -) TERM4)              # - (x^6 / 720)
((((TERM1 TERM2 +) TERM3 +) TERM4 +) RESULT_COS)
```

**Execução:**
```bash
python compilador.py inputs/RA4/taylor.txt
```

**Estatísticas:**
- Instruções TAC originais: **30**
- Instruções TAC otimizadas: **23**
- Redução: **23.3%**
- Técnicas aplicadas:
  - Constant Folding: 7 aplicações (ex: 1.0 * 1.0 → 1.0)
  - Constant Propagation: 3 aplicações
  - Dead Code Elimination: 0 aplicações
  - Jump Elimination: 0 aplicações

**Resultado esperado:** `RESULT_COS ≈ 0.5403` (cos(1.0) em radianos)

**Valor matemático exato:** cos(1.0) = 0.5403023...

---

### Exemplo 4: Fibonacci com FOR (fibonacci.txt)

**Entrada:**
```
(0 FIB_0)
(1 FIB_1)
(2 INICIO)
(24 FIM)
(1 PASSO)
(INICIO FIM PASSO (((FIB_0 FIB_1 +) FIB_NEXT)) FOR)
(FIB_NEXT RESULT)
```

**Descrição:** Tentativa de calcular Fibonacci com loop FOR.

**Execução:**
```bash
python compilador.py inputs/RA4/fibonacci.txt
```

**Estatísticas:**
- Instruções TAC originais: **20**
- Instruções TAC otimizadas: **14**
- Redução: **30.0%**

**⚠️ PROBLEMA CONHECIDO:**

O código **compila sem erros**, mas a **lógica está incompleta**:

**Por que não funciona:**
- Cada iteração calcula `FIB_NEXT = FIB_0 + FIB_1` (sempre 0 + 1 = 1)
- **FIB_0 e FIB_1 nunca são atualizados!**
- Para Fibonacci funcionar, precisaria de 3 instruções no loop:
  1. `FIB_NEXT = FIB_0 + FIB_1`
  2. `FIB_0 = FIB_1`
  3. `FIB_1 = FIB_NEXT`

**Limitação do Parser:**
- A gramática atual aceita apenas **1 instrução** no corpo do FOR
- Sintaxe: `(init fim passo (single_instruction) FOR)`

**Solução:** Usar `fibonacci_desenrolado.txt` (loop manual com 23 iterações explícitas)

**Resultado final:** `FIB_NEXT = 1` ❌ (incorreto, deveria ser 46368)

---

### Comparação de Resultados

| Arquivo | Instruções (Antes) | Instruções (Depois) | Redução | Status |
|---------|-------------------|---------------------|---------|--------|
| `fatorial.txt` | 17 | 12 | **29.4%** | ✅ Correto (8! = 40320) |
| `fibonacci_desenrolado.txt` | 97 | 95 | **2.1%** | ✅ Correto (F(24) = 46368) |
| `taylor.txt` | 30 | 23 | **23.3%** | ✅ Correto (cos(1.0) ≈ 0.5403) |
| `fibonacci.txt` | 20 | 14 | **30.0%** | ⚠️ Compila, mas lógica incompleta |

---

## Limitações Conhecidas

### 1. Loop FOR com Múltiplas Instruções

**Problema:** O parser aceita apenas 1 instrução no corpo do loop FOR.

**Exemplo que NÃO funciona:**
```
(init fim passo ((inst1) (inst2) (inst3)) FOR)  # ❌ Erro de sintaxe
```

**Workaround:** Desenrolar o loop manualmente ou usar variáveis auxiliares.

### 2. Loop WHILE com Múltiplas Instruções

**Problema:** Similar ao FOR, WHILE também aceita apenas 1 instrução.

**Mensagem de erro:** "Estrutura da linha não reconhecida" (RA3)

### 3. Operações de Ponto Flutuante

**Status:** Suportado no TAC, mas precisão limitada.

**Observação:** Quando implementada geração de Assembly AVR:
- AVR não possui FPU (Floating Point Unit) nativo
- Operações float requerem biblioteca software (AVR-libc)
- Alternativa: Aritmética de ponto fixo (inteiros escalados)

### 4. Geração de Assembly AVR

**Status:** **NÃO IMPLEMENTADO** (planejado para fase futura)

**Atualmente disponível:**
- ✅ Tokenização (RA1)
- ✅ Parsing (RA2)
- ✅ Análise semântica (RA3)
- ✅ Geração de TAC (RA4)
- ✅ Otimização de TAC (RA4)
- ❌ Geração de Assembly AVR (Fase 5 - futuro)

---

## Referências

### Documentação Técnica

- **AVR Instruction Set Manual:** [Microchip Official](https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf)
- **Arduino Uno Datasheet:** [Arduino.cc](https://docs.arduino.cc/hardware/uno-rev3/)
- **AVR-libc Documentation:** [nongnu.org](https://www.nongnu.org/avr-libc/)

### Livros de Compiladores

- **"Compilers: Principles, Techniques, and Tools"** (Dragon Book) - Aho, Sethi, Ullman
- **"Engineering a Compiler"** - Cooper, Torczon
- **"Modern Compiler Implementation in C"** - Appel

### Otimização de Código

- **"Advanced Compiler Design and Implementation"** - Muchnick
- **"Optimizing Compilers for Modern Architectures"** - Allen, Kennedy

---

## Contato

Para dúvidas ou sugestões:

- **Breno Rossi Duarte:** [@breno-rossi](https://github.com/breno-rossi)
- **Francisco Bley Ruthes:** [@fbleyruthes](https://github.com/fbleyruthes)
- **Rafael Olivare Piveta:** [@RafaPiveta](https://github.com/RafaPiveta)
- **Stefan Benjamim Seixas Lourenço Rodrigues:** [@waifuisalie](https://github.com/waifuisalie)

---

**Última atualização:** 24/11/2025
**Versão:** RA4 - Geração e Otimização de TAC

# Issue Principal 3: Geração de Assembly (gerarAssembly)

**Responsável:** Aluno 3
**Labels:** `phase-4`, `assembly`, `avr`, `aluno-3`

## Descrição

Gerar código Assembly AVR para Arduino Uno (ATmega328P) a partir do TAC otimizado.

## Entrada

- Instruções TAC otimizadas de `otimizarTAC()`
- TAC_otimizado.json

## Saída

- String de código Assembly AVR
- Arquivo: `program.s` (código fonte Assembly AVR)
- Arquivo: `assembly.md` (representação/documentação markdown do Assembly gerado)
- Arquivo: `convencoes_registradores.md` (documentação das convenções de registradores AVR)

---

## Sub-Issues

### 3.1 Definir Convenções de Registradores
**Descrição:**
- Documentar estratégia de alocação de registradores:
  - `R16-R23`: Variáveis temporárias e computação
  - `R24-R25`: Parâmetros de função e valores de retorno
  - `R26-R27 (X)`: Ponteiro de endereço para acesso à memória
  - `R28-R29 (Y)`: Frame pointer
  - `R30-R31 (Z)`: Ponteiro de pilha
- Criar arquivo `convencoes_registradores.md` (conforme linhas 149, 463 da especificação)

**Formato convencoes_registradores.md:**
```markdown
# Convenções de Registradores AVR - Arduino Uno (ATmega328P)

## 1. Visão Geral
Este documento descreve as convenções de uso de registradores adotadas
para a geração de código Assembly AVR neste compilador.

## 2. Mapa de Alocação de Registradores

| Registrador(es) | Uso | Descrição |
|----------------|-----|-----------|
| R16-R23 | Temporários | Variáveis temporárias e computação |
| R24-R25 | Parâmetros/Retorno | Valores de 16-bit |
| R26-R27 (X) | Ponteiro | Acesso à memória |
| R28-R29 (Y) | Frame Pointer | Variáveis locais |
| R30-R31 (Z) | Stack Pointer | Gerenciado pelo sistema |

## 3. Justificativa
[Explicar razões para cada escolha]

## 4. Exemplos de Uso
[Exemplos práticos de cada tipo de registrador]
```

**Critério de Aceitação:**
- [ ] Arquivo convencoes_registradores.md criado
- [ ] Convenções claramente definidas e documentadas
- [ ] Mapa de alocação completo
- [ ] Justificativas para escolhas incluídas
- [ ] Exemplos de uso fornecidos

---

### 3.2 Alocador de Registradores
**Descrição:**
- Implementar alocação simples de registradores
- Rastrear registradores disponíveis
- Fazer spill para memória quando registradores esgotarem
- Funções: `allocateRegister()`, `freeRegister()`, `spillToMemory()`

**Critério de Aceitação:**
- [ ] Pode alocar e rastrear registradores
- [ ] Spill para memória funciona quando necessário
- [ ] Registradores são liberados corretamente
- [ ] Sem conflitos de registradores

---

### 3.3 Geração de Prólogo/Epílogo do Programa
**Descrição:**
- Gerar código de inicialização (seção .text)
- Configurar ponteiro de pilha
- Inicializar registradores
- Gerar terminação do programa (loop infinito ou halt)

**Exemplo:**
```asm
.section .text
.global main

main:
    ; Inicializar stack pointer
    ldi r16, lo8(RAMEND)
    out SPL, r16
    ldi r16, hi8(RAMEND)
    out SPH, r16

    ; Código do programa aqui

fim:
    rjmp fim    ; Loop infinito
```

**Critério de Aceitação:**
- [ ] Estrutura válida de programa AVR
- [ ] Stack pointer configurado corretamente
- [ ] Programa termina apropriadamente
- [ ] Compila com avr-gcc

---

### 3.4 Mapeamento de Operações Aritméticas
**Descrição:**
- Mapear operações binárias TAC para instruções AVR:
  - `+` → `add`, `adc` (com carry para 16-bit)
  - `-` → `sub`, `sbc`
  - `*` → `mul` (8-bit) ou chamada de biblioteca
  - `/`, `%` → Chamadas de biblioteca de divisão
  - `^` → Exponenciação (biblioteca/loop)
- Tratar tipos int vs real

**Exemplo TAC → Assembly:**
```
TAC: t2 = t0 + t1

Assembly:
    ; t0 está em r16, t1 está em r17
    add r16, r17      ; r16 = r16 + r17
    ; resultado (t2) está em r16
```

**Critério de Aceitação:**
- [ ] Todos os operadores aritméticos geram código AVR correto
- [ ] Operações de 8-bit funcionam
- [ ] Operações de 16-bit com carry funcionam
- [ ] Multiplicação e divisão implementadas (biblioteca ou inline)

---

### 3.5 Suporte a Ponto Flutuante (16-bit IEEE 754)
**Descrição:**
- Pesquisar bibliotecas AVR de ponto flutuante ou aritmética de ponto fixo
- Implementar ou integrar operações de float de 16-bit
- Documentar limitações de precisão

**Opções:**
1. Usar aritmética de ponto fixo (inteiros escalados)
2. Usar suporte float16 da AVR-libc
3. Implementar rotinas básicas de float

**Critério de Aceitação:**
- [ ] Pode tratar operações de tipo real
- [ ] Funciona no teste taylor.txt
- [ ] Limitações de precisão documentadas
- [ ] Abordagem escolhida justificada

---

### 3.6 Implementação de Acesso à Memória
**Descrição:**
- Implementar operações de load: `ld`, `ldd`
- Implementar operações de store: `st`, `std`
- Tratar armazenamento de variáveis MEM
- Mapear temporários TAC para registradores ou memória

**Exemplo:**
```
TAC: MEM[X] = t1

Assembly:
    ; t1 está em r16
    ; Endereço de X está definido
    ldi r26, lo8(X)
    ldi r27, hi8(X)
    st X, r16
```

**Critério de Aceitação:**
- [ ] Operações de memória funcionam corretamente
- [ ] Variáveis MEM são armazenadas/carregadas
- [ ] Endereçamento de memória está correto
- [ ] Sem corrupção de dados

---

### 3.7 Mapeamento de Fluxo de Controle
**Descrição:**
- Mapear rótulos: `L1:` → sintaxe de rótulo AVR
- Mapear `goto L1` → `rjmp L1` ou `jmp L1`
- Mapear `if a goto L1`:
  ```asm
  ld r16, a
  cpi r16, 0
  brne L1
  ```
- Mapear `ifFalse a goto L1`:
  ```asm
  ld r16, a
  cpi r16, 0
  breq L1
  ```

**Critério de Aceitação:**
- [ ] Todo fluxo de controle corretamente traduzido
- [ ] Rótulos funcionam
- [ ] Saltos condicionais funcionam
- [ ] Saltos incondicionais funcionam
- [ ] Alcance de salto tratado (rjmp vs jmp)

---

### 3.8 Geração de Comentários
**Descrição:**
- Adicionar comentários mostrando instrução TAC original
- Adicionar comentários para uso de registradores
- Documentar operações complexas

**Exemplo:**
```asm
    ; TAC: t2 = t0 + t1 (linha 5)
    ; t0 em r16, t1 em r17, t2 irá para r16
    add r16, r17
```

**Critério de Aceitação:**
- [ ] Assembly está bem comentado e legível
- [ ] Instruções TAC originais referenciadas
- [ ] Alocação de registradores documentada
- [ ] Operações complexas explicadas

---

### 3.9 Saída de Arquivo Assembly
**Descrição:**
- Escrever program.s com sintaxe AVR apropriada
- Gerar assembly.md (representação markdown do Assembly conforme linha 276)
- Garantir compatibilidade com `avr-gcc`
- Testar compilação: `avr-gcc -mmcu=atmega328p -o program.elf program.s`

**Formato assembly.md:**
```markdown
# Código Assembly Gerado - [nome_arquivo]

## 1. Informações do Programa
- Arquivo fonte: [nome]
- Data de geração: [data]
- Arquitetura: ATmega328P (Arduino Uno)

## 2. Código Assembly Completo
```asm
[código assembly com comentários detalhados]
```

## 3. Mapeamento TAC → Assembly

### Linha X: [expressão original]

**TAC:**
```
[instruções TAC]
```

**Assembly:**
```asm
[instruções assembly correspondentes]
```

## 4. Estatísticas
- Total de instruções Assembly: N
- Registradores utilizados: [lista]
- Tamanho estimado: N bytes
```

**Critério de Aceitação:**
- [ ] program.s compila sem erros
- [ ] assembly.md gerado em formato markdown
- [ ] assembly.md inclui mapeamento TAC → Assembly
- [ ] Sintaxe AVR está correta
- [ ] Seções .text e .data apropriadas
- [ ] Pode ser montado e linkado
- [ ] assembly.md tem estatísticas corretas

---

## Dependências

- Requer formato TAC do Aluno 2 (saída do otimizador)
- Deve compilar com sucesso para integração do Aluno 4

## Critérios de Aceitação Gerais

- [ ] convencoes_registradores.md criado e completo
- [ ] Convenções de registradores definidas e documentadas
- [ ] Todos os tipos de instrução TAC mapeados para AVR
- [ ] Operações de ponto flutuante suportadas
- [ ] program.s compila com avr-gcc
- [ ] assembly.md gerado em formato markdown
- [ ] assembly.md inclui mapeamento TAC → Assembly
- [ ] Funciona em todos os 3 arquivos de teste
- [ ] Assembly é legível com comentários
- [ ] Sem conflitos de registradores
- [ ] Acesso à memória funciona corretamente

## Referências Úteis

- [Manual de Conjunto de Instruções AVR](https://ww1.microchip.com/downloads/en/devicedoc/atmel-0856-avr-instruction-set-manual.pdf)
- [Arduino Uno Datasheet](https://docs.arduino.cc/hardware/uno-rev3/)
- [AVR-libc Documentation](https://www.nongnu.org/avr-libc/)

## Interface com Outros Componentes

**Entrada esperada (do Aluno 2):**
```json
{
  "instructions": [
    {"type": "assignment", "dest": "t0", "source": "5", "line": 1},
    {"type": "assignment", "dest": "t1", "source": "3", "line": 1},
    {"type": "binary_op", "result": "t2", "op1": "t0", "operator": "+", "op2": "t1", "line": 1}
  ]
}
```

**Saída esperada (program.s):**
```asm
.section .text
.global main

main:
    ; Inicialização
    ldi r16, lo8(RAMEND)
    out SPL, r16
    ldi r16, hi8(RAMEND)
    out SPH, r16

    ; TAC: t0 = 5 (linha 1)
    ldi r16, 5

    ; TAC: t1 = 3 (linha 1)
    ldi r17, 3

    ; TAC: t2 = t0 + t1 (linha 1)
    add r16, r17

fim:
    rjmp fim
```

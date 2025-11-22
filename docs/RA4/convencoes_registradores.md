# Convenções de Registradores AVR - Arduino Uno (ATmega328P)

## 1. Visão Geral

Este documento descreve as convenções de uso de registradores adotadas para a geração de código Assembly AVR neste compilador. O ATmega328P possui 32 registradores de 8 bits (R0-R31) de propósito geral com acesso em um único ciclo de clock.

## 2. Mapa de Alocação de Registradores

| Registrador(es) | Uso | Descrição |
|-----------------|-----|-----------|
| R0-R1 | Multiplicação | Resultado de operações MUL (definido pelo hardware) |
| R2-R15 | Reservados | Variáveis locais e uso futuro |
| **R16-R23** | **Temporários 16-bit** | **4 pares para variáveis TAC (R16:R17, R18:R19, R20:R21, R22:R23)** |
| R24-R25 | Parâmetros/Retorno | Parâmetros de função e valores de retorno (16-bit) |
| R26-R27 (X) | Ponteiro | Acesso à memória e addressing indireto |
| R28-R29 (Y) | Frame Pointer | Variáveis locais na pilha |
| R30-R31 (Z) | Ponteiro Auxiliar | Lookup de programa e addressing indireto |

## 3. Justificativa

### Restrições de Hardware
- **R0-R1**: As instruções de multiplicação (MUL, MULS, MULSU, FMUL, etc.) armazenam automaticamente o resultado de 16 bits em R1:R0.
- **R16-R31**: Apenas estes registradores suportam instruções com operandos imediatos (LDI, ANDI, ORI, SUBI, CPI, etc.).
- **R26-R31**: Formam três pares de ponteiros de 16 bits (X, Y, Z) para addressing indireto.

### Escolhas de Alocação
- **R16-R23 (Temporários)**: Permitem operações imediatas e são suficientes para expressões aritméticas complexas.
- **R24-R25 (Parâmetros/Retorno)**: Convenção padrão AVR-GCC para passagem de parâmetros e valores de retorno.
- **X, Y, Z (Ponteiros)**: Utilizados para acesso à memória, sendo Y preferido para frame pointer por suportar displacement.

## 4. Exemplos de Uso

### Exemplo 1: Operação Aritmética com Temporários
```asm
; TAC: t2 = t0 + t1
; t0 em R16, t1 em R17, t2 em R18

ldi r16, 5          ; t0 = 5
ldi r17, 3          ; t1 = 3
add r18, r16        ; r18 = r16 + r17
add r18, r17        ; t2 = t0 + t1 (resultado em R18)
```

### Exemplo 2: Acesso à Memória com Ponteiro X
```asm
; TAC: MEM[endereco] = t1
; t1 em R16, endereço em X (R27:R26)

ldi r26, lo8(0x0100)    ; X baixo = byte baixo do endereço
ldi r27, hi8(0x0100)    ; X alto = byte alto do endereço
st X, r16               ; Armazena R16 no endereço apontado por X
```

### Exemplo 3: Multiplicação
```asm
; TAC: t2 = t0 * t1
; t0 em R16, t1 em R17, resultado em R1:R0

mul r16, r17        ; R1:R0 = R16 × R17 (16-bit resultado)
mov r18, r0         ; t2 = byte baixo (se 8-bit é suficiente)
; ou usar ambos R1:R0 se precisar 16-bit
```

## 5. Alocação Dinâmica de Registradores (16-bit)

### 5.1. Estratégia de Alocação

O compilador utiliza **4 pares de registradores** (R16:R17, R18:R19, R20:R21, R22:R23) para alocar variáveis temporárias do TAC em formato de 16-bit (suportando inteiros e floats half-precision).

**Características:**
- **Alocação Lazy (on-demand)**: Registradores são alocados apenas quando a variável é usada pela primeira vez.
- **Suporte a 16-bit nativo**: Cada variável TAC ocupa um par de registradores (low:high byte).
- **Constantes literais**: Carregadas com `ldi` (load immediate) sem alocar do pool.

### 5.2. Spilling para Memória (FIFO)

Quando os 4 pares de registradores estão ocupados e uma nova variável precisa ser alocada, o compilador realiza **spilling** (despejo para memória SRAM).

**Algoritmo:**
1. Seleciona a variável mais antiga (FIFO - First In First Out)
2. Salva o conteúdo do par de registradores na SRAM usando `sts`
3. Libera o par de registradores para nova alocação
4. Se a variável spillada for usada novamente, carrega de volta com `lds`

**Endereçamento de Spill:**
- Inicia em `0x0100` (RAMSTART)
- Cada variável 16-bit ocupa 2 bytes consecutivos
- Incremento automático: `0x0100`, `0x0102`, `0x0104`, etc.

### 5.3. Exemplo de Spilling

```asm
; Cenário: 5 variáveis (t0, t1, t2, t3, t4)
; Apenas 4 pares disponíveis → t0 será spillada

; Alocar t0, t1, t2, t3 (usa 4 pares)
ldi r16, 1      ; t0 = R16:R17
ldi r18, 2      ; t1 = R18:R19
ldi r20, 3      ; t2 = R20:R21
ldi r22, 4      ; t3 = R22:R23

; Tentar alocar t4 → sem pares disponíveis!
; Spill t0 (mais antiga, FIFO)
sts 0x0100, r16      ; Salva t0 low byte
sts 0x0101, r17      ; Salva t0 high byte

; Agora R16:R17 está livre para t4
ldi r16, 5      ; t4 = R16:R17

; Se t0 for usada depois:
lds r18, 0x0100      ; Carrega t0 low byte
lds r19, 0x0101      ; Carrega t0 high byte
```

### 5.4. Estatísticas de Alocação

| Métrica | Valor |
|---------|-------|
| Pares de registradores disponíveis | 4 (R16:R17, R18:R19, R20:R21, R22:R23) |
| Variáveis simultâneas sem spilling | 4 |
| Endereço inicial de spill | 0x0100 (RAMSTART) |
| Bytes por variável spillada | 2 (16-bit) |
| Estratégia de spilling | FIFO (First In First Out) |

## 6. Observações Importantes

- **Preservação de Registradores**: Funções devem preservar R2-R17 e R28-R29 (salvar/restaurar na pilha).
- **Volatilidade**: R18-R27 e R30-R31 são considerados voláteis (caller-saved).
- **Stack Pointer**: O ponteiro de pilha (SP) é gerenciado pelo hardware nos registradores SPH:SPL (não é um registrador de propósito geral).
- **Instruções Limitadas**: R0-R15 não podem usar LDI, ANDI, ORI, SBCI, SUBI, CPI - apenas instruções entre registradores.
- **Spilling Automático**: O compilador gerencia spilling automaticamente quando necessário (transparente ao programador).

---

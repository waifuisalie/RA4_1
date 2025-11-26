# Validação de Hardware - Arduino Uno (ATmega328P)

Este diretório contém testes de validação em hardware real para o gerador de Assembly AVR (Sub-issue 3.2).

## Objetivo

Validar que o código Assembly gerado pelo compilador executa corretamente em um Arduino Uno (ATmega328P), testando:

1. **Alocação de registradores básica** - Test 1
2. **Spilling para SRAM** - Test 2

## Estrutura de Arquivos

```
hardware_validation/
├── test1_serial.s      # Assembly: 1 + 2 = 3 (sem spilling)
├── test2_serial.s      # Assembly: 5 + 2 = 7 (com spilling)
├── Makefile            # Compilação e upload automatizados
├── run_tests.sh        # Script de automação completo
└── README.md           # Esta documentação
```

## Pré-requisitos

### Hardware
- Arduino Uno (ATmega328P)
- Cabo USB A-B
- Conexão serial (115200 baud)

### Software

```bash
# Ubuntu/Debian
sudo apt-get install avr-libc gcc-avr avrdude screen

# Verificar instalação
avr-gcc --version
avrdude -v
```

## Método de Validação

Os testes usam **saída serial (UART)** para reportar resultados:

- **Baud Rate:** 115200
- **Formato:** 8N1 (8 data bits, no parity, 1 stop bit)
- **Porta:** `/dev/ttyUSB0` (ou `/dev/ttyACM0`)

Cada teste envia:
1. Mensagem de início (descrição do teste)
2. Resultado da computação
3. Mensagem de sucesso

## Testes Disponíveis

### Test 1: Alocação Básica (1 + 2 = 3)

**Arquivo:** `test1_serial.s`

**TAC Simulado:**
```
t0 = 1
t1 = 2
t2 = t0 + t1
```

**Registradores Utilizados:**
- `R16:R17` → t0
- `R18:R19` → t1
- `R20:R21` → t2 (resultado)

**Saída Esperada:**
```
Teste 1: 1 + 2 = ?
Resultado: 3
OK - Teste passou!
```

**O que valida:**
- Carregamento de constantes com `ldi`
- Soma 16-bit com `add` e `adc`
- Transferência entre registradores com `mov`
- Comunicação UART

### Test 2: Spilling (5 + 2 = 7)

**Arquivo:** `test2_serial.s`

**TAC Simulado:**
```
t0 = 1
t1 = 2
t2 = 3
t3 = 4
t4 = 5   # Força spilling de t0
t5 = t4 + t1
```

**Registradores Utilizados:**
- `R16:R17` → t0 (depois spillado), então reutilizado para t4
- `R18:R19` → t1
- `R20:R21` → t2, depois reutilizado para t5
- `R22:R23` → t3

**Spilling:**
- t0 spillado para `0x0100:0x0101` (SRAM)

**Saída Esperada:**
```
Teste 2: Spilling test (5 + 2 = ?)
Resultado: 7
OK - Teste passou!
```

**O que valida:**
- Alocação de 5 variáveis com apenas 4 pares disponíveis
- Spilling FIFO para SRAM usando `sts`
- Operação aritmética após spilling
- Reutilização de registradores

## Como Usar

### Opção 1: Makefile (Controle Manual)

```bash
cd tests/RA4/hardware_validation

# Compilar Test 1
make test1

# Upload Test 1 para Arduino
make upload1

# Abrir monitor serial (Ctrl+A, K para sair)
make monitor

# Ou tudo em um comando
make run1
```

**Targets disponíveis:**
- `make test1` - Compila Test 1
- `make test2` - Compila Test 2
- `make upload1` - Upload Test 1
- `make upload2` - Upload Test 2
- `make monitor` - Abre monitor serial
- `make clean` - Remove arquivos compilados
- `make run1` - Compila, upload e monitor (Test 1)
- `make run2` - Compila, upload e monitor (Test 2)

### Opção 2: Script Automatizado (Recomendado)

```bash
cd tests/RA4/hardware_validation

# Executar todos os testes sequencialmente
./run_tests.sh

# Porta customizada
PORT=/dev/ttyACM0 ./run_tests.sh

# Ver ajuda
./run_tests.sh --help
```

O script automaticamente:
1. Verifica dependências
2. Detecta Arduino
3. Compila cada teste
4. Faz upload
5. Captura saída serial
6. Valida resultado
7. Reporta sucesso/falha

## Saídas Geradas

Após compilação, os seguintes arquivos são criados:

```
test1_serial.elf    # Executável ELF (Test 1)
test1_serial.hex    # HEX para upload (Test 1)
test2_serial.elf    # Executável ELF (Test 2)
test2_serial.hex    # HEX para upload (Test 2)
```

## Troubleshooting

### Arduino não detectado

```bash
# Verificar portas disponíveis
ls /dev/tty{USB,ACM}*

# Dar permissão de acesso
sudo usermod -a -G dialout $USER
# (Relogar após este comando)
```

### Upload falha com "permission denied"

```bash
sudo chmod 666 /dev/ttyUSB0
# Ou adicionar usuário ao grupo dialout (permanente)
sudo usermod -a -G dialout $USER
```

### Nenhuma saída serial

1. Verifique baud rate (deve ser 115200)
2. Pressione botão RESET no Arduino
3. Verifique conexão USB
4. Use outro terminal serial:
   ```bash
   screen /dev/ttyUSB0 115200
   # Ou
   minicom -D /dev/ttyUSB0 -b 115200
   ```

### Compilação falha

```bash
# Verificar instalação
avr-gcc --version
avr-objcopy --version

# Reinstalar ferramentas
sudo apt-get install --reinstall avr-libc gcc-avr
```

## Detalhes Técnicos

### Registradores UART (ATmega328P)

| Endereço | Nome | Função |
|----------|------|--------|
| 0xC0 | UCSR0A | Status UART |
| 0xC1 | UCSR0B | Controle UART (TX/RX enable) |
| 0xC2 | UCSR0C | Configuração (8N1) |
| 0xC4 | UBRR0L | Baud rate low byte |
| 0xC5 | UBRR0H | Baud rate high byte |
| 0xC6 | UDR0 | Data register |

### Cálculo de Baud Rate

Para 115200 baud @ 16MHz:
```
UBRR = (F_CPU / (16 * BAUD)) - 1
     = (16000000 / (16 * 115200)) - 1
     = 8.68 - 1
     ≈ 8
```

**Erro:** ~0.2% (aceitável)

### Stack Pointer

Os testes inicializam SP para `0x08FF` (final da SRAM):

```asm
ldi r16, lo8(0x08FF)
out 0x3D, r16          ; SPL
ldi r16, hi8(0x08FF)
out 0x3E, r16          ; SPH
```

### Mapa de Memória SRAM

| Endereço | Uso |
|----------|-----|
| 0x0100 | Início de spilling (t0 spillado) |
| 0x0102 | Próxima variável spillada |
| ... | Crescimento para cima |
| 0x08FF | Stack pointer inicial (cresce para baixo) |

## Integração com Gerador de Assembly

Estes testes validam a implementação do `gerador_assembly.py`:

- `test1_serial.s` → Equivalente ao output de `test_register_allocator_basic()`
- `test2_serial.s` → Equivalente ao output de `test_register_allocator_with_spill()`

A diferença é que os testes de hardware incluem:
1. Inicialização de stack pointer
2. Código UART completo
3. Conversão de número para ASCII
4. Loop infinito ao final

**Núcleo computacional** (linhas 24-60 em test1, 24-62 em test2) deve ser **idêntico** ao Assembly gerado pelo compilador.

## Próximos Passos

Após validação bem-sucedida:

1. ✅ Sub-issue 3.1 completa (convencoes_registradores.md)
2. ✅ Sub-issue 3.2 completa (gerador_assembly.py)
3. ⏳ Sub-issue 3.3: Prólogo/Epílogo
4. ⏳ Sub-issue 3.4: Operações Aritméticas (*, /, %, ^)
5. ⏳ Sub-issue 3.5: Suporte Float 16-bit
6. ⏳ Sub-issue 3.6: Acesso à Memória
7. ⏳ Sub-issue 3.7: Controle de Fluxo
8. ⏳ Sub-issue 3.8: Comentários
9. ⏳ Sub-issue 3.9: Saída de Arquivo

## Referências

- [ATmega328P Datasheet](../../../docs/RA4/reference_docs/atmega328p/manual_atmega328p.txt)
- [AVR Instruction Set](../../../docs/RA4/reference_docs/atmega328p/instruction_set_atmega328p.txt)
- [Convenções de Registradores](../../../docs/RA4/convencoes_registradores.md)
- [Issue 3: Geração de Assembly](../../../docs/RA4/github_issues/issue_3_geracao_assembly.md)

---

**Autor:** Aluno 3 - RA4 Compiladores
**Data:** 2025-11-22
**Versão:** 1.0

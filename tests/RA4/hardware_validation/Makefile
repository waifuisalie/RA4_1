# ====================================================================
# Makefile para Validação de Hardware - Arduino Uno (ATmega328P)
# ====================================================================
# Compila e faz upload de testes Assembly para validação em hardware
# ====================================================================

# Configuração do hardware
MCU = atmega328p
F_CPU = 16000000UL
BAUD = 115200
PORT = /dev/ttyUSB0
PROGRAMMER = arduino

# Ferramentas
CC = avr-gcc
OBJCOPY = avr-objcopy
AVRDUDE = avrdude
SCREEN = screen

# Flags de compilação
CFLAGS = -mmcu=$(MCU) -DF_CPU=$(F_CPU)
LDFLAGS = -mmcu=$(MCU)

# Arquivos
TEST1_SRC = test1_serial.s
TEST1_ELF = test1_serial.elf
TEST1_HEX = test1_serial.hex

TEST2_SRC = test2_serial.s
TEST2_ELF = test2_serial.elf
TEST2_HEX = test2_serial.hex

TEST3_SRC = test3_subtraction.s
TEST3_ELF = test3_subtraction.elf
TEST3_HEX = test3_subtraction.hex

TEST4_SRC = test4_multiplication.s
TEST4_ELF = test4_multiplication.elf
TEST4_HEX = test4_multiplication.hex

TEST5_SRC = test5_division.s
TEST5_ELF = test5_division.elf
TEST5_HEX = test5_division.hex

TEST6_SRC = test6_modulo.s
TEST6_ELF = test6_modulo.elf
TEST6_HEX = test6_modulo.hex

TEST7_SRC = test7_div_by_zero.s
TEST7_ELF = test7_div_by_zero.elf
TEST7_HEX = test7_div_by_zero.hex

TEST8_SRC = test8_comparison_eq.s
TEST8_ELF = test8_comparison_eq.elf
TEST8_HEX = test8_comparison_eq.hex

TEST9_SRC = test9_comparison_lt.s
TEST9_ELF = test9_comparison_lt.elf
TEST9_HEX = test9_comparison_lt.hex

TEST10_SRC = test10_comparison_ge.s
TEST10_ELF = test10_comparison_ge.elf
TEST10_HEX = test10_comparison_ge.hex

TEST11_SRC = test11_while_loop.s
TEST11_ELF = test11_while_loop.elf
TEST11_HEX = test11_while_loop.hex

TEST12_SRC = test12_real_division.s
TEST12_ELF = test12_real_division.elf
TEST12_HEX = test12_real_division.hex

TEST12_DEBUG_SRC = test12_real_division_debug.s
TEST12_DEBUG_ELF = test12_real_division_debug.elf
TEST12_DEBUG_HEX = test12_real_division_debug.hex

# ====================================================================
# Targets Principais
# ====================================================================

.PHONY: all test1 test2 test3 test4 test5 test6 test7 test8 test9 test10 test11 test12 test12_debug upload1 upload2 upload3 upload4 upload5 upload6 upload7 upload8 upload9 upload10 upload11 upload12 upload12_debug monitor clean help

all: test1 test2 test3 test4 test5 test6 test7 test8 test9 test10 test11 test12

help:
	@echo "====================================================================="
	@echo "Makefile - Validação de Hardware Arduino Uno"
	@echo "====================================================================="
	@echo "Targets disponíveis:"
	@echo "  make test1      - Compila Test 1 (Addition: 1 + 2 = 3)"
	@echo "  make test2      - Compila Test 2 (Spilling: 5 + 2 = 7)"
	@echo "  make test3      - Compila Test 3 (Subtraction: 1000 - 234 = 766)"
	@echo "  make test4      - Compila Test 4 (Multiplication: 123 * 45 = 5535)"
	@echo "  make test5      - Compila Test 5 (Division: 1234 / 56 = 22)"
	@echo "  make test6      - Compila Test 6 (Modulo: 1234 % 56 = 2)"
	@echo "  make test7      - Compila Test 7 (Div by zero: 100 / 0 = 65535)"
	@echo "  make test8      - Compila Test 8 (Comparison ==: 1 0)"
	@echo "  make test9      - Compila Test 9 (Comparison <: 1 0)"
	@echo "  make test10     - Compila Test 10 (Comparison >=: 1 0 1)"
	@echo "  make test11     - Compila Test 11 (WHILE loop: 10)"
	@echo "  make test12     - Compila Test 12 (Real division: 1 | 2 = 500)"
	@echo "  make test12_debug - Compila Test 12 DEBUG (with UART logging)"
	@echo "  make upload1    - Upload Test 1 para Arduino"
	@echo "  make upload2    - Upload Test 2 para Arduino"
	@echo "  make upload3    - Upload Test 3 para Arduino"
	@echo "  make upload4    - Upload Test 4 para Arduino"
	@echo "  make upload5    - Upload Test 5 para Arduino"
	@echo "  make upload6    - Upload Test 6 para Arduino"
	@echo "  make upload7    - Upload Test 7 para Arduino"
	@echo "  make upload8    - Upload Test 8 para Arduino"
	@echo "  make upload9    - Upload Test 9 para Arduino"
	@echo "  make upload10   - Upload Test 10 para Arduino"
	@echo "  make upload11   - Upload Test 11 para Arduino"
	@echo "  make upload12   - Upload Test 12 para Arduino"
	@echo "  make upload12_debug - Upload Test 12 DEBUG para Arduino"
	@echo "  make monitor    - Abre monitor serial (115200 baud)"
	@echo "  make clean      - Remove arquivos compilados"
	@echo ""
	@echo "Exemplo de uso completo:"
	@echo "  make test5 upload5 monitor"
	@echo "====================================================================="

# ====================================================================
# Compilação
# ====================================================================

test1: $(TEST1_HEX)
	@echo "✓ Test 1 compilado com sucesso!"
	@echo "  Saída esperada: 'Teste 1: 1 + 2 = ?\\r\\nResultado: 3\\r\\n'"

test2: $(TEST2_HEX)
	@echo "✓ Test 2 compilado com sucesso!"
	@echo "  Saída esperada: 'Teste 2: Spilling test (5 + 2 = ?)\\r\\nResultado: 7\\r\\n'"

test3: $(TEST3_HEX)
	@echo "✓ Test 3 compilado com sucesso!"
	@echo "  Saída esperada: 'Teste 3: 1000 - 234 = ?\\r\\nResultado: 766\\r\\n'"

test4: $(TEST4_HEX)
	@echo "✓ Test 4 compilado com sucesso!"
	@echo "  Saída esperada: 'Teste 4: 123 * 45 = ?\\r\\nResultado: 5535\\r\\n'"

test5: $(TEST5_HEX)
	@echo "✓ Test 5 compilado com sucesso!"
	@echo "  Saída esperada: 'Teste 5: 1234 / 56 = ?\\r\\nResultado: 22\\r\\n'"

test6: $(TEST6_HEX)
	@echo "✓ Test 6 compilado com sucesso!"
	@echo "  Saída esperada: 'Teste 6: 1234 % 56 = ?\\r\\nResultado: 2\\r\\n'"

test7: $(TEST7_HEX)
	@echo "✓ Test 7 compilado com sucesso!"
	@echo "  Saída esperada: 'Teste 7: 100 / 0 = ?\\r\\nResultado: 65535 (ERRO)\\r\\n'"

test8: $(TEST8_HEX)
	@echo "✓ Test 8 compilado com sucesso!"
	@echo "  Saída esperada: '1 0\\r\\n' (100==100=1, 100==99=0)"

test9: $(TEST9_HEX)
	@echo "✓ Test 9 compilado com sucesso!"
	@echo "  Saída esperada: '1 0\\r\\n' (50<100=1, 100<50=0)"

test10: $(TEST10_HEX)
	@echo "✓ Test 10 compilado com sucesso!"
	@echo "  Saída esperada: '1 0 1\\r\\n' (100>=50=1, 50>=100=0, 100>=100=1)"

test11: $(TEST11_HEX)
	@echo "✓ Test 11 compilado com sucesso!"
	@echo "  Saída esperada: '10\\r\\n' (WHILE loop counts 0-9, final value 10)"

test12: $(TEST12_HEX)
	@echo "✓ Test 12 compilado com sucesso!"
	@echo "  Saída esperada: '500\\r\\n' (Real division: 1 | 2 = 500)"

test12_debug: $(TEST12_DEBUG_HEX)
	@echo "✓ Test 12 DEBUG compilado com sucesso!"
	@echo "  Saída esperada: 'A01F4 B05:00 C00:00 500\\r\\n'"

$(TEST1_ELF): $(TEST1_SRC)
	@echo "Compilando $(TEST1_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST1_HEX): $(TEST1_ELF)
	@echo "Gerando HEX para Test 1..."
	$(OBJCOPY) -O ihex $< $@

$(TEST2_ELF): $(TEST2_SRC)
	@echo "Compilando $(TEST2_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST2_HEX): $(TEST2_ELF)
	@echo "Gerando HEX para Test 2..."
	$(OBJCOPY) -O ihex $< $@

$(TEST3_ELF): $(TEST3_SRC)
	@echo "Compilando $(TEST3_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST3_HEX): $(TEST3_ELF)
	@echo "Gerando HEX para Test 3..."
	$(OBJCOPY) -O ihex $< $@

$(TEST4_ELF): $(TEST4_SRC)
	@echo "Compilando $(TEST4_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST4_HEX): $(TEST4_ELF)
	@echo "Gerando HEX para Test 4..."
	$(OBJCOPY) -O ihex $< $@

$(TEST5_ELF): $(TEST5_SRC)
	@echo "Compilando $(TEST5_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST5_HEX): $(TEST5_ELF)
	@echo "Gerando HEX para Test 5..."
	$(OBJCOPY) -O ihex $< $@

$(TEST6_ELF): $(TEST6_SRC)
	@echo "Compilando $(TEST6_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST6_HEX): $(TEST6_ELF)
	@echo "Gerando HEX para Test 6..."
	$(OBJCOPY) -O ihex $< $@

$(TEST7_ELF): $(TEST7_SRC)
	@echo "Compilando $(TEST7_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST7_HEX): $(TEST7_ELF)
	@echo "Gerando HEX para Test 7..."
	$(OBJCOPY) -O ihex $< $@

$(TEST8_ELF): $(TEST8_SRC)
	@echo "Compilando $(TEST8_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST8_HEX): $(TEST8_ELF)
	@echo "Gerando HEX para Test 8..."
	$(OBJCOPY) -O ihex $< $@

$(TEST9_ELF): $(TEST9_SRC)
	@echo "Compilando $(TEST9_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST9_HEX): $(TEST9_ELF)
	@echo "Gerando HEX para Test 9..."
	$(OBJCOPY) -O ihex $< $@

$(TEST10_ELF): $(TEST10_SRC)
	@echo "Compilando $(TEST10_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST10_HEX): $(TEST10_ELF)
	@echo "Gerando HEX para Test 10..."
	$(OBJCOPY) -O ihex $< $@

$(TEST11_ELF): $(TEST11_SRC)
	@echo "Compilando $(TEST11_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST11_HEX): $(TEST11_ELF)
	@echo "Gerando HEX para Test 11..."
	$(OBJCOPY) -O ihex $< $@

$(TEST12_ELF): $(TEST12_SRC)
	@echo "Compilando $(TEST12_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST12_HEX): $(TEST12_ELF)
	@echo "Gerando HEX para Test 12..."
	$(OBJCOPY) -O ihex $< $@

$(TEST12_DEBUG_ELF): $(TEST12_DEBUG_SRC)
	@echo "Compilando $(TEST12_DEBUG_SRC)..."
	$(CC) $(LDFLAGS) -o $@ $<

$(TEST12_DEBUG_HEX): $(TEST12_DEBUG_ELF)
	@echo "Gerando HEX para Test 12 DEBUG..."
	$(OBJCOPY) -O ihex $< $@

# ====================================================================
# Upload para Arduino
# ====================================================================

upload1: $(TEST1_HEX)
	@echo "Fazendo upload de Test 1 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload2: $(TEST2_HEX)
	@echo "Fazendo upload de Test 2 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload3: $(TEST3_HEX)
	@echo "Fazendo upload de Test 3 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload4: $(TEST4_HEX)
	@echo "Fazendo upload de Test 4 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload5: $(TEST5_HEX)
	@echo "Fazendo upload de Test 5 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload6: $(TEST6_HEX)
	@echo "Fazendo upload de Test 6 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload7: $(TEST7_HEX)
	@echo "Fazendo upload de Test 7 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload8: $(TEST8_HEX)
	@echo "Fazendo upload de Test 8 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload9: $(TEST9_HEX)
	@echo "Fazendo upload de Test 9 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload10: $(TEST10_HEX)
	@echo "Fazendo upload de Test 10 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload11: $(TEST11_HEX)
	@echo "Fazendo upload de Test 11 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload12: $(TEST12_HEX)
	@echo "Fazendo upload de Test 12 para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."

upload12_debug: $(TEST12_DEBUG_HEX)
	@echo "Fazendo upload de Test 12 DEBUG para $(PORT)..."
	$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(PORT) -b 115200 -U flash:w:$<
	@echo "✓ Upload concluído! Execute 'make monitor' para ver a saída serial."
	@echo "Expected output: A01F4 B05:00 C00:00 500"

# ====================================================================
# Monitor Serial
# ====================================================================

monitor:
	@echo "Abrindo monitor serial em $(PORT) @ $(BAUD) baud..."
	@echo "Pressione Ctrl+A seguido de K para sair."
	$(SCREEN) $(PORT) $(BAUD)

# ====================================================================
# Limpeza
# ====================================================================

clean:
	@echo "Removendo arquivos compilados..."
	rm -f *.elf *.hex
	@echo "✓ Limpeza concluída!"

# ====================================================================
# Targets de Conveniência
# ====================================================================

# Compila, faz upload e abre monitor em uma única operação
run1: test1 upload1 monitor

run2: test2 upload2 monitor

run3: test3 upload3 monitor

run4: test4 upload4 monitor

run5: test5 upload5 monitor

run6: test6 upload6 monitor

run7: test7 upload7 monitor

run8: test8 upload8 monitor

run9: test9 upload9 monitor

run10: test10 upload10 monitor

run11: test11 upload11 monitor

run12: test12 upload12 monitor

run12_debug: test12_debug upload12_debug monitor

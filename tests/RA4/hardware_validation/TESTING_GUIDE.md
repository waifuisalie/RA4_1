# Hardware Validation Testing Guide - Sub-issue 3.4

This guide explains how to test the arithmetic operations implemented in Sub-issue 3.4 on real Arduino Uno hardware.

## Tests Available

### Test 1: Addition (Basic) ✅
- **Operation:** 1 + 2 = 3
- **Validates:** Basic register allocation, 16-bit addition with carry
- **File:** `test1_serial.s`
- **Expected output:** `Resultado: 3`

### Test 2: Spilling ✅
- **Operation:** 5 + 2 = 7 (with register spilling)
- **Validates:** FIFO spilling to SRAM when registers exhaust
- **File:** `test2_serial.s`
- **Expected output:** `Resultado: 7`

### Test 3: Subtraction (NEW) 🆕
- **Operation:** 1000 - 234 = 766
- **Validates:** 16-bit subtraction with borrow (SUB/SBC instructions)
- **File:** `test3_subtraction.s`
- **Expected output:** `Resultado: 766`
- **Hardware:** Uses SUB (low byte) and SBC (high byte with borrow)

### Test 4: Multiplication (NEW) 🆕
- **Operation:** 123 × 45 = 5535
- **Validates:** 16×16→16 bit multiplication using mul16 subroutine
- **File:** `test4_multiplication.s`
- **Expected output:** `Resultado: 5535`
- **Hardware:** Uses AVR MUL instruction with 4 partial products algorithm

### Test 5: Division (PHASE 3) 🆕
- **Operation:** 1234 ÷ 56 = 22
- **Validates:** 16-bit division using div16 subroutine (shift-subtract algorithm)
- **File:** `test5_division.s`
- **Expected output:** `Resultado: 22`
- **Hardware:** Uses 17-iteration restoring shift-subtract division, ~245 cycles

### Test 6: Modulo (PHASE 3) 🆕
- **Operation:** 1234 % 56 = 2
- **Validates:** 16-bit modulo using div16 subroutine (returns remainder)
- **File:** `test6_modulo.s`
- **Expected output:** `Resultado: 2`
- **Hardware:** Uses same div16 routine, but returns remainder instead of quotient

### Test 7: Division by Zero (ERROR HANDLING) 🆕
- **Operation:** 100 ÷ 0 = error (returns 65535)
- **Validates:** Division by zero error handling
- **File:** `test7_div_by_zero.s`
- **Expected output:** `Resultado: 65535 (ERRO)`
- **Hardware:** Returns 0xFFFF (65535) as error indicator when divisor is zero

## Quick Start

### Option 1: Manual Commands

```bash
cd tests/RA4/hardware_validation

# Test 5 (Division)
avr-gcc -mmcu=atmega328p -o test5_division.elf test5_division.s
avr-objcopy -O ihex test5_division.elf test5_division.hex
avrdude -c arduino -p atmega328p -P /dev/ttyUSB0 -b 115200 -U flash:w:test5_division.hex
screen /dev/ttyUSB0 115200

# Test 6 (Modulo)
avr-gcc -mmcu=atmega328p -o test6_modulo.elf test6_modulo.s
avr-objcopy -O ihex test6_modulo.elf test6_modulo.hex
avrdude -c arduino -p atmega328p -P /dev/ttyUSB0 -b 115200 -U flash:w:test6_modulo.hex
screen /dev/ttyUSB0 115200

# Test 7 (Division by Zero)
avr-gcc -mmcu=atmega328p -o test7_div_by_zero.elf test7_div_by_zero.s
avr-objcopy -O ihex test7_div_by_zero.elf test7_div_by_zero.hex
avrdude -c arduino -p atmega328p -P /dev/ttyUSB0 -b 115200 -U flash:w:test7_div_by_zero.hex
screen /dev/ttyUSB0 115200
```

### Option 2: Using Makefile (Recommended)

```bash
cd tests/RA4/hardware_validation

# Compile only
make test5  # or test6, test7

# Compile and upload
make test5 upload5  # or test6 upload6, test7 upload7

# Compile, upload, and open serial monitor (all-in-one)
make run5  # or run6, run7

# View all available commands
make help
```

## Expected Serial Output

### Test 3 (Subtraction)
```
Teste 3: 1000 - 234 = ?
Resultado: 766
OK - Teste passou!
```

### Test 4 (Multiplication)
```
Teste 4: 123 * 45 = ?
Resultado: 5535
OK - Teste passou!
```

### Test 5 (Division)
```
Teste 5: 1234 / 56 = ?
Resultado: 22
OK - Teste passou!
```

### Test 6 (Modulo)
```
Teste 6: 1234 % 56 = ?
Resultado: 2
OK - Teste passou!
```

### Test 7 (Division by Zero)
```
Teste 7: 100 / 0 = ?
Resultado: 65535 (ERRO)
OK - Teste passou!
```

## Technical Details

### Test 3: Subtraction Implementation

**Assembly Code Generated:**
```asm
; t0 = 1000 (0x03E8)
ldi r16, lo8(1000)    ; r16 = 0xE8
ldi r17, hi8(1000)    ; r17 = 0x03

; t1 = 234 (0x00EA)
ldi r18, lo8(234)     ; r18 = 0xEA
ldi r19, hi8(234)     ; r19 = 0x00

; t2 = t0 - t1
sub r16, r18   ; r16 = 0xE8 - 0xEA = 0xFE (with borrow)
sbc r17, r19   ; r17 = 0x03 - 0x00 - borrow = 0x02
mov r20, r16   ; Result: 0x02FE = 766
mov r21, r17
```

**Verification:**
- 1000 in hex: 0x03E8
- 234 in hex: 0x00EA
- Subtraction: 0x03E8 - 0x00EA = 0x02FE = 766 ✓

### Test 4: Multiplication Implementation

**Assembly Code Generated:**
```asm
; t0 = 123 (0x007B)
ldi r18, lo8(123)
ldi r19, hi8(123)

; t1 = 45 (0x002D)
ldi r20, lo8(45)
ldi r21, hi8(45)

; t2 = t0 * t1
rcall mul16    ; Calls 16-bit multiplication subroutine
mov r20, r24   ; Result in r24:r25
mov r21, r25
```

**mul16 Subroutine Algorithm:**

For (AH:AL) × (BH:BL):
1. **Partial Product 1:** AL × BL → Full 16-bit result
2. **Partial Product 2:** AL × BH → Add to high byte
3. **Partial Product 3:** AH × BL → Add to high byte
4. **Partial Product 4:** AH × BH → Discarded (overflow beyond 16 bits)

**For 123 × 45:**
- 123 = 0x7B (AL=0x7B, AH=0x00)
- 45 = 0x2D (BL=0x2D, BH=0x00)
- P1: 0x7B × 0x2D = 0x159F (keeps 0x9F low, 0x15 to accumulator)
- P2: 0x7B × 0x00 = 0x0000 (contributes nothing)
- P3: 0x00 × 0x2D = 0x0000 (contributes nothing)
- **Result:** 0x159F = 5535 ✓

### Test 5: Division Implementation

**Assembly Code Generated:**
```asm
; t0 = 1234 (0x04D2)
ldi r16, lo8(1234)    ; r16 = 0xD2
ldi r17, hi8(1234)    ; r17 = 0x04

; t1 = 56 (0x0038)
ldi r20, lo8(56)      ; r20 = 0x38
ldi r21, hi8(56)      ; r21 = 0x00

; t2 = t0 / t1
mov r18, r16   ; Dividend to R18:R19
mov r19, r17
rcall div16    ; Calls 16-bit division subroutine
mov r20, r24   ; Quotient from R24:R25
mov r21, r25
```

**div16 Subroutine Algorithm (Restoring Shift-Subtract):**

For dividend D ÷ divisor d:
1. **Initialize:** quotient Q = 0, remainder R = 0
2. **Loop 17 times:**
   - Shift D left (MSB → carry)
   - Shift carry into R
   - If R ≥ d: R = R - d, set quotient bit = 1
   - Else: restore R (already done), quotient bit = 0
3. **Complement:** Final quotient = ~Q (due to carry flag accumulation)
4. **Output:** R24:R25 = quotient, R22:R23 = remainder

**For 1234 ÷ 56:**
- 1234 = 0x04D2 (dividend)
- 56 = 0x0038 (divisor)
- **Result:** 0x0016 = 22 (quotient) ✓
- **Remainder:** 0x0002 = 2

**Performance:** ~245 cycles (17 iterations × ~14 cycles/iteration + overhead)

### Test 6: Modulo Implementation

**Assembly Code Generated:**
```asm
; t0 = 1234 (0x04D2)
ldi r16, lo8(1234)
ldi r17, hi8(1234)

; t1 = 56 (0x0038)
ldi r20, lo8(56)
ldi r21, hi8(56)

; t2 = t0 % t1
mov r18, r16   ; Dividend to R18:R19
mov r19, r17
rcall div16    ; Calls SAME division subroutine
mov r20, r22   ; Remainder from R22:R23 (not quotient!)
mov r21, r23
```

**Key difference from division:** Copies R22:R23 (remainder) instead of R24:R25 (quotient)

**For 1234 % 56:**
- Uses same div16 algorithm
- **Quotient (discarded):** 22
- **Remainder (returned):** 2 ✓

### Test 7: Division by Zero Handling

**Error Handling in div16:**
```asm
div16:
    push r16

    ; Check for division by zero
    cp      r20, r1       ; Compare divisor low with 0
    cpc     r21, r1       ; Compare divisor high with 0
    breq    div16_by_zero ; If zero, jump to error handler

    ; ... normal division algorithm ...

div16_by_zero:
    ; Return error values
    ldi     r24, 0xFF     ; Quotient = 0xFFFF (error indicator)
    ldi     r25, 0xFF
    mov     r22, r18      ; Remainder = original dividend
    mov     r23, r19
    pop r16
    ret
```

**For 100 ÷ 0:**
- **Quotient returned:** 0xFFFF = 65535 (error indicator)
- **Remainder returned:** 100 (original dividend)
- **Purpose:** Prevents infinite loop, provides detectable error value

## Troubleshooting

### Test 3 Issues

**Problem:** Wrong result displayed

**Possible causes:**
1. SUB/SBC order incorrect (should be SUB then SBC)
2. Borrow flag not propagating correctly
3. Operands in wrong order (should be op1 - op2, not op2 - op1)

**Verification:**
- Expected: 1000 - 234 = 766
- If you get 65770 (0xFFFFFDA), operands are swapped (234 - 1000 with underflow)

### Test 4 Issues

**Problem:** Wrong multiplication result

**Possible causes:**
1. Partial products not accumulated correctly
2. MUL instruction result (R1:R0) not copied properly
3. Register allocation conflict in mul16 routine
4. R1 not cleared after MUL (can affect subsequent operations)

**Verification:**
- Expected: 123 × 45 = 5535
- Common errors:
  - 5535 (0x159F) ✓ Correct
  - 159 (0x9F) → Only using low byte of P1
  - 21 (0x15) → Only using high byte of P1

### Test 5 Issues

**Problem:** Wrong division result

**Possible causes:**
1. Shift direction incorrect (should be ROL, not ROR)
2. Comparison logic inverted (BRCS vs BRCC)
3. Quotient not complemented at end (missing COM instruction)
4. Loop counter wrong (should be 17, not 16)

**Verification:**
- Expected: 1234 ÷ 56 = 22
- Common errors:
  - 22 (0x16) ✓ Correct
  - 233 (0xE9) → Quotient not complemented (~22 = 233)
  - 0 or garbage → Loop/shift logic broken

### Test 6 Issues

**Problem:** Wrong modulo result

**Possible causes:**
1. Copying quotient (R24:R25) instead of remainder (R22:R23)
2. Remainder not accumulated correctly in div16
3. Using wrong output registers

**Verification:**
- Expected: 1234 % 56 = 2
- Common errors:
  - 2 (0x02) ✓ Correct
  - 22 (0x16) → Copied quotient instead of remainder

### Test 7 Issues

**Problem:** Division by zero doesn't return error

**Possible causes:**
1. Zero check missing or incorrect (CP/CPC instructions)
2. Branch to error handler missing (BREQ div16_by_zero)
3. R1 not zero (should be CLR R1 in initialization)

**Verification:**
- Expected: 100 ÷ 0 = 65535
- If you get 0, 100, or other values → Error handler not working

## Register Usage

### Test 3 (Subtraction)
- **R16:R17** - t0 (1000), then modified to result
- **R18:R19** - t1 (234)
- **R20:R21** - t2 (result = 766)

### Test 4 (Multiplication)
- **R18:R19** - Input: operand 1 (123)
- **R20:R21** - Input: operand 2 (45), Output: result (5535)
- **R24:R25** - mul16 result register
- **R0:R1** - MUL instruction result (volatile)
- **R22:R23** - Accumulator in mul16 (saved/restored)

### Test 5 (Division)
- **R16:R17** - Input: dividend (1234)
- **R18:R19** - Working: dividend/quotient (modified during algorithm)
- **R20:R21** - Input: divisor (56), Output: quotient (22)
- **R22:R23** - Remainder accumulator (discarded for division)
- **R24:R25** - div16 quotient result register
- **R16** - Loop counter (saved/restored)

### Test 6 (Modulo)
- **R16:R17** - Input: dividend (1234)
- **R18:R19** - Working: dividend/quotient (modified during algorithm)
- **R20:R21** - Input: divisor (56), Output: remainder (2)
- **R22:R23** - div16 remainder result register
- **R24:R25** - Quotient (discarded for modulo)
- **R16** - Loop counter (saved/restored)

### Test 7 (Division by Zero)
- Same register usage as Test 5
- **Special return:** R24:R25 = 0xFFFF (error indicator)

## Serial Communication

- **Baud Rate:** 115200
- **Format:** 8N1 (8 data bits, no parity, 1 stop bit)
- **UART Registers:**
  - UBRR0L (0xC4) = 8
  - UBRR0H (0xC5) = 0
  - UCSR0B (0xC1) = TX enable
  - UCSR0C (0xC2) = 8N1 format
  - UDR0 (0xC6) = Data register

## Integration with Compiler

These tests validate that the code generated by `gerador_assembly.py` will work correctly on real hardware:

### Subtraction Operator (`-`)
```python
def _processar_subtracao_16bit(self, instr):
    # Generates:
    # sub r{op1_low}, r{op2_low}
    # sbc r{op1_high}, r{op2_high}
    # mov r{res_low}, r{op1_low}
    # mov r{res_high}, r{op1_high}
```

### Multiplication Operator (`*`)
```python
def _processar_multiplicacao_16bit(self, instr):
    # Generates:
    # mov r18, r{op1_low}
    # mov r19, r{op1_high}
    # mov r20, r{op2_low}
    # mov r21, r{op2_high}
    # rcall mul16
    # mov r{res_low}, r24
    # mov r{res_high}, r25
```

The `mul16` subroutine is automatically generated in the epilogue when multiplication is used.

### Division Operator (`/`)
```python
def _processar_divisao_16bit(self, instr):
    # Generates:
    # mov r18, r{op1_low}   ; Dividend
    # mov r19, r{op1_high}
    # mov r20, r{op2_low}   ; Divisor
    # mov r21, r{op2_high}
    # rcall div16
    # mov r{res_low}, r24   ; Quotient
    # mov r{res_high}, r25
```

The `div16` subroutine is automatically generated in the epilogue when division is used.

### Modulo Operator (`%`)
```python
def _processar_modulo_16bit(self, instr):
    # Generates:
    # mov r18, r{op1_low}   ; Dividend
    # mov r19, r{op1_high}
    # mov r20, r{op2_low}   ; Divisor
    # mov r21, r{op2_high}
    # rcall div16
    # mov r{res_low}, r22   ; Remainder (not quotient!)
    # mov r{res_high}, r23
```

Uses the same `div16` subroutine, but extracts the remainder instead of quotient.

## Next Steps

After validating these tests on hardware:

1. ✅ **Subtraction** - Implemented and unit tested
2. ✅ **Multiplication** - Implemented and unit tested
3. ✅ **Division** - Implemented and unit tested
4. ✅ **Modulo** - Implemented and unit tested
5. ⏳ **Hardware validation** - Tests 5-7 ready for Arduino upload
6. ⏳ **Exponentiation** (Phase 4) - To be implemented

---

**Created:** 2025-11-22
**Updated:** 2025-11-22 (Phase 3 completed)
**Sub-issue:** 3.4 (Arithmetic Operations Mapping)
**Status:** Phases 1-3 complete (unit tests passed), hardware validation ready

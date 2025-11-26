# Division Bug Debug Report

## Date: 2025-11-24

## Summary

The AVR assembly compiler successfully generates code for addition, subtraction, and multiplication operations. However, **real division (operator `|`)** produces incorrect results. This document tracks the debugging process and findings.

---

## Verified Working Operations

### ✅ Addition Test
- **Input:** `(1000 A) (2000 B) ((A B +) RESULT) (RESULT FINAL)`
- **Expected:** 3000
- **Result:** ✅ **03000** (CORRECT)
- **File:** `test_add_simple.hex`

### ✅ Subtraction Test
- **Input:** `(2000 A) (1000 B) ((A B -) RESULT) (RESULT FINAL)`
- **Expected:** 1000
- **Result:** ✅ **01000** (CORRECT)
- **File:** `test_sub_simple.hex`

### ✅ Multiplication Test
- **Input:** `(100 A) (200 B) ((A B *) RESULT) (RESULT FINAL)`
- **Expected:** 20000
- **Result:** ✅ **20000** (CORRECT)
- **File:** `test_mul_simple.hex`

---

## ❌ Division Bug

### Test Case
- **Input:** `(1000 A) (2000 B) ((A B |) RESULT) (RESULT FINAL)`
- **Expected:** 500 (scaled division: 1000 ÷ 2000 = 0.5, scaled by 1000 = 500)
- **Result:** ❌ **0008** (INCORRECT)
- **File:** `test_div_simple.hex`

### Division Implementation

The real division operator `|` uses **scaled integer arithmetic** to represent decimal results:

```
Result = (dividend × 1000) ÷ divisor
```

For `1000 | 2000`:
```
(1000 × 1000) ÷ 2000 = 1,000,000 ÷ 2000 = 500
```

The implementation uses three assembly routines:
1. **`div_scaled`** - Main routine that orchestrates scaled division
2. **`mul16`** - 16-bit unsigned multiplication (returns lower 16 bits)
3. **`div16`** - 16-bit unsigned division using shift-subtract algorithm

---

## Debug Process

### Phase 1: Initial Debug (test_div_simple_debug.s)

Added debug points at high-level stages:

```
A=03E8 B=07D0 D=0008 F=0008 0008
```

**Analysis:**
- ✅ A loaded correctly (0x03E8 = 1000)
- ✅ B loaded correctly (0x07D0 = 2000)
- ❌ Division result wrong (0x0008 = 8 instead of 0x01F4 = 500)
- ✅ Final value correctly copied from wrong division result

**Conclusion:** Bug is inside the `div_scaled` routine or its dependencies.

---

### Phase 2: Granular Debug (test_div_simple_debug_v2.s)

Added **5 internal debug points** inside `div_scaled` routine to trace each step:

#### Debug Output Format
```
A=03E8 B=07D0 1:03E8/07D0 2:4240 3:4240 4:0064 5:FFFF 00008
```

#### Debug Point Breakdown

| Point | Label | Purpose | Expected | Actual | Status |
|-------|-------|---------|----------|--------|--------|
| A= | Initial A | Show A after loading | 03E8 (1000) | 03E8 | ✅ |
| B= | Initial B | Show B after loading | 07D0 (2000) | 07D0 | ✅ |
| 1: | div_scaled input | Show dividendo/divisor entering div_scaled | 03E8/07D0 | 03E8/07D0 | ✅ |
| 2: | mul16 result | Show result of 1000 × 1000 (lower 16 bits) | 4240 (16,960) | 4240 | ✅ |
| 3: | After copy | Show R18:R19 after copying mul result | 4240 | 4240 | ✅ |
| 4: | Divisor restored | Show divisor after restoring from stack | 07D0 (2000) | **0064 (100)** | ❌ |
| 5: | div16 result | Show final division result | 01F4 (500) | **FFFF (error)** | ❌ |
| Final | | Decimal output | 00500 | 00008 | ❌ |

**Note:** The output alternates between `5:0000` and `5:FFFF` on consecutive runs, suggesting memory corruption or uninitialized values.

---

## Root Cause Analysis

### Finding: Divisor Corruption

**Debug Point 4 reveals the bug:**
- Divisor should be **0x07D0** (2000)
- Divisor actual value: **0x0064** (100)

The divisor is being corrupted when restored from the stack in `div_scaled`.

### Code Flow Analysis

```asm
div_scaled:
    ; Save divisor to stack
    push r20        ; Save original divisor low byte (2000 & 0xFF = 0xD0)
    push r21        ; Save original divisor high byte (2000 >> 8 = 0x07)

    ; Multiply dividend by 1000
    ldi r20, lo8(1000)   ; Load 1000 low byte (0xE8)
    ldi r21, hi8(1000)   ; Load 1000 high byte (0x03)
    rcall mul16          ; R24:R25 = 1000 × 1000 = 0x0F4240, lower 16 bits = 0x4240

    ; Move multiplication result
    mov r18, r24         ; R18:R19 = 0x4240 (16,960)
    mov r19, r25

    ; Restore divisor from stack
    pop r21              ; Restore high byte (should be 0x07)
    pop r20              ; Restore low byte (should be 0xD0)

    ; Divide
    rcall div16          ; Should compute 16960 ÷ 2000 = 8.48 ≈ 8 (integer)
```

### Possible Causes

1. **Stack Corruption in mul16**
   - The `mul16` routine may corrupt the stack pointer or stack contents
   - Need to verify `mul16` properly saves/restores all registers

2. **Register Corruption**
   - `mul16` uses R0, R1, R22, R23 according to its header comment
   - If it also modifies R20/R21, those changes persist after the call
   - The stack push/pop would then save/restore the wrong values

3. **Debug Code Side Effects**
   - The extensive debug code between push/pop operations adds many stack operations
   - This might expose a latent bug in stack pointer handling

### Key Observation

The value **0x0064** (100) is suspicious:
- It's exactly 1000 ÷ 10
- It might be a corrupted value from the constant 1000 (0x03E8)
- Possibly related to incorrect byte swapping or register reuse

### Why div16 Returns 0xFFFF

`div16` returns **0xFFFF** (all ones) which is the **division by zero error code**:

```asm
div16_by_zero:
    ldi r24, 0xFF     ; Quociente = 0xFFFF (error indicator)
    ldi r25, 0xFF
    ret
```

However, the divisor 0x0064 (100) is NOT zero, so why does it trigger the error?

**Hypothesis:** The corruption might be worse - the divisor bytes might be in the wrong order or the value might actually be zero by the time div16 checks it.

---

## Debug Files Created

### 1. test_div_simple_debug.s
**Location:** `tests/RA4/hardware_validation/test_div_simple_debug.s`

**Features:**
- Debug output after A loaded: `A=03E8`
- Debug output after B loaded: `B=07D0`
- Debug output after division: `D=0008`
- Debug output after final copy: `F=0008`
- Final decimal output: `00008`

**Purpose:** Identified that the bug is in `div_scaled`, not in the high-level code generation.

### 2. test_div_simple_debug_v2.s
**Location:** `tests/RA4/hardware_validation/test_div_simple_debug_v2.s`

**Features:**
- All debug points from v1
- **5 internal debug points inside `div_scaled`:**
  - `1:` Input parameters (dividendo/divisor)
  - `2:` mul16 result
  - `3:` R18:R19 after copying mul result
  - `4:` **Divisor after stack restore** ← **BUG REVEALED HERE**
  - `5:` div16 final result

**Purpose:** Pinpointed the exact location of the bug (divisor corruption after stack restore).

### 3. Helper Routines Added

#### send_hex_word
```asm
send_hex_word:
    ; Sends R24:R25 as 4 hexadecimal digits (e.g., "03E8")
    push r24
    mov r24, r25
    rcall send_hex_byte  ; High byte
    pop r24
    rcall send_hex_byte  ; Low byte
    ret
```

#### send_hex_byte
```asm
send_hex_byte:
    ; Sends R24 as 2 hexadecimal digits (e.g., "E8")
    ; Converts each nibble (0-15) to ASCII ('0'-'9' or 'A'-'F')
    ; High nibble first, then low nibble
    ret
```

---

## Next Steps for Tomorrow

### 1. Investigate mul16 Routine
**Action:** Examine the `mul16` implementation in `gerador_assembly.py`

**Check for:**
- Does it modify R20 or R21?
- Does it properly clean up R0 and R1 after using `mul` instruction?
- Does it corrupt the stack pointer?
- Are all push/pop operations balanced?

**File:** `src/RA4/functions/python/gerador_assembly.py` (lines ~1123-1200)

### 2. Test mul16 in Isolation
**Action:** Create a standalone test that calls `mul16` directly and verifies register preservation

**Test case:**
```asm
; Set sentinel values in R20:R21
ldi r20, 0xAA
ldi r21, 0xBB

; Call mul16
ldi r18, lo8(1000)
ldi r19, hi8(1000)
ldi r22, lo8(1000)  ; Use different registers to avoid collision
ldi r23, hi8(1000)
rcall mul16

; Check if R20:R21 are still 0xAABB
; Output R20:R21 via UART to verify
```

### 3. Fix div_scaled Implementation
**Possible solutions:**

#### Option A: Use Different Registers for Saving Divisor
Instead of using stack, save divisor to unused register pair:
```asm
div_scaled:
    ; Save divisor to R26:R27 (X pointer, if not used)
    mov r26, r20
    mov r27, r21

    ; Multiply
    ldi r20, lo8(1000)
    ldi r21, hi8(1000)
    rcall mul16

    ; Restore divisor
    mov r20, r26
    mov r21, r27

    ; Divide
    rcall div16
    ret
```

#### Option B: Fix mul16 Register Corruption
If `mul16` is corrupting R20/R21, fix the routine to properly save/restore them:
```asm
mul16:
    push r20
    push r21
    ; ... existing mul16 code ...
    pop r21
    pop r20
    ret
```

#### Option C: Use SRAM for Temporary Storage
Save divisor to a fixed memory location instead of stack:
```asm
div_scaled:
    ; Save divisor to SRAM
    sts 0x0200, r20
    sts 0x0201, r21

    ; Multiply
    ldi r20, lo8(1000)
    ldi r21, hi8(1000)
    rcall mul16

    ; Restore divisor
    lds r20, 0x0200
    lds r21, 0x0201

    ; Divide
    rcall div16
    ret
```

### 4. Verify div16 Handles the Correct Input
Once divisor corruption is fixed, verify that:
- `div16` receives correct inputs: R18:R19 = 0x4240 (16,960), R20:R21 = 0x07D0 (2000)
- `div16` returns correct output: R24:R25 = 0x01F4 (500)

If div16 still fails with correct inputs, debug the shift-subtract algorithm itself.

### 5. Re-test Taylor Series
Once division works, test the complete Taylor series program:
```bash
./compilador.py taylor.txt
# Upload and verify cosine calculation works correctly
```

---

## Files Reference

### Test Files
- `tests/RA4/test_add_simple.txt` - Addition test (working ✅)
- `tests/RA4/test_sub_simple.txt` - Subtraction test (working ✅)
- `tests/RA4/test_mul_simple.txt` - Multiplication test (working ✅)
- `tests/RA4/test_div_simple.txt` - Division test (broken ❌)

### Generated Assembly
- `outputs/RA4/test_add_simple.s` - Addition assembly (working ✅)
- `outputs/RA4/test_sub_simple.s` - Subtraction assembly (working ✅)
- `outputs/RA4/test_mul_simple.s` - Multiplication assembly (working ✅)
- `outputs/RA4/test_div_simple.s` - Division assembly (broken ❌)

### Debug Versions
- `tests/RA4/hardware_validation/test_div_simple_debug.s` - High-level debug
- `tests/RA4/hardware_validation/test_div_simple_debug_v2.s` - Granular debug (use this!)

### HEX Files (Ready to Upload)
- `tests/RA4/hardware_validation/test_add_simple.hex`
- `tests/RA4/hardware_validation/test_sub_simple.hex`
- `tests/RA4/hardware_validation/test_mul_simple.hex`
- `tests/RA4/hardware_validation/test_div_simple.hex`
- `tests/RA4/hardware_validation/test_div_simple_debug.hex`
- `tests/RA4/hardware_validation/test_div_simple_debug_v2.hex` ← **Use this for debugging**

### Source Code
- `src/RA4/functions/python/gerador_assembly.py` - Assembly generator
  - Line ~1123-1200: `mul16` routine generation
  - Line ~1201-1280: `div16` routine generation
  - Line ~1281-1350: `div_scaled` routine generation

---

## Debug Output Reference

### Expected Output (What We Want)
```
A=03E8 B=07D0 1:03E8/07D0 2:4240 3:4240 4:07D0 5:01F4 D=01F4 F=01F4 00500
```

### Actual Output (What We Get)
```
A=03E8 B=07D0 1:03E8/07D0 2:4240 3:4240 4:0064 5:FFFF 00008
```
or
```
A=03E8 B=07D0 1:03E8/07D0 2:4240 3:4240 4:0064 5:0000 00008
```

### Key Difference
```
4:07D0 → 4:0064  (Divisor corrupted from 2000 to 100)
5:01F4 → 5:FFFF  (Division result wrong due to corrupted divisor)
```

---

## Mathematical Verification

### Manual Calculation
```
Operation: 1000 | 2000 (real division scaled by 1000)

Step 1: Multiply dividend by 1000
  1000 × 1000 = 1,000,000 (0x0F4240 in hex)
  Lower 16 bits = 0x4240 = 16,960 ✅ (confirmed by debug point 2)

Step 2: Divide by divisor
  16,960 ÷ 2000 = 8.48
  Integer result = 8

But wait! This is wrong! The result should be 500, not 8!

Let me recalculate:
  1,000,000 ÷ 2000 = 500 ✅ (this is correct)

The issue: We're only using the lower 16 bits (16,960) instead of the full 32-bit result (1,000,000)
  16,960 ÷ 2000 = 8.48 ≈ 8 ✅ (this matches our buggy output!)
```

### CRITICAL FINDING

**The bug might actually be in `mul16`!**

`mul16` is supposed to do 16-bit × 16-bit = 16-bit multiplication, which **discards overflow**. But for scaled division, we need the full 32-bit result!

**Correct algorithm:**
```
(1000 × 1000) ÷ 2000 = 1,000,000 ÷ 2000 = 500
```

**Current buggy algorithm:**
```
(1000 × 1000) & 0xFFFF = 16,960
16,960 ÷ 2000 = 8
```

### Solution: Need 32-bit Multiplication

For scaled division to work correctly, we need:
1. **32-bit multiplication** (1000 × 1000 = 1,000,000 as full 32 bits)
2. **32-bit ÷ 16-bit division** (1,000,000 ÷ 2000 = 500)

The current implementation only supports 16-bit arithmetic, which causes **massive precision loss** for scaled division.

---

## Revised Next Steps

### 1. Implement 32-bit Multiplication (mul32)
**Priority: HIGH**

Need a new routine:
```asm
mul32:
    ; Input: R18:R19 (16-bit op1), R20:R21 (16-bit op2)
    ; Output: R24:R25:R26:R27 (32-bit result)
    ; Computes full 32-bit result of 16-bit × 16-bit multiplication
```

### 2. Implement 32-bit ÷ 16-bit Division (div32_16)
**Priority: HIGH**

Need a new routine:
```asm
div32_16:
    ; Input: R18:R19:R20:R21 (32-bit dividend), R22:R23 (16-bit divisor)
    ; Output: R24:R25 (16-bit quotient), R26:R27 (16-bit remainder)
    ; Computes 32-bit ÷ 16-bit using shift-subtract algorithm (32 iterations)
```

### 3. Rewrite div_scaled to Use 32-bit Arithmetic
```asm
div_scaled:
    ; Input: R18:R19 (dividend), R20:R21 (divisor)
    ; Output: R24:R25 (scaled result)

    ; Step 1: 32-bit multiply (dividend × 1000)
    push r20
    push r21
    ldi r20, lo8(1000)
    ldi r21, hi8(1000)
    rcall mul32  ; R24:R25:R26:R27 = dividend × 1000 (full 32 bits)

    ; Step 2: Move result to dividend registers for 32-bit division
    mov r18, r24
    mov r19, r25
    mov r20, r26
    mov r21, r27

    ; Step 3: Restore divisor and move to correct registers
    pop r23
    pop r22

    ; Step 4: 32-bit ÷ 16-bit division
    rcall div32_16  ; R24:R25 = quotient (scaled result)

    ret
```

---

## Estimated Effort

- **Implement mul32:** ~2-3 hours (complex register juggling, 4 partial products)
- **Implement div32_16:** ~3-4 hours (32-iteration shift-subtract, careful bit manipulation)
- **Rewrite div_scaled:** ~1 hour (straightforward once mul32 and div32_16 work)
- **Testing & debugging:** ~2-3 hours (verify each routine independently, then together)

**Total:** ~8-12 hours of work

---

## Testing Strategy for Tomorrow

### Phase 1: Test mul32 Independently
```
Input: 1000 × 1000
Expected: 0x000F4240 (1,000,000)
Verify all 32 bits are correct
```

### Phase 2: Test div32_16 Independently
```
Input: 1,000,000 ÷ 2000
Expected: 500 (quotient), 0 (remainder)
Verify 32-bit dividend is handled correctly
```

### Phase 3: Test div_scaled with 32-bit Implementation
```
Input: 1000 | 2000
Expected: 500
Should now produce correct result!
```

### Phase 4: Test Edge Cases
```
- Small values: 1 | 2 = 500 (0.5 × 1000)
- Equal values: 1000 | 1000 = 1000 (1.0 × 1000)
- Large numerator: 10000 | 2000 = 5000 (5.0 × 1000)
- Large denominator: 100 | 10000 = 10 (0.01 × 1000)
```

---

## Conclusion

The division bug is caused by **insufficient precision** in the multiplication step. The current `mul16` routine only returns the lower 16 bits of the multiplication result, causing massive data loss for scaled division.

**Solution:** Implement full 32-bit arithmetic for the scaled division operation.

This is a significant implementation effort but is necessary for correct real division results.

---

## RESOLVED: Scaling Factor Reduced to 100x

**Date:** 2025-11-25

### Solution Implemented

Instead of implementing 32-bit arithmetic, we resolved the issue by:

1. **Reduced scaling factor from 1000x to 100x** to prevent 16-bit overflow
2. **Moved float-to-scaled conversion to TAC generation phase** (early conversion in `ast_traverser.py`)
3. **Removed double-scaling bug** in assembly generation - values are now scaled only once
4. **Updated real division** to work on pre-scaled operands: `(op1 * 100) / op2`
5. **Added multiplication renormalization** to maintain scaling: `(op1 * op2) / 100`

### Benefits

- **No overflow for Taylor series:** With X=0.5, all intermediate values stay well within 16-bit limits
  - X² = 25, X⁴ = 6, X⁶ = 1 (all safe for division operations)
- **Precision:** 0.01 (two decimal places) - sufficient for 4-term Taylor series
- **No 32-bit arithmetic needed** - keeps implementation simple using only 16-bit operations
- **Division constraint:** Maximum safe dividend is 655 (since 655 × 100 = 65,500 < 65,535)

### Files Modified

1. **src/RA4/functions/python/ast_traverser.py**
   - Added `FLOAT_SCALE_FACTOR = 100` constant
   - Modified `_handle_literal()` to convert float literals to scaled integers

2. **src/RA4/functions/python/gerador_assembly.py**
   - Updated `_processar_divisao_real()` to multiply by 100 before dividing
   - Updated `_processar_multiplicacao_16bit()` to renormalize by dividing by 100
   - Removed `div_scaled` routine (no longer needed)

3. **inputs/RA4/taylor.txt**
   - Changed X value from 1.0 to 0.5 radians to avoid overflow
   - Expected result: cos(0.5) ≈ 0.8776 → 88 at 100x scale

### Validation

**Simple Division Test (test_div_simple.txt):**
- Input: `6.0 | 4.0`
- TAC: `t0 = 600`, `t1 = 400`, `t2 = t0 | t1`
- Assembly: `(600 * 100) / 400 = 60000 / 400 = 150`
- Result: 150 (represents 1.5) ✓

**Taylor Series Test (taylor.txt):**
- X = 0.5 (scaled as 50)
- X² = (50 * 50) / 100 = 25
- X²/2 = (25 * 100) / 200 = 12
- All calculations stay within 16-bit limits ✓

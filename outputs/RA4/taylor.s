; ====================================================================
; Código Assembly gerado automaticamente
; Arquitetura: AVR ATmega328P (Arduino Uno)
; Compilador: RA4_Compiladores - Fase 4
; ====================================================================

.section .text
.global main

main:
    ; Inicializar stack pointer
    ldi r16, lo8(0x08FF)   ; RAMEND low byte
    out 0x3D, r16          ; SPL
    ldi r16, hi8(0x08FF)   ; RAMEND high byte
    out 0x3E, r16          ; SPH

    ; Inicializar UART (115200 baud @ 16MHz)
    rcall uart_init

    ; ==== INÍCIO DO CÓDIGO GERADO ====

    ; TAC linha 1: t0 = 100
    ldi r16, 100   ; Constante 100 (low byte)
    ldi r17, 0  ; Constante 100 (high byte)

    ; TAC linha 1: X_VAL = t0
    mov r18, r16   ; X_VAL = t0
    mov r19, r17

    ; TAC linha 2: t1 = 100
    ldi r20, 100   ; Constante 100 (low byte)
    ldi r21, 0  ; Constante 100 (high byte)

    ; TAC linha 2: TERM1 = t1
    mov r22, r20   ; TERM1 = t1
    mov r23, r21

    ; TAC linha 3: t2 = 1
    ldi r16, 1   ; Constante 1 (low byte)
    ldi r17, 0  ; Constante 1 (high byte)

    ; Spill t0 (r16:r17) -> 0x0100
    sts 0x0100, r16      ; Store low byte
    sts 0x0101, r17  ; Store high byte

    ; TAC linha 3: COUNTER = t2
    mov r18, r16   ; COUNTER = t2
    mov r19, r17

    ; Spill X_VAL (r18:r19) -> 0x0102
    sts 0x0102, r18      ; Store low byte
    sts 0x0103, r19  ; Store high byte

L0:

    ; TAC linha 4: t3 = 1
    ldi r20, 1   ; Constante 1 (low byte)
    ldi r21, 0  ; Constante 1 (high byte)

    ; Spill t1 (r20:r21) -> 0x0104
    sts 0x0104, r20      ; Store low byte
    sts 0x0105, r21  ; Store high byte

    ; TAC linha 4: t4 = COUNTER <= t3
    ; Comparação 16-bit menor ou igual (unsigned)
    ; Implementado como: B >= A (operandos trocados)
    cp r20, r18      ; Compare B with A (reversed)
    cpc r21, r19
    ldi r22, 0               ; Assume false
    ldi r23, 0
    brlo skip_le_4               ; If B < A, skip
    ldi r22, 1               ; Set true (B >= A, i.e., A <= B)
skip_le_4:

    ; Spill TERM1 (r22:r23) -> 0x0106
    sts 0x0106, r22      ; Store low byte
    sts 0x0107, r23  ; Store high byte

    ; TAC linha 4: ifFalse t4 goto L1
    ; Check if t4 == 0 (false)
    ldi r24, 0                  ; Zero constant for comparison
    ldi r25, 0
    cp r22, r24         ; Compare low byte with 0
    cpc r23, r25       ; Compare high byte with carry
    breq L1               ; Branch if equal (condition is false)

    ; TAC linha 4: t5 = X_VAL * X_VAL
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r16
    mov r19, r17
    mov r20, r16
    mov r21, r17
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r18, r24
    mov r19, r25

    ; Spill t2 (r16:r17) -> 0x0108
    sts 0x0108, r16      ; Store low byte
    sts 0x0109, r17  ; Store high byte

    ; Load X_VAL de 0x0102 -> r16:r17
    lds r16, 0x0102      ; Load low byte
    lds r17, 0x0103  ; Load high byte

    ; Spill COUNTER (r18:r19) -> 0x010A
    sts 0x010A, r18      ; Store low byte
    sts 0x010B, r19  ; Store high byte

    ; TAC linha 4: X_SQUARE = t5
    mov r20, r18   ; X_SQUARE = t5
    mov r21, r19

    ; Spill t3 (r20:r21) -> 0x010C
    sts 0x010C, r20      ; Store low byte
    sts 0x010D, r21  ; Store high byte

    ; TAC linha 4: t6 = 200
    ldi r22, 200   ; Constante 200 (low byte)
    ldi r23, 0  ; Constante 200 (high byte)

    ; Spill t4 (r22:r23) -> 0x010E
    sts 0x010E, r22      ; Store low byte
    sts 0x010F, r23  ; Store high byte

    ; TAC linha 4: FACT_2 = t6
    mov r16, r22   ; FACT_2 = t6
    mov r17, r23

    ; Spill X_VAL (r16:r17) -> 0x0110
    sts 0x0110, r16      ; Store low byte
    sts 0x0111, r17  ; Store high byte

    ; TAC linha 4: t7 = X_SQUARE | FACT_2
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r18, r20      ; Dividendo
    mov r19, r21
    ldi r20, 100             ; Scale factor (100)
    ldi r21, 0
    rcall mul16              ; R24:R25 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r18, r24             ; Move result to dividend registers
    mov r19, r25
    mov r20, r16      ; Divisor
    mov r21, r17
    rcall div16              ; R24:R25 = (op1 * 100) / op2
    mov r18, r24      ; Copy result
    mov r19, r25

    ; Spill t5 (r18:r19) -> 0x0112
    sts 0x0112, r18      ; Store low byte
    sts 0x0113, r19  ; Store high byte

    ; TAC linha 4: TEMP2 = t7
    mov r20, r18   ; TEMP2 = t7
    mov r21, r19

    ; Spill X_SQUARE (r20:r21) -> 0x0114
    sts 0x0114, r20      ; Store low byte
    sts 0x0115, r21  ; Store high byte

    ; TAC linha 4: t8 = 0
    ldi r22, 0   ; Constante 0 (low byte)
    ldi r23, 0  ; Constante 0 (high byte)

    ; Spill t6 (r22:r23) -> 0x0116
    sts 0x0116, r22      ; Store low byte
    sts 0x0117, r23  ; Store high byte

    ; TAC linha 4: t9 = t8 - TEMP2
    ; Subtração 16-bit: t9 = t8 - TEMP2
    sub r22, r20   ; Low byte com borrow
    sbc r23, r21 ; High byte com borrow
    mov r16, r22   ; Resultado em t9
    mov r17, r23

    ; Spill FACT_2 (r16:r17) -> 0x0118
    sts 0x0118, r16      ; Store low byte
    sts 0x0119, r17  ; Store high byte

    ; TAC linha 4: TERM2 = t9
    mov r18, r16   ; TERM2 = t9
    mov r19, r17

    ; Spill t7 (r18:r19) -> 0x011A
    sts 0x011A, r18      ; Store low byte
    sts 0x011B, r19  ; Store high byte

    ; TAC linha 4: t10 = X_SQUARE * X_SQUARE
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r20
    mov r19, r21
    mov r20, r20
    mov r21, r21
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r22, r24
    mov r23, r25

    ; Spill TEMP2 (r20:r21) -> 0x011C
    sts 0x011C, r20      ; Store low byte
    sts 0x011D, r21  ; Store high byte

    ; Load X_SQUARE de 0x0114 -> r20:r21
    lds r20, 0x0114      ; Load low byte
    lds r21, 0x0115  ; Load high byte

    ; Spill t8 (r22:r23) -> 0x011E
    sts 0x011E, r22      ; Store low byte
    sts 0x011F, r23  ; Store high byte

    ; TAC linha 4: X_FOURTH = t10
    mov r16, r22   ; X_FOURTH = t10
    mov r17, r23

    ; Spill t9 (r16:r17) -> 0x0120
    sts 0x0120, r16      ; Store low byte
    sts 0x0121, r17  ; Store high byte

    ; TAC linha 4: t11 = 400
    ldi r18, 144   ; Constante 400 (low byte)
    ldi r19, 1  ; Constante 400 (high byte)

    ; Spill TERM2 (r18:r19) -> 0x0122
    sts 0x0122, r18      ; Store low byte
    sts 0x0123, r19  ; Store high byte

    ; TAC linha 4: t12 = 300
    ldi r20, 44   ; Constante 300 (low byte)
    ldi r21, 1  ; Constante 300 (high byte)

    ; Spill X_SQUARE (r20:r21) -> 0x0124
    sts 0x0124, r20      ; Store low byte
    sts 0x0125, r21  ; Store high byte

    ; TAC linha 4: t13 = t11 * t12
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r18
    mov r19, r19
    mov r20, r20
    mov r21, r21
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r22, r24
    mov r23, r25

    ; Spill t10 (r22:r23) -> 0x0126
    sts 0x0126, r22      ; Store low byte
    sts 0x0127, r23  ; Store high byte

    ; TAC linha 4: TEMP4A = t13
    mov r16, r22   ; TEMP4A = t13
    mov r17, r23

    ; Spill X_FOURTH (r16:r17) -> 0x0128
    sts 0x0128, r16      ; Store low byte
    sts 0x0129, r17  ; Store high byte

    ; TAC linha 4: t14 = 200
    ldi r18, 200   ; Constante 200 (low byte)
    ldi r19, 0  ; Constante 200 (high byte)

    ; Spill t11 (r18:r19) -> 0x012A
    sts 0x012A, r18      ; Store low byte
    sts 0x012B, r19  ; Store high byte

    ; TAC linha 4: t15 = TEMP4A * t14
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r16
    mov r19, r17
    mov r20, r18
    mov r21, r19
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r20, r24
    mov r21, r25

    ; Spill t12 (r20:r21) -> 0x012C
    sts 0x012C, r20      ; Store low byte
    sts 0x012D, r21  ; Store high byte

    ; TAC linha 4: TEMP4B = t15
    mov r22, r20   ; TEMP4B = t15
    mov r23, r21

    ; Spill t13 (r22:r23) -> 0x012E
    sts 0x012E, r22      ; Store low byte
    sts 0x012F, r23  ; Store high byte

    ; TAC linha 4: t16 = 100
    ldi r16, 100   ; Constante 100 (low byte)
    ldi r17, 0  ; Constante 100 (high byte)

    ; Spill TEMP4A (r16:r17) -> 0x0130
    sts 0x0130, r16      ; Store low byte
    sts 0x0131, r17  ; Store high byte

    ; TAC linha 4: t17 = TEMP4B * t16
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r22
    mov r19, r23
    mov r20, r16
    mov r21, r17
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r18, r24
    mov r19, r25

    ; Spill t14 (r18:r19) -> 0x0132
    sts 0x0132, r18      ; Store low byte
    sts 0x0133, r19  ; Store high byte

    ; TAC linha 4: FACT_4 = t17
    mov r20, r18   ; FACT_4 = t17
    mov r21, r19

    ; Spill t15 (r20:r21) -> 0x0134
    sts 0x0134, r20      ; Store low byte
    sts 0x0135, r21  ; Store high byte

    ; TAC linha 4: t18 = X_FOURTH | FACT_4
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r18, r22      ; Dividendo
    mov r19, r23
    ldi r20, 100             ; Scale factor (100)
    ldi r21, 0
    rcall mul16              ; R24:R25 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r18, r24             ; Move result to dividend registers
    mov r19, r25
    mov r20, r20      ; Divisor
    mov r21, r21
    rcall div16              ; R24:R25 = (op1 * 100) / op2
    mov r16, r24      ; Copy result
    mov r17, r25

    ; Spill TEMP4B (r22:r23) -> 0x0136
    sts 0x0136, r22      ; Store low byte
    sts 0x0137, r23  ; Store high byte

    ; Load X_FOURTH de 0x0128 -> r22:r23
    lds r22, 0x0128      ; Load low byte
    lds r23, 0x0129  ; Load high byte

    ; Spill t16 (r16:r17) -> 0x0138
    sts 0x0138, r16      ; Store low byte
    sts 0x0139, r17  ; Store high byte

    ; TAC linha 4: TERM3 = t18
    mov r18, r16   ; TERM3 = t18
    mov r19, r17

    ; Spill t17 (r18:r19) -> 0x013A
    sts 0x013A, r18      ; Store low byte
    sts 0x013B, r19  ; Store high byte

    ; TAC linha 4: t19 = X_FOURTH * X_SQUARE
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r22
    mov r19, r23
    mov r20, r20
    mov r21, r21
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r22, r24
    mov r23, r25

    ; Spill FACT_4 (r20:r21) -> 0x013C
    sts 0x013C, r20      ; Store low byte
    sts 0x013D, r21  ; Store high byte

    ; Load X_SQUARE de 0x0124 -> r20:r21
    lds r20, 0x0124      ; Load low byte
    lds r21, 0x0125  ; Load high byte

    ; Spill X_FOURTH (r22:r23) -> 0x013E
    sts 0x013E, r22      ; Store low byte
    sts 0x013F, r23  ; Store high byte

    ; TAC linha 4: X_SIXTH = t19
    mov r16, r22   ; X_SIXTH = t19
    mov r17, r23

    ; Spill t18 (r16:r17) -> 0x0140
    sts 0x0140, r16      ; Store low byte
    sts 0x0141, r17  ; Store high byte

    ; TAC linha 4: t20 = 600
    ldi r18, 88   ; Constante 600 (low byte)
    ldi r19, 2  ; Constante 600 (high byte)

    ; Spill TERM3 (r18:r19) -> 0x0142
    sts 0x0142, r18      ; Store low byte
    sts 0x0143, r19  ; Store high byte

    ; TAC linha 4: t21 = 500
    ldi r20, 244   ; Constante 500 (low byte)
    ldi r21, 1  ; Constante 500 (high byte)

    ; Spill X_SQUARE (r20:r21) -> 0x0144
    sts 0x0144, r20      ; Store low byte
    sts 0x0145, r21  ; Store high byte

    ; TAC linha 4: t22 = t20 * t21
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r18
    mov r19, r19
    mov r20, r20
    mov r21, r21
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r22, r24
    mov r23, r25

    ; Spill t19 (r22:r23) -> 0x0146
    sts 0x0146, r22      ; Store low byte
    sts 0x0147, r23  ; Store high byte

    ; TAC linha 4: TEMP6A = t22
    mov r16, r22   ; TEMP6A = t22
    mov r17, r23

    ; Spill X_SIXTH (r16:r17) -> 0x0148
    sts 0x0148, r16      ; Store low byte
    sts 0x0149, r17  ; Store high byte

    ; TAC linha 4: t23 = 400
    ldi r18, 144   ; Constante 400 (low byte)
    ldi r19, 1  ; Constante 400 (high byte)

    ; Spill t20 (r18:r19) -> 0x014A
    sts 0x014A, r18      ; Store low byte
    sts 0x014B, r19  ; Store high byte

    ; TAC linha 4: t24 = TEMP6A * t23
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r16
    mov r19, r17
    mov r20, r18
    mov r21, r19
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r20, r24
    mov r21, r25

    ; Spill t21 (r20:r21) -> 0x014C
    sts 0x014C, r20      ; Store low byte
    sts 0x014D, r21  ; Store high byte

    ; TAC linha 4: TEMP6B = t24
    mov r22, r20   ; TEMP6B = t24
    mov r23, r21

    ; Spill t22 (r22:r23) -> 0x014E
    sts 0x014E, r22      ; Store low byte
    sts 0x014F, r23  ; Store high byte

    ; TAC linha 4: t25 = 300
    ldi r16, 44   ; Constante 300 (low byte)
    ldi r17, 1  ; Constante 300 (high byte)

    ; Spill TEMP6A (r16:r17) -> 0x0150
    sts 0x0150, r16      ; Store low byte
    sts 0x0151, r17  ; Store high byte

    ; TAC linha 4: t26 = TEMP6B * t25
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r22
    mov r19, r23
    mov r20, r16
    mov r21, r17
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r18, r24
    mov r19, r25

    ; Spill t23 (r18:r19) -> 0x0152
    sts 0x0152, r18      ; Store low byte
    sts 0x0153, r19  ; Store high byte

    ; TAC linha 4: TEMP6C = t26
    mov r20, r18   ; TEMP6C = t26
    mov r21, r19

    ; Spill t24 (r20:r21) -> 0x0154
    sts 0x0154, r20      ; Store low byte
    sts 0x0155, r21  ; Store high byte

    ; TAC linha 4: t27 = 200
    ldi r22, 200   ; Constante 200 (low byte)
    ldi r23, 0  ; Constante 200 (high byte)

    ; Spill TEMP6B (r22:r23) -> 0x0156
    sts 0x0156, r22      ; Store low byte
    sts 0x0157, r23  ; Store high byte

    ; TAC linha 4: t28 = TEMP6C * t27
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r20
    mov r19, r21
    mov r20, r22
    mov r21, r23
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r16, r24
    mov r17, r25

    ; Spill t25 (r16:r17) -> 0x0158
    sts 0x0158, r16      ; Store low byte
    sts 0x0159, r17  ; Store high byte

    ; TAC linha 4: TEMP6D = t28
    mov r18, r16   ; TEMP6D = t28
    mov r19, r17

    ; Spill t26 (r18:r19) -> 0x015A
    sts 0x015A, r18      ; Store low byte
    sts 0x015B, r19  ; Store high byte

    ; TAC linha 4: t29 = 100
    ldi r20, 100   ; Constante 100 (low byte)
    ldi r21, 0  ; Constante 100 (high byte)

    ; Spill TEMP6C (r20:r21) -> 0x015C
    sts 0x015C, r20      ; Store low byte
    sts 0x015D, r21  ; Store high byte

    ; TAC linha 4: t30 = TEMP6D * t29
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r18
    mov r19, r19
    mov r20, r20
    mov r21, r21
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r22, r24
    mov r23, r25

    ; Spill t27 (r22:r23) -> 0x015E
    sts 0x015E, r22      ; Store low byte
    sts 0x015F, r23  ; Store high byte

    ; TAC linha 4: FACT_6 = t30
    mov r16, r22   ; FACT_6 = t30
    mov r17, r23

    ; Spill t28 (r16:r17) -> 0x0160
    sts 0x0160, r16      ; Store low byte
    sts 0x0161, r17  ; Store high byte

    ; TAC linha 4: t31 = X_SIXTH | FACT_6
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r18, r18      ; Dividendo
    mov r19, r19
    ldi r20, 100             ; Scale factor (100)
    ldi r21, 0
    rcall mul16              ; R24:R25 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r18, r24             ; Move result to dividend registers
    mov r19, r25
    mov r20, r16      ; Divisor
    mov r21, r17
    rcall div16              ; R24:R25 = (op1 * 100) / op2
    mov r20, r24      ; Copy result
    mov r21, r25

    ; Spill TEMP6D (r18:r19) -> 0x0162
    sts 0x0162, r18      ; Store low byte
    sts 0x0163, r19  ; Store high byte

    ; Load X_SIXTH de 0x0148 -> r18:r19
    lds r18, 0x0148      ; Load low byte
    lds r19, 0x0149  ; Load high byte

    ; Spill t29 (r20:r21) -> 0x0164
    sts 0x0164, r20      ; Store low byte
    sts 0x0165, r21  ; Store high byte

    ; TAC linha 4: TEMP8 = t31
    mov r22, r20   ; TEMP8 = t31
    mov r23, r21

    ; Spill t30 (r22:r23) -> 0x0166
    sts 0x0166, r22      ; Store low byte
    sts 0x0167, r23  ; Store high byte

    ; TAC linha 4: t32 = 0
    ldi r16, 0   ; Constante 0 (low byte)
    ldi r17, 0  ; Constante 0 (high byte)

    ; Spill FACT_6 (r16:r17) -> 0x0168
    sts 0x0168, r16      ; Store low byte
    sts 0x0169, r17  ; Store high byte

    ; TAC linha 4: t33 = t32 - TEMP8
    ; Subtração 16-bit: t33 = t32 - TEMP8
    sub r16, r22   ; Low byte com borrow
    sbc r17, r23 ; High byte com borrow
    mov r18, r16   ; Resultado em t33
    mov r19, r17

    ; Spill X_SIXTH (r18:r19) -> 0x016A
    sts 0x016A, r18      ; Store low byte
    sts 0x016B, r19  ; Store high byte

    ; TAC linha 4: TERM4 = t33
    mov r20, r18   ; TERM4 = t33
    mov r21, r19

    ; Spill t31 (r20:r21) -> 0x016C
    sts 0x016C, r20      ; Store low byte
    sts 0x016D, r21  ; Store high byte

    ; TAC linha 4: t34 = TERM1 + TERM2
    ; Soma 16-bit: t34 = TERM1 + TERM2
    add r22, r16   ; Low byte com carry
    adc r23, r17 ; High byte com carry
    mov r18, r22   ; Resultado em t34
    mov r19, r23

    ; Spill TEMP8 (r22:r23) -> 0x016E
    sts 0x016E, r22      ; Store low byte
    sts 0x016F, r23  ; Store high byte

    ; Load TERM1 de 0x0106 -> r22:r23
    lds r22, 0x0106      ; Load low byte
    lds r23, 0x0107  ; Load high byte

    ; Spill t32 (r16:r17) -> 0x0170
    sts 0x0170, r16      ; Store low byte
    sts 0x0171, r17  ; Store high byte

    ; Load TERM2 de 0x0122 -> r16:r17
    lds r16, 0x0122      ; Load low byte
    lds r17, 0x0123  ; Load high byte

    ; Spill t33 (r18:r19) -> 0x0172
    sts 0x0172, r18      ; Store low byte
    sts 0x0173, r19  ; Store high byte

    ; TAC linha 4: SUM12 = t34
    mov r20, r18   ; SUM12 = t34
    mov r21, r19

    ; Spill TERM4 (r20:r21) -> 0x0174
    sts 0x0174, r20      ; Store low byte
    sts 0x0175, r21  ; Store high byte

    ; TAC linha 4: t35 = SUM12 + TERM3
    ; Soma 16-bit: t35 = SUM12 + TERM3
    add r20, r22   ; Low byte com carry
    adc r21, r23 ; High byte com carry
    mov r16, r20   ; Resultado em t35
    mov r17, r21

    ; Spill TERM1 (r22:r23) -> 0x0176
    sts 0x0176, r22      ; Store low byte
    sts 0x0177, r23  ; Store high byte

    ; Load TERM3 de 0x0142 -> r22:r23
    lds r22, 0x0142      ; Load low byte
    lds r23, 0x0143  ; Load high byte

    ; Spill TERM2 (r16:r17) -> 0x0178
    sts 0x0178, r16      ; Store low byte
    sts 0x0179, r17  ; Store high byte

    ; TAC linha 4: SUM123 = t35
    mov r18, r16   ; SUM123 = t35
    mov r19, r17

    ; Spill t34 (r18:r19) -> 0x017A
    sts 0x017A, r18      ; Store low byte
    sts 0x017B, r19  ; Store high byte

    ; TAC linha 4: t36 = SUM123 + TERM4
    ; Soma 16-bit: t36 = SUM123 + TERM4
    add r18, r20   ; Low byte com carry
    adc r19, r21 ; High byte com carry
    mov r22, r18   ; Resultado em t36
    mov r23, r19

    ; Spill SUM12 (r20:r21) -> 0x017C
    sts 0x017C, r20      ; Store low byte
    sts 0x017D, r21  ; Store high byte

    ; Load TERM4 de 0x0174 -> r20:r21
    lds r20, 0x0174      ; Load low byte
    lds r21, 0x0175  ; Load high byte

    ; Spill TERM3 (r22:r23) -> 0x017E
    sts 0x017E, r22      ; Store low byte
    sts 0x017F, r23  ; Store high byte

    ; TAC linha 4: RESULT_COS = t36
    mov r16, r22   ; RESULT_COS = t36
    mov r17, r23

    ; Spill t35 (r16:r17) -> 0x0180
    sts 0x0180, r16      ; Store low byte
    sts 0x0181, r17  ; Store high byte

    ; TAC linha 4: FINAL_COS = RESULT_COS
    mov r18, r16   ; FINAL_COS = RESULT_COS
    mov r19, r17

    ; Spill SUM123 (r18:r19) -> 0x0182
    sts 0x0182, r18      ; Store low byte
    sts 0x0183, r19  ; Store high byte

    ; TAC linha 4: t37 = 1
    ldi r20, 1   ; Constante 1 (low byte)
    ldi r21, 0  ; Constante 1 (high byte)

    ; Spill TERM4 (r20:r21) -> 0x0184
    sts 0x0184, r20      ; Store low byte
    sts 0x0185, r21  ; Store high byte

    ; TAC linha 4: t38 = COUNTER + t37
    ; Soma 16-bit: t38 = COUNTER + t37
    add r22, r20   ; Low byte com carry
    adc r23, r21 ; High byte com carry
    mov r16, r22   ; Resultado em t38
    mov r17, r23

    ; Spill t36 (r22:r23) -> 0x0186
    sts 0x0186, r22      ; Store low byte
    sts 0x0187, r23  ; Store high byte

    ; Load COUNTER de 0x010A -> r22:r23
    lds r22, 0x010A      ; Load low byte
    lds r23, 0x010B  ; Load high byte

    ; Spill RESULT_COS (r16:r17) -> 0x0188
    sts 0x0188, r16      ; Store low byte
    sts 0x0189, r17  ; Store high byte

    ; TAC linha 4: COUNTER = t38
    mov r22, r16   ; COUNTER = t38
    mov r23, r17

    ; TAC linha 4: goto L0
    rjmp L0   ; Salto relativo para L0

L1:

    ; TAC linha 5: t39 = 1000
    ldi r18, 232   ; Constante 1000 (low byte)
    ldi r19, 3  ; Constante 1000 (high byte)

    ; Spill FINAL_COS (r18:r19) -> 0x018A
    sts 0x018A, r18      ; Store low byte
    sts 0x018B, r19  ; Store high byte

    ; TAC linha 5: X_VAL = t39
    mov r20, r18   ; X_VAL = t39
    mov r21, r19

    ; Spill t37 (r20:r21) -> 0x018C
    sts 0x018C, r20      ; Store low byte
    sts 0x018D, r21  ; Store high byte

    ; Load X_VAL de 0x0110 -> r20:r21
    lds r20, 0x0110      ; Load low byte
    lds r21, 0x0111  ; Load high byte

    ; TAC linha 6: t40 = X_VAL * X_VAL
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r20
    mov r19, r21
    mov r20, r20
    mov r21, r21
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r22, r24
    mov r23, r25

    ; Spill COUNTER (r22:r23) -> 0x018E
    sts 0x018E, r22      ; Store low byte
    sts 0x018F, r23  ; Store high byte

    ; TAC linha 6: X_SQUARED = t40
    mov r16, r22   ; X_SQUARED = t40
    mov r17, r23

    ; Spill t38 (r16:r17) -> 0x0190
    sts 0x0190, r16      ; Store low byte
    sts 0x0191, r17  ; Store high byte

    ; TAC linha 7: t41 = 1000
    ldi r18, 232   ; Constante 1000 (low byte)
    ldi r19, 3  ; Constante 1000 (high byte)

    ; Spill t39 (r18:r19) -> 0x0192
    sts 0x0192, r18      ; Store low byte
    sts 0x0193, r19  ; Store high byte

    ; TAC linha 7: TERM1 = t41
    mov r20, r18   ; TERM1 = t41
    mov r21, r19

    ; Spill X_VAL (r20:r21) -> 0x0194
    sts 0x0194, r20      ; Store low byte
    sts 0x0195, r21  ; Store high byte

    ; Load TERM1 de 0x0176 -> r20:r21
    lds r20, 0x0176      ; Load low byte
    lds r21, 0x0177  ; Load high byte

    ; TAC linha 8: t42 = 2000
    ldi r22, 208   ; Constante 2000 (low byte)
    ldi r23, 7  ; Constante 2000 (high byte)

    ; Spill t40 (r22:r23) -> 0x0196
    sts 0x0196, r22      ; Store low byte
    sts 0x0197, r23  ; Store high byte

    ; TAC linha 8: t43 = X_SQUARED | t42
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r18, r16      ; Dividendo
    mov r19, r17
    ldi r20, 100             ; Scale factor (100)
    ldi r21, 0
    rcall mul16              ; R24:R25 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r18, r24             ; Move result to dividend registers
    mov r19, r25
    mov r20, r22      ; Divisor
    mov r21, r23
    rcall div16              ; R24:R25 = (op1 * 100) / op2
    mov r16, r24      ; Copy result
    mov r17, r25

    ; Spill X_SQUARED (r16:r17) -> 0x0198
    sts 0x0198, r16      ; Store low byte
    sts 0x0199, r17  ; Store high byte

    ; TAC linha 8: TEMP1 = t43
    mov r18, r16   ; TEMP1 = t43
    mov r19, r17

    ; Spill t41 (r18:r19) -> 0x019A
    sts 0x019A, r18      ; Store low byte
    sts 0x019B, r19  ; Store high byte

    ; TAC linha 9: t44 = 0
    ldi r20, 0   ; Constante 0 (low byte)
    ldi r21, 0  ; Constante 0 (high byte)

    ; Spill TERM1 (r20:r21) -> 0x019C
    sts 0x019C, r20      ; Store low byte
    sts 0x019D, r21  ; Store high byte

    ; TAC linha 9: t45 = t44 - TEMP1
    ; Subtração 16-bit: t45 = t44 - TEMP1
    sub r20, r18   ; Low byte com borrow
    sbc r21, r19 ; High byte com borrow
    mov r22, r20   ; Resultado em t45
    mov r23, r21

    ; Spill t42 (r22:r23) -> 0x019E
    sts 0x019E, r22      ; Store low byte
    sts 0x019F, r23  ; Store high byte

    ; TAC linha 9: TERM2 = t45
    mov r16, r22   ; TERM2 = t45
    mov r17, r23

    ; Spill t43 (r16:r17) -> 0x01A0
    sts 0x01A0, r16      ; Store low byte
    sts 0x01A1, r17  ; Store high byte

    ; Load TERM2 de 0x0178 -> r16:r17
    lds r16, 0x0178      ; Load low byte
    lds r17, 0x0179  ; Load high byte

    ; TAC linha 10: t46 = X_SQUARED * X_SQUARED
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r18
    mov r19, r19
    mov r20, r18
    mov r21, r19
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r20, r24
    mov r21, r25

    ; Spill TEMP1 (r18:r19) -> 0x01A2
    sts 0x01A2, r18      ; Store low byte
    sts 0x01A3, r19  ; Store high byte

    ; Load X_SQUARED de 0x0198 -> r18:r19
    lds r18, 0x0198      ; Load low byte
    lds r19, 0x0199  ; Load high byte

    ; Spill t44 (r20:r21) -> 0x01A4
    sts 0x01A4, r20      ; Store low byte
    sts 0x01A5, r21  ; Store high byte

    ; TAC linha 10: X_POW4 = t46
    mov r22, r20   ; X_POW4 = t46
    mov r23, r21

    ; Spill t45 (r22:r23) -> 0x01A6
    sts 0x01A6, r22      ; Store low byte
    sts 0x01A7, r23  ; Store high byte

    ; TAC linha 11: t47 = 24000
    ldi r16, 192   ; Constante 24000 (low byte)
    ldi r17, 93  ; Constante 24000 (high byte)

    ; Spill TERM2 (r16:r17) -> 0x01A8
    sts 0x01A8, r16      ; Store low byte
    sts 0x01A9, r17  ; Store high byte

    ; TAC linha 11: t48 = X_POW4 | t47
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r18, r22      ; Dividendo
    mov r19, r23
    ldi r20, 100             ; Scale factor (100)
    ldi r21, 0
    rcall mul16              ; R24:R25 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r18, r24             ; Move result to dividend registers
    mov r19, r25
    mov r20, r16      ; Divisor
    mov r21, r17
    rcall div16              ; R24:R25 = (op1 * 100) / op2
    mov r18, r24      ; Copy result
    mov r19, r25

    ; Spill X_SQUARED (r18:r19) -> 0x01AA
    sts 0x01AA, r18      ; Store low byte
    sts 0x01AB, r19  ; Store high byte

    ; TAC linha 11: TERM3 = t48
    mov r20, r18   ; TERM3 = t48
    mov r21, r19

    ; Spill t46 (r20:r21) -> 0x01AC
    sts 0x01AC, r20      ; Store low byte
    sts 0x01AD, r21  ; Store high byte

    ; Load TERM3 de 0x017E -> r20:r21
    lds r20, 0x017E      ; Load low byte
    lds r21, 0x017F  ; Load high byte

    ; TAC linha 12: t49 = X_POW4 * X_SQUARED
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r18, r22
    mov r19, r23
    mov r20, r22
    mov r21, r23
    rcall mul16              ; R24:R25 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r18, r24
    mov r19, r25
    ldi r20, 100             ; Divide by scale factor
    ldi r21, 0
    rcall div16              ; R24:R25 = result (scaled¹)
    mov r16, r24
    mov r17, r25

    ; Spill X_POW4 (r22:r23) -> 0x01AE
    sts 0x01AE, r22      ; Store low byte
    sts 0x01AF, r23  ; Store high byte

    ; Load X_SQUARED de 0x01AA -> r22:r23
    lds r22, 0x01AA      ; Load low byte
    lds r23, 0x01AB  ; Load high byte

    ; Spill t47 (r16:r17) -> 0x01B0
    sts 0x01B0, r16      ; Store low byte
    sts 0x01B1, r17  ; Store high byte

    ; TAC linha 12: X_POW6 = t49
    mov r18, r16   ; X_POW6 = t49
    mov r19, r17

    ; Spill t48 (r18:r19) -> 0x01B2
    sts 0x01B2, r18      ; Store low byte
    sts 0x01B3, r19  ; Store high byte

    ; TAC linha 13: t50 = 720000
    ldi r20, 128   ; Constante 720000 (low byte)
    ldi r21, 252  ; Constante 720000 (high byte)

    ; Spill TERM3 (r20:r21) -> 0x01B4
    sts 0x01B4, r20      ; Store low byte
    sts 0x01B5, r21  ; Store high byte

    ; TAC linha 13: t51 = X_POW6 | t50
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r18, r18      ; Dividendo
    mov r19, r19
    ldi r20, 100             ; Scale factor (100)
    ldi r21, 0
    rcall mul16              ; R24:R25 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r18, r24             ; Move result to dividend registers
    mov r19, r25
    mov r20, r20      ; Divisor
    mov r21, r21
    rcall div16              ; R24:R25 = (op1 * 100) / op2
    mov r22, r24      ; Copy result
    mov r23, r25

    ; Spill X_SQUARED (r22:r23) -> 0x01B6
    sts 0x01B6, r22      ; Store low byte
    sts 0x01B7, r23  ; Store high byte

    ; TAC linha 13: TEMP2 = t51
    mov r16, r22   ; TEMP2 = t51
    mov r17, r23

    ; Spill t49 (r16:r17) -> 0x01B8
    sts 0x01B8, r16      ; Store low byte
    sts 0x01B9, r17  ; Store high byte

    ; Load TEMP2 de 0x011C -> r16:r17
    lds r16, 0x011C      ; Load low byte
    lds r17, 0x011D  ; Load high byte

    ; TAC linha 14: t52 = 0
    ldi r18, 0   ; Constante 0 (low byte)
    ldi r19, 0  ; Constante 0 (high byte)

    ; Spill X_POW6 (r18:r19) -> 0x01BA
    sts 0x01BA, r18      ; Store low byte
    sts 0x01BB, r19  ; Store high byte

    ; TAC linha 14: t53 = t52 - TEMP2
    ; Subtração 16-bit: t53 = t52 - TEMP2
    sub r18, r16   ; Low byte com borrow
    sbc r19, r17 ; High byte com borrow
    mov r20, r18   ; Resultado em t53
    mov r21, r19

    ; Spill t50 (r20:r21) -> 0x01BC
    sts 0x01BC, r20      ; Store low byte
    sts 0x01BD, r21  ; Store high byte

    ; TAC linha 14: TERM4 = t53
    mov r22, r20   ; TERM4 = t53
    mov r23, r21

    ; Spill t51 (r22:r23) -> 0x01BE
    sts 0x01BE, r22      ; Store low byte
    sts 0x01BF, r23  ; Store high byte

    ; Load TERM4 de 0x0184 -> r22:r23
    lds r22, 0x0184      ; Load low byte
    lds r23, 0x0185  ; Load high byte

    ; TAC linha 15: t54 = TERM1 + TERM2
    ; Soma 16-bit: t54 = TERM1 + TERM2
    add r16, r18   ; Low byte com carry
    adc r17, r19 ; High byte com carry
    mov r20, r16   ; Resultado em t54
    mov r21, r17

    ; Spill TEMP2 (r16:r17) -> 0x01C0
    sts 0x01C0, r16      ; Store low byte
    sts 0x01C1, r17  ; Store high byte

    ; Load TERM1 de 0x019C -> r16:r17
    lds r16, 0x019C      ; Load low byte
    lds r17, 0x019D  ; Load high byte

    ; Spill t52 (r18:r19) -> 0x01C2
    sts 0x01C2, r18      ; Store low byte
    sts 0x01C3, r19  ; Store high byte

    ; Load TERM2 de 0x01A8 -> r18:r19
    lds r18, 0x01A8      ; Load low byte
    lds r19, 0x01A9  ; Load high byte

    ; Spill t53 (r20:r21) -> 0x01C4
    sts 0x01C4, r20      ; Store low byte
    sts 0x01C5, r21  ; Store high byte

    ; TAC linha 15: PARTIAL1 = t54
    mov r22, r20   ; PARTIAL1 = t54
    mov r23, r21

    ; Spill TERM4 (r22:r23) -> 0x01C6
    sts 0x01C6, r22      ; Store low byte
    sts 0x01C7, r23  ; Store high byte

    ; TAC linha 16: t55 = PARTIAL1 + TERM3
    ; Soma 16-bit: t55 = PARTIAL1 + TERM3
    add r22, r16   ; Low byte com carry
    adc r23, r17 ; High byte com carry
    mov r18, r22   ; Resultado em t55
    mov r19, r23

    ; Spill TERM1 (r16:r17) -> 0x01C8
    sts 0x01C8, r16      ; Store low byte
    sts 0x01C9, r17  ; Store high byte

    ; Load TERM3 de 0x01B4 -> r16:r17
    lds r16, 0x01B4      ; Load low byte
    lds r17, 0x01B5  ; Load high byte

    ; Spill TERM2 (r18:r19) -> 0x01CA
    sts 0x01CA, r18      ; Store low byte
    sts 0x01CB, r19  ; Store high byte

    ; TAC linha 16: PARTIAL2 = t55
    mov r20, r18   ; PARTIAL2 = t55
    mov r21, r19

    ; Spill t54 (r20:r21) -> 0x01CC
    sts 0x01CC, r20      ; Store low byte
    sts 0x01CD, r21  ; Store high byte

    ; TAC linha 17: t56 = PARTIAL2 + TERM4
    ; Soma 16-bit: t56 = PARTIAL2 + TERM4
    add r20, r22   ; Low byte com carry
    adc r21, r23 ; High byte com carry
    mov r16, r20   ; Resultado em t56
    mov r17, r21

    ; Spill PARTIAL1 (r22:r23) -> 0x01CE
    sts 0x01CE, r22      ; Store low byte
    sts 0x01CF, r23  ; Store high byte

    ; Load TERM4 de 0x01C6 -> r22:r23
    lds r22, 0x01C6      ; Load low byte
    lds r23, 0x01C7  ; Load high byte

    ; Spill TERM3 (r16:r17) -> 0x01D0
    sts 0x01D0, r16      ; Store low byte
    sts 0x01D1, r17  ; Store high byte

    ; TAC linha 17: RESULT_COS = t56
    mov r18, r16   ; RESULT_COS = t56
    mov r19, r17

    ; Spill t55 (r18:r19) -> 0x01D2
    sts 0x01D2, r18      ; Store low byte
    sts 0x01D3, r19  ; Store high byte

    ; Load RESULT_COS de 0x0188 -> r18:r19
    lds r18, 0x0188      ; Load low byte
    lds r19, 0x0189  ; Load high byte

    ; TAC linha 18: FINAL_COS = RESULT_COS
    mov r20, r18   ; FINAL_COS = RESULT_COS
    mov r21, r19

    ; ==== FIM DO CÓDIGO GERADO ====

    ; Enviar resultado final via UART
    mov r24, r20    ; Copiar resultado para R24:R25
    mov r25, r21
    rcall send_number_16bit
    ldi r24, 13            ; CR
    rcall uart_transmit
    ldi r24, 10            ; LF
    rcall uart_transmit
    jmp fim                ; Saltar para loop infinito

; ====================================================================
; mul16: Multiplicação 16-bit × 16-bit = 16-bit (unsigned)
; Entrada: R18:R19 (op1), R20:R21 (op2)
; Saída: R24:R25 (resultado)
; Usa: R0, R1, R22, R23
; ====================================================================
mul16:
    ; Salvar registradores que serão modificados
    push r22
    push r23

    ; Zerar acumulador resultado
    clr r24
    clr r25

    ; Produto parcial 1: AL × BL (contribui totalmente)
    mul r18, r20      ; R1:R0 = AL × BL
    mov r24, r0       ; Byte baixo do resultado
    mov r22, r1       ; Byte alto vai para temporário

    ; Produto parcial 2: AL × BH (contribui byte baixo para byte alto do resultado)
    mul r18, r21      ; R1:R0 = AL × BH
    add r22, r0       ; Somar byte baixo ao acumulador
    adc r25, r1       ; Somar byte alto com carry

    ; Produto parcial 3: AH × BL (contribui byte baixo para byte alto do resultado)
    mul r19, r20      ; R1:R0 = AH × BL
    add r22, r0       ; Somar byte baixo ao acumulador
    adc r25, r1       ; Somar byte alto com carry

    ; Produto parcial 4: AH × BH (descartado - overflow além de 16 bits)
    ; Não precisamos calcular pois descartamos resultado > 16 bits

    ; Mover acumulador para resultado final
    mov r25, r22      ; Byte alto do resultado

    ; Restaurar registradores
    pop r23
    pop r22

    ; Limpar R0 e R1 (boa prática após MUL)
    clr r1

    ret

; ====================================================================
; div16: Divisão 16-bit ÷ 16-bit = quociente e resto (unsigned)
; Algoritmo: Restoring shift-subtract (17 iterações, resto corrigido)
; Entrada: R18:R19 (dividendo), R20:R21 (divisor)
; Saída: R24:R25 (quociente), R22:R23 (resto)
; Usa: R16 (contador de loop)
; Ciclos: ~232
; ====================================================================
div16:
    push r16              ; Salvar registrador usado

    ; Verificar divisão por zero
    cp      r20, r1       ; Comparar divisor low com 0
    cpc     r21, r1       ; Comparar divisor high com 0
    breq    div16_by_zero ; Se zero, pular para tratamento de erro

    ; Inicializar resto = 0
    clr     r22           ; Resto low = 0
    clr     r23           ; Resto high = 0

    ; Inicializar contador de loop (16 iterações para divisão 16-bit)
    ldi     r16, 16

div16_loop:
    ; Deslocar dividendo/quociente para esquerda
    lsl     r18           ; Logical shift left (LSB=0, no carry dependency)
    rol     r19           ; Shift dividend/quotient high

    ; Deslocar bit MSB do dividendo para o resto
    rol     r22           ; Shift into remainder low
    rol     r23           ; Shift into remainder high

    ; Comparar resto com divisor
    cp      r22, r20      ; Compare remainder with divisor (low)
    cpc     r23, r21      ; Compare remainder with divisor (high)
    brcs    div16_skip    ; If remainder < divisor, skip subtraction

    ; Resto >= divisor: subtrair divisor do resto
    sub     r22, r20      ; Subtract divisor from remainder (low)
    sbc     r23, r21      ; Subtract divisor from remainder (high)
    inc     r18           ; Set quotient LSB bit to 1

div16_skip:
    dec     r16           ; Decrementar contador
    brne    div16_loop    ; Loop se não terminou

    ; Mover quociente para registradores de saída
    mov     r24, r18      ; Quotient to output (low)
    mov     r25, r19      ; Quotient to output (high)

    ; Resto já está em R22:R23 (correto)

    pop r16
    ret

div16_by_zero:
    ; Retornar valores de erro
    ldi     r24, 0xFF     ; Quociente = 0xFFFF (indicador de erro)
    ldi     r25, 0xFF
    mov     r22, r18      ; Resto = dividendo original (low)
    mov     r23, r19      ; Resto = dividendo original (high)
    pop r16
    ret

; ====================================================================
; ROTINAS UART (115200 baud @ 16MHz)
; ====================================================================

uart_init:
    ldi r16, 0
    sts 0xC5, r16        ; UBRR0H = 0
    ldi r16, 8
    sts 0xC4, r16        ; UBRR0L = 8 (115200 baud @ 16MHz)
    ldi r16, (1 << 3)    ; TXEN0
    sts 0xC1, r16        ; UCSR0B
    ldi r16, (1 << 2) | (1 << 1)
    sts 0xC2, r16        ; UCSR0C (8N1)
    ret

uart_transmit:
    push r25
uart_wait:
    lds r25, 0xC0        ; UCSR0A
    sbrs r25, 5          ; Wait for UDRE0
    rjmp uart_wait
    sts 0xC6, r24        ; UDR0 = data
    pop r25
    ret

; ====================================================================
; send_number_16bit: Envia número 16-bit como decimal via UART
; Entrada: R24:R25 (número 16-bit, 0-65535)
; Saída: Nenhuma (envia via UART)
; ====================================================================
send_number_16bit:
    push r20
    push r21
    push r22
    push r23
    push r16
    push r17
    push r18
    push r19

    mov r20, r24
    mov r21, r25

    ; Dezenas de milhares (10000)
    ldi r16, lo8(10000)
    ldi r17, hi8(10000)
    clr r18

div_10000:
    cp r20, r16
    cpc r21, r17
    brlo div_1000
    sub r20, r16
    sbc r21, r17
    inc r18
    rjmp div_10000

div_1000:
    ; Imprimir dezena de milhares se != 0
    cpi r18, 0
    breq skip_10000
    mov r24, r18
    subi r24, -48
    rcall uart_transmit
skip_10000:

    ; Milhares (1000)
    ldi r16, lo8(1000)
    ldi r17, hi8(1000)
    clr r18

div_1000_loop:
    cp r20, r16
    cpc r21, r17
    brlo div_100
    sub r20, r16
    sbc r21, r17
    inc r18
    rjmp div_1000_loop

div_100:
    ; Imprimir milhares
    mov r24, r18
    subi r24, -48
    rcall uart_transmit

    ; Centenas (100)
    ldi r16, 100
    clr r17
    clr r18

div_100_loop:
    cp r20, r16
    cpc r21, r17
    brlo div_10
    sub r20, r16
    sbc r21, r17
    inc r18
    rjmp div_100_loop

div_10:
    ; Imprimir centenas
    mov r24, r18
    subi r24, -48
    rcall uart_transmit

    ; Dezenas (10)
    ldi r16, 10
    clr r17
    clr r18

div_10_loop:
    cp r20, r16
    cpc r21, r17
    brlo print_units
    sub r20, r16
    sbc r21, r17
    inc r18
    rjmp div_10_loop

print_units:
    ; Imprimir dezenas
    mov r24, r18
    subi r24, -48
    rcall uart_transmit

    ; Imprimir unidades
    mov r24, r20
    subi r24, -48
    rcall uart_transmit

    pop r19
    pop r18
    pop r17
    pop r16
    pop r23
    pop r22
    pop r21
    pop r20
    ret

fim:
    rjmp fim   ; Loop infinito

; ====================================================================
; Fim do programa
; ====================================================================
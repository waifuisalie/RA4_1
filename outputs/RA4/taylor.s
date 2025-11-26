; ====================================================================
; Código Assembly gerado automaticamente
; Arquitetura: AVR ATmega328P (Arduino Uno)
; Compilador: RA4_Compiladores - Fase 4
; ====================================================================

.section .text
.global main

main:
    ; Inicializar stack pointer
    ldi r16, 0xFF   ; RAMEND low byte
    out 0x3D, r16          ; SPL
    ldi r16, 0x08   ; RAMEND high byte
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

    ; Liberando registradores de variáveis mortas: t0

    ; TAC linha 2: t1 = 100
    ldi r20, 100   ; Constante 100 (low byte)
    ldi r21, 0  ; Constante 100 (high byte)

    ; TAC linha 2: TERM1 = t1
    mov r22, r20   ; TERM1 = t1
    mov r23, r21

    ; Liberando registradores de variáveis mortas: t1

    ; TAC linha 3: t2 = 1
    ldi r24, 1   ; Constante 1 (low byte)
    ldi r25, 0  ; Constante 1 (high byte)

    ; TAC linha 3: COUNTER = t2
    mov r26, r24   ; COUNTER = t2
    mov r27, r25

    ; Liberando registradores de variáveis mortas: t2

L0:

    ; TAC linha 4: t3 = 1
    ldi r28, 1   ; Constante 1 (low byte)
    ldi r29, 0  ; Constante 1 (high byte)

    ; TAC linha 4: t4 = COUNTER <= t3
    ; Comparação 16-bit menor ou igual (unsigned)
    ; Implementado como: B >= A (operandos trocados)
    cp r28, r26      ; Compare B with A (reversed)
    cpc r29, r27
    ldi r30, 0               ; Assume false
    ldi r31, 0
    brlo skip_le_4               ; If B < A, skip
    ldi r30, 1               ; Set true (B >= A, i.e., A <= B)
skip_le_4:

    ; Liberando registradores de variáveis mortas: t3

    ; TAC linha 4: ifFalse t4 goto L1
    ; Check if t4 == 0 (false)
    ldi r18, 0                  ; Zero constant for comparison
    mov r2, r18
    mov r3, r18
    cp r30, r2         ; Compare low byte with 0
    cpc r31, r3       ; Compare high byte with carry
    brne .+2              ; If not equal (true), skip jmp
    jmp L1                ; If equal (false), jump to L1

    ; Liberando registradores de variáveis mortas: t4

    ; TAC linha 4: t5 = X_VAL * X_VAL
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r18
    mov r1, r19
    mov r2, r18
    mov r3, r19
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r16, r4
    mov r17, r5

    ; Liberando registradores de variáveis mortas: X_VAL

    ; TAC linha 4: X_SQUARE = t5
    mov r20, r16   ; X_SQUARE = t5
    mov r21, r17

    ; Liberando registradores de variáveis mortas: t5

    ; TAC linha 4: t6 = 200
    ldi r24, 200   ; Constante 200 (low byte)
    ldi r25, 0  ; Constante 200 (high byte)

    ; TAC linha 4: FACT_2 = t6
    mov r28, r24   ; FACT_2 = t6
    mov r29, r25

    ; Liberando registradores de variáveis mortas: t6

    ; TAC linha 4: t7 = X_SQUARE | FACT_2
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r0, r20      ; Dividendo
    mov r1, r21
    ldi r16, 100             ; Scale factor (100)
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall mul16              ; R4:R5 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r0, r4             ; Move result to dividend registers
    mov r1, r5
    mov r2, r28      ; Divisor
    mov r3, r29
    rcall div16              ; R4:R5 = (op1 * 100) / op2
    mov r30, r4      ; Copy result
    mov r31, r5

    ; Liberando registradores de variáveis mortas: FACT_2

    ; TAC linha 4: TEMP2 = t7
    mov r18, r30   ; TEMP2 = t7
    mov r19, r31

    ; Liberando registradores de variáveis mortas: t7

    ; TAC linha 4: t8 = 0
    ldi r16, 0   ; Constante 0 (low byte)
    ldi r17, 0  ; Constante 0 (high byte)

    ; TAC linha 4: t9 = t8 - TEMP2
    ; Subtração 16-bit: t9 = t8 - TEMP2
    sub r16, r18   ; Low byte com borrow
    sbc r17, r19 ; High byte com borrow
    mov r24, r16   ; Resultado em t9
    mov r25, r17

    ; Liberando registradores de variáveis mortas: TEMP2, t8

    ; TAC linha 4: TERM2 = t9
    mov r28, r24   ; TERM2 = t9
    mov r29, r25

    ; Liberando registradores de variáveis mortas: t9

    ; TAC linha 4: t10 = X_SQUARE * X_SQUARE
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r20
    mov r1, r21
    mov r2, r20
    mov r3, r21
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r30, r4
    mov r31, r5

    ; TAC linha 4: X_FOURTH = t10
    mov r18, r30   ; X_FOURTH = t10
    mov r19, r31

    ; Liberando registradores de variáveis mortas: t10

    ; TAC linha 4: t11 = 400
    ldi r16, 144   ; Constante 400 (low byte)
    ldi r17, 1  ; Constante 400 (high byte)

    ; TAC linha 4: t12 = 300
    ldi r24, 44   ; Constante 300 (low byte)
    ldi r25, 1  ; Constante 300 (high byte)

    ; TAC linha 4: t13 = t11 * t12
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r16
    mov r1, r17
    mov r2, r24
    mov r3, r25
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r30, r4
    mov r31, r5

    ; Liberando registradores de variáveis mortas: t11, t12

    ; TAC linha 4: TEMP4A = t13
    mov r16, r30   ; TEMP4A = t13
    mov r17, r31

    ; Liberando registradores de variáveis mortas: t13

    ; TAC linha 4: t14 = 200
    ldi r24, 200   ; Constante 200 (low byte)
    ldi r25, 0  ; Constante 200 (high byte)

    ; TAC linha 4: t15 = TEMP4A * t14
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r16
    mov r1, r17
    mov r2, r24
    mov r3, r25
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r30, r4
    mov r31, r5

    ; Liberando registradores de variáveis mortas: TEMP4A, t14

    ; TAC linha 4: TEMP4B = t15
    mov r16, r30   ; TEMP4B = t15
    mov r17, r31

    ; Liberando registradores de variáveis mortas: t15

    ; TAC linha 4: t16 = 100
    ldi r24, 100   ; Constante 100 (low byte)
    ldi r25, 0  ; Constante 100 (high byte)

    ; TAC linha 4: t17 = TEMP4B * t16
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r16
    mov r1, r17
    mov r2, r24
    mov r3, r25
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r30, r4
    mov r31, r5

    ; Liberando registradores de variáveis mortas: TEMP4B, t16

    ; TAC linha 4: FACT_4 = t17
    mov r16, r30   ; FACT_4 = t17
    mov r17, r31

    ; Liberando registradores de variáveis mortas: t17

    ; TAC linha 4: t18 = X_FOURTH | FACT_4
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r0, r18      ; Dividendo
    mov r1, r19
    ldi r16, 100             ; Scale factor (100)
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall mul16              ; R4:R5 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r0, r4             ; Move result to dividend registers
    mov r1, r5
    mov r2, r16      ; Divisor
    mov r3, r17
    rcall div16              ; R4:R5 = (op1 * 100) / op2
    mov r24, r4      ; Copy result
    mov r25, r5

    ; Liberando registradores de variáveis mortas: FACT_4

    ; TAC linha 4: TERM3 = t18
    mov r30, r24   ; TERM3 = t18
    mov r31, r25

    ; Liberando registradores de variáveis mortas: t18

    ; TAC linha 4: t19 = X_FOURTH * X_SQUARE
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r18
    mov r1, r19
    mov r2, r20
    mov r3, r21
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r16, r4
    mov r17, r5

    ; Liberando registradores de variáveis mortas: X_SQUARE, X_FOURTH

    ; TAC linha 4: X_SIXTH = t19
    mov r24, r16   ; X_SIXTH = t19
    mov r25, r17

    ; Liberando registradores de variáveis mortas: t19

    ; TAC linha 4: t20 = 600
    ldi r20, 88   ; Constante 600 (low byte)
    ldi r21, 2  ; Constante 600 (high byte)

    ; TAC linha 4: t21 = 500
    ldi r18, 244   ; Constante 500 (low byte)
    ldi r19, 1  ; Constante 500 (high byte)

    ; TAC linha 4: t22 = t20 * t21
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r20
    mov r1, r21
    mov r2, r18
    mov r3, r19
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r16, r4
    mov r17, r5

    ; Liberando registradores de variáveis mortas: t20, t21

    ; TAC linha 4: TEMP6A = t22
    mov r20, r16   ; TEMP6A = t22
    mov r21, r17

    ; Liberando registradores de variáveis mortas: t22

    ; TAC linha 4: t23 = 400
    ldi r18, 144   ; Constante 400 (low byte)
    ldi r19, 1  ; Constante 400 (high byte)

    ; TAC linha 4: t24 = TEMP6A * t23
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r20
    mov r1, r21
    mov r2, r18
    mov r3, r19
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r16, r4
    mov r17, r5

    ; Liberando registradores de variáveis mortas: TEMP6A, t23

    ; TAC linha 4: TEMP6B = t24
    mov r20, r16   ; TEMP6B = t24
    mov r21, r17

    ; Liberando registradores de variáveis mortas: t24

    ; TAC linha 4: t25 = 300
    ldi r18, 44   ; Constante 300 (low byte)
    ldi r19, 1  ; Constante 300 (high byte)

    ; TAC linha 4: t26 = TEMP6B * t25
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r20
    mov r1, r21
    mov r2, r18
    mov r3, r19
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r16, r4
    mov r17, r5

    ; Liberando registradores de variáveis mortas: TEMP6B, t25

    ; TAC linha 4: TEMP6C = t26
    mov r20, r16   ; TEMP6C = t26
    mov r21, r17

    ; Liberando registradores de variáveis mortas: t26

    ; TAC linha 4: t27 = 200
    ldi r18, 200   ; Constante 200 (low byte)
    ldi r19, 0  ; Constante 200 (high byte)

    ; TAC linha 4: t28 = TEMP6C * t27
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r20
    mov r1, r21
    mov r2, r18
    mov r3, r19
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r16, r4
    mov r17, r5

    ; Liberando registradores de variáveis mortas: TEMP6C, t27

    ; TAC linha 4: TEMP6D = t28
    mov r20, r16   ; TEMP6D = t28
    mov r21, r17

    ; Liberando registradores de variáveis mortas: t28

    ; TAC linha 4: t29 = 100
    ldi r18, 100   ; Constante 100 (low byte)
    ldi r19, 0  ; Constante 100 (high byte)

    ; TAC linha 4: t30 = TEMP6D * t29
    ; Multiplicação 16-bit com re-normalização de escala
    ; Preparar parâmetros para mul16
    mov r0, r20
    mov r1, r21
    mov r2, r18
    mov r3, r19
    rcall mul16              ; R4:R5 = op1 * op2 (scaled²)
    ; Re-normalize: divide by 100 to restore 100x scaling
    mov r0, r4
    mov r1, r5
    ldi r16, 100             ; Divide by scale factor
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall div16              ; R4:R5 = result (scaled¹)
    mov r16, r4
    mov r17, r5

    ; Liberando registradores de variáveis mortas: TEMP6D, t29

    ; TAC linha 4: FACT_6 = t30
    mov r20, r16   ; FACT_6 = t30
    mov r21, r17

    ; Liberando registradores de variáveis mortas: t30

    ; TAC linha 4: t31 = X_SIXTH | FACT_6
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r0, r24      ; Dividendo
    mov r1, r25
    ldi r16, 100             ; Scale factor (100)
    mov r2, r16
    ldi r16, 0
    mov r3, r16
    rcall mul16              ; R4:R5 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r0, r4             ; Move result to dividend registers
    mov r1, r5
    mov r2, r20      ; Divisor
    mov r3, r21
    rcall div16              ; R4:R5 = (op1 * 100) / op2
    mov r18, r4      ; Copy result
    mov r19, r5

    ; Liberando registradores de variáveis mortas: X_SIXTH, FACT_6

    ; TAC linha 4: TEMP8 = t31
    mov r16, r18   ; TEMP8 = t31
    mov r17, r19

    ; Liberando registradores de variáveis mortas: t31

    ; TAC linha 4: t32 = 0
    ldi r24, 0   ; Constante 0 (low byte)
    ldi r25, 0  ; Constante 0 (high byte)

    ; TAC linha 4: t33 = t32 - TEMP8
    ; Subtração 16-bit: t33 = t32 - TEMP8
    sub r24, r16   ; Low byte com borrow
    sbc r25, r17 ; High byte com borrow
    mov r20, r24   ; Resultado em t33
    mov r21, r25

    ; Liberando registradores de variáveis mortas: TEMP8, t32

    ; TAC linha 4: TERM4 = t33
    mov r18, r20   ; TERM4 = t33
    mov r19, r21

    ; Liberando registradores de variáveis mortas: t33

    ; TAC linha 4: t34 = TERM1 + TERM2
    ; Soma 16-bit: t34 = TERM1 + TERM2
    add r22, r28   ; Low byte com carry
    adc r23, r29 ; High byte com carry
    mov r16, r22   ; Resultado em t34
    mov r17, r23

    ; Liberando registradores de variáveis mortas: TERM1, TERM2

    ; TAC linha 4: SUM12 = t34
    mov r24, r16   ; SUM12 = t34
    mov r25, r17

    ; Liberando registradores de variáveis mortas: t34

    ; TAC linha 4: t35 = SUM12 + TERM3
    ; Soma 16-bit: t35 = SUM12 + TERM3
    add r24, r30   ; Low byte com carry
    adc r25, r31 ; High byte com carry
    mov r20, r24   ; Resultado em t35
    mov r21, r25

    ; Liberando registradores de variáveis mortas: TERM3, SUM12

    ; TAC linha 4: SUM123 = t35
    mov r22, r20   ; SUM123 = t35
    mov r23, r21

    ; Liberando registradores de variáveis mortas: t35

    ; TAC linha 4: t36 = SUM123 + TERM4
    ; Soma 16-bit: t36 = SUM123 + TERM4
    add r22, r18   ; Low byte com carry
    adc r23, r19 ; High byte com carry
    mov r28, r22   ; Resultado em t36
    mov r29, r23

    ; Liberando registradores de variáveis mortas: TERM4, SUM123

    ; TAC linha 4: RESULT_COS = t36
    mov r16, r28   ; RESULT_COS = t36
    mov r17, r29

    ; Liberando registradores de variáveis mortas: t36

    ; TAC linha 4: t37 = 1
    ldi r30, 1   ; Constante 1 (low byte)
    ldi r31, 0  ; Constante 1 (high byte)

    ; TAC linha 4: t38 = COUNTER + t37
    ; Soma 16-bit: t38 = COUNTER + t37
    add r26, r30   ; Low byte com carry
    adc r27, r31 ; High byte com carry
    mov r24, r26   ; Resultado em t38
    mov r25, r27

    ; Liberando registradores de variáveis mortas: t37

    ; TAC linha 4: COUNTER = t38
    mov r26, r24   ; COUNTER = t38
    mov r27, r25

    ; Liberando registradores de variáveis mortas: COUNTER, t38

    ; TAC linha 4: goto L0
    rjmp L0   ; Salto relativo para L0

L1:

    ; TAC linha 5: FINAL_COS = RESULT_COS
    mov r20, r16   ; FINAL_COS = RESULT_COS
    mov r21, r17

    ; ==== FIM DO CÓDIGO GERADO ====

    ; Enviar resultado final via UART
    mov r4, r20    ; Copiar resultado para R4:R5
    mov r5, r21
    rcall send_number_16bit
    ldi r16, 13            ; CR
    mov r0, r16
    rcall uart_transmit
    ldi r16, 10            ; LF
    mov r0, r16
    rcall uart_transmit
    jmp fim                ; Saltar para loop infinito

; ====================================================================
; mul16: Multiplicação 16-bit × 16-bit = 16-bit (unsigned)
; Entrada: R0:R1 (op1), R2:R3 (op2)
; Saída: R4:R5 (resultado)
; Usa: R6, R7, R8, R9
; ====================================================================
mul16:
    ; Salvar registradores que serão modificados
    push r8
    push r9

    ; Zerar acumulador resultado
    clr r4
    clr r5

    ; Produto parcial 1: AL × BL (contribui totalmente)
    mul r0, r2      ; R1:R0 = AL × BL
    mov r4, r0       ; Byte baixo do resultado
    mov r6, r1       ; Byte alto vai para temporário

    ; Produto parcial 2: AL × BH (contribui byte baixo para byte alto do resultado)
    mul r0, r3      ; R1:R0 = AL × BH
    add r6, r0       ; Somar byte baixo ao acumulador
    adc r5, r1       ; Somar byte alto com carry

    ; Produto parcial 3: AH × BL (contribui byte baixo para byte alto do resultado)
    mul r1, r2      ; R1:R0 = AH × BL
    add r6, r0       ; Somar byte baixo ao acumulador
    adc r5, r1       ; Somar byte alto com carry

    ; Produto parcial 4: AH × BH (descartado - overflow além de 16 bits)
    ; Não precisamos calcular pois descartamos resultado > 16 bits

    ; Mover acumulador para resultado final
    mov r5, r6      ; Byte alto do resultado

    ; Restaurar registradores
    pop r9
    pop r8

    ; Limpar R0 e R1 (boa prática após MUL)
    clr r1

    ret

; ====================================================================
; div16: Divisão 16-bit ÷ 16-bit = quociente e resto (unsigned)
; Algoritmo: Restoring shift-subtract (17 iterações, resto corrigido)
; Entrada: R0:R1 (dividendo), R2:R3 (divisor)
; Saída: R4:R5 (quociente), R6:R7 (resto)
; Usa: R8 (contador de loop)
; Ciclos: ~232
; ====================================================================
div16:
    push r8              ; Salvar registrador usado

    ; Verificar divisão por zero
    cp      r2, r1       ; Comparar divisor low com 0
    cpc     r3, r1       ; Comparar divisor high com 0
    breq    div16_by_zero ; Se zero, pular para tratamento de erro

    ; Inicializar resto = 0
    clr     r6           ; Resto low = 0
    clr     r7           ; Resto high = 0

    ; Inicializar contador de loop (16 iterações para divisão 16-bit)
    ldi     r16, 16
    mov     r8, r16

div16_loop:
    ; Deslocar dividendo/quociente para esquerda
    lsl     r0           ; Logical shift left (LSB=0, no carry dependency)
    rol     r1           ; Shift dividend/quotient high

    ; Deslocar bit MSB do dividendo para o resto
    rol     r6           ; Shift into remainder low
    rol     r7           ; Shift into remainder high

    ; Comparar resto com divisor
    cp      r6, r2      ; Compare remainder with divisor (low)
    cpc     r7, r3      ; Compare remainder with divisor (high)
    brcs    div16_skip    ; If remainder < divisor, skip subtraction

    ; Resto >= divisor: subtrair divisor do resto
    sub     r6, r2      ; Subtract divisor from remainder (low)
    sbc     r7, r3      ; Subtract divisor from remainder (high)
    inc     r0           ; Set quotient LSB bit to 1

div16_skip:
    dec     r8           ; Decrementar contador
    brne    div16_loop    ; Loop se não terminou

    ; Mover quociente para registradores de saída
    mov     r4, r0      ; Quotient to output (low)
    mov     r5, r1      ; Quotient to output (high)

    ; Resto já está em R6:R7 (correto)

    pop r8
    ret

div16_by_zero:
    ; Retornar valores de erro
    ldi     r16, 0xFF     ; Quociente = 0xFFFF (indicador de erro)
    mov     r4, r16
    mov     r5, r16
    mov     r6, r0      ; Resto = dividendo original (low)
    mov     r7, r1      ; Resto = dividendo original (high)
    pop r8
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
    push r1
uart_wait:
    lds r1, 0xC0        ; UCSR0A
    sbrs r1, 5          ; Wait for UDRE0
    rjmp uart_wait
    sts 0xC6, r0        ; UDR0 = data
    pop r1
    ret

; ====================================================================
; send_number_16bit: Envia número 16-bit como decimal via UART
; Entrada: R4:R5 (número 16-bit, 0-65535)
; Saída: Nenhuma (envia via UART)
; ====================================================================
send_number_16bit:
    push r6
    push r7
    push r8
    push r9
    push r10
    push r11
    push r12
    push r13
    push r16

    mov r6, r4
    mov r7, r5

    ; Dezenas de milhares (10000)
    ldi r16, 16
    mov r8, r16
    ldi r16, 39
    mov r9, r16
    clr r10

div_10000:
    cp r6, r8
    cpc r7, r9
    brlo div_1000
    sub r6, r8
    sbc r7, r9
    inc r10
    rjmp div_10000

div_1000:
    ; Imprimir dezena de milhares se != 0
    ldi r16, 0
    cp r10, r16
    breq skip_10000
    mov r0, r10
    ldi r16, 48
    add r0, r16
    rcall uart_transmit
skip_10000:

    ; Milhares (1000)
    ldi r16, 232
    mov r8, r16
    ldi r16, 3
    mov r9, r16
    clr r10

div_1000_loop:
    cp r6, r8
    cpc r7, r9
    brlo div_100
    sub r6, r8
    sbc r7, r9
    inc r10
    rjmp div_1000_loop

div_100:
    ; Imprimir milhares
    mov r0, r10
    ldi r16, 48
    add r0, r16
    rcall uart_transmit

    ; Centenas (100)
    ldi r16, 100
    mov r8, r16
    clr r9
    clr r10

div_100_loop:
    cp r6, r8
    cpc r7, r9
    brlo div_10
    sub r6, r8
    sbc r7, r9
    inc r10
    rjmp div_100_loop

div_10:
    ; Imprimir centenas
    mov r0, r10
    ldi r16, 48
    add r0, r16
    rcall uart_transmit

    ; Dezenas (10)
    ldi r16, 10
    mov r8, r16
    clr r9
    clr r10

div_10_loop:
    cp r6, r8
    cpc r7, r9
    brlo print_units
    sub r6, r8
    sbc r7, r9
    inc r10
    rjmp div_10_loop

print_units:
    ; Imprimir dezenas
    mov r0, r10
    ldi r16, 48
    add r0, r16
    rcall uart_transmit

    ; Imprimir unidades
    mov r0, r6
    ldi r16, 48
    add r0, r16
    rcall uart_transmit

    pop r13
    pop r12
    pop r11
    pop r10
    pop r9
    pop r8
    pop r7
    pop r6
    pop r16
    ret

fim:
    rjmp fim   ; Loop infinito

; ====================================================================
; Fim do programa
; ====================================================================
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

    ; TAC linha 1: t0 = 1
    ldi r16, 1   ; Constante 1 (low byte)
    ldi r17, 0  ; Constante 1 (high byte)

    ; TAC linha 1: COUNTER = t0
    mov r18, r16   ; COUNTER = t0
    mov r19, r17

    ; Liberando registradores de variáveis mortas: t0

    ; TAC linha 2: t1 = 1
    ldi r20, 1   ; Constante 1 (low byte)
    ldi r21, 0  ; Constante 1 (high byte)

    ; TAC linha 2: RESULT = t1
    mov r22, r20   ; RESULT = t1
    mov r23, r21

    ; Liberando registradores de variáveis mortas: t1

    ; TAC linha 3: t2 = 8
    ldi r24, 8   ; Constante 8 (low byte)
    ldi r25, 0  ; Constante 8 (high byte)

    ; TAC linha 3: LIMIT = t2
    mov r26, r24   ; LIMIT = t2
    mov r27, r25

    ; Liberando registradores de variáveis mortas: t2

L0:

    ; TAC linha 4: t3 = COUNTER <= LIMIT
    ; Comparação 16-bit menor ou igual (unsigned)
    ; Implementado como: B >= A (operandos trocados)
    cp r26, r18      ; Compare B with A (reversed)
    cpc r27, r19
    ldi r28, 0               ; Assume false
    ldi r29, 0
    brlo skip_le_4               ; If B < A, skip
    ldi r28, 1               ; Set true (B >= A, i.e., A <= B)
skip_le_4:

    ; Liberando registradores de variáveis mortas: LIMIT

    ; TAC linha 4: ifFalse t3 goto L1
    ; Check if t3 == 0 (false)
    ldi r18, 0                  ; Zero constant for comparison
    mov r2, r18
    mov r3, r18
    cp r28, r2         ; Compare low byte with 0
    cpc r29, r3       ; Compare high byte with carry
    brne .+2              ; If not equal (true), skip jmp
    jmp L1                ; If equal (false), jump to L1

    ; Liberando registradores de variáveis mortas: t3

    ; TAC linha 4: t4 = RESULT * COUNTER
    ; Multiplicação 16-bit inteira
    mov r0, r22
    mov r1, r23
    mov r2, r18
    mov r3, r19
    rcall mul16              ; R4:R5 = op1 * op2
    mov r30, r4
    mov r31, r5

    ; TAC linha 4: RESULT = t4
    mov r22, r30   ; RESULT = t4
    mov r23, r31

    ; Liberando registradores de variáveis mortas: t4

    ; TAC linha 4: t5 = 1
    ldi r16, 1   ; Constante 1 (low byte)
    ldi r17, 0  ; Constante 1 (high byte)

    ; TAC linha 4: t6 = COUNTER + t5
    ; Soma 16-bit: t6 = COUNTER + t5
    add r18, r16   ; Low byte com carry
    adc r19, r17 ; High byte com carry
    mov r20, r18   ; Resultado em t6
    mov r21, r19

    ; Liberando registradores de variáveis mortas: t5

    ; TAC linha 4: COUNTER = t6
    mov r18, r20   ; COUNTER = t6
    mov r19, r21

    ; Liberando registradores de variáveis mortas: COUNTER, t6

    ; TAC linha 4: goto L0
    rjmp L0   ; Salto relativo para L0

L1:

    ; TAC linha 5: FINAL_RESULT = RESULT
    mov r24, r22   ; FINAL_RESULT = RESULT
    mov r25, r23

    ; TAC linha 6: FINAL_RESULT = RESULT
    mov r24, r22   ; FINAL_RESULT = RESULT
    mov r25, r23

    ; ==== FIM DO CÓDIGO GERADO ====

    ; Enviar resultado final via UART
    mov r4, r24    ; Copiar resultado para R4:R5
    mov r5, r25
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
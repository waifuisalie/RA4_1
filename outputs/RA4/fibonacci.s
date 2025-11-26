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

    ; TAC linha 1: t0 = 0
    ldi r16, 0   ; Constante 0 (low byte)
    ldi r17, 0  ; Constante 0 (high byte)

    ; TAC linha 1: FIB_0 = t0
    mov r18, r16   ; FIB_0 = t0
    mov r19, r17

    ; Liberando registradores de variáveis mortas: t0

    ; TAC linha 2: t1 = 1
    ldi r20, 1   ; Constante 1 (low byte)
    ldi r21, 0  ; Constante 1 (high byte)

    ; TAC linha 2: FIB_1 = t1
    mov r22, r20   ; FIB_1 = t1
    mov r23, r21

    ; Liberando registradores de variáveis mortas: t1

    ; TAC linha 3: t2 = 2
    ldi r24, 2   ; Constante 2 (low byte)
    ldi r25, 0  ; Constante 2 (high byte)

    ; TAC linha 3: COUNTER = t2
    mov r26, r24   ; COUNTER = t2
    mov r27, r25

    ; Liberando registradores de variáveis mortas: t2

    ; TAC linha 4: t3 = 24
    ldi r28, 24   ; Constante 24 (low byte)
    ldi r29, 0  ; Constante 24 (high byte)

    ; TAC linha 4: LIMIT = t3
    mov r30, r28   ; LIMIT = t3
    mov r31, r29

    ; Liberando registradores de variáveis mortas: t3

L0:

    ; TAC linha 5: t4 = COUNTER <= LIMIT
    ; Comparação 16-bit menor ou igual (unsigned)
    ; Implementado como: B >= A (operandos trocados)
    cp r30, r26      ; Compare B with A (reversed)
    cpc r31, r27
    ldi r16, 0               ; Assume false
    ldi r17, 0
    brlo skip_le_5               ; If B < A, skip
    ldi r16, 1               ; Set true (B >= A, i.e., A <= B)
skip_le_5:

    ; Liberando registradores de variáveis mortas: LIMIT

    ; TAC linha 5: ifFalse t4 goto L1
    ; Check if t4 == 0 (false)
    ldi r16, 0                  ; Zero constant for comparison
    mov r2, r16
    mov r3, r16
    cp r16, r2         ; Compare low byte with 0
    cpc r17, r3       ; Compare high byte with carry
    brne .+2              ; If not equal (true), skip jmp
    jmp L1                ; If equal (false), jump to L1

    ; Liberando registradores de variáveis mortas: t4

    ; TAC linha 5: t5 = FIB_0 + FIB_1
    ; Soma 16-bit: t5 = FIB_0 + FIB_1
    add r18, r22   ; Low byte com carry
    adc r19, r23 ; High byte com carry
    mov r20, r18   ; Resultado em t5
    mov r21, r19

    ; TAC linha 5: FIB_NEXT = t5
    mov r24, r20   ; FIB_NEXT = t5
    mov r25, r21

    ; Liberando registradores de variáveis mortas: t5

    ; TAC linha 5: FIB_0 = FIB_1
    mov r18, r22   ; FIB_0 = FIB_1
    mov r19, r23

    ; Liberando registradores de variáveis mortas: FIB_0

    ; TAC linha 5: FIB_1 = FIB_NEXT
    mov r22, r24   ; FIB_1 = FIB_NEXT
    mov r23, r25

    ; Liberando registradores de variáveis mortas: FIB_1

    ; TAC linha 5: t6 = 1
    ldi r28, 1   ; Constante 1 (low byte)
    ldi r29, 0  ; Constante 1 (high byte)

    ; TAC linha 5: t7 = COUNTER + t6
    ; Soma 16-bit: t7 = COUNTER + t6
    add r26, r28   ; Low byte com carry
    adc r27, r29 ; High byte com carry
    mov r30, r26   ; Resultado em t7
    mov r31, r27

    ; Liberando registradores de variáveis mortas: t6

    ; TAC linha 5: COUNTER = t7
    mov r26, r30   ; COUNTER = t7
    mov r27, r31

    ; Liberando registradores de variáveis mortas: COUNTER, t7

    ; TAC linha 5: goto L0
    rjmp L0   ; Salto relativo para L0

L1:

    ; TAC linha 6: RESULT = FIB_NEXT
    mov r16, r24   ; RESULT = FIB_NEXT
    mov r17, r25

    ; ==== FIM DO CÓDIGO GERADO ====

    ; Enviar resultado final via UART
    mov r4, r16    ; Copiar resultado para R4:R5
    mov r5, r17
    rcall send_number_16bit
    ldi r16, 13            ; CR
    mov r0, r16
    rcall uart_transmit
    ldi r16, 10            ; LF
    mov r0, r16
    rcall uart_transmit
    jmp fim                ; Saltar para loop infinito

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
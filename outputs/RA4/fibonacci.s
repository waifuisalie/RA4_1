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

    ; TAC linha 1: t0 = 0
    ldi r24, 0   ; Constante 0 (low byte)
    ldi r25, 0  ; Constante 0 (high byte)

    ; TAC linha 1: FIB_0 = t0
    mov r6, r24   ; FIB_0 = t0
    mov r7, r25

    ; TAC linha 2: t1 = 1
    ldi r24, 1   ; Constante 1 (low byte)
    ldi r25, 0  ; Constante 1 (high byte)

    ; TAC linha 2: FIB_1 = t1
    mov r8, r24   ; FIB_1 = t1
    mov r9, r25

    ; TAC linha 3: t2 = 2
    ldi r24, 2   ; Constante 2 (low byte)
    ldi r25, 0  ; Constante 2 (high byte)

    ; TAC linha 3: COUNTER = t2
    mov r12, r24   ; COUNTER = t2
    mov r13, r25

    ; TAC linha 4: t3 = 24
    ldi r24, 24   ; Constante 24 (low byte)
    ldi r25, 0  ; Constante 24 (high byte)

    ; TAC linha 4: LIMIT = t3
    mov r16, r24   ; LIMIT = t3
    mov r17, r25

L0:

    ; TAC linha 5: t4 = COUNTER <= LIMIT
    ; Comparação 16-bit menor ou igual (unsigned)
    ; Implementado como: B >= A (operandos trocados)
    cp r16, r12      ; Compare B with A (reversed)
    cpc r17, r13
    ldi r24, 0               ; Assume false
    ldi r25, 0
    brlo skip_le_5               ; If B < A, skip
    ldi r24, 1               ; Set true (B >= A, i.e., A <= B)
skip_le_5:

    ; TAC linha 5: ifFalse t4 goto L1
    ; Check if t4 == 0 (false)
    cp r24, r1          ; Compare low byte with 0 (R1 is always 0)
    cpc r25, r1        ; Compare high byte with 0
    breq L1               ; Branch if equal (condition is false)

    ; TAC linha 5: t5 = FIB_0 + FIB_1
    ; Soma 16-bit: t5 = FIB_0 + FIB_1
    mov r24, r6   ; Copia op1 pro resultado
    mov r25, r7
    add r24, r8   ; Soma op2 (byte baixo)
    adc r25, r9 ; Soma op2 (byte alto com carry)

    ; TAC linha 5: FIB_NEXT = t5
    mov r10, r24   ; FIB_NEXT = t5
    mov r11, r25

    ; TAC linha 5: FIB_0 = FIB_1
    mov r6, r8   ; FIB_0 = FIB_1
    mov r7, r9

    ; TAC linha 5: FIB_1 = FIB_NEXT
    mov r8, r10   ; FIB_1 = FIB_NEXT
    mov r9, r11

    ; TAC linha 5: t7 = COUNTER + 1
    ; Soma 16-bit: t7 = COUNTER + 1 (constante)
    mov r24, r12   ; Copia op1 pro resultado
    mov r25, r13
    ldi r22, 1          ; Carrega constante (byte baixo)
    ldi r23, 0         ; Carrega constante (byte alto)
    add r24, r22          ; Soma constante (byte baixo)
    adc r25, r23         ; Soma constante (byte alto com carry)

    ; TAC linha 5: COUNTER = t7
    mov r12, r24   ; COUNTER = t7
    mov r13, r25

    ; TAC linha 5: goto L0
    rjmp L0   ; Salto relativo para L0

L1:

    ; TAC linha 6: RESULT = FIB_NEXT
    mov r14, r10   ; RESULT = FIB_NEXT
    mov r15, r11

    ; ==== FIM DO CÓDIGO GERADO ====

    ; Enviar resultado final via UART
    mov r24, r14    ; Copiar resultado para R24:R25
    mov r25, r15
    rcall send_number_16bit
    ldi r24, 13            ; CR
    rcall uart_transmit
    ldi r24, 10            ; LF
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
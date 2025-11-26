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

    ; TAC linha 1: t0 = 1000
    ldi r16, 232   ; Constante 1000 (low byte)
    ldi r17, 3  ; Constante 1000 (high byte)

    ; TAC linha 1: A = t0
    mov r18, r16   ; A = t0
    mov r19, r17

    ; TAC linha 2: t1 = 2000
    ldi r20, 208   ; Constante 2000 (low byte)
    ldi r21, 7  ; Constante 2000 (high byte)

    ; TAC linha 2: B = t1
    mov r22, r20   ; B = t1
    mov r23, r21

    ; TAC linha 3: t2 = A + B
    ; Soma 16-bit: t2 = A + B
    add r18, r22   ; Low byte com carry
    adc r19, r23 ; High byte com carry
    mov r16, r18   ; Resultado em t2
    mov r17, r19

    ; Spill t0 (r16:r17) -> 0x0100
    sts 0x0100, r16      ; Store low byte
    sts 0x0101, r17  ; Store high byte

    ; TAC linha 3: RESULT = t2
    mov r18, r16   ; RESULT = t2
    mov r19, r17

    ; Spill A (r18:r19) -> 0x0102
    sts 0x0102, r18      ; Store low byte
    sts 0x0103, r19  ; Store high byte

    ; TAC linha 4: FINAL = RESULT
    mov r20, r18   ; FINAL = RESULT
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
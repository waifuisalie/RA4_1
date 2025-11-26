; ====================================================================
; TESTE 10: Comparação Maior ou Igual
; ====================================================================
; Valida: 100 >= 50 = 1, 50 >= 100 = 0, 100 >= 100 = 1
; Saída esperada via UART 115200: "1 0 1"
; ====================================================================

.section .text
.global main

main:
    ; Inicializar stack pointer
    ldi r16, lo8(0x08FF)
    out 0x3D, r16          ; SPL
    ldi r16, hi8(0x08FF)
    out 0x3E, r16          ; SPH

    ; Inicializar UART (115200 baud @ 16MHz)
    rcall uart_init

    ; ==== TESTE 1: 100 >= 50 (esperado: 1) ====
    ldi r16, 100
    ldi r17, 0
    ldi r18, 50
    ldi r19, 0

    ; Comparação
    cp r16, r18
    cpc r17, r19
    ldi r20, 0
    ldi r21, 0
    brlo skip_ge_1
    ldi r20, 1
skip_ge_1:

    ; Enviar resultado
    mov r24, r20
    subi r24, -48
    rcall uart_transmit

    ; Espaço
    ldi r24, ' '
    rcall uart_transmit

    ; ==== TESTE 2: 50 >= 100 (esperado: 0) ====
    ldi r16, 50
    ldi r17, 0
    ldi r18, 100
    ldi r19, 0

    ; Comparação
    cp r16, r18
    cpc r17, r19
    ldi r20, 0
    ldi r21, 0
    brlo skip_ge_2
    ldi r20, 1
skip_ge_2:

    ; Enviar resultado
    mov r24, r20
    subi r24, -48
    rcall uart_transmit

    ; Espaço
    ldi r24, ' '
    rcall uart_transmit

    ; ==== TESTE 3: 100 >= 100 (esperado: 1) ====
    ldi r16, 100
    ldi r17, 0
    ldi r18, 100
    ldi r19, 0

    ; Comparação
    cp r16, r18
    cpc r17, r19
    ldi r20, 0
    ldi r21, 0
    brlo skip_ge_3
    ldi r20, 1
skip_ge_3:

    ; Enviar resultado
    mov r24, r20
    subi r24, -48
    rcall uart_transmit

    ; Newline
    ldi r24, 13
    rcall uart_transmit
    ldi r24, 10
    rcall uart_transmit

fim:
    rjmp fim

; ====================================================================
; ROTINAS UART
; ====================================================================

uart_init:
    ldi r16, 0
    sts 0xC5, r16        ; UBRR0H = 0
    ldi r16, 8
    sts 0xC4, r16        ; UBRR0L = 8
    ldi r16, (1 << 3)    ; TXEN0
    sts 0xC1, r16        ; UCSR0B
    ldi r16, (1 << 2) | (1 << 1)
    sts 0xC2, r16        ; UCSR0C
    ret

uart_transmit:
    push r25
uart_wait:
    lds r25, 0xC0
    sbrs r25, 5
    rjmp uart_wait
    sts 0xC6, r24
    pop r25
    ret

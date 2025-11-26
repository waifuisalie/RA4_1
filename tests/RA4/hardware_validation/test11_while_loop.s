; ====================================================================
; TESTE 11: WHILE Loop (Count 0 to 9)
; ====================================================================
; Valida: Contador de 0 até 9, saída final = 10
; Saída esperada via UART 115200: "10"
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

    ; ==== WHILE LOOP: while (counter < 10) { counter++; } ====

    ; Initialize counter = 0
    ldi r16, 0
    ldi r17, 0

L0:
    ; Condition: counter < 10
    ldi r18, 10
    ldi r19, 0

    ; Compare counter with 10
    cp r16, r18
    cpc r17, r19
    ldi r20, 0              ; Assume false
    ldi r21, 0
    brsh skip_lt            ; If counter >= 10, skip
    ldi r20, 1              ; Set true
skip_lt:

    ; ifFalse (counter < 10) goto L1
    ldi r24, 0
    ldi r25, 0
    cp r20, r24
    cpc r21, r25
    breq L1                 ; Exit loop if false

    ; Loop body: counter = counter + 1
    ldi r18, 1
    ldi r19, 0
    add r16, r18
    adc r17, r19

    ; goto L0
    rjmp L0

L1:
    ; Loop exited, counter should be 10
    ; Send result via UART (single digit "1" and "0")

    ; Divide by 10 to get tens digit
    ldi r18, 10
    ldi r19, 0
    clr r20                 ; Tens digit counter

div_10:
    cp r16, r18
    cpc r17, r19
    brlo print_tens
    sub r16, r18
    sbc r17, r19
    inc r20
    rjmp div_10

print_tens:
    ; Send tens digit
    mov r24, r20
    subi r24, -48
    rcall uart_transmit

    ; Send units digit
    mov r24, r16
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

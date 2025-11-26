; ====================================================================
; Código Assembly DEBUGADO MANUALMENTE
; Arquitetura: AVR ATmega328P (Arduino Uno)
; Teste: Factorial (1 to 8)
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

    ; DEBUG: Send "S" (Start)
    ldi r24, 'S'
    rcall uart_transmit
    ldi r24, 13            ; CR
    rcall uart_transmit
    ldi r24, 10            ; LF
    rcall uart_transmit

    ; ==== INÍCIO DO CÓDIGO ====

    ; Inicializar: COUNTER = 1
    ldi r18, 1
    ldi r19, 0

    ; Inicializar: RESULT = 1
    ldi r20, 1
    ldi r21, 0

    ; Inicializar: LIMIT = 8
    ldi r22, 8
    ldi r23, 0

    ; DEBUG: Send "I" (Initialized)
    ldi r24, 'I'
    rcall uart_transmit
    ldi r24, 13
    rcall uart_transmit
    ldi r24, 10
    rcall uart_transmit

loop_start:
    ; Comparação: COUNTER <= LIMIT
    cp r18, r22      ; Compare COUNTER with LIMIT (low)
    cpc r19, r23     ; Compare COUNTER with LIMIT (high)
    brsh loop_end    ; Branch if COUNTER > LIMIT (unsigned)

    ; DEBUG: Send "L" (Loop iteration)
    push r18
    push r19
    push r20
    push r21
    push r22
    push r23

    ldi r24, 'L'
    rcall uart_transmit

    ; Send COUNTER value
    mov r24, r18
    mov r25, r19
    rcall send_number_16bit

    ldi r24, ':'
    rcall uart_transmit

    ; Send RESULT value
    mov r24, r20
    mov r25, r21
    rcall send_number_16bit

    ldi r24, 13
    rcall uart_transmit
    ldi r24, 10
    rcall uart_transmit

    pop r23
    pop r22
    pop r21
    pop r20
    pop r19
    pop r18

    ; Multiplicação: RESULT = RESULT * COUNTER
    ; Setup for mul16: R18:R19 = RESULT, R20:R21 = COUNTER
    ; We need to swap because RESULT is in R20:R21 and COUNTER in R18:R19
    push r18        ; Save COUNTER
    push r19

    mov r18, r20    ; R18:R19 = RESULT
    mov r19, r21
    pop r21         ; R20:R21 = COUNTER
    pop r20

    rcall mul16     ; R24:R25 = RESULT * COUNTER

    mov r20, r24    ; RESULT = R24:R25
    mov r21, r25

    ; Increment COUNTER
    ldi r24, 1
    ldi r25, 0
    add r18, r24
    adc r19, r25

    rjmp loop_start

loop_end:
    ; DEBUG: Send "E" (End)
    ldi r24, 'E'
    rcall uart_transmit
    ldi r24, 13
    rcall uart_transmit
    ldi r24, 10
    rcall uart_transmit

    ; Send final RESULT
    ldi r24, 'R'
    rcall uart_transmit
    ldi r24, '='
    rcall uart_transmit

    mov r24, r20    ; RESULT is in R20:R21
    mov r25, r21
    rcall send_number_16bit

    ldi r24, 13
    rcall uart_transmit
    ldi r24, 10
    rcall uart_transmit

fim:
    rjmp fim

; ====================================================================
; mul16: Multiplicação 16-bit × 16-bit = 16-bit (unsigned)
; ====================================================================
mul16:
    push r22
    push r23

    clr r24
    clr r25

    mul r18, r20
    mov r24, r0
    mov r22, r1

    mul r18, r21
    add r22, r0
    adc r25, r1

    mul r19, r20
    add r22, r0
    adc r25, r1

    mov r25, r22

    pop r23
    pop r22

    clr r1
    ret

; ====================================================================
; ROTINAS UART
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
    cpi r18, 0
    breq skip_10000
    mov r24, r18
    subi r24, -48
    rcall uart_transmit
skip_10000:

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
    mov r24, r18
    subi r24, -48
    rcall uart_transmit

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
    mov r24, r18
    subi r24, -48
    rcall uart_transmit

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
    mov r24, r18
    subi r24, -48
    rcall uart_transmit

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

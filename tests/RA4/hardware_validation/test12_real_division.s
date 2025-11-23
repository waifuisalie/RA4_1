; ====================================================================
; TESTE 12: Real Division with Scaling (1 | 2 = 500)
; ====================================================================
; Valida: Divisão real escalada por 1000
; Operação: 1 | 2 deve resultar em 500 (representa 0.500)
; Saída esperada via UART 115200: "500"
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

    ; ==== DIVISÃO REAL ESCALADA: 1 | 2 = 500 ====

    ; Carregar operandos
    ldi r18, 1             ; Dividendo = 1 (low)
    ldi r19, 0             ; Dividendo = 1 (high)
    ldi r20, 2             ; Divisor = 2 (low)
    ldi r21, 0             ; Divisor = 2 (high)

    ; Chamar rotina de divisão escalada
    rcall div_scaled       ; R24:R25 = (1 * 1000) / 2 = 500

    ; Resultado em R24:R25 = 500 (0x01F4)
    ; Enviar via UART

    ; Converter 500 para string decimal "500"
    ; Dividir por 100 para obter centenas
    mov r16, r24           ; Copiar resultado
    mov r17, r25

    ; Centenas: 500 / 100 = 5
    mov r18, r16           ; Copiar resultado para r18:r19
    mov r19, r17
    ldi r20, lo8(100)      ; Divisor = 100
    ldi r21, hi8(100)
    rcall div16            ; R24:R25 = quociente, R22:R23 = resto

    ; Enviar centenas
    subi r24, -48          ; Converter para ASCII
    rcall uart_transmit

    ; Dezenas e unidades estão em R22:R23 (resto = 0)
    ; Dividir por 10
    mov r18, r22
    mov r19, r23
    ldi r20, 10
    ldi r21, 0
    rcall div16            ; R24:R25 = dezenas, R22:R23 = unidades

    ; Enviar dezenas
    subi r24, -48
    rcall uart_transmit

    ; Enviar unidades
    mov r24, r22
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
; ROTINA: div_scaled - Divisão Real Escalada
; ====================================================================
; Entrada: R18:R19 (dividendo), R20:R21 (divisor)
; Saída: R24:R25 (resultado = (dividendo * 1000) / divisor)
; ====================================================================
div_scaled:
    ; Salvar divisor
    push r20
    push r21

    ; Etapa 1: Multiplicar dividendo por 1000
    ldi r20, lo8(1000)
    ldi r21, hi8(1000)
    rcall mul16            ; R24:R25 = dividendo * 1000

    ; Etapa 2: Preparar para divisão
    mov r18, r24
    mov r19, r25

    ; Restaurar divisor
    pop r21
    pop r20

    ; Etapa 3: Dividir
    rcall div16            ; R24:R25 = quociente

    ret

; ====================================================================
; ROTINA: mul16 - Multiplicação 16-bit
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
; ROTINA: div16 - Divisão 16-bit
; ====================================================================
div16:
    push r16

    ; Verificar divisão por zero
    cp r20, r1
    cpc r21, r1
    breq div16_by_zero

    ; Inicializar resto = 0
    clr r22
    clr r23

    ; Loop de 16 iterações (16-bit division)
    ldi r16, 16

div16_loop:
    lsl r18            ; Logical shift left (LSB always = 0, no carry dependency)
    rol r19            ; Rotate to get carry from r18's bit7
    rol r22
    rol r23

    ; Comparar resto com divisor
    cp r22, r20
    cpc r23, r21
    brlo div16_skip_sub

    ; Subtrair divisor do resto
    sub r22, r20
    sbc r23, r21
    inc r18            ; Set quotient LSB bit to 1

div16_skip_sub:
    dec r16
    brne div16_loop

    ; Mover quociente para R24:R25
    mov r24, r18
    mov r25, r19

    pop r16
    ret

div16_by_zero:
    ldi r24, 0xFF
    ldi r25, 0xFF
    mov r22, r18
    mov r23, r19
    pop r16
    ret

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

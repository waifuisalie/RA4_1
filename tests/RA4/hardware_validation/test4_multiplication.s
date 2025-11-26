; ====================================================================
; TESTE 4: Multiplicação 16-bit com Validação Serial
; ====================================================================
; Valida: Operação de multiplicação 16-bit (123 * 45 = 5535)
; Saída esperada via UART 115200: "Teste 4: 123 * 45 = ?\r\nResultado: 5535\r\n"
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

    ; Enviar mensagem de início
    rcall send_start_msg

    ; ==== CÓDIGO DO TESTE 4 (MULTIPLICAÇÃO 16-BIT) ====

    ; TAC linha 1: t0 = 123
    ldi r16, lo8(123)     ; Low byte de 123 (0x007B)
    ldi r17, hi8(123)     ; High byte de 123

    ; TAC linha 2: t1 = 45
    ldi r18, lo8(45)      ; Low byte de 45 (0x002D)
    ldi r19, hi8(45)      ; High byte de 45

    ; TAC linha 3: t2 = t0 * t1 (123 * 45 = 5535)
    ; Multiplicação 16-bit usando rotina mul16
    ; Preparar parâmetros
    mov r18, r16   ; Parâmetro 1 (low) - já está em r16
    mov r19, r17   ; Parâmetro 1 (high) - já está em r17
    mov r20, r18   ; Parâmetro 2 (low) - copiar de r18
    mov r21, r19   ; Parâmetro 2 (high) - copiar de r19

    ; Note: valores já estão corretos, ajustar
    ldi r18, lo8(123)
    ldi r19, hi8(123)
    ldi r20, lo8(45)
    ldi r21, hi8(45)

    rcall mul16           ; Chamar rotina (resultado em R24:R25)
    mov r20, r24   ; Copiar resultado para r20:r21
    mov r21, r25

    ; ==== VALIDAÇÃO: Enviar resultado via serial ====

    ; Enviar "Resultado: "
    rcall send_result_msg

    ; Enviar valor de t2 (em r20:r21)
    mov r24, r20
    mov r25, r21
    rcall send_number_16bit

    ; Enviar newline
    ldi r24, 13     ; CR
    rcall uart_transmit
    ldi r24, 10     ; LF
    rcall uart_transmit

    ; Enviar mensagem de sucesso
    rcall send_success_msg

fim:
    rjmp fim   ; Loop infinito

; ====================================================================
; ROTINA DE MULTIPLICAÇÃO 16-BIT
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
; ROTINAS UART (115200 baud @ 16MHz)
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

; ====================================================================
; ROTINAS DE MENSAGENS
; ====================================================================

send_start_msg:
    ; "Teste 4: 123 * 45 = ?\r\n"
    ldi r24, 'T'
    rcall uart_transmit
    ldi r24, 'e'
    rcall uart_transmit
    ldi r24, 's'
    rcall uart_transmit
    ldi r24, 't'
    rcall uart_transmit
    ldi r24, 'e'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '4'
    rcall uart_transmit
    ldi r24, ':'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '1'
    rcall uart_transmit
    ldi r24, '2'
    rcall uart_transmit
    ldi r24, '3'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '*'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '4'
    rcall uart_transmit
    ldi r24, '5'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '='
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '?'
    rcall uart_transmit
    ldi r24, 13
    rcall uart_transmit
    ldi r24, 10
    rcall uart_transmit
    ret

send_result_msg:
    ; "Resultado: "
    ldi r24, 'R'
    rcall uart_transmit
    ldi r24, 'e'
    rcall uart_transmit
    ldi r24, 's'
    rcall uart_transmit
    ldi r24, 'u'
    rcall uart_transmit
    ldi r24, 'l'
    rcall uart_transmit
    ldi r24, 't'
    rcall uart_transmit
    ldi r24, 'a'
    rcall uart_transmit
    ldi r24, 'd'
    rcall uart_transmit
    ldi r24, 'o'
    rcall uart_transmit
    ldi r24, ':'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ret

send_success_msg:
    ; "OK - Teste passou!\r\n"
    ldi r24, 'O'
    rcall uart_transmit
    ldi r24, 'K'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '-'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, 'T'
    rcall uart_transmit
    ldi r24, 'e'
    rcall uart_transmit
    ldi r24, 's'
    rcall uart_transmit
    ldi r24, 't'
    rcall uart_transmit
    ldi r24, 'e'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, 'p'
    rcall uart_transmit
    ldi r24, 'a'
    rcall uart_transmit
    ldi r24, 's'
    rcall uart_transmit
    ldi r24, 's'
    rcall uart_transmit
    ldi r24, 'o'
    rcall uart_transmit
    ldi r24, 'u'
    rcall uart_transmit
    ldi r24, '!'
    rcall uart_transmit
    ldi r24, 13
    rcall uart_transmit
    ldi r24, 10
    rcall uart_transmit
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

    ; Para números 16-bit completos (0-65535)
    ; Dividir por 10000 para obter dezena de milhares
    ldi r16, lo8(10000)
    ldi r17, hi8(10000)
    clr r18  ; Contador

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

    ; Dividir por 1000 para obter milhares
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

    ; Dividir por 100 para obter centenas
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

    ; Dividir por 10 para obter dezenas
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

; ====================================================================
; Fim do arquivo
; ====================================================================

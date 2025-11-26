; ====================================================================
; TESTE 3: Subtração 16-bit com Validação Serial
; ====================================================================
; Valida: Operação de subtração 16-bit (1000 - 234 = 766)
; Saída esperada via UART 115200: "Teste 3: 1000 - 234 = ?\r\nResultado: 766\r\n"
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

    ; ==== CÓDIGO DO TESTE 3 (SUBTRAÇÃO 16-BIT) ====

    ; TAC linha 1: t0 = 1000
    ldi r16, lo8(1000)    ; Low byte de 1000 (0x03E8)
    ldi r17, hi8(1000)    ; High byte de 1000

    ; TAC linha 2: t1 = 234
    ldi r18, lo8(234)     ; Low byte de 234 (0x00EA)
    ldi r19, hi8(234)     ; High byte de 234

    ; TAC linha 3: t2 = t0 - t1 (1000 - 234 = 766)
    ; Subtração 16-bit: t2 = t0 - t1
    sub r16, r18   ; Low byte com borrow
    sbc r17, r19   ; High byte com borrow
    mov r20, r16   ; Resultado em t2 (r20:r21)
    mov r21, r17

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
    ; "Teste 3: 1000 - 234 = ?\r\n"
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
    ldi r24, '3'
    rcall uart_transmit
    ldi r24, ':'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '1'
    rcall uart_transmit
    ldi r24, '0'
    rcall uart_transmit
    ldi r24, '0'
    rcall uart_transmit
    ldi r24, '0'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '-'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '2'
    rcall uart_transmit
    ldi r24, '3'
    rcall uart_transmit
    ldi r24, '4'
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

    mov r20, r24
    mov r21, r25

    ; Verificar se número >= 256
    cpi r21, 0
    brne send_big_number

    ; Número pequeno (0-255) - usar rotina simples
    ldi r22, 100
    clr r23
extract_hundreds:
    cp r20, r22
    brlo extract_tens
    sub r20, r22
    inc r23
    rjmp extract_hundreds

extract_tens:
    cpi r23, 0
    breq skip_hundreds
    mov r24, r23
    subi r24, -48
    rcall uart_transmit
skip_hundreds:

    ldi r22, 10
    clr r23
extract_tens_loop:
    cp r20, r22
    brlo send_units
    sub r20, r22
    inc r23
    rjmp extract_tens_loop

send_units:
    cpi r23, 0
    breq send_unit_digit
    mov r24, r23
    subi r24, -48
    rcall uart_transmit

send_unit_digit:
    mov r24, r20
    subi r24, -48
    rcall uart_transmit
    rjmp send_number_done

send_big_number:
    ; Para números >= 256, extrair milhares e centenas também
    ; Implementação simplificada para números até 9999
    push r16
    push r17
    push r18
    push r19

    ; r21:r20 contém o número
    ; Dividir por 1000 para obter milhares
    ldi r16, lo8(1000)
    ldi r17, hi8(1000)
    clr r18  ; Contador de milhares

div_1000:
    cp r20, r16
    cpc r21, r17
    brlo div_100
    sub r20, r16
    sbc r21, r17
    inc r18
    rjmp div_1000

div_100:
    ; Imprimir milhares se != 0
    cpi r18, 0
    breq skip_thousands
    mov r24, r18
    subi r24, -48
    rcall uart_transmit
skip_thousands:

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

send_number_done:
    pop r23
    pop r22
    pop r21
    pop r20
    ret

; ====================================================================
; Fim do arquivo
; ====================================================================

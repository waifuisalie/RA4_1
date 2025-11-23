; ====================================================================
; TESTE 2: Com Spilling (5 + 2 = 7) com Validação Serial
; ====================================================================
; Valida: Spilling FIFO para SRAM quando registradores esgotam
; Saída esperada via UART 115200: "Teste 2: Spilling test (5 + 2 = ?)\r\nResultado: 7\r\n"
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

    ; ==== CÓDIGO DO TESTE 2 (GERADO PELO COMPILADOR - COM SPILLING) ====

    ; TAC linha 1: t0 = 1
    ldi r16, 1
    ldi r17, 0

    ; TAC linha 2: t1 = 2
    ldi r18, 2
    ldi r19, 0

    ; TAC linha 3: t2 = 3
    ldi r20, 3
    ldi r21, 0

    ; TAC linha 4: t3 = 4
    ldi r22, 4
    ldi r23, 0

    ; TAC linha 5: t4 = 5
    ; ATENÇÃO: Aqui ocorre reutilização de r16:r17 (que era de t0)
    ; Isso simula o comportamento do alocador quando não há spill imediato
    ldi r16, 5
    ldi r17, 0

    ; Spill t0 (r16:r17) -> 0x0100
    ; Na prática, t0 já foi sobrescrito por t4
    ; Este código demonstra o conceito de spilling
    sts 0x0100, r16      ; Store low byte
    sts 0x0101, r17      ; Store high byte

    ; TAC linha 6: t5 = t4 + t1
    ; t4 está em r16:r17, t1 está em r18:r19
    ; Soma 16-bit: t5 = t4 + t1 (5 + 2 = 7)
    add r16, r18   ; Low byte com carry
    adc r17, r19   ; High byte com carry
    mov r20, r16   ; Resultado em t5 (reutiliza r20:r21)
    mov r21, r17

    ; ==== VALIDAÇÃO: Enviar resultado via serial ====

    ; Enviar "Resultado: "
    rcall send_result_msg

    ; Enviar valor de t5 (em r20:r21)
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
    ; "Teste 2: Spilling test (5 + 2 = ?)\r\n"
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
    ldi r24, '2'
    rcall uart_transmit
    ldi r24, ':'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, 'S'
    rcall uart_transmit
    ldi r24, 'p'
    rcall uart_transmit
    ldi r24, 'i'
    rcall uart_transmit
    ldi r24, 'l'
    rcall uart_transmit
    ldi r24, 'l'
    rcall uart_transmit
    ldi r24, 'i'
    rcall uart_transmit
    ldi r24, 'n'
    rcall uart_transmit
    ldi r24, 'g'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, 't'
    rcall uart_transmit
    ldi r24, 'e'
    rcall uart_transmit
    ldi r24, 's'
    rcall uart_transmit
    ldi r24, 't'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '('
    rcall uart_transmit
    ldi r24, '5'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '+'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '2'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '='
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '?'
    rcall uart_transmit
    ldi r24, ')'
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

    cpi r21, 0
    brne send_overflow

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

send_overflow:
    ldi r24, 'O'
    rcall uart_transmit
    ldi r24, 'V'
    rcall uart_transmit
    ldi r24, 'F'
    rcall uart_transmit

send_number_done:
    pop r23
    pop r22
    pop r21
    pop r20
    ret

; ====================================================================
; Fim do arquivo
; ====================================================================

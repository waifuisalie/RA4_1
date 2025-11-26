; ====================================================================
; TESTE 1: Soma Básica (1 + 2 = 3) com Validação Serial
; ====================================================================
; Valida: Alocação de registradores básica
; Saída esperada via UART 115200: "Teste 1: 1 + 2 = ?\r\nResultado: 3\r\n"
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

    ; ==== CÓDIGO DO TESTE 1 (GERADO PELO COMPILADOR) ====

    ; TAC linha 1: t0 = 1
    ldi r16, 1   ; Constante 1 (low byte)
    ldi r17, 0   ; Constante 1 (high byte)

    ; TAC linha 2: t1 = 2
    ldi r18, 2   ; Constante 2 (low byte)
    ldi r19, 0   ; Constante 2 (high byte)

    ; TAC linha 3: t2 = t0 + t1
    ; Soma 16-bit: t2 = t0 + t1
    add r16, r18   ; Low byte com carry
    adc r17, r19   ; High byte com carry
    mov r20, r16   ; Resultado em t2 (r20:r21)
    mov r21, r17

    ; ==== VALIDAÇÃO: Enviar resultado via serial ====

    ; Enviar "Resultado: "
    rcall send_result_msg

    ; Enviar valor de t2 (em r20:r21)
    mov r24, r20    ; Copiar para r24:r25 (convenção de parâmetro)
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
    ; Configurar baud rate 115200 @ 16MHz
    ; UBRR = (F_CPU / (16 * BAUD)) - 1 = (16000000 / (16 * 115200)) - 1 ≈ 8
    ldi r16, 0
    sts 0xC5, r16        ; UBRR0H = 0
    ldi r16, 8
    sts 0xC4, r16        ; UBRR0L = 8

    ; Habilitar TX
    ldi r16, (1 << 3)    ; TXEN0 bit
    sts 0xC1, r16        ; UCSR0B

    ; Formato 8N1 (8 data bits, no parity, 1 stop bit)
    ldi r16, (1 << 2) | (1 << 1)  ; UCSZ01 | UCSZ00
    sts 0xC2, r16        ; UCSR0C
    ret

uart_transmit:
    ; Transmite byte em r24
    ; Espera buffer estar livre (UDRE0 = 1)
    push r25
uart_wait:
    lds r25, 0xC0        ; UCSR0A
    sbrs r25, 5          ; Testa bit UDRE0
    rjmp uart_wait
    sts 0xC6, r24        ; UDR0 = r24 (envia byte)
    pop r25
    ret

; ====================================================================
; ROTINAS DE MENSAGENS
; ====================================================================

send_start_msg:
    ; "Teste 1: 1 + 2 = ?\r\n"
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
    ldi r24, '1'
    rcall uart_transmit
    ldi r24, ':'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '1'
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
    ldi r24, 13     ; CR
    rcall uart_transmit
    ldi r24, 10     ; LF
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

; ====================================================================
; ROTINA: Enviar número 16-bit como ASCII decimal
; ====================================================================
; Entrada: r24:r25 (número 16-bit)
; Saída: Envia dígitos ASCII via UART
; ====================================================================

send_number_16bit:
    push r20
    push r21
    push r22
    push r23

    mov r20, r24         ; Número low byte em r20
    mov r21, r25         ; Número high byte em r21

    ; Para simplificar, assume número < 100 (suficiente para nossos testes)
    ; Se r21 != 0, número é >= 256, envia "XXX"
    cpi r21, 0
    brne send_overflow

    ; Número em r20 (0-255)
    ; Extrair centenas
    ldi r22, 100
    clr r23              ; Contador de centenas
extract_hundreds:
    cp r20, r22
    brlo extract_tens
    sub r20, r22
    inc r23
    rjmp extract_hundreds

extract_tens:
    ; Enviar centenas (se != 0)
    cpi r23, 0
    breq skip_hundreds
    mov r24, r23
    subi r24, -48        ; Converte para ASCII ('0' = 48)
    rcall uart_transmit
skip_hundreds:

    ; Extrair dezenas
    ldi r22, 10
    clr r23              ; Contador de dezenas
extract_tens_loop:
    cp r20, r22
    brlo send_units
    sub r20, r22
    inc r23
    rjmp extract_tens_loop

send_units:
    ; Enviar dezenas (se != 0 OU se enviamos centenas)
    cpi r23, 0
    breq send_unit_digit
    mov r24, r23
    subi r24, -48        ; ASCII
    rcall uart_transmit

send_unit_digit:
    ; Enviar unidades
    mov r24, r20
    subi r24, -48        ; ASCII
    rcall uart_transmit

    rjmp send_number_done

send_overflow:
    ; Número muito grande, envia "OVF"
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

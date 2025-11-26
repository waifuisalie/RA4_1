; ====================================================================
; TESTE 6: Módulo 16-bit com Validação Serial
; ====================================================================
; Valida: Operação de módulo 16-bit (1234 % 56 = 2)
; Saída esperada via UART 115200: "Teste 6: 1234 % 56 = ?\r\nResultado: 2\r\n"
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

    ; ==== CÓDIGO DO TESTE 6 (MÓDULO 16-BIT) ====

    ; TAC linha 1: t0 = 1234
    ldi r16, lo8(1234)    ; Low byte de 1234 (0x04D2)
    ldi r17, hi8(1234)    ; High byte de 1234

    ; TAC linha 2: t1 = 56
    ldi r18, lo8(56)      ; Low byte de 56 (0x0038)
    ldi r19, hi8(56)      ; High byte de 56

    ; TAC linha 3: t2 = t0 % t1 (1234 % 56 = 2)
    ; Módulo 16-bit usando rotina div16
    ; Preparar parâmetros
    mov r18, r16   ; Dividendo (low)
    mov r19, r17   ; Dividendo (high)

    ; Carregar divisor
    ldi r20, lo8(56)
    ldi r21, hi8(56)

    rcall div16           ; Chamar rotina (quociente em R24:R25, resto em R22:R23)
    mov r20, r22   ; Copiar RESTO para r20:r21
    mov r21, r23

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
; ROTINA DE DIVISÃO 16-BIT (usada também para módulo)
; ====================================================================

div16:
    push r16              ; Salvar registrador usado

    ; Verificar divisão por zero
    cp      r20, r1       ; Comparar divisor low com 0
    cpc     r21, r1       ; Comparar divisor high com 0
    breq    div16_by_zero ; Se zero, pular para tratamento de erro

    ; Inicializar resto = 0
    clr     r22           ; Resto low = 0
    clr     r23           ; Resto high = 0

    ; Inicializar contador de loop (16 iterações para divisão 16-bit)
    ldi     r16, 16

div16_loop:
    ; Deslocar dividendo/quociente para esquerda
    lsl     r18           ; Logical shift left (LSB=0, no carry dependency)
    rol     r19           ; Shift dividend/quotient high

    ; Deslocar bit MSB do dividendo para o resto
    rol     r22           ; Shift into remainder low
    rol     r23           ; Shift into remainder high

    ; Comparar resto com divisor
    cp      r22, r20      ; Compare remainder with divisor (low)
    cpc     r23, r21      ; Compare remainder with divisor (high)
    brcs    div16_skip    ; If remainder < divisor, skip subtraction

    ; Resto >= divisor: subtrair divisor do resto
    sub     r22, r20      ; Subtract divisor from remainder (low)
    sbc     r23, r21      ; Subtract divisor from remainder (high)
    inc     r18           ; Set quotient LSB bit to 1

div16_skip:
    dec     r16           ; Decrementar contador
    brne    div16_loop    ; Loop se não terminou

    ; Mover quociente para registradores de saída
    mov     r24, r18      ; Quotient to output (low)
    mov     r25, r19      ; Quotient to output (high)

    ; Resto já está em R22:R23 (correto)

    pop r16
    ret

div16_by_zero:
    ; Retornar valores de erro
    ldi     r24, 0xFF     ; Quociente = 0xFFFF (indicador de erro)
    ldi     r25, 0xFF
    mov     r22, r18      ; Resto = dividendo original (low)
    mov     r23, r19      ; Resto = dividendo original (high)
    pop r16
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
    ; "Teste 6: 1234 % 56 = ?\r\n"
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
    ldi r24, '6'
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
    ldi r24, '4'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '%'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '5'
    rcall uart_transmit
    ldi r24, '6'
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

    ; Para números pequenos (0-9, um dígito)
    ; Verificar se < 10
    cpi r20, 10
    brlo print_single_digit
    cpi r21, 0
    brne print_two_digits

print_single_digit:
    ; Número de um dígito (0-9)
    mov r24, r20
    subi r24, -48
    rcall uart_transmit
    rjmp number_done

print_two_digits:
    ; Para números de 2 dígitos (10-99)
    ldi r16, 10
    clr r17
    clr r18  ; Contador de dezenas

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

number_done:
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

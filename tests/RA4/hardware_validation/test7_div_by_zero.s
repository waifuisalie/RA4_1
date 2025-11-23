; ====================================================================
; TESTE 7: Divisão por Zero (Tratamento de Erro)
; ====================================================================
; Valida: Tratamento de divisão por zero (100 ÷ 0 = erro → 65535)
; Saída esperada via UART 115200: "Teste 7: 100 / 0 = ?\r\nResultado: 65535 (ERRO)\r\n"
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

    ; ==== CÓDIGO DO TESTE 7 (DIVISÃO POR ZERO) ====

    ; TAC linha 1: t0 = 100
    ldi r16, lo8(100)     ; Low byte de 100 (0x0064)
    ldi r17, hi8(100)     ; High byte de 100

    ; TAC linha 2: t1 = 0 (divisor zero!)
    ldi r18, 0            ; Low byte de 0
    ldi r19, 0            ; High byte de 0

    ; TAC linha 3: t2 = t0 / t1 (100 / 0 = erro)
    ; Divisão 16-bit usando rotina div16
    ; Preparar parâmetros
    mov r18, r16   ; Dividendo (low)
    mov r19, r17   ; Dividendo (high)

    ; Carregar divisor (0)
    ldi r20, 0
    ldi r21, 0

    rcall div16           ; Chamar rotina (deve retornar 0xFFFF como erro)
    mov r20, r24   ; Copiar quociente para r20:r21
    mov r21, r25

    ; ==== VALIDAÇÃO: Enviar resultado via serial ====

    ; Enviar "Resultado: "
    rcall send_result_msg

    ; Enviar valor de t2 (em r20:r21 - deve ser 0xFFFF = 65535)
    mov r24, r20
    mov r25, r21
    rcall send_number_16bit

    ; Enviar " (ERRO)"
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '('
    rcall uart_transmit
    ldi r24, 'E'
    rcall uart_transmit
    ldi r24, 'R'
    rcall uart_transmit
    ldi r24, 'R'
    rcall uart_transmit
    ldi r24, 'O'
    rcall uart_transmit
    ldi r24, ')'
    rcall uart_transmit

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
; ROTINA DE DIVISÃO 16-BIT
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
    ; "Teste 7: 100 / 0 = ?\r\n"
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
    ldi r24, '7'
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
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '/'
    rcall uart_transmit
    ldi r24, ' '
    rcall uart_transmit
    ldi r24, '0'
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

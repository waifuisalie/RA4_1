; ====================================================================
; Código Assembly gerado automaticamente
; Arquitetura: AVR ATmega328P (Arduino Uno)
; Compilador: RA4_Compiladores - Fase 4
; ====================================================================

.section .text
.global main

main:
    ; Inicializar stack pointer
    ldi r16, lo8(0x08FF)   ; RAMEND low byte
    out 0x3D, r16          ; SPL
    ldi r16, hi8(0x08FF)   ; RAMEND high byte
    out 0x3E, r16          ; SPH

    ; Inicializar UART (115200 baud @ 16MHz)
    rcall uart_init

    ; ==== INÍCIO DO CÓDIGO GERADO ====

    ; TAC linha 1: t0 = 600
    ldi r16, 88   ; Constante 600 (low byte)
    ldi r17, 2  ; Constante 600 (high byte)

    ; TAC linha 1: A = t0
    mov r18, r16   ; A = t0
    mov r19, r17

    ; TAC linha 2: t1 = 400
    ldi r20, 144   ; Constante 400 (low byte)
    ldi r21, 1  ; Constante 400 (high byte)

    ; TAC linha 2: B = t1
    mov r22, r20   ; B = t1
    mov r23, r21

    ; TAC linha 3: t2 = A | B
    ; Real division: (op1 * 100) / op2 for precision
    ; Step 1: Multiply dividend by scale factor (100)
    mov r18, r18      ; Dividendo
    mov r19, r19
    ldi r20, 100             ; Scale factor (100)
    ldi r21, 0
    rcall mul16              ; R24:R25 = op1 * 100
    ; Step 2: Divide scaled dividend by divisor
    mov r18, r24             ; Move result to dividend registers
    mov r19, r25
    mov r20, r22      ; Divisor
    mov r21, r23
    rcall div16              ; R24:R25 = (op1 * 100) / op2
    mov r16, r24      ; Copy result
    mov r17, r25

    ; Spill t0 (r16:r17) -> 0x0100
    sts 0x0100, r16      ; Store low byte
    sts 0x0101, r17  ; Store high byte

    ; TAC linha 3: RESULT = t2
    mov r18, r16   ; RESULT = t2
    mov r19, r17

    ; Spill A (r18:r19) -> 0x0102
    sts 0x0102, r18      ; Store low byte
    sts 0x0103, r19  ; Store high byte

    ; TAC linha 4: FINAL = RESULT
    mov r20, r18   ; FINAL = RESULT
    mov r21, r19

    ; ==== FIM DO CÓDIGO GERADO ====

    ; Enviar resultado final via UART
    mov r24, r20    ; Copiar resultado para R24:R25
    mov r25, r21
    rcall send_number_16bit
    ldi r24, 13            ; CR
    rcall uart_transmit
    ldi r24, 10            ; LF
    rcall uart_transmit
    jmp fim                ; Saltar para loop infinito

; ====================================================================
; mul16: Multiplicação 16-bit × 16-bit = 16-bit (unsigned)
; Entrada: R18:R19 (op1), R20:R21 (op2)
; Saída: R24:R25 (resultado)
; Usa: R0, R1, R22, R23
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
; div16: Divisão 16-bit ÷ 16-bit = quociente e resto (unsigned)
; Algoritmo: Restoring shift-subtract (17 iterações, resto corrigido)
; Entrada: R18:R19 (dividendo), R20:R21 (divisor)
; Saída: R24:R25 (quociente), R22:R23 (resto)
; Usa: R16 (contador de loop)
; Ciclos: ~232
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

; ====================================================================
; send_number_16bit: Envia número 16-bit como decimal via UART
; Entrada: R24:R25 (número 16-bit, 0-65535)
; Saída: Nenhuma (envia via UART)
; ====================================================================
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
    ; Imprimir dezena de milhares se != 0
    cpi r18, 0
    breq skip_10000
    mov r24, r18
    subi r24, -48
    rcall uart_transmit
skip_10000:

    ; Milhares (1000)
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

    ; Centenas (100)
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

    ; Dezenas (10)
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

fim:
    rjmp fim   ; Loop infinito

; ====================================================================
; Fim do programa
; ====================================================================
#!/usr/bin/env python3

# Integrantes do grupo (ordem alfabética):
# Nome Completo 1 - Breno Rossi Duarte
# Nome Completo 2 - Francisco Bley Ruthes
# Nome Completo 3 - Rafael Olivare Piveta
# Nome Completo 4 - Stefan Benjamim Seixas Lourenço Rodrigues
#
# Nome do grupo no Canvas: RA2_1

# ============================================================================
# LEGACY CODE - RA1 PHASE ONLY (Assembly Generation)
# ============================================================================
# Geração de código Assembly RISC-V para Arduino Uno
# Não usado em RA2/RA3+ - mantido apenas para referência histórica do RA1
# ============================================================================

from pathlib import Path

def save_registers_inc(nome_arquivo="registers.inc"):
    """Cria o arquivo registers.inc com as definições do ATmega328P - 16-BIT VERSION"""
    conteudo = """; ATmega328P Register Definitions
; Custom header for assembly programming
; Updated for RPN Calculator Project - TRUE 16-BIT VERSION
; Supports integers from 0 to 65535

; Stack Pointer Registers
.equ SPL,     0x3D
.equ SPH,     0x3E

; SRAM Memory Layout
.equ RAMSTART, 0x0100
.equ RAMEND,   0x08FF

; UART0 Registers
.equ UDR0,    0xC6
.equ UBRR0L,  0xC4
.equ UBRR0H,  0xC5
.equ UCSR0A,  0xC0
.equ UCSR0B,  0xC1
.equ UCSR0C,  0xC2

; UART0 Control Bits
.equ RXC0,    7
.equ TXC0,    6
.equ UDRE0,   5
.equ FE0,     4
.equ DOR0,    3
.equ UPE0,    2
.equ U2X0,    1
.equ MPCM0,   0

.equ RXCIE0,  7
.equ TXCIE0,  6
.equ UDRIE0,  5
.equ RXEN0,   4
.equ TXEN0,   3
.equ UCSZ02,  2
.equ RXB80,   1
.equ TXB80,   0

.equ UMSEL01, 7
.equ UMSEL00, 6
.equ UPM01,   5
.equ UPM00,   4
.equ USBS0,   3
.equ UCSZ01,  2
.equ UCSZ00,  1
.equ UCPOL0,  0

; GPIO
.equ PORTB,   0x05
.equ DDRB,    0x04
.equ PINB,    0x03

.equ PORTC,   0x08
.equ DDRC,    0x07
.equ PINC,    0x06

.equ PORTD,   0x0B
.equ DDRD,    0x0A
.equ PIND,    0x09

; Timer/Counter0
.equ TCNT0,   0x46
.equ TCCR0A,  0x44
.equ TCCR0B,  0x45
.equ TIMSK0,  0x6E
.equ TIFR0,   0x15

; Vectors
.equ RESET_VECTOR,        0x0000

; Useful constants
.equ BAUD_9600,  103
.equ BAUD_19200, 51
.equ BAUD_38400, 25

; ASCII
.equ ASCII_0,     48
.equ ASCII_9,     57
.equ ASCII_CR,    13
.equ ASCII_LF,    10
.equ ASCII_SPACE, 32

; 16-bit calculator
.equ MAX_STACK_SIZE, 16
.equ MAX_VARIABLES,  26
.equ MAX_INT16, 65535
.equ MIN_INT16, 0

; Memory map for RPN
.equ RPN_STACK_START, 0x0200
.equ RPN_VARS_START,  0x0300
.equ RPN_TEMP_START,  0x0400
.equ DIGIT_BUFFER,    0x0500

; Flags
.equ FLAG_OVERFLOW,  0
.equ FLAG_UNDERFLOW, 1
.equ FLAG_DIVZERO,   2
.equ FLAG_INVALID,   3
"""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"Arquivo {nome_arquivo} criado com sucesso (16-bit version).")
        return True
    except Exception as e:
        print(f"Erro ao criar {nome_arquivo}: {e}")
        return False

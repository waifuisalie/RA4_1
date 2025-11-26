#!/bin/bash
# ====================================================================
# Script de Automação - Validação de Hardware Arduino Uno
# ====================================================================
# Executa testes sequencialmente e captura saídas seriais
# ====================================================================

set -e  # Aborta se qualquer comando falhar

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuração
PORT=${PORT:-/dev/ttyUSB0}
BAUD=115200
TIMEOUT=5  # segundos para aguardar saída serial

# ====================================================================
# Funções Auxiliares
# ====================================================================

print_header() {
    echo -e "${BLUE}====================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}====================================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

check_dependencies() {
    print_header "Verificando Dependências"

    local deps=("avr-gcc" "avr-objcopy" "avrdude" "screen")
    local missing=0

    for dep in "${deps[@]}"; do
        if command -v "$dep" &> /dev/null; then
            print_success "$dep encontrado"
        else
            print_error "$dep NÃO encontrado"
            missing=$((missing + 1))
        fi
    done

    if [ $missing -gt 0 ]; then
        print_error "Dependências faltando! Instale-as primeiro."
        echo ""
        echo "No Ubuntu/Debian:"
        echo "  sudo apt-get install avr-libc gcc-avr avrdude screen"
        exit 1
    fi

    echo ""
}

check_arduino() {
    print_header "Verificando Conexão com Arduino"

    if [ ! -e "$PORT" ]; then
        print_error "Arduino não encontrado em $PORT"
        print_info "Verifique a conexão e tente novamente"
        print_info "Portas disponíveis:"
        ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null || echo "  Nenhuma porta USB serial encontrada"
        exit 1
    fi

    print_success "Arduino encontrado em $PORT"
    echo ""
}

compile_test() {
    local test_num=$1
    print_info "Compilando Test $test_num..."
    make test$test_num > /dev/null 2>&1
    print_success "Test $test_num compilado"
}

upload_test() {
    local test_num=$1
    print_info "Fazendo upload de Test $test_num..."
    make upload$test_num > /dev/null 2>&1
    print_success "Upload concluído"
    sleep 2  # Aguarda Arduino reiniciar
}

capture_serial() {
    local test_num=$1
    local expected=$2

    print_info "Capturando saída serial (timeout: ${TIMEOUT}s)..."

    # Captura saída serial por TIMEOUT segundos
    local output=$(timeout $TIMEOUT screen -L -Logfile /tmp/serial_output_$test_num.txt $PORT $BAUD 2>/dev/null || true)

    # Lê o arquivo de log gerado pelo screen
    if [ -f /tmp/serial_output_$test_num.txt ]; then
        output=$(cat /tmp/serial_output_$test_num.txt)
        rm -f /tmp/serial_output_$test_num.txt
    fi

    echo "$output"
}

validate_output() {
    local test_num=$1
    local output=$2
    local expected_result=$3

    print_info "Validando resultado..."

    if echo "$output" | grep -q "Resultado: $expected_result"; then
        print_success "Test $test_num PASSOU - Resultado correto: $expected_result"
        return 0
    else
        print_error "Test $test_num FALHOU - Resultado esperado: $expected_result"
        echo "Saída recebida:"
        echo "$output"
        return 1
    fi
}

run_test() {
    local test_num=$1
    local expected_result=$2

    print_header "Executando Test $test_num"

    compile_test $test_num
    upload_test $test_num

    local output=$(capture_serial $test_num)
    echo ""
    echo "Saída Serial:"
    echo "----------------------------------------"
    echo "$output"
    echo "----------------------------------------"
    echo ""

    validate_output $test_num "$output" $expected_result
    echo ""
}

# ====================================================================
# Main
# ====================================================================

main() {
    print_header "Validação de Hardware - Testes de Assembly AVR"
    echo ""

    check_dependencies
    check_arduino

    local failed=0

    # Test 1: 1 + 2 = 3
    if ! run_test 1 3; then
        failed=$((failed + 1))
    fi

    # Test 2: 5 + 2 = 7 (com spilling)
    if ! run_test 2 7; then
        failed=$((failed + 1))
    fi

    # Resumo final
    print_header "Resumo Final"

    if [ $failed -eq 0 ]; then
        print_success "TODOS OS TESTES PASSARAM!"
        exit 0
    else
        print_error "$failed teste(s) falharam"
        exit 1
    fi
}

# ====================================================================
# Ajuda
# ====================================================================

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "Uso: $0 [OPÇÕES]"
    echo ""
    echo "Executa testes de validação de hardware sequencialmente."
    echo ""
    echo "Opções:"
    echo "  PORT=<porta>    Especifica porta serial (padrão: /dev/ttyUSB0)"
    echo "  --help, -h      Mostra esta mensagem"
    echo ""
    echo "Exemplos:"
    echo "  $0                    # Usa porta padrão"
    echo "  PORT=/dev/ttyACM0 $0  # Usa porta personalizada"
    exit 0
fi

main

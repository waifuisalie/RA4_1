#!/usr/bin/env python3
"""
Upload Arduino - Compilacao e Upload de Assembly AVR para Arduino Uno
Uso: python upload_arduino.py <arquivo.s>
"""

import sys
from pathlib import Path

# Path: src/RA4/functions/python/upload_arduino.py
# Adiciona o diretório raiz do projeto ao sys.path
base_dir = Path(__file__).parent.parent.parent.parent  # RA4_1/
sys.path.insert(0, str(base_dir))

try:
    from src.RA4.functions.python.arduino_tools import (
        check_avr_toolchain,
        detect_arduino_port,
        compile_assembly,
        upload_hex
    )
except ImportError as e:
    print(f"ERRO: {e}")
    sys.exit(1)


def find_assembly_file(filename: str) -> Path:
    """Busca arquivo Assembly em outputs/RA4/."""
    # base_dir já aponta para RA4_1/
    asm_dir = base_dir / 'outputs' / 'RA4'
    asm_path = asm_dir / filename

    if not asm_path.exists():
        print(f"ERRO: Arquivo nao encontrado: {asm_path}")
        asm_files = list(asm_dir.glob('*.s')) if asm_dir.exists() else []
        if asm_files:
            print("Arquivos disponiveis:")
            for f in asm_files:
                print(f"  {f.name}")
        raise FileNotFoundError(asm_path)

    return asm_path


def main():
    if len(sys.argv) != 2:
        print("Uso: python upload_arduino.py <arquivo.s>")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.s'):
        filename += '.s'

    # Busca arquivo
    try:
        asm_path = find_assembly_file(filename)
    except FileNotFoundError:
        sys.exit(1)

    # Verifica ferramentas AVR
    success, missing = check_avr_toolchain()
    if not success:
        print("ERRO: Ferramentas AVR nao encontradas:")
        for tool in missing:
            print(f"  {tool}")
        sys.exit(1)

    # Compila
    success, elf_path, hex_path = compile_assembly(str(asm_path))
    if not success:
        sys.exit(1)

    # Detecta porta
    port = detect_arduino_port()
    if port is None:
        print("ERRO: Porta Arduino nao detectada")
        sys.exit(1)

    # Upload
    success = upload_hex(hex_path, port)
    if not success:
        sys.exit(1)

    print(f"\nConcluido: {hex_path}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelado")
        sys.exit(130)
    except Exception as e:
        print(f"\nERRO: {e}")
        sys.exit(1)

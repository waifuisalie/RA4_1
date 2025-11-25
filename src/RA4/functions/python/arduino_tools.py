"""
Arduino Tools - Funções auxiliares para compilação e upload de Assembly AVR
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from typing import Optional, Tuple, List


def detect_msys2_paths() -> List[str]:
    """Detecta instalações do MSYS2 no Windows."""
    if platform.system() != 'Windows':
        return []

    possible_paths = [
        Path('C:/msys64/mingw64/bin'),
        Path('C:/msys64/usr/bin'),
        Path('C:/msys32/mingw32/bin'),
        Path('C:/msys32/usr/bin'),
    ]

    found_paths = []
    for path in possible_paths:
        if path.exists() and (path / 'avr-gcc.exe').exists():
            found_paths.append(str(path))

    return found_paths


def setup_avr_environment():
    """Configura o ambiente para usar ferramentas AVR."""
    if platform.system() != 'Windows':
        return

    msys2_paths = detect_msys2_paths()

    other_paths = [
        Path('C:/Program Files (x86)/Arduino/hardware/tools/avr/bin'),
        Path('C:/Program Files/Arduino/hardware/tools/avr/bin'),
        Path('C:/WinAVR/bin'),
        Path('C:/avr8-gnu-toolchain/bin'),
    ]

    found_other = []
    for path in other_paths:
        if path.exists() and (path / 'avr-gcc.exe').exists():
            found_other.append(str(path))

    all_paths = msys2_paths + found_other
    if all_paths:
        current_path = os.environ.get('PATH', '')
        new_paths = [p for p in all_paths if p not in current_path]
        if new_paths:
            os.environ['PATH'] = os.pathsep.join(new_paths) + os.pathsep + current_path


def check_avr_toolchain() -> Tuple[bool, list]:
    """Verifica se as ferramentas AVR estão instaladas."""
    setup_avr_environment()

    tools = ['avr-gcc', 'avr-objcopy', 'avrdude']
    missing_tools = []

    for tool in tools:
        try:
            result = subprocess.run(
                [tool, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                missing_tools.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            missing_tools.append(tool)

    return (len(missing_tools) == 0, missing_tools)


def detect_arduino_port() -> Optional[str]:
    """Detecta automaticamente a porta serial do Arduino."""
    try:
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()
        arduino_keywords = ['arduino', 'ch340', 'cp210', 'ftdi', 'usb']

        for port in ports:
            description = port.description.lower()
            manufacturer = (port.manufacturer or "").lower()

            if any(keyword in description or keyword in manufacturer
                   for keyword in arduino_keywords):
                return port.device

        if ports:
            return ports[0].device

        return None

    except ImportError:
        print("ERRO: pyserial não instalado")
        return None
    except Exception as e:
        print(f"ERRO: {e}")
        return None


def compile_assembly(asm_path: str, output_dir: str = None,
                     mcu: str = 'atmega328p') -> Tuple[bool, str, str]:
    """Compila arquivo Assembly AVR para ELF e HEX."""
    asm_path = Path(asm_path)

    if not asm_path.exists():
        return False, "", ""

    if output_dir is None:
        output_dir = asm_path.parent
    else:
        output_dir = Path(output_dir)

    base_name = asm_path.stem
    elf_path = output_dir / f"{base_name}.elf"
    hex_path = output_dir / f"{base_name}.hex"

    # Compilar .s para .elf
    try:
        result = subprocess.run(
            ['avr-gcc', f'-mmcu={mcu}', '-o', str(elf_path), str(asm_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"ERRO avr-gcc: {result.stderr}")
            return False, "", ""

    except subprocess.TimeoutExpired:
        return False, "", ""
    except Exception as e:
        print(f"ERRO: {e}")
        return False, "", ""

    # Gerar .hex
    try:
        result = subprocess.run(
            ['avr-objcopy', '-O', 'ihex', '-R', '.eeprom',
             str(elf_path), str(hex_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"ERRO avr-objcopy: {result.stderr}")
            return False, str(elf_path), ""

    except subprocess.TimeoutExpired:
        return False, str(elf_path), ""
    except Exception as e:
        print(f"ERRO: {e}")
        return False, str(elf_path), ""

    return True, str(elf_path), str(hex_path)


def upload_hex(hex_path: str, port: str, mcu: str = 'atmega328p',
               baud: int = 115200, programmer: str = 'arduino') -> bool:
    """Faz upload do arquivo HEX para o Arduino via avrdude."""
    hex_path = Path(hex_path)

    if not hex_path.exists():
        return False

    cmd = [
        'avrdude',
        '-c', programmer,
        '-p', mcu,
        '-P', port,
        '-b', str(baud),
        '-U', f'flash:w:{hex_path}:i'
    ]

    try:
        # Suprime output do avrdude (muito verboso)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return True
        else:
            # Mostra erro apenas se falhar
            print(f"ERRO avrdude: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        return False
    except FileNotFoundError:
        print("ERRO: avrdude nao encontrado")
        return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False


def get_system_info() -> dict:
    """Retorna informações do sistema."""
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'python_version': sys.version
    }

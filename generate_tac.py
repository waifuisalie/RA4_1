#!/usr/bin/env python3
"""
TAC Generator Script

Generates Three Address Code (TAC) from the attributed AST produced by Phase 3.
Works with any test file - just run the compiler first to generate the AST,
then run this script to generate TAC.

Usage:
    # First, generate AST with the compiler
    ./compilador.py inputs/RA3/teste2.txt

    # Then generate TAC
    python generate_tac.py

Output Files:
    - outputs/RA4/tac_instructions.json (structured JSON format)
    - outputs/RA4/tac_output.txt (human-readable debug format)


THIS IS JUST TO MAKE TESTING TAC EASIER, I SHOULD BE DELETED LATER
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.RA4.functions.python.tac_manager import TACManager
from src.RA4.functions.python.ast_traverser import ASTTraverser

# File paths
AST_INPUT = PROJECT_ROOT / "outputs" / "RA3" / "arvore_atribuida.json"
TAC_JSON_OUTPUT = PROJECT_ROOT / "outputs" / "RA4" / "tac_instructions.json"
TAC_TEXT_OUTPUT = PROJECT_ROOT / "outputs" / "RA4" / "tac_output.txt"


def load_ast():
    """Load the attributed AST from Phase 3 output."""
    if not AST_INPUT.exists():
        print(f"❌ Error: AST file not found at {AST_INPUT}")
        print("\nPlease run the compiler first to generate the AST:")
        print("  ./compilador.py inputs/RA3/teste2.txt")
        sys.exit(1)

    try:
        with open(AST_INPUT, 'r') as f:
            ast = json.load(f)
        return ast
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in AST file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading AST: {e}")
        sys.exit(1)


def generate_tac(ast):
    """Generate TAC instructions from AST."""
    try:
        manager = TACManager()
        traverser = ASTTraverser(manager)
        instructions = traverser.generate_tac(ast)
        stats = traverser.get_statistics()
        return instructions, stats
    except IndexError as e:
        # Known issue: Logical operators (!, &&, ||) not fully implemented yet
        print(f"\n⚠️  Warning: TAC generation stopped due to unimplemented feature")
        print(f"   Error: {e}")
        print(f"\n   This is likely due to logical operators (!, &&, ||) which are")
        print(f"   not yet implemented (Issues 1.5+). Arithmetic and comparison")
        print(f"   operators should work correctly.")
        print(f"\n   Try using a test file without logical operators, or wait for")
        print(f"   Issue 1.5 implementation.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating TAC: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def save_json_output(instructions, stats):
    """Save TAC in structured JSON format."""
    TAC_JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Convert instructions to JSON-serializable format
    json_instructions = []
    for instr in instructions:
        instr_dict = {
            "line": instr.line,
            "instruction": instr.to_string(),
            "type": instr.__class__.__name__,
        }

        # Add type information if available
        if hasattr(instr, 'data_type') and instr.data_type:
            instr_dict["data_type"] = instr.data_type

        # Add operation-specific fields
        if hasattr(instr, 'dest'):
            instr_dict["dest"] = instr.dest
        if hasattr(instr, 'source'):
            instr_dict["source"] = instr.source
        if hasattr(instr, 'left'):
            instr_dict["left"] = instr.left
        if hasattr(instr, 'right'):
            instr_dict["right"] = instr.right
        if hasattr(instr, 'operator'):
            instr_dict["operator"] = instr.operator

        json_instructions.append(instr_dict)

    output = {
        "metadata": {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "source_ast": str(AST_INPUT),
            "total_instructions": len(instructions)
        },
        "instructions": json_instructions,
        "statistics": stats
    }

    with open(TAC_JSON_OUTPUT, 'w') as f:
        json.dump(output, f, indent=2)

    return TAC_JSON_OUTPUT


def save_text_output(instructions, stats):
    """Save TAC in human-readable debug format."""
    TAC_TEXT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(TAC_TEXT_OUTPUT, 'w') as f:
        f.write("TAC Output - Generated from arvore_atribuida.json\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        for instr in instructions:
            type_info = f"[type: {instr.data_type}]" if hasattr(instr, 'data_type') and instr.data_type else ""
            f.write(f"Line {instr.line:2}: {instr.to_string():<25} {type_info}\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("Statistics:\n")
        for key, value in stats.items():
            f.write(f"  {key}: {value}\n")
        f.write("=" * 70 + "\n")

    return TAC_TEXT_OUTPUT


def print_summary(instructions, stats, json_path, text_path):
    """Print summary to console."""
    print("\n" + "=" * 70)
    print("TAC GENERATION COMPLETE")
    print("=" * 70)
    print(f"\n📄 Source AST: {AST_INPUT}")
    print(f"✅ Generated {len(instructions)} TAC instructions")
    print("\n📊 Statistics:")
    for key, value in stats.items():
        print(f"  • {key}: {value}")

    print("\n💾 Output Files:")
    print(f"  • JSON: {json_path}")
    print(f"  • Text: {text_path}")

    print("\n📝 First 10 Instructions:")
    for i, instr in enumerate(instructions[:10], 1):
        type_info = f"[{instr.data_type}]" if hasattr(instr, 'data_type') and instr.data_type else ""
        print(f"  {i:2}. Line {instr.line:2}: {instr.to_string():<25} {type_info}")

    if len(instructions) > 10:
        print(f"  ... and {len(instructions) - 10} more")

    print("\n" + "=" * 70)
    print("\n✨ Done! View the outputs with:")
    print(f"  cat {text_path}")
    print(f"  cat {json_path}")
    print()


def main():
    """Main entry point."""
    print("\n🚀 TAC Generator")
    print("=" * 70)

    # Load AST
    print(f"\n📖 Loading AST from: {AST_INPUT}")
    ast = load_ast()
    num_lines = len(ast.get('arvore_atribuida', []))
    print(f"✅ Loaded AST with {num_lines} lines")

    # Generate TAC
    print("\n⚙️  Generating TAC instructions...")
    instructions, stats = generate_tac(ast)
    print(f"✅ Generated {len(instructions)} instructions")

    # Save outputs
    print("\n💾 Saving outputs...")
    json_path = save_json_output(instructions, stats)
    print(f"  ✅ JSON saved to: {json_path}")

    text_path = save_text_output(instructions, stats)
    print(f"  ✅ Text saved to: {text_path}")

    # Print summary
    print_summary(instructions, stats, json_path, text_path)


if __name__ == "__main__":
    main()

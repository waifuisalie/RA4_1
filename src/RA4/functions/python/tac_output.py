"""
TAC Output - Serialization Functions for TAC Instructions

Issue 1.8 - Output File Generation

This module provides functions to serialize TAC instructions to various formats:
- JSON: For programmatic access and further processing
- Markdown: For human-readable documentation

Output files:
- outputs/RA4/TAC.json - Machine-readable TAC representation
- outputs/RA4/TAC.md - Human-readable TAC documentation
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .tac_instructions import TACInstruction


def to_json(
    instructions: List[TACInstruction],
    statistics: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Convert TAC instructions to JSON-serializable dictionary.

    Args:
        instructions: List of TACInstruction objects
        statistics: Optional statistics dictionary from ASTTraverser
        metadata: Optional metadata (source file, timestamp, etc.)

    Returns:
        Dictionary ready for JSON serialization:
        {
            "metadata": {...},
            "statistics": {...},
            "instructions": [...]
        }

    Example:
        >>> data = to_json(instructions, stats, {"source": "teste1.txt"})
        >>> json.dumps(data, indent=2)
    """
    result = {
        "metadata": metadata or {
            "generated_at": datetime.now().isoformat(),
            "generator": "RA4 TAC Generator",
            "version": "1.0"
        },
        "statistics": statistics or {},
        "instructions": [instr.to_dict() for instr in instructions]
    }

    return result


def to_markdown(
    instructions: List[TACInstruction],
    statistics: Optional[Dict[str, Any]] = None,
    title: str = "TAC Output"
) -> str:
    """
    Convert TAC instructions to Markdown formatted string.

    Args:
        instructions: List of TACInstruction objects
        statistics: Optional statistics dictionary
        title: Title for the markdown document

    Returns:
        Markdown formatted string

    Example:
        >>> md = to_markdown(instructions, stats, "TAC - teste1.txt")
        >>> print(md)
    """
    lines = []

    # Header
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # Statistics section
    if statistics:
        lines.append("## Statistics")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        for key, value in statistics.items():
            lines.append(f"| {key} | {value} |")
        lines.append("")

    # Instructions section
    lines.append("## Instructions")
    lines.append("")
    lines.append("```")

    current_line = None
    for instr in instructions:
        # Add line separator when source line changes
        if hasattr(instr, 'line') and instr.line != current_line:
            if current_line is not None:
                lines.append("")  # Blank line between source lines
            lines.append(f"# Line {instr.line}")
            current_line = instr.line

        # Format instruction with type annotation
        instr_str = instr.to_string()
        type_info = ""
        if hasattr(instr, 'data_type') and instr.data_type:
            type_info = f"  ; [{instr.data_type}]"

        lines.append(f"    {instr_str}{type_info}")

    lines.append("```")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total Instructions:** {len(instructions)}")

    # Count instruction types
    type_counts = {}
    for instr in instructions:
        instr_type = type(instr).__name__
        type_counts[instr_type] = type_counts.get(instr_type, 0) + 1

    lines.append("- **Instruction Types:**")
    for instr_type, count in sorted(type_counts.items()):
        lines.append(f"  - {instr_type}: {count}")

    return "\n".join(lines)


def save_json(
    instructions: List[TACInstruction],
    output_path: Path,
    statistics: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> None:
    """
    Save TAC instructions to JSON file.

    Args:
        instructions: List of TACInstruction objects
        output_path: Path to output JSON file
        statistics: Optional statistics dictionary
        metadata: Optional metadata dictionary
    """
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate JSON data
    data = to_json(instructions, statistics, metadata)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_markdown(
    instructions: List[TACInstruction],
    output_path: Path,
    statistics: Optional[Dict[str, Any]] = None,
    title: str = "TAC Output"
) -> None:
    """
    Save TAC instructions to Markdown file.

    Args:
        instructions: List of TACInstruction objects
        output_path: Path to output Markdown file
        statistics: Optional statistics dictionary
        title: Title for the markdown document
    """
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate Markdown content
    content = to_markdown(instructions, statistics, title)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def save_tac_output(
    instructions: List[TACInstruction],
    output_dir: Path,
    statistics: Optional[Dict[str, Any]] = None,
    source_file: Optional[str] = None
) -> Dict[str, Path]:
    """
    Save TAC instructions to both JSON and Markdown files.

    This is the main convenience function that generates both output formats.

    Args:
        instructions: List of TACInstruction objects
        output_dir: Directory to save output files
        statistics: Optional statistics dictionary
        source_file: Optional source file name for metadata

    Returns:
        Dictionary with paths to generated files:
        {"json": Path, "markdown": Path}

    Example:
        >>> paths = save_tac_output(instructions, Path("outputs/RA4"), stats, "teste1.txt")
        >>> print(f"JSON: {paths['json']}")
        >>> print(f"Markdown: {paths['markdown']}")
    """
    # Prepare metadata
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "generator": "RA4 TAC Generator",
        "version": "1.0"
    }
    if source_file:
        metadata["source_file"] = source_file

    # Define output paths
    json_path = output_dir / "TAC.json"
    md_path = output_dir / "TAC.md"

    # Generate title for markdown
    title = "TAC Output"
    if source_file:
        title = f"TAC Output - {source_file}"

    # Save both formats
    save_json(instructions, json_path, statistics, metadata)
    save_markdown(instructions, md_path, statistics, title)

    return {
        "json": json_path,
        "markdown": md_path
    }

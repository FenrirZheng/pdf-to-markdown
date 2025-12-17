#!/usr/bin/env python3
"""
PDF to Markdown Converter (One Page = One File) with Image Extraction

Usage:
    python pdf_to_markdown.py <input.pdf> [output_dir]

Each page will be saved as a separate Markdown file:
    output_dir/filename_page_001.md
    output_dir/filename_page_002.md
    ...

Images will be extracted to:
    output_dir/images/filename_page_001_img_001.png
    output_dir/images/filename_page_001_img_002.png
    ...

If output_dir is not specified, files will be created in the same directory as the PDF.

Requirements:
    pip install pymupdf4llm
"""

import sys
import os
from pathlib import Path

try:
    import pymupdf4llm
    import pymupdf
except ImportError:
    print("Error: pymupdf4llm is not installed.")
    print("Please install it with: pip install pymupdf4llm")
    sys.exit(1)


def convert_pdf_to_markdown(pdf_path: str, output_dir: str = None) -> list:
    """
    Convert a PDF file to Markdown format, one page per file.

    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory for the output Markdown files (optional)

    Returns:
        List of paths to the created Markdown files
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_path.suffix.lower() == '.pdf':
        raise ValueError(f"File does not appear to be a PDF: {pdf_path}")

    # Determine output directory
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # Get the base name without extension
    base_name = pdf_path.stem

    # Get total page count
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)
    doc.close()

    # Create images directory
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    print(f"Converting: {pdf_path}")
    print(f"Total pages: {total_pages}")
    print(f"Output directory: {output_dir}")
    print(f"Images directory: {images_dir}")

    output_files = []

    # Convert each page separately
    for page_num in range(total_pages):
        # Convert single page to Markdown with image extraction
        markdown_text = pymupdf4llm.to_markdown(
            str(pdf_path),
            pages=[page_num],
            write_images=True,
            image_path=str(images_dir)
        )

        # Create output filename with zero-padded page number
        output_filename = f"{base_name}_page_{page_num + 1:03d}.md"
        output_path = output_dir / output_filename

        # Write to output file
        output_path.write_text(markdown_text, encoding='utf-8')
        output_files.append(str(output_path))

        print(f"  Page {page_num + 1}/{total_pages} -> {output_filename}")

    print(f"Successfully converted {total_pages} pages.")
    return output_files


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        convert_pdf_to_markdown(pdf_path, output_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

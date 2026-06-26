import subprocess
from pathlib import Path
import os

MAX_SIZE = 10 * 1024 * 1024  # 10 MB


def compress_pdf(pdf_path, max_size=MAX_SIZE, tail="_compressed"):
    """
    Nếu file >10MB thì tạo file _compressed.pdf.
    Trả về đường dẫn file sẽ dùng để upload.
    """

    if os.path.getsize(pdf_path) <= max_size:
        print(
            f"{os.path.basename(pdf_path)}: {os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB"
        )
        return pdf_path

    OUTPUT_DIR = os.path.join(os.path.dirname(pdf_path), "compressed")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    out_file = os.path.join(
        OUTPUT_DIR, os.path.basename(pdf_path).replace(".pdf", f"{tail}.pdf")
    )

    print(
        f"Compressing {os.path.basename(pdf_path)} ({os.path.getsize(pdf_path) / 1024 / 1024:.2f} MB) ..."
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    gswin64c = os.path.join(base_dir, "bin", "gswin64c.exe")

    cmd = [
        "gswin64c",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={out_file}",
        pdf_path,
    ]

    subprocess.run(cmd, check=True)
    print(
        f"After compression: {os.path.basename(out_file)} ({os.path.getsize(out_file) / 1024 / 1024:.2f} MB) ..."
    )

    return os.path.realpath(out_file)

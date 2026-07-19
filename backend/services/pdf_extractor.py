import fitz  # PyMuPDF
from fastapi import HTTPException


MIN_CHARS_PER_PAGE = 50


def extract_text_from_pdf(file_bytes: bytes, filename: str) -> list[dict]:
    """
    Extract Arabic text from a PDF file.
    Returns a list of dicts with page_number and text.
    Raises HTTPException if the PDF is image-only or has no extractable text.
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception:
        raise HTTPException(status_code=422, detail="Could not open PDF — file may be corrupted.")

    pages = []
    total_chars = 0
    total_pages = len(doc)

    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text("text").strip()
        total_chars += len(text)
        if text:
            pages.append({
                "page_number": page_num + 1,
                "text": text,
            })

    doc.close()

    if len(pages) == 0:
        raise HTTPException(
            status_code=422,
            detail="This PDF appears to be scanned — no extractable Arabic text found."
        )

    avg_chars_per_page = total_chars / total_pages
    if avg_chars_per_page < MIN_CHARS_PER_PAGE:
        raise HTTPException(
            status_code=422,
            detail=f"Very little text was extracted (avg {avg_chars_per_page:.0f} chars/page). "
                   "This PDF may be image-based or mostly scanned content."
        )

    return pages
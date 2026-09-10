"""
tests/fixtures/pdf_generator.py
Synthetic PDF generator utility for opaque-box preflight and layout test verification.
Uses PyMuPDF (fitz), PIL, and NumPy to produce calibrated test fixtures.
"""

import os
import io
import math
import fitz
import numpy as np
from PIL import Image

MM_TO_PT = 72.0 / 25.4

def create_synthetic_pdf(
    output_path: str,
    page_count: int = 2,
    width_pt: float = 841.89,  # A4 Landscape width
    height_pt: float = 595.28, # A4 Landscape height
    bleed_mm: float = 3.0,
    safety_margin_mm: float = 5.0,
    add_safety_breach: bool = False,
    effective_dpi: float = 300.0,
    tac_percentage: float = 280.0,
    is_cmyk: bool = True,
    add_pdfx4: bool = True,
    add_text_collision: bool = False,
    font_name: str = "ABCDEF+SpaceGrotesk-Regular",
    is_subset: bool = True,
    is_type3: bool = False
) -> str:
    """
    Creates a precisely calibrated synthetic PDF for testing preflight validation.
    """
    doc = fitz.open()
    bleed_pt = bleed_mm * MM_TO_PT
    safety_pt = safety_margin_mm * MM_TO_PT
    for p in range(page_count):
        # Prepress sheet: MediaBox encloses BleedBox, which encloses TrimBox
        sheet_margin = 15.0 # pt border for slug / trim marks
        media_w = width_pt + 2 * bleed_pt + 2 * sheet_margin
        media_h = height_pt + 2 * bleed_pt + 2 * sheet_margin
        media_rect = fitz.Rect(0, 0, media_w, media_h)
        bleed_rect = fitz.Rect(sheet_margin, sheet_margin, sheet_margin + width_pt + 2 * bleed_pt, sheet_margin + height_pt + 2 * bleed_pt)
        trim_rect = fitz.Rect(sheet_margin + bleed_pt, sheet_margin + bleed_pt, sheet_margin + bleed_pt + width_pt, sheet_margin + bleed_pt + height_pt)

        page = doc.new_page(width=media_w, height=media_h)
        page.set_mediabox(media_rect)
        page.set_bleedbox(bleed_rect)
        page.set_trimbox(trim_rect)

        # Standard safe text block
        text_x = trim_rect.x0 + safety_pt + 20
        text_y = trim_rect.y0 + safety_pt + 30
        page.insert_text(
            fitz.Point(text_x, text_y),
            f"Page {p+1}: Architectural Monograph Test Layout",
            fontsize=12
        )

        # Optional safety zone breach
        if add_safety_breach and p == 0:
            # Place text 1mm inside trim box (breaching the 5mm safety zone)
            breach_x = trim_rect.x0 + (1.0 * MM_TO_PT)
            breach_y = trim_rect.y0 + (1.0 * MM_TO_PT) + 10
            page.insert_text(
                fitz.Point(breach_x, breach_y),
                "CRITICAL_SAFETY_BREACH_TEXT",
                fontsize=9
            )

        # Add raster image if specified
        if effective_dpi > 0:
            # Desired printed box in points
            box_w_pt = 200.0
            box_h_pt = 150.0
            img_x = trim_rect.x0 + 40
            img_y = trim_rect.y0 + 100

            # Compute pixel dimensions needed for requested effective DPI
            px_w = int(round((box_w_pt / 72.0) * effective_dpi))
            px_h = int(round((box_h_pt / 72.0) * effective_dpi))
            px_w = max(px_w, 10)
            px_h = max(px_h, 10)

            if is_cmyk:
                # CMYK image with specified TAC
                # TAC = C + M + Y + K as percentage (0 - 400%)
                # Distribute TAC across channels:
                k_frac = min(tac_percentage / 400.0, 1.0)
                channel_val = int(round((tac_percentage / 4.0 / 100.0) * 255.0))
                channel_val = min(max(channel_val, 0), 255)
                
                cmyk_arr = np.full((px_h, px_w, 4), channel_val, dtype=np.uint8)
                pil_img = Image.fromarray(cmyk_arr, mode="CMYK")
                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG")
                img_bytes = buf.getvalue()
            else:
                # RGB image
                rgb_arr = np.full((px_h, px_w, 3), 128, dtype=np.uint8)
                pil_img = Image.fromarray(rgb_arr, mode="RGB")
                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG")
                img_bytes = buf.getvalue()

            img_rect = fitz.Rect(img_x, img_y, img_x + box_w_pt, img_y + box_h_pt)
            page.insert_image(img_rect, stream=img_bytes)

            # Optional text collision over the image
            if add_text_collision and p == 0:
                # Text directly overlapping image with low contrast
                col_text_x = img_x + 20
                col_text_y = img_y + 40
                page.insert_text(
                    fitz.Point(col_text_x, col_text_y),
                    "COLLIDING_CAPTION_TEXT",
                    fontsize=10,
                    color=(0.5, 0.5, 0.5) # Grey on grey
                )

    # Ensure fonts adhere to subset/embedding requirements
    if is_subset:
        font_key = font_name.split("+")[-1].replace("-", "")
        # Rename font key in resources and content streams to prevent collision on subsequent insert_text calls
        for i in range(1, doc.xref_length()):
            obj_str = doc.xref_object(i)
            if "/Font" in obj_str and "/helv" in obj_str:
                doc.update_object(i, obj_str.replace("/helv", f"/{font_key}"))
            if doc.xref_is_stream(i):
                stream_bytes = doc.xref_stream(i)
                if stream_bytes and b"/helv" in stream_bytes:
                    doc.update_stream(i, stream_bytes.replace(b"/helv", f"/{font_key}".encode("latin1")))

        for p_idx in range(len(doc)):
            for f in doc[p_idx].get_fonts(full=True):
                xref = f[0]
                doc.update_object(
                    xref,
                    f"<< /Type /Font /Subtype /Type1 /BaseFont /{font_name} /Encoding /WinAnsiEncoding >>"
                )
    elif is_type3:
        for p_idx in range(len(doc)):
            for f in doc[p_idx].get_fonts(full=True):
                xref = f[0]
                doc.update_object(
                    xref,
                    "<< /Type /Font /Subtype /Type3 /BaseFont /ForbiddenType3 /Encoding /WinAnsiEncoding >>"
                )


    # Save PDF
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    doc.close()

    return output_path


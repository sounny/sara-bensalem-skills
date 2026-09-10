import os, io, fitz, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

os.makedirs("tmp_test", exist_ok=True)
img_w, img_h = 1200, 800
cmyk_arr = np.full((img_h, img_w, 4), 60, dtype=np.uint8)
pil_img = Image.fromarray(cmyk_arr, mode="CMYK")
img_path = os.path.abspath("tmp_test/test_cmyk.jpg")
pil_img.save(img_path, format="JPEG", dpi=(300, 300))

html_path = os.path.abspath("tmp_test/test_cmyk.html")
html = f"""<!DOCTYPE html>
<html>
<head>
<style>
@page {{ size: 297mm 210mm; margin: 20mm; }}
body {{ font-family: Arial, sans-serif; }}
img {{ width: 100mm; }}
</style>
</head>
<body>
<h1>CMYK Image Test</h1>
<img src="{img_path.replace('\\', '/')}">
</body>
</html>"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(f"file:///{html_path.replace('\\', '/')}")
    pg.pdf(path="tmp_test/test_cmyk.pdf", prefer_css_page_size=True)
    b.close()

doc = fitz.open("tmp_test/test_cmyk.pdf")
print("Images in doc:", len(doc[0].get_images()))
for img_info in doc[0].get_images():
    xref = img_info[0]
    pix = fitz.Pixmap(doc, xref)
    print("Pixmap colorspace:", pix.colorspace.n, pix.colorspace.name)
doc.close()

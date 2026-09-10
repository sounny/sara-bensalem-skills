import os
from playwright.sync_api import sync_playwright

html_path = os.path.abspath("tmp_test/test_10p.html")
vendor_js = os.path.abspath("engine/pagedjs/vendor/paged.polyfill.js")

html = f"""<!DOCTYPE html>
<html>
<head>
<style>
@page {{
  size: 297mm 210mm;
  marks: crop cross;
  bleed: 3.0mm;
  margin: 20mm;
}}
.page {{
  page-break-after: always;
  break-after: page;
}}
h1 {{ font-family: Arial, sans-serif; }}
p {{ font-family: Garamond, serif; }}
</style>
<script>
window.PagedConfig = {{
  auto: true,
  after: function(flow) {{
    window.__PAGEDJS_RENDERED__ = true;
    document.body.setAttribute("data-pagedjs-rendered", "true");
    console.log("PAGED FLOW TOTAL:", flow.total);
  }}
}};
</script>
<script src="{vendor_js.replace('\\', '/')}"></script>
</head>
<body>
"""

for i in range(1, 11):
    html += f"""<div class="page">
<h1>Page {i}</h1>
<p>Content for page {i}.</p>
</div>
"""
html += "</body></html>"

with open("tmp_test/test_debug.html", "w", encoding="utf-8") as f:
    f.write(html)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.on("console", lambda msg: print("CONSOLE:", msg.text))
    pg.goto(f"file:///{os.path.abspath('tmp_test/test_debug.html').replace('\\', '/')}")
    pg.wait_for_function("window.__PAGEDJS_RENDERED__ === true", timeout=10000)
    page_count = pg.evaluate("() => document.querySelectorAll('.pagedjs_page').length")
    print("PAGE COUNT IN DOM:", page_count)
    pg.pdf(path="tmp_test/test_debug.pdf", prefer_css_page_size=True)
    b.close()

import fitz
doc = fitz.open("tmp_test/test_debug.pdf")
print("PDF PAGE COUNT:", len(doc))

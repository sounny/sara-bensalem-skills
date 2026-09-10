import os
from engine.compile import compile_document
from preflight.audit_publication import audit_pdf

html_test = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sara Bensalem: The Tectonic Rescue</title>
<style>
@page {
  size: 297mm 210mm;
  marks: crop cross;
  bleed: 3.0mm;
}
@page :left {
  margin-left: 15.0mm;
  margin-right: 25.0mm;
  margin-top: 20mm;
  margin-bottom: 20mm;
  @bottom-left {
    content: counter(page);
    font-family: Consolas, monospace;
    font-size: 8pt;
  }
  @top-left {
    content: "SARA BENSALEM MONOGRAPH";
    font-family: Consolas, monospace;
    font-size: 7.5pt;
  }
}
@page :right {
  margin-left: 25.0mm;
  margin-right: 15.0mm;
  margin-top: 20mm;
  margin-bottom: 20mm;
  @bottom-right {
    content: counter(page);
    font-family: Consolas, monospace;
    font-size: 8pt;
  }
  @top-right {
    content: "ACT 4: TECTONIC PROOF";
    font-family: Consolas, monospace;
    font-size: 7.5pt;
  }
}
@page :first {
  marks: none;
  bleed: 0mm;
  @top-left { content: none; }
  @bottom-left { content: none; }
  @top-right { content: none; }
  @bottom-right { content: none; }
}
body {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 9pt;
  line-height: 12pt;
  margin: 0;
  padding: 0;
}
.page {
  page-break-after: always;
  break-after: page;
  height: 100%;
}
h1 { font-family: Arial, Helvetica, sans-serif; font-size: 18pt; margin: 0 0 12pt 0; }
p { font-family: Garamond, Georgia, serif; font-size: 9pt; }
</style>
<script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
<script>
window.PagedConfig = {
  auto: true,
  after: function(flow) {
    window.__PAGEDJS_RENDERED__ = true;
    document.body.setAttribute("data-pagedjs-rendered", "true");
  }
};
</script>
</head>
<body>
"""

for i in range(1, 11):
    html_test += f"""<section class="page">
<h1>Page {i}: Act Header</h1>
<p>This is page {i} of the 10-page demonstration architectural monograph.</p>
</section>
"""

html_test += """</body></html>"""

os.makedirs("tmp_test", exist_ok=True)
with open("tmp_test/test_10p.html", "w", encoding="utf-8") as f:
    f.write(html_test)

res = compile_document(
    input_path="tmp_test/test_10p.html",
    output_path="tmp_test/test_10p.pdf",
    engine="pagedjs",
    benchmark=True
)
print("Compile result:", res)

audit_res = audit_pdf("tmp_test/test_10p.pdf")
print("Audit status:", audit_res["status"])
print("Scorecard:", audit_res["scorecard"])
for k, v in audit_res["checks"].items():
    print(f"  {k}: {v['status']}")

import os
from playwright.sync_api import sync_playwright
from PIL import Image

web_dir = os.path.dirname(os.path.abspath(__file__))

# Design the SVG with exact site colors:
# Background: Studio Graphite (#161615)
# Accent / Subtle Specular: #333330 and #DDD9D0
# Text: Archival Swiss Bone (#F8F8F5)
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@900&amp;family=Space+Grotesk:wght@900&amp;display=swap');
      .sb-text {
        font-family: 'Space Grotesk', 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-weight: 900;
        font-size: 265px;
        fill: #F8F8F5;
        letter-spacing: -14px;
      }
    </style>
  </defs>

  <!-- Studio Graphite Background (#161615) with squircle curvature (rx=116) -->
  <rect width="512" height="512" rx="116" fill="#161615"/>
  
  <!-- Architectural Subtle Specular Border -->
  <rect x="12" y="12" width="488" height="488" rx="104" fill="none" stroke="#2D2D29" stroke-width="10"/>
  <rect x="22" y="22" width="468" height="468" rx="94" fill="none" stroke="#DDD9D0" stroke-opacity="0.16" stroke-width="2" stroke-dasharray="12 12"/>

  <!-- Centered "SB" in Archival Swiss Bone (#F8F8F5) -->
  <text x="250" y="348" text-anchor="middle" class="sb-text">SB</text>
</svg>"""

svg_path = os.path.join(web_dir, "favicon.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write(svg_content)
print(f"[+] Wrote {svg_path}")

# Render 512x512 PNG using Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 512, "height": 512})
    html_page = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>body{{margin:0;padding:0;background:transparent;overflow:hidden;}}</style></head>
<body>{svg_content}</body>
</html>"""
    page.set_content(html_page)
    page.wait_for_timeout(1000)
    png_512_path = os.path.join(web_dir, "favicon-512x512.png")
    page.screenshot(path=png_512_path, omit_background=True)
    browser.close()
print(f"[+] Rendered high-res {png_512_path}")

# Generate multi-size icons using Pillow
img = Image.open(png_512_path)

# Apple Touch Icon (180x180)
img_180 = img.resize((180, 180), Image.Resampling.LANCZOS)
img_180.save(os.path.join(web_dir, "apple-touch-icon.png"))
print("[+] Generated apple-touch-icon.png (180x180)")

# Favicon 32x32
img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
img_32.save(os.path.join(web_dir, "favicon-32x32.png"))
print("[+] Generated favicon-32x32.png (32x32)")

# Favicon 16x16
img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
img_16.save(os.path.join(web_dir, "favicon-16x16.png"))
print("[+] Generated favicon-16x16.png (16x16)")

# Favicon 192x192 (Android / PWA)
img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
img_192.save(os.path.join(web_dir, "favicon-192x192.png"))
print("[+] Generated favicon-192x192.png (192x192)")

# Multi-resolution ICO (16, 32, 48)
img_48 = img.resize((48, 48), Image.Resampling.LANCZOS)
ico_path = os.path.join(web_dir, "favicon.ico")
img_48.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
print(f"[+] Generated multi-resolution {ico_path}")

# Write site.webmanifest
manifest_content = """{
  "name": "Sara Bensalem Skills",
  "short_name": "SB Skills",
  "icons": [
    {
      "src": "/favicon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/favicon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#161615",
  "background_color": "#F8F8F5",
  "display": "standalone"
}"""
with open(os.path.join(web_dir, "site.webmanifest"), "w", encoding="utf-8") as f:
    f.write(manifest_content)
print("[+] Generated site.webmanifest")

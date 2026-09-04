// Spatial Stitch — Minimalist Skill Download & Preview Engine

const MCP_SNIPPETS = {
  claude: `{
  "mcpServers": {
    "spatial-stitch": {
      "command": "python",
      "args": ["path/to/spatial-stitch/engine/server.py"]
    }
  }
}`,
  cursor: `{
  "mcpServers": {
    "spatial-stitch": {
      "command": "python",
      "args": ["path/to/spatial-stitch/engine/server.py"]
    }
  }
}`,
  antigravity: `# Antigravity Native Skill:
# Placed in ~/.gemini/config/skills/spatial-stitch/
# Activate in chat with:
/spatial-stitch generate spread for 1:20 wall section`,
  cli: `# Run stdio JSON-RPC server directly:
git clone https://github.com/sounny/sara-bensalem-skills.git
cd sara-bensalem-skills/spatial-stitch
python -m engine.server`
};

const SAMPLE_SPREAD_SVG = `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FBFBF8; font-family:Inter, sans-serif;">
  <!-- Grid Layer -->
  <g id="preview-grid-cols" opacity="0.35">
    <rect x="64" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="212" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="360" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="508" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="656" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="804" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="952" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="1100" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="1248" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="1396" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="1544" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
    <rect x="1692" y="64" width="124" height="952" fill="#E6E2DA" fill-opacity="0.25" stroke="#E6E2DA" stroke-dasharray="2 4" />
  </g>
  <g id="preview-grid-margins">
    <rect x="64" y="64" width="1792" height="952" fill="none" stroke="#FFAF01" stroke-width="1" stroke-opacity="0.4" />
    <circle cx="64" cy="64" r="3" fill="#FFAF01" />
    <circle cx="1856" cy="64" r="3" fill="#FFAF01" />
    <circle cx="64" cy="1016" r="3" fill="#FFAF01" />
    <circle cx="1856" cy="1016" r="3" fill="#FFAF01" />
  </g>

  <!-- Folio Header -->
  <text x="64" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470" letter-spacing="1">PROJECT MONOGRAPH: MAISON BRETONNE ADAPTIVE REUSE</text>
  <text x="1856" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#FFAF01" font-weight="700" text-anchor="end">ACT 4 // CONSTRUCTIVE PROOF (1:20)</text>
  <line x1="64" y1="64" x2="1856" y2="64" stroke="#E6E2DA" stroke-width="1" />

  <!-- Left Technical Column: Material Callouts -->
  <g transform="translate(64, 120)">
    <text x="0" y="28" font-size="24" font-weight="800" fill="#090B0E">1:20 Wall Section Detail</text>
    <text x="0" y="52" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">SCALE 1:20 @ A3 // DIMENSIONS IN MM // PMR CLEARANCES</text>

    <g transform="translate(0, 84)">
      <rect x="0" y="0" width="24" height="24" fill="#FFAF01" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FBFBF8" text-anchor="middle">01</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#090B0E">Breton Granite Ashlar (180mm)</text>
      <text x="36" y="28" font-size="11" fill="#5C6470">Consolidated lime mortar joints, exterior breathability</text>
    </g>

    <g transform="translate(0, 144)">
      <rect x="0" y="0" width="24" height="24" fill="#090B0E" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FBFBF8" text-anchor="middle">02</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#090B0E">Lime-Hemp Biotamping (140mm)</text>
      <text x="36" y="28" font-size="11" fill="#5C6470">Hygrothermal monolithic insulation, λ = 0.076 W/m·K</text>
    </g>

    <g transform="translate(0, 204)">
      <rect x="0" y="0" width="24" height="24" fill="#002B49" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FBFBF8" text-anchor="middle">03</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#090B0E">Thermal Break & EPDM Flashing</text>
      <text x="36" y="28" font-size="11" fill="#5C6470">Continuous capillary moisture seal at plinth threshold</text>
    </g>

    <g transform="translate(0, 264)">
      <rect x="0" y="0" width="24" height="24" fill="#090B0E" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FBFBF8" text-anchor="middle">04</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#090B0E">Oak Glulam Post & Beam (160x280)</text>
      <text x="36" y="28" font-size="11" fill="#5C6470">Concealed steel plate flitch connector w/ dowels</text>
    </g>

    <g transform="translate(0, 680)">
      <rect x="0" y="0" width="560" height="120" fill="#E6E2DA" fill-opacity="0.35" stroke="#E6E2DA" />
      <text x="16" y="28" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FFAF01">CONSTRUCTIVE PROOF GUARANTEE</text>
      <text x="16" y="48" font-size="12" fill="#090B0E">Individual Line-Item Work: Envelope detailing &</text>
      <text x="16" y="66" font-size="12" fill="#090B0E">construction administration documentation.</text>
      <text x="16" y="94" font-family="'IBM Plex Mono', monospace" font-size="10" fill="#5C6470">ANTI-RENDER-TRAP COMPLIANT • 100% BUILDABLE</text>
    </g>
  </g>

  <!-- Right Technical Canvas: 1:20 Detailing -->
  <g transform="translate(680, 120)">
    <rect x="0" y="0" width="1176" height="820" fill="#FFFFFF" stroke="#E6E2DA" stroke-width="1" />
    <rect x="180" y="520" width="860" height="130" fill="#EAE6DF" stroke="#090B0E" stroke-width="2.5" />
    <line x1="190" y1="560" x2="1030" y2="560" stroke="#5C6470" stroke-width="1" stroke-dasharray="8 6" />
    <line x1="190" y1="620" x2="1030" y2="620" stroke="#5C6470" stroke-width="1" stroke-dasharray="8 6" />

    <rect x="180" y="40" width="180" height="480" fill="#DFD9D0" stroke="#090B0E" stroke-width="2.5" />
    <line x1="180" y1="120" x2="360" y2="120" stroke="#090B0E" stroke-width="1" />
    <line x1="180" y1="200" x2="360" y2="200" stroke="#090B0E" stroke-width="1" />
    <line x1="180" y1="280" x2="360" y2="280" stroke="#090B0E" stroke-width="1" />
    <line x1="180" y1="360" x2="360" y2="360" stroke="#090B0E" stroke-width="1" />
    <line x1="180" y1="440" x2="360" y2="440" stroke="#090B0E" stroke-width="1" />

    <rect x="360" y="40" width="120" height="480" fill="#F4EFE6" stroke="#090B0E" stroke-width="1.5" stroke-dasharray="4 2" />
    <rect x="480" y="40" width="20" height="480" fill="#FBFBF8" stroke="#090B0E" stroke-width="1" />

    <rect x="500" y="160" width="540" height="260" fill="#E8F1F5" fill-opacity="0.4" stroke="#002B49" stroke-width="2" />
    <line x1="500" y1="290" x2="1040" y2="290" stroke="#002B49" stroke-width="2" />
    <text x="770" y="278" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#002B49" text-anchor="middle">TRIPLE GLAZED TIMBER-ALU ENVELOPE // Uw = 0.78 W/m²K</text>

    <!-- Dimension Strings -->
    <g stroke="#FFAF01" stroke-width="1.5">
      <line x1="120" y1="40" x2="120" y2="520" />
      <line x1="108" y1="40" x2="132" y2="40" />
      <line x1="108" y1="520" x2="132" y2="520" />
      <line x1="112" y1="44" x2="128" y2="36" stroke-width="2.5" />
      <line x1="112" y1="524" x2="128" y2="516" stroke-width="2.5" />
    </g>
    <text x="100" y="290" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="bold" fill="#FFAF01" text-anchor="middle" transform="rotate(-90 100 290)">4800 MM CLEARANCE</text>

    <g stroke="#FFAF01" stroke-width="1.5">
      <line x1="180" y1="18" x2="500" y2="18" />
      <line x1="180" y1="8" x2="180" y2="28" />
      <line x1="500" y1="8" x2="500" y2="28" />
      <line x1="176" y1="22" x2="184" y2="14" stroke-width="2.5" />
      <line x1="496" y1="22" x2="504" y2="14" stroke-width="2.5" />
    </g>
    <text x="340" y="12" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#FFAF01" text-anchor="middle">320 MM COMPOSITE ENVELOPE</text>
  </g>

  <!-- Folio Footer -->
  <line x1="64" y1="1008" x2="1856" y2="1008" stroke="#E6E2DA" stroke-width="1" />
  <text x="64" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">LEAD ARCHITECT: SARA BENSALEM • 48°51'24"N 02°21'07"E</text>
  <text x="960" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470" text-anchor="middle">WORK RIGHTS: EU CITIZEN // ZERO VISA SPONSORSHIP REQUIRED</text>
  <text x="1856" y="1034" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#090B0E" text-anchor="end">SPREAD 04</text>
</svg>`;

document.addEventListener('DOMContentLoaded', () => {
  // 1. Theme toggle
  const themeBtn = document.getElementById('theme-toggle-btn');
  if (themeBtn) {
    if (localStorage.getItem('sara_theme') === 'light') {
      document.documentElement.classList.add('light');
    }
    themeBtn.addEventListener('click', () => {
      document.documentElement.classList.toggle('light');
      const isLight = document.documentElement.classList.contains('light');
      localStorage.setItem('sara_theme', isLight ? 'light' : 'dark');
      if (window.lucide) lucide.createIcons();
    });
  }

  // 2. Install Snippets Tabs
  const codeEl = document.getElementById('code-display');
  const copyBtn = document.getElementById('copy-snippet-btn');
  const copyLabel = document.getElementById('copy-label');
  const tabs = document.querySelectorAll('.install-tab');

  function setSnippet(key) {
    if (!codeEl) return;
    codeEl.textContent = MCP_SNIPPETS[key] || MCP_SNIPPETS.claude;
  }
  setSnippet('claude');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => {
        t.className = "install-tab px-3 py-1.5 rounded-lg bg-dark-800 text-slate-400 hover:text-white transition";
      });
      tab.className = "install-tab active px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 font-bold transition";
      setSnippet(tab.getAttribute('data-target'));
    });
  });

  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      if (!codeEl) return;
      navigator.clipboard.writeText(codeEl.textContent).then(() => {
        copyLabel.textContent = "Copied!";
        copyBtn.className = "px-4 py-2 rounded-lg bg-emerald-500 text-slate-950 font-mono font-bold text-xs transition flex items-center gap-2 self-start sm:self-auto";
        setTimeout(() => {
          copyLabel.textContent = "Copy Snippet";
          copyBtn.className = "px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-mono font-bold text-xs transition flex items-center gap-2 self-start sm:self-auto";
        }, 2000);
      });
    });
  }

  // 3. Spread Preview & Grid Toggle
  const canvas = document.getElementById('preview-canvas');
  const toggleGridBtn = document.getElementById('toggle-grid-btn');
  const downloadSvgBtn = document.getElementById('download-svg-btn');
  let gridVisible = true;

  if (canvas) {
    canvas.innerHTML = SAMPLE_SPREAD_SVG;
  }

  if (toggleGridBtn) {
    toggleGridBtn.addEventListener('click', () => {
      gridVisible = !gridVisible;
      const cols = canvas.querySelector('#preview-grid-cols');
      const margins = canvas.querySelector('#preview-grid-margins');
      if (cols) cols.style.display = gridVisible ? 'block' : 'none';
      if (margins) margins.style.display = gridVisible ? 'block' : 'none';
      const label = document.getElementById('grid-btn-label');
      if (label) label.textContent = gridVisible ? "Hide Swiss Grid" : "Show Swiss Grid";
    });
  }

  if (downloadSvgBtn) {
    downloadSvgBtn.addEventListener('click', () => {
      const blob = new Blob([SAMPLE_SPREAD_SVG], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "spatial_stitch_1_20_wall_section.svg";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  if (window.lucide) {
    lucide.createIcons();
  }
});

// Sara Bensalem Skills — Minimalist Studio Monochrome Engine & Interactive Canvas

const MCP_SNIPPETS = {
  claude: `{
  "mcpServers": {
    "sara-bensalem-skills": {
      "command": "python",
      "args": ["path/to/sara-bensalem-skills/mcp-server/server.py"]
    }
  }
}`,
  cursor: `{
  "mcpServers": {
    "sara-bensalem-skills": {
      "command": "python",
      "args": ["path/to/sara-bensalem-skills/mcp-server/server.py"]
    }
  }
}`,
  antigravity: `# Native Antigravity / Cursor Skills:
# 1. Monograph & 1:20 Spreads:
/portfolio-design generate spread for 1:20 wall section

# 2. Socratic Architectural Crit:
/grill-my-design audit my project against 1:20 constructibility`,
  cli: `# Run stdio JSON-RPC server directly:
git clone https://github.com/sounny/sara-bensalem-skills.git
cd sara-bensalem-skills
python mcp-server/server.py`
};

// Specifications for Tectonic Assemblies
const TECTONIC_SPECS = {
  all: {
    title: "Complete 1:20 Wall Envelope Assembly",
    thickness: "Total Envelope: 340 mm",
    lambda: "Composite Assembly",
    uvalue: "0.18 W/m²K (Passivhaus Standard)",
    acoustic: "54 dB (Flanking Protected)",
    carbon: "-32 kgCO₂e/m² (Net Carbon Sink)",
    vapor: "Vapor Open (Breathable μ = 5-10)"
  },
  granite: {
    title: "01 Breton Granite Ashlar",
    thickness: "Thickness: 180 mm",
    lambda: "2.10 W/m·K (High Thermal Mass)",
    uvalue: "Exterior Rainscreen & Weather Barrier",
    acoustic: "48 dB Airborne Attenuation",
    carbon: "12 kgCO₂e/m² (Local Quarry Provenance)",
    vapor: "Vapor Open Mortar Joints (Lime NHL 3.5)"
  },
  hemp: {
    title: "02 Lime-Hemp Biotamping",
    thickness: "Thickness: 140 mm",
    lambda: "0.076 W/m·K (Hygrothermal Monolith)",
    uvalue: "0.22 W/m²K (Core Insulation)",
    acoustic: "44 dB Absorption Coefficient",
    carbon: "-45 kgCO₂e/m² (Carbon Negative)",
    vapor: "Breathable Capillary Active (μ = 5.0)"
  },
  break: {
    title: "03 Thermal Break & EPDM Flashing",
    thickness: "Thickness: 20 mm Continuous Barrier",
    lambda: "0.031 W/m·K (Structural Thermal Decoupler)",
    uvalue: "Eliminates Cantilever Thermal Bridging",
    acoustic: "Vibration Isolating Decoupler",
    carbon: "4 kgCO₂e/m² (Recycled EPDM Polymer)",
    vapor: "Airtight Capillary Barrier (Sd >= 1500m)"
  },
  timber: {
    title: "04 Oak Glulam Post & Beam",
    thickness: "Dimensions: 160 mm x 280 mm",
    lambda: "0.13 W/m·K (Mass Timber Structure)",
    uvalue: "Structural Frame & Lintels",
    acoustic: "Low Resonant Flanking Transfer",
    carbon: "-68 kgCO₂e/m³ (PEFC Certified French Oak)",
    vapor: "Hygroscopic Moisture Buffering"
  },
  glazing: {
    title: "05 Triple Glazed Timber-Alu Envelope",
    thickness: "Thickness: 48 mm (4-18-4-18-4 Argon)",
    lambda: "Uw = 0.78 W/m²K (Triple Low-E)",
    uvalue: "g = 0.52 (Optimal Passive Solar Gain)",
    acoustic: "Rw = 42 dB Acoustic Laminated",
    carbon: "18 kgCO₂e/m²",
    vapor: "Continuous Warm-Edge Perimeter Seal"
  }
};

// Generates SVG Monograph Spreads with Dynamic Swiss Columns
function generateSpreadSVG(cols = 12) {
  let gridRects = '';
  const totalWidth = 1792;
  const startX = 64;
  const colWidth = (totalWidth - (cols - 1) * 16) / cols;

  for (let i = 0; i < cols; i++) {
    const x = startX + i * (colWidth + 16);
    gridRects += `<rect x="${x.toFixed(1)}" y="64" width="${colWidth.toFixed(1)}" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
`;
  }

  return `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FFFFFF; font-family:Inter, sans-serif;">
  <!-- Grid Layer (Architectural Drafting Hairlines) -->
  <g id="preview-grid-cols" opacity="0.45">
    ${gridRects}
  </g>
  <g id="preview-grid-margins">
    <rect x="64" y="64" width="1792" height="952" fill="none" stroke="#111110" stroke-width="1" stroke-opacity="0.25" />
    <circle cx="64" cy="64" r="2.5" fill="#111110" />
    <circle cx="1856" cy="64" r="2.5" fill="#111110" />
    <circle cx="64" cy="1016" r="2.5" fill="#111110" />
    <circle cx="1856" cy="1016" r="2.5" fill="#111110" />
  </g>

  <!-- Folio Header -->
  <text x="64" y="48" font-family="'JetBrains Mono', monospace" font-size="11" fill="#55544E" letter-spacing="1">PROJECT MONOGRAPH: MAISON BRETONNE ADAPTIVE REUSE</text>
  <text x="1856" y="48" font-family="'JetBrains Mono', monospace" font-size="11" fill="#111110" font-weight="700" text-anchor="end">ACT 4 // CONSTRUCTIVE PROOF (1:20)</text>
  <line x1="64" y1="64" x2="1856" y2="64" stroke="#E8E5DC" stroke-width="1" />

  <!-- Left Technical Column: Material Callouts -->
  <g transform="translate(64, 120)">
    <text x="0" y="28" font-size="24" font-weight="800" fill="#111110">1:20 Wall Section Detail</text>
    <text x="0" y="52" font-family="'JetBrains Mono', monospace" font-size="11" fill="#55544E">SCALE 1:20 @ A3 // DIMENSIONS IN MM // STRASBOURG ATELIER</text>

    <!-- Callout 01 -->
    <g class="tectonic-callout" data-layer="granite" transform="translate(0, 84)" cursor="pointer">
      <rect x="0" y="0" width="24" height="24" fill="#111110" />
      <text x="12" y="16" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">01</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Breton Granite Ashlar (180mm)</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Consolidated lime mortar joints, exterior breathability</text>
    </g>

    <!-- Callout 02 -->
    <g class="tectonic-callout" data-layer="hemp" transform="translate(0, 144)" cursor="pointer">
      <rect x="0" y="0" width="24" height="24" fill="#55544E" />
      <text x="12" y="16" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">02</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Lime-Hemp Biotamping (140mm)</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Hygrothermal monolithic insulation, λ = 0.076 W/m·K</text>
    </g>

    <!-- Callout 03 -->
    <g class="tectonic-callout" data-layer="break" transform="translate(0, 204)" cursor="pointer">
      <rect x="0" y="0" width="24" height="24" fill="#111110" />
      <text x="12" y="16" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">03</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Thermal Break & EPDM Flashing</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Continuous capillary moisture seal at plinth threshold</text>
    </g>

    <!-- Callout 04 -->
    <g class="tectonic-callout" data-layer="timber" transform="translate(0, 264)" cursor="pointer">
      <rect x="0" y="0" width="24" height="24" fill="#55544E" />
      <text x="12" y="16" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">04</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Oak Glulam Post & Beam (160x280)</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Concealed steel plate flitch connector w/ dowels</text>
    </g>

    <g transform="translate(0, 680)">
      <rect x="0" y="0" width="560" height="120" fill="#F8F8F5" stroke="#E8E5DC" />
      <text x="16" y="28" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="bold" fill="#111110">CONSTRUCTIVE PROOF GUARANTEE</text>
      <text x="16" y="48" font-size="12" fill="#111110">Individual Line-Item Work: Envelope detailing &</text>
      <text x="16" y="66" font-size="12" fill="#111110">construction administration documentation.</text>
      <text x="16" y="94" font-family="'JetBrains Mono', monospace" font-size="10" fill="#55544E">ANTI-RENDER-TRAP COMPLIANT • 100% BUILDABLE</text>
    </g>
  </g>

  <!-- Right Technical Canvas: 1:20 Detailing -->
  <g transform="translate(680, 120)">
    <rect x="0" y="0" width="1176" height="820" fill="#FFFFFF" stroke="#E8E5DC" stroke-width="1" />
    
    <!-- Floor Slab & Foundation Plinth -->
    <rect id="layer-slab" class="tectonic-layer" x="180" y="520" width="860" height="130" fill="#F4F4F0" stroke="#111110" stroke-width="2" />
    <line x1="190" y1="560" x2="1030" y2="560" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />
    <line x1="190" y1="620" x2="1030" y2="620" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />

    <!-- 01 Breton Granite Ashlar -->
    <g id="layer-granite" class="tectonic-layer">
      <rect x="180" y="40" width="180" height="480" fill="#EAEAE5" stroke="#111110" stroke-width="2" />
      <line x1="180" y1="120" x2="360" y2="120" stroke="#111110" stroke-width="1" />
      <line x1="180" y1="200" x2="360" y2="200" stroke="#111110" stroke-width="1" />
      <line x1="180" y1="280" x2="360" y2="280" stroke="#111110" stroke-width="1" />
      <line x1="180" y1="360" x2="360" y2="360" stroke="#111110" stroke-width="1" />
      <line x1="180" y1="440" x2="360" y2="440" stroke="#111110" stroke-width="1" />
    </g>

    <!-- 02 Lime-Hemp Biotamping -->
    <g id="layer-hemp" class="tectonic-layer">
      <rect x="360" y="40" width="120" height="480" fill="#F8F8F5" stroke="#111110" stroke-width="1.5" stroke-dasharray="4 2" />
    </g>

    <!-- 03 Thermal Break & EPDM -->
    <g id="layer-break" class="tectonic-layer">
      <rect x="480" y="40" width="20" height="480" fill="#DDD9D0" stroke="#111110" stroke-width="1.5" />
      <line x1="480" y1="520" x2="500" y2="520" stroke="#111110" stroke-width="3" />
    </g>

    <!-- 04 Oak Glulam Framing -->
    <g id="layer-timber" class="tectonic-layer">
      <rect x="500" y="40" width="140" height="480" fill="#F3F0E8" stroke="#111110" stroke-width="2" />
      <line x1="500" y1="40" x2="640" y2="520" stroke="#DDD9D0" stroke-width="1" />
      <line x1="640" y1="40" x2="500" y2="520" stroke="#DDD9D0" stroke-width="1" />
    </g>

    <!-- 05 Triple Glazed Timber-Alu Envelope -->
    <g id="layer-glazing" class="tectonic-layer">
      <rect x="640" y="160" width="400" height="260" fill="#F8F8F5" stroke="#111110" stroke-width="2" />
      <line x1="640" y1="290" x2="1040" y2="290" stroke="#111110" stroke-width="1.5" />
      <text x="840" y="278" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="bold" fill="#111110" text-anchor="middle">TRIPLE GLAZED TIMBER-ALU // Uw = 0.78 W/m²K</text>
    </g>

    <!-- Dimension Strings -->
    <g stroke="#111110" stroke-width="1.25">
      <line x1="120" y1="40" x2="120" y2="520" />
      <line x1="108" y1="40" x2="132" y2="40" />
      <line x1="108" y1="520" x2="132" y2="520" />
      <line x1="112" y1="44" x2="128" y2="36" stroke-width="2" />
      <line x1="112" y1="524" x2="128" y2="516" stroke-width="2" />
    </g>
    <text x="100" y="290" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="bold" fill="#111110" text-anchor="middle" transform="rotate(-90 100 290)">4800 MM CLEARANCE</text>

    <g stroke="#111110" stroke-width="1.25">
      <line x1="180" y1="18" x2="500" y2="18" />
      <line x1="180" y1="8" x2="180" y2="28" />
      <line x1="500" y1="8" x2="500" y2="28" />
      <line x1="176" y1="22" x2="184" y2="14" stroke-width="2" />
      <line x1="496" y1="22" x2="504" y2="14" stroke-width="2" />
    </g>
    <text x="340" y="12" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="bold" fill="#111110" text-anchor="middle">320 MM COMPOSITE ENVELOPE</text>
  </g>

  <!-- Folio Footer -->
  <line x1="64" y1="1008" x2="1856" y2="1008" stroke="#E8E5DC" stroke-width="1" />
  <text x="64" y="1034" font-family="'JetBrains Mono', monospace" font-size="11" fill="#55544E">LEAD ARCHITECT: SARA BENSALEM • 48°35'05"N 07°45'02"E</text>
  <text x="960" y="1034" font-family="'JetBrains Mono', monospace" font-size="11" fill="#55544E" text-anchor="middle">WORK RIGHTS: EU CITIZEN // ZERO VISA SPONSORSHIP REQUIRED</text>
  <text x="1856" y="1034" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="bold" fill="#111110" text-anchor="end">SPREAD 04</text>
</svg>`;
}

// Preset submissions for Grill My Design
const GRILL_PRESETS = {
  artdeco: "A 36-story Art Deco commercial tower featuring stepped ziggurat setbacks, vertical limestone piers, stylized satin brass chevron spandrels, and a 1:20 wall section detailing terrace waterproofing and structural thermal breaks.",
  beauxarts: "A grand Beaux-Arts municipal library with a clear axial parti pris, an experiential marche leading to a monumental coffered rotunda, and symmetrical egress corridors flanking the main reading room.",
  artnouveau: "An Art Nouveau artist atelier featuring organic whiplash curves (coup de fouet), structural wrought-iron columns with R60 intumescent fireproofing, biomorphic stained glass skylights, and custom cast brass ironmongery.",
  neoclassic: "A Neoclassical justice hall defined by a monumental octastyle Corinthian portico, tripartite elevation hierarchy, rusticated granite plinth, and flush-grade PMR accessibility discreetly integrated into the base.",

  alula: "The Memory of Air: A conceptual fragrance dinner experience within the desert canyons of Al-’Ula. A dialectic of contrasts: raw prehistoric rock vs deep petrol-blue draped chambers, mirror-polished stainless steel reflection banquet dissolving into the desert, atomized scent mist, and French crystal chandeliers in open night air.",
  indic: "Aayojan 2047 Master of Education & Cognitive Space: A 100-year institutional knowledge ecosystem rooted in Indic spatial systems and the Vāstu-Purusha mandala. Featuring stereotomic Jaipur sandstone massing, deep shaded colonnades, passive courtyard microclimates, porous jali ventilation screens, and a multi-level perception continuum linking mind, space, and form.",
  deconstruct: "A contemporary performing arts pavilion featuring non-rectilinear fractured titanium roof planes, an expressive 18-meter cantilevered observation deck with structural steel moment frames, non-Euclidean glazed fissures, and zero visible intermediate columns.",
  wabisabi: "A minimalist meditation tea pavilion set in a moss courtyard, featuring charred shou sugi ban cedar cladding, hand-troweled acoustic washi lime plaster walls, 5mm negative shadow reveals (joint creux) at the plinth, and concealed mortise-and-tenon oak framing.", 
  brutalist: "A monumental Brutalist civic archive featuring in-situ board-marked concrete (béton brut), exposed tie-rod holes, stereotomic massing, deep shadow brise-soleil, and a 1:20 constructive wall section with structural thermal breaks.",
  phenomenological: "A thermal bathhouse carved into alpine granite, featuring 1:5 shadow reveals (joint creux) between cleft stone and cedar, raking clerestory daylight, multi-sensory acoustic damping, and verified 1500mm PMR accessibility.",
  timber: "A contemporary timber cultural pavilion governed by a 12-column Swiss grid, featuring cantilevered oak glulam rafters, lime-hemp biotamping walls, and RE2020 net-negative embodied carbon.",
  render: "A luxury private villa in the hills documented through photorealistic Lumion and Midjourney renders, highlighting atmospheric sunset lighting, mood boards, and textured materiality."
};

document.addEventListener('DOMContentLoaded', () => {

  // 1. MISTRAL / ANTIGRAVITY ANIMATED DRAFTING CANVAS & CLICK-TO-DRAFT
  const canvas = document.getElementById('drafting-canvas');

  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width = canvas.width = canvas.parentElement.clientWidth;
    let height = canvas.height = canvas.parentElement.clientHeight;

    window.addEventListener('resize', () => {
      width = canvas.width = canvas.parentElement.clientWidth;
      height = canvas.height = canvas.parentElement.clientHeight;
    });

    // Particle nodes simulating architectural drafting vertices
    const particleCount = Math.min(50, Math.floor(width / 24));
    const particles = [];
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        size: Math.random() > 0.8 ? 2.5 : 1.5,
        type: Math.random() > 0.7 ? 'cross' : 'dot'
      });
    }

    // User-placed drafting nodes (Click-to-Draft feature)
    const userAnchors = [];
    canvas.parentElement.addEventListener('click', (e) => {
      if (e.target !== canvas) return;
      const rect = canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;
      userAnchors.push({ x: clickX, y: clickY, time: Date.now() });
      if (userAnchors.length > 8) userAnchors.shift();
    });

    let mouseX = -1000;
    let mouseY = -1000;

    canvas.parentElement.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });

    canvas.parentElement.addEventListener('mouseleave', () => {
      mouseX = -1000;
      mouseY = -1000;
    });

    // 60FPS animation loop
    function renderCanvas() {
      ctx.clearRect(0, 0, width, height);

      // Subtle architectural drafting grid dots
      ctx.fillStyle = 'rgba(20, 20, 18, 0.035)';
      const step = 48;
      for (let x = 0; x < width; x += step) {
        for (let y = 0; y < height; y += step) {
          ctx.fillRect(x, y, 1, 1);
        }
      }

      // Draw user placed anchors
      for (let k = 0; k < userAnchors.length; k++) {
        const a1 = userAnchors[k];
        ctx.strokeStyle = 'rgba(22, 22, 21, 0.7)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(a1.x, a1.y, 4, 0, Math.PI * 2);
        ctx.stroke();

        if (k > 0) {
          const a0 = userAnchors[k - 1];
          ctx.beginPath();
          ctx.moveTo(a0.x, a0.y);
          ctx.lineTo(a1.x, a1.y);
          ctx.strokeStyle = 'rgba(22, 22, 21, 0.35)';
          ctx.setLineDash([4, 4]);
          ctx.stroke();
          ctx.setLineDash([]);
        }
      }

      // Draw floating drafting vertices
      for (let i = 0; i < particles.length; i++) {
        const p1 = particles[i];

        p1.x += p1.vx;
        p1.y += p1.vy;
        if (p1.x < 0 || p1.x > width) p1.vx *= -1;
        if (p1.y < 0 || p1.y > height) p1.vy *= -1;

        // Interactive mouse repulsion & drafting snap hairlines
        const dxMouse = mouseX - p1.x;
        const dyMouse = mouseY - p1.y;
        const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
        if (distMouse < 150) {
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(mouseX, mouseY);
          ctx.strokeStyle = `rgba(22, 22, 21, ${0.18 * (1 - distMouse / 150)})`;
          ctx.lineWidth = 0.75;
          ctx.setLineDash([2, 2]);
          ctx.stroke();
          ctx.setLineDash([]);
        }

        // Draw node
        ctx.fillStyle = 'rgba(22, 22, 21, 0.35)';
        if (p1.type === 'cross') {
          ctx.strokeStyle = 'rgba(22, 22, 21, 0.4)';
          ctx.lineWidth = 0.8;
          ctx.beginPath();
          ctx.moveTo(p1.x - 3, p1.y);
          ctx.lineTo(p1.x + 3, p1.y);
          ctx.moveTo(p1.x, p1.y - 3);
          ctx.lineTo(p1.x, p1.y + 3);
          ctx.stroke();
        } else {
          ctx.beginPath();
          ctx.arc(p1.x, p1.y, p1.size, 0, Math.PI * 2);
          ctx.fill();
        }

        // Connect nearby particles
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 90) {
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(22, 22, 21, ${0.08 * (1 - dist / 90)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(renderCanvas);
    }
    renderCanvas();
  }

  // 2. INSTALL SNIPPETS TABS
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
        t.className = "install-tab px-3.5 py-1.5 rounded-lg bg-studio-subtle text-studio-textSecondary hover:text-studio-textPrimary hover:bg-studio-borderLight transition";
      });
      tab.className = "install-tab active px-3.5 py-1.5 rounded-lg bg-studio-graphite text-white font-bold transition shadow-xs";
      setSnippet(tab.getAttribute('data-target'));
    });
  });

  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      if (!codeEl) return;
      navigator.clipboard.writeText(codeEl.textContent).then(() => {
        copyLabel.textContent = "Copied!";
        copyBtn.className = "px-4 py-2 rounded-lg bg-stone-700 text-white font-mono font-bold text-xs transition flex items-center gap-2 self-start sm:self-auto";
        setTimeout(() => {
          copyLabel.textContent = "Copy Snippet";
          copyBtn.className = "px-4 py-2 rounded-lg bg-studio-graphite hover:bg-black text-white font-mono font-bold text-xs transition flex items-center gap-2 self-start sm:self-auto shadow-xs";
        }, 2000);
      });
    });
  }

  // 3. INTERACTIVE 1:20 EXPLORER & SWISS GRID CONTROLS
  const previewCanvas = document.getElementById('preview-canvas');
  const toggleGridBtn = document.getElementById('toggle-grid-btn');
  const downloadSvgBtn = document.getElementById('download-svg-btn');
  const gridModeBtns = document.querySelectorAll('.grid-mode-btn');
  const layerChips = document.querySelectorAll('.layer-chip');

  let currentCols = 12;
  let gridVisible = true;

  function renderSpread(cols = 12) {
    if (!previewCanvas) return;
    previewCanvas.innerHTML = generateSpreadSVG(cols);
    attachLayerEventListeners();
  }
  renderSpread(12);

  gridModeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      gridModeBtns.forEach(b => {
        b.className = "grid-mode-btn px-2.5 py-1 rounded text-studio-textSecondary hover:text-studio-textPrimary font-medium transition";
      });
      btn.className = "grid-mode-btn active px-2.5 py-1 rounded bg-studio-graphite text-white font-bold transition shadow-2xs";
      currentCols = parseInt(btn.getAttribute('data-cols'), 10) || 12;
      renderSpread(currentCols);
    });
  });

  if (toggleGridBtn) {
    toggleGridBtn.addEventListener('click', () => {
      gridVisible = !gridVisible;
      const cols = previewCanvas.querySelector('#preview-grid-cols');
      const margins = previewCanvas.querySelector('#preview-grid-margins');
      if (cols) cols.style.display = gridVisible ? 'block' : 'none';
      if (margins) margins.style.display = gridVisible ? 'block' : 'none';
      const label = document.getElementById('grid-btn-label');
      if (label) label.textContent = gridVisible ? "Hide Swiss Grid" : "Show Swiss Grid";
    });
  }

  if (downloadSvgBtn) {
    downloadSvgBtn.addEventListener('click', () => {
      const svgData = generateSpreadSVG(currentCols);
      const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sara_bensalem_1_20_wall_section_${currentCols}col.svg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  // Spec card elements
  const specTitle = document.getElementById('spec-title');
  const specThick = document.getElementById('spec-thickness');
  const specLambda = document.getElementById('spec-lambda');
  const specU = document.getElementById('spec-uvalue');
  const specAcoustic = document.getElementById('spec-acoustic');
  const specCarbon = document.getElementById('spec-carbon');
  const specVapor = document.getElementById('spec-vapor');

  function updateSpec(key) {
    const s = TECTONIC_SPECS[key] || TECTONIC_SPECS.all;
    if (specTitle) specTitle.textContent = s.title;
    if (specThick) specThick.textContent = s.thickness;
    if (specLambda) specLambda.textContent = s.lambda;
    if (specU) specU.textContent = s.uvalue;
    if (specAcoustic) specAcoustic.textContent = s.acoustic;
    if (specCarbon) specCarbon.textContent = s.carbon;
    if (specVapor) specVapor.textContent = s.vapor;
  }

  function highlightLayer(layerKey) {
    if (!previewCanvas) return;
    const layers = previewCanvas.querySelectorAll('.tectonic-layer');
    layers.forEach(l => {
      l.classList.remove('active');
      if (layerKey === 'all') {
        l.style.opacity = '1';
      } else if (l.id === `layer-${layerKey}`) {
        l.classList.add('active');
        l.style.opacity = '1';
      } else {
        l.style.opacity = '0.35';
      }
    });
    updateSpec(layerKey);
  }

  function attachLayerEventListeners() {
    if (!previewCanvas) return;
    const callouts = previewCanvas.querySelectorAll('.tectonic-callout');
    callouts.forEach(c => {
      c.addEventListener('mouseenter', () => {
        const lk = c.getAttribute('data-layer');
        highlightLayer(lk);
        layerChips.forEach(chip => {
          chip.className = chip.getAttribute('data-layer') === lk ?
            "layer-chip active px-3 py-1.5 rounded-lg bg-studio-graphite text-white font-bold transition shadow-2xs whitespace-nowrap" :
            "layer-chip px-3 py-1.5 rounded-lg bg-studio-subtle text-studio-textSecondary hover:text-studio-textPrimary hover:bg-studio-borderLight transition whitespace-nowrap";
        });
      });
      c.addEventListener('mouseleave', () => {
        highlightLayer('all');
      });
    });
  }

  layerChips.forEach(chip => {
    chip.addEventListener('click', () => {
      layerChips.forEach(c => {
        c.className = "layer-chip px-3 py-1.5 rounded-lg bg-studio-subtle text-studio-textSecondary hover:text-studio-textPrimary hover:bg-studio-borderLight transition whitespace-nowrap";
      });
      chip.className = "layer-chip active px-3 py-1.5 rounded-lg bg-studio-graphite text-white font-bold transition shadow-2xs whitespace-nowrap";
      const layerKey = chip.getAttribute('data-layer');
      highlightLayer(layerKey);
    });
  });

  // 4. GRILL MY DESIGN INTERACTIVE JURY SANDBOX & 5-AXIS AUDIT
  const grillInput = document.getElementById('grill-input');
  const runGrillBtn = document.getElementById('run-grill-btn');
  const grillResult = document.getElementById('grill-result');
  const grillVerdict = document.getElementById('grill-verdict-badge');
  const grillScore = document.getElementById('grill-score-badge');
  const grillQuestion = document.getElementById('grill-question');
  const grillVuln = document.getElementById('grill-vulnerability');
  const grillRemedy = document.getElementById('grill-remedy');
  const presetBtns = document.querySelectorAll('.preset-btn');

  // Metric bars
  const metricConstructiveVal = document.getElementById('metric-constructive-val');
  const metricConstructiveBar = document.getElementById('metric-constructive-bar');
  const metricPmrVal = document.getElementById('metric-pmr-val');
  const metricPmrBar = document.getElementById('metric-pmr-bar');
  const metricBioVal = document.getElementById('metric-bio-val');
  const metricBioBar = document.getElementById('metric-bio-bar');
  const metricRecruiterVal = document.getElementById('metric-recruiter-val');
  const metricRecruiterBar = document.getElementById('metric-recruiter-bar');
  const metricSwissVal = document.getElementById('metric-swiss-val');
  const metricSwissBar = document.getElementById('metric-swiss-bar');

  presetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const p = btn.getAttribute('data-preset');
      if (grillInput && GRILL_PRESETS[p]) {
        grillInput.value = GRILL_PRESETS[p];
        if (runGrillBtn) runGrillBtn.click();
      }
    });
  });

  if (runGrillBtn && grillInput) {
    runGrillBtn.addEventListener('click', () => {
      const text = (grillInput.value || "").trim().toLowerCase();
      if (!text) {
        grillInput.focus();
        return;
      }

      runGrillBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Grilling Design...</span>`;
      if (window.lucide) lucide.createIcons();

      setTimeout(() => {
        grillResult.classList.remove('hidden');

        let verdict = "CONDITIONAL PASS";
        let score = 74;
        let q = "Where is the continuous thermal break at your cantilevered glulam-to-slab junction? How do you prevent interstitial condensation during winter freeze-thaw cycles?";
        let vuln = "Uninsulated envelope penetration risking thermal bridging and structural degradation.";
        let remedy = "Detail a modular structural thermal break connector (e.g. Isokorb) with 120mm continuous exterior stone-wool wrapping.";
        let metrics = { constructive: 72, pmr: 88, bio: 68, recruiter: 80, swiss: 85 };

        if (text.includes('art deco') || text.includes('artdeco') || text.includes('ziggurat') || text.includes('chevron')) {
          verdict = "STREAMLINED GEOMETRIC CRAFT";
          score = 92;
          q = "Your stepped ziggurat setbacks and satin brass chevrons capture the 1925 Paris Moderne elegance. Detail your horizontal terrace tanking: how do you prevent water ingress at the setback transitions?";
          vuln = "Horizontal setbacks create high-risk ponding water traps if flashing and slope falloffs (< 2%) are inadequately detailed.";
          remedy = "Specify dual-layer elastomeric EPDM tanking with stainless steel clamping reglets and continuous insulated parapet caps.";
          metrics = { constructive: 90, pmr: 88, bio: 86, recruiter: 95, swiss: 94 };
        } else if (text.includes('beaux') || text.includes('rotunda') || text.includes('parti')) {
          verdict = "MONUMENTAL HIERARCHY (BEAUX-ARTS)";
          score = 94;
          q = "Your Beaux-Arts parti pris and spatial marche from entrance vestibule to grand rotunda is compelling. Where are your secondary emergency egress paths, and do travel distances comply with IBC Chapter 10?";
          vuln = "Grand ceremonial volumes frequently conceal long dead-end service corridors exceeding statutory 12m limits.";
          remedy = "Incorporate direct-to-exterior pressurized egress stairs within the symmetrical secondary corner pavilions.";
          metrics = { constructive: 92, pmr: 95, bio: 82, recruiter: 96, swiss: 95 };
        } else if (text.includes('art nouveau') || text.includes('whiplash') || text.includes('biomorphic')) {
          verdict = "BIOMORPHIC TECTONIC ELEGANCE";
          score = 90;
          q = "Your organic whiplash ironwork echoes Victor Horta. What is your fire-resistance rating (R60/R120) on the exposed slender biomorphic iron columns, and how are differential movements accommodated?";
          vuln = "Exposed decorative iron columns without certified intumescent protection fail contemporary life-safety fire resistance.";
          remedy = "Specify R60 certified thin-film intumescent coating with concealed Teflon expansion slip joints at floor slab anchors.";
          metrics = { constructive: 88, pmr: 92, bio: 85, recruiter: 94, swiss: 92 };
        } else if (text.includes('neoclassic') || text.includes('palladian') || text.includes('portico')) {
          verdict = "CLASSICAL PROPORTIONAL DISCIPLINE";
          score = 93;
          q = "Your Palladian axial symmetry and tripartite elevation hierarchy honor Schinkel. How is universal PMR wheelchair access integrated into the monumental rusticated plinth without disrupting the axial portico?";
          vuln = "Monumental exterior staircases often force humiliating secondary side ramps for wheelchair users.";
          remedy = "Integrate a grade-level central accessible loggia beneath the portico podium directly linking to the main atrium elevator.";
          metrics = { constructive: 94, pmr: 96, bio: 84, recruiter: 95, swiss: 96 };
        } else if (text.includes('brutalist') || text.includes('béton brut') || text.includes('concrete')) {
          verdict = "TECTONIC HONESTY (BRUTALIST)";
          score = 91;
          q = "Your stereotomic massing and board-marked béton brut shuttering embody Banham's 'truth to materials'. How do you detail the structural thermal break at your cantilevered concrete slab to prevent thermal bridging?";
          vuln = "Cantilevered exposed concrete slabs create severe interstitial condensation risks if uninsulated.";
          remedy = "Detail a structural thermal break module (e.g. Schöck Isokorb type K) with 120mm continuous interior/exterior stone-wool wrapping.";
          metrics = { constructive: 94, pmr: 88, bio: 85, recruiter: 96, swiss: 92 };
        } else if (text.includes('phenomenological') || text.includes('bathhouse') || text.includes('granite')) {
          verdict = "ATMOSPHERIC MASTERY";
          score = 93;
          q = "Your spatial sequence and sensory material triptych recall Peter Zumthor's Vals. Show me your 1:5 shadow reveal (joint creux) between wet granite floor tiles and vertical wall panels.";
          vuln = "Sub-millimeter shadow reveals in high-humidity zones require concealed stainless steel reglets with capillary drainage.";
          remedy = "Incorporate a 5mm recessed anodized aluminum reglet with a continuous EPDM tanking membrane.";
          metrics = { constructive: 92, pmr: 90, bio: 95, recruiter: 94, swiss: 95 };
        } else if (text.includes('lumion') || text.includes('midjourney') || text.includes('render') && !text.includes('wall section')) {
          verdict = "RENDER TRAP ALERT";
          score = 38;
          q = "I have 15 seconds to review this portfolio: you showcase atmospheric 3D sunset renderings, but where is your 1:20 constructive proof? How does this wall envelope meet the ground plane?";
          vuln = "Over-reliance on photorealistic 3D imagery with zero verified constructive drawings.";
          remedy = "Dedicate Plate IV to an uncropped 1:20 wall section with material callouts, EPDM flashing, and dimension chains.";
          metrics = { constructive: 25, pmr: 45, bio: 30, recruiter: 20, swiss: 70 };
        } else if (text.includes('high-rise') || text.includes('curtain wall') || text.includes('glass')) {
          verdict = "REWORK REQUIRED";
          score = 58;
          q = "With a frameless unitized glass curtain wall, what is your calculated Solar Heat Gain Coefficient (SHGC) on the south and west facades, and where are your mechanical air shafts located?";
          vuln = "Unprotected large-span glazing risks extreme summer solar overheating and excessive chiller loads.";
          remedy = "Integrate vertical exterior fins or micro-perforated louvers with Uw <= 0.8 W/m²K triple glazing.";
          metrics = { constructive: 60, pmr: 75, bio: 40, recruiter: 65, swiss: 80 };
        } else if (text.includes('library') || text.includes('pmr') || text.includes('airlock')) {
          verdict = "EXEMPLARY COMPLIANCE";
          score = 94;
          q = "Your universal accessibility geometry and dual egress corridors meet IBC Chapter 10 flawlessly. Detail your acoustic reverberation control at the double-height atrium ceiling.";
          vuln = "High volumetric reverberation time (RT60) may exceed 1.4 seconds in the central atrium.";
          remedy = "Incorporate micro-perforated oak veneer ceiling panels backed with 50mm recycled acoustic fleece.";
          metrics = { constructive: 95, pmr: 98, bio: 90, recruiter: 96, swiss: 92 };
        } else if (text.includes('terrace') || text.includes('accessible')) {
          verdict = "STRONG CANDIDATE";
          score = 86;
          q = "Your spatial sequence is clear. Show me how your universal accessibility turning circle (1500mm) functions at the entrance airlock without obstructing egress door swing.";
          vuln = "Entrance vestibule depth requires verified 1500mm PMR clearance circles.";
          remedy = "Widen entry vestibule to 1800mm and offset secondary swing door 300mm from corner.";
          metrics = { constructive: 85, pmr: 92, bio: 82, recruiter: 88, swiss: 90 };
        }

        if (grillVerdict) grillVerdict.textContent = verdict;
        if (grillScore) grillScore.textContent = `SCORE: ${score}/100`;
        if (grillQuestion) grillQuestion.textContent = `"${q}"`;
        if (grillVuln) grillVuln.textContent = vuln;
        if (grillRemedy) grillRemedy.textContent = remedy;

        // Animate metrics
        if (metricConstructiveVal) metricConstructiveVal.textContent = `${metrics.constructive}%`;
        if (metricConstructiveBar) metricConstructiveBar.style.width = `${metrics.constructive}%`;
        if (metricPmrVal) metricPmrVal.textContent = `${metrics.pmr}%`;
        if (metricPmrBar) metricPmrBar.style.width = `${metrics.pmr}%`;
        if (metricBioVal) metricBioVal.textContent = `${metrics.bio}%`;
        if (metricBioBar) metricBioBar.style.width = `${metrics.bio}%`;
        if (metricRecruiterVal) metricRecruiterVal.textContent = `${metrics.recruiter}%`;
        if (metricRecruiterBar) metricRecruiterBar.style.width = `${metrics.recruiter}%`;
        if (metricSwissVal) metricSwissVal.textContent = `${metrics.swiss}%`;
        if (metricSwissBar) metricSwissBar.style.width = `${metrics.swiss}%`;

        runGrillBtn.innerHTML = `<i data-lucide="flame" class="w-4 h-4"></i><span>Grill My Design</span>`;
        if (window.lucide) lucide.createIcons();

        grillResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 450);
    });
  }

  
  // 5. PORTFOLIO DESIGN LIBRARY (LOOKS, FONTS & PALETTES)
  const PORTFOLIO_LOOKS_DATA = {
  "swiss_editorial": {
    "id": "swiss_editorial",
    "title": "01. The Swiss Editorial Monograph",
    "archetype": "The Swiss International Style (Lars M\u00fcller / El Croquis)",
    "ideal_for": "Junior to Senior Architects targeting European Design Consultancies & Competitions",
    "spread_aspect": "16:9 Landscape / Double-A3",
    "grid": "12-Column Modular Grid w/ 8pt Baseline Rhythm",
    "typography": {
      "display": "Space Grotesk (700)",
      "body": "Inter / Plus Jakarta Sans (400, 500)",
      "technical": "JetBrains Mono (600)"
    },
    "palette": [
      {
        "name": "Archival Bone",
        "hex": "#F8F8F5",
        "role": "Spread Canvas Paper"
      },
      {
        "name": "Deep Graphite",
        "hex": "#111110",
        "role": "Primary Ink & Cut Lines"
      },
      {
        "name": "Muted Hairline",
        "hex": "#DDD9D0",
        "role": "Drafting Grid & Margins"
      },
      {
        "name": "Subtle Wash",
        "hex": "#F1F1EB",
        "role": "Sectional Poch\u00e9 & Cards"
      }
    ],
    "key_proof_elements": "Uncropped 1:20 constructive sections, 20% opacity folio numbering ('01'-'06'), Project Passports, zero cosmetic render fluff.",
    "category": "architecture"
  },
  "french_luxury": {
    "id": "french_luxury",
    "title": "02. The French Luxury Atelier",
    "archetype": "Haute D\u00e9coration & Heritage Long\u00e8re Conversion (MJM / Parisian Ateliers)",
    "ideal_for": "Interior Architects, Spatial Scenographers & Luxury Boutique Studios",
    "spread_aspect": "A4 Landscape (1:1.414)",
    "grid": "Tripartite 6-Column Columnar Grid w/ 45%+ White Space",
    "typography": {
      "display": "Bodoni Moda / Playfair Display (600)",
      "body": "Plus Jakarta Sans (300, 400)",
      "technical": "IBM Plex Mono (500)"
    },
    "palette": [
      {
        "name": "Linen Greige",
        "hex": "#F4F1EA",
        "role": "Warm Ambient Background"
      },
      {
        "name": "Noir Saint-Laurent",
        "hex": "#1C1B1A",
        "role": "Marble Tone & High Contrast"
      },
      {
        "name": "French Raw Oak",
        "hex": "#D4C5B9",
        "role": "Joinery Woodgrain Tone"
      },
      {
        "name": "Satin Brass",
        "hex": "#B89F7D",
        "role": "Hardware Inlay Accent"
      }
    ],
    "key_proof_elements": "Tactile material triptychs, bespoke 1:5 millwork reveals (joint creux), luminaire schedules (L1-L29), verified on-site supervision photos.",
    "category": "interior"
  },
  "technical_blueprints": {
    "id": "technical_blueprints",
    "title": "03. The Technical Office Working Set",
    "archetype": "High-Density Execution Blueprints (Salma Sameh / General Contractors)",
    "ideal_for": "Technical Office Engineers, Site Architects & Permitting Specialists",
    "spread_aspect": "A3 / A4 Landscape",
    "grid": "High-Density 16-Column Engineering Grid",
    "typography": {
      "display": "Space Grotesk (700)",
      "body": "Inter (400, 600)",
      "technical": "JetBrains Mono (700 Heavy)"
    },
    "palette": [
      {
        "name": "Crisp Paper",
        "hex": "#FFFFFF",
        "role": "High-Contrast Blueprint Sheet"
      },
      {
        "name": "Drafting Ink",
        "hex": "#0F1115",
        "role": "Primary Cut Profiles (0.50mm)"
      },
      {
        "name": "Technical Slate",
        "hex": "#55544E",
        "role": "Secondary Assemblies (0.25mm)"
      },
      {
        "name": "Hairline Grid",
        "hex": "#E8E5DC",
        "role": "Dimension Strings & Hatches"
      }
    ],
    "key_proof_elements": "90% technical working drawings, 10% renders. Parapet waterproofing, mechanical anchor brackets, basement parking (68 stalls) coordination.",
    "category": "architecture"
  },
  "brutalist_tectonics": {
    "id": "brutalist_tectonics",
    "title": "04. Brutalist B\u00e9ton Brut & Tectonic Honesty",
    "archetype": "The New Brutalism (Banham / Alison & Peter Smithson / Louis Kahn)",
    "ideal_for": "Civic Monumentalists, Mass Concrete & Mass Timber Architecture Practices",
    "spread_aspect": "Square 1:1 or 16:9 Monolith",
    "grid": "Monumental 8-Column Block Grid",
    "typography": {
      "display": "Space Grotesk / Heavy Display (800)",
      "body": "JetBrains Mono (400)",
      "technical": "JetBrains Mono (700)"
    },
    "palette": [
      {
        "name": "B\u00e9ton Brut",
        "hex": "#E6E6E2",
        "role": "Raw Board-Formed Shuttering"
      },
      {
        "name": "Cast Charcoal",
        "hex": "#161615",
        "role": "Stereotomic Massing Cut"
      },
      {
        "name": "Shuttering Grain",
        "hex": "#D0CDC5",
        "role": "Texture & Formwork Tone"
      },
      {
        "name": "Weathered Steel",
        "hex": "#7A4D3B",
        "role": "Expressed Structural Flitch Plates"
      }
    ],
    "key_proof_elements": "Stereotomic weight, exposed board-marked concrete shuttering ties, uncropped 1:20 rebar and thermal break drawings, zero decorative trim.",
    "category": "architecture"
  },
  "vernacular_bioclimatic": {
    "id": "vernacular_bioclimatic",
    "title": "05. Vernacular Earth & Bioclimatic Clay",
    "archetype": "Ecological Publishing & Tropical Vernacular (Alif Ahammed / Geoffrey Bawa)",
    "ideal_for": "Bioclimatic Designers, Heritage Conservationists & Bamboo/Earth Architects",
    "spread_aspect": "Square 1:1 Format (Editorial Monograph)",
    "grid": "Organic Tripartite Grid w/ Deep Gutter Margins",
    "typography": {
      "display": "Space Grotesk (700)",
      "body": "Plus Jakarta Sans (400, 500)",
      "technical": "JetBrains Mono (500)"
    },
    "palette": [
      {
        "name": "Terracotta Clay",
        "hex": "#D97757",
        "role": "Primary Tectonic Accent"
      },
      {
        "name": "Rammed Earth",
        "hex": "#4A3B32",
        "role": "Loadbearing Wall Cut"
      },
      {
        "name": "Sun-Dried Lime",
        "hex": "#F7F4EE",
        "role": "Natural Plaster Canvas"
      },
      {
        "name": "Basalt Stone",
        "hex": "#2B2A29",
        "role": "Foundation Plinth"
      }
    ],
    "key_proof_elements": "Solar altitude vector geometry (65\u00b0 vs 18\u00b0), natural stack airflow chimney loops, quarry provenance coordinates, RE2020 net-negative carbon.",
    "category": "architecture"
  },
  "art_deco_moderne": {
    "id": "art_deco_moderne",
    "title": "06. Art Deco & Streamlined Geometric Moderne",
    "archetype": "1925 Paris Exposition & Skyscraper Moderne (Van Alen / Ruhlmann)",
    "ideal_for": "High-Rise Commercial Architects & Bespoke Furniture/Hospitality Designers",
    "spread_aspect": "A4 Vertical & 16:9 Stepped Spread",
    "grid": "Stepped Ziggurat 12-Column Grid",
    "typography": {
      "display": "Space Grotesk (800)",
      "body": "Inter (400, 500)",
      "technical": "JetBrains Mono (600)"
    },
    "palette": [
      {
        "name": "Belgian Black",
        "hex": "#121212",
        "role": "High-Gloss Granite Base"
      },
      {
        "name": "Satin Brass",
        "hex": "#D4AF37",
        "role": "Chevron & Spandrel Accent"
      },
      {
        "name": "Limestone Pier",
        "hex": "#EFECE6",
        "role": "Vertical Mullion Face"
      },
      {
        "name": "Macassar Ebony",
        "hex": "#2C221E",
        "role": "1:5 Joinery Casework"
      }
    ],
    "key_proof_elements": "Stepped massing setback diagrams, chevron spandrel details, 1:5 brass inlay millwork reveals, horizontal terrace waterproofing details.",
    "category": "interior"
  },
  "phenomenological_story": {
    "id": "phenomenological_story",
    "title": "07. The Phenomenological Storyboard",
    "archetype": "Sensory User Journey & Memorials (Neha George / Peter Zumthor)",
    "ideal_for": "Cultural Institutions, Memorial Competitions & Museum Scenographers",
    "spread_aspect": "24-26 Double Spreads / A4 Landscape",
    "grid": "6-Panel Sequential Storyboard Grid",
    "typography": {
      "display": "Space Grotesk (700)",
      "body": "Plus Jakarta Sans (300, 400)",
      "technical": "JetBrains Mono (500)"
    },
    "palette": [
      {
        "name": "Chiaroscuro Dark",
        "hex": "#141414",
        "role": "Deep Shadow Boundary"
      },
      {
        "name": "Raking Daylight",
        "hex": "#FFFDF8",
        "role": "Luminous Light Well"
      },
      {
        "name": "Acoustic Wood",
        "hex": "#C7B299",
        "role": "Slatted Ceiling Damping"
      },
      {
        "name": "Cleft Alpine Stone",
        "hex": "#8C8A84",
        "role": "Textured Plinth"
      }
    ],
    "key_proof_elements": "Sequential 6-panel graphic narrative, compression and release threshold chambers, acoustic reflection pools, physical clay and cast-plaster models.",
    "category": "architecture"
  },
  "structural_expression": {
    "id": "structural_expression",
    "title": "08. High-Tech Structural Expressionism",
    "archetype": "Legibility of Forces & Kinetic Assemblies (Piano, Rogers & Rice)",
    "ideal_for": "Transit Infrastructure, Stadium & Large-Span Mass Timber Specialists",
    "spread_aspect": "Panoramic 16:9 Double Spread",
    "grid": "16-Column High-Precision Engineering Grid",
    "typography": {
      "display": "Space Grotesk (700)",
      "body": "Inter (400, 600)",
      "technical": "JetBrains Mono (700)"
    },
    "palette": [
      {
        "name": "Machine Silver",
        "hex": "#E2E8F0",
        "role": "Anodized Aluminum Shrouds"
      },
      {
        "name": "Structural Steel",
        "hex": "#1E293B",
        "role": "Primary Compression Columns"
      },
      {
        "name": "Tension Tie-Rod",
        "hex": "#475569",
        "role": "Pin-Jointed Cables"
      },
      {
        "name": "Safety Signal",
        "hex": "#334155",
        "role": "Service Core Articulation"
      }
    ],
    "key_proof_elements": "Cast steel node details at 1:10, tension cable calculations, Louis Kahn serviced vs servant spaces, Vierendeel transfer trusses.",
    "category": "architecture"
  },
  "indic_spatial_systems": {
    "id": "indic_spatial_systems",
    "title": "09. Indic Spatial Systems & Cognitive Continuum",
    "archetype": "Sacred Geometry & Systems Architecture (Pearl Gupta / Balkrishna Doshi / Charles Correa)",
    "ideal_for": "Institutional Masterplanners, Educational Campuses & Cultural Research Fellows",
    "spread_aspect": "Square 1:1 or Double-A3 Landscape",
    "grid": "Mandala 9-Square Modular Matrix w/ Concentric Margins",
    "typography": {
      "display": "Space Grotesk / Cinzel (700)",
      "body": "Plus Jakarta Sans (400, 500)",
      "technical": "JetBrains Mono (600)"
    },
    "palette": [
      {
        "name": "Jaipur Sandstone",
        "hex": "#D9825B",
        "role": "Stereotomic Thermal Massing"
      },
      {
        "name": "Saffron Ochre",
        "hex": "#E59A38",
        "role": "Sacred Threshold & Axis"
      },
      {
        "name": "Deep Graphite Slate",
        "hex": "#1F2328",
        "role": "Precision Cut Profile"
      },
      {
        "name": "Temple Lime Plaster",
        "hex": "#F7F3EB",
        "role": "Courtyard Wash & Light Canvas"
      }
    ],
    "key_proof_elements": "V\u0101stu-Purusha mandala spatial grids, perception continuum charts, 100-year institutional lifecycle models, passive courtyard microclimates.",
    "category": "architecture"
  },
  "ephemeral_scenography": {
    "id": "ephemeral_scenography",
    "title": "10. Ephemeral Scenography & Olfactory Monument",
    "archetype": "Desert Scenography & Fragrance Architecture (Yasmine Chouchane / Atelier Adeline \u2014 Al-\u2019Ula)",
    "ideal_for": "Luxury Scenographers, Exhibition Designers & Spatial Brand Directors",
    "spread_aspect": "Cinematic 16:9 Landscape Monograph",
    "grid": "Cinematic Asymmetric 12-Column Grid w/ 50%+ White Space",
    "typography": {
      "display": "Playfair Display / Bodoni Moda (600)",
      "body": "Plus Jakarta Sans (300, 400)",
      "technical": "IBM Plex Mono (500)"
    },
    "palette": [
      {
        "name": "Petrol Blue Textile",
        "hex": "#103544",
        "role": "Sensory Fabric & Sea Memory"
      },
      {
        "name": "Al-\u2019Ula Sandstone",
        "hex": "#C49A6C",
        "role": "Canyon Wall & Mineral Mass"
      },
      {
        "name": "Mirrored Stainless",
        "hex": "#E2E8F0",
        "role": "Specular Desert Reflection"
      },
      {
        "name": "Desert Mist",
        "hex": "#F4F6F8",
        "role": "Atmospheric Diffusion & Muslin"
      }
    ],
    "key_proof_elements": "Material contrast dialectics (raw stone vs flowing drapery vs mirror stainless), sensory chamber isolated mist details, zero-clutter negative space, French chandeliers in open desert air.",
    "category": "scenography"
  },
  "japandi_wabi_sabi": {
    "id": "japandi_wabi_sabi",
    "category": "interior",
    "title": "11. Japandi Hybrid & Wabi-Sabi Tectonics",
    "archetype": "Muted Organic Asymmetry & Scandinavian Joinery (Kengo Kuma / Axel Vervoordt)",
    "ideal_for": "Boutique Residential Architects, Tea Pavilions & Meditative Wellness Designers",
    "spread_aspect": "Square 1:1 or A4 Landscape",
    "grid": "Asymmetric 9-Column Japanese Grid w/ Generous Ma (Negative Space)",
    "typography": {
      "display": "Space Grotesk / Cormorant Garamond (500)",
      "body": "Plus Jakarta Sans (300, 400)",
      "technical": "JetBrains Mono (400)"
    },
    "palette": [
      {
        "name": "Hinoki Cypress",
        "hex": "#E8DCB8",
        "role": "Joinery Substrate & Screening"
      },
      {
        "name": "Shou Sugi Ban",
        "hex": "#1B1B19",
        "role": "Charred Timber Massing"
      },
      {
        "name": "Washi Lime Plaster",
        "hex": "#F6F5F0",
        "role": "Tactile Textured Canvas"
      },
      {
        "name": "Raw Iron Patina",
        "hex": "#5A554C",
        "role": "Concealed Hardware Accents"
      }
    ],
    "key_proof_elements": "Concealed mortise-and-tenon joints, acoustic washi paper screens, raking light on hand-troweled lime, zero synthetic gloss."
  },
  "alpine_bivouac": {
    "id": "alpine_bivouac",
    "category": "architecture",
    "title": "12. Alpine Bivouac & Extreme Climate Shelter",
    "archetype": "Prefabricated Lightweight Monocoque & Extreme Terrain (Thibault Chr\u00e9tien / Charlotte Perriand)",
    "ideal_for": "High-Altitude Expedition Architects, Modular Prefab & Disaster-Resilience Specialists",
    "spread_aspect": "Panoramic 16:9 Landscape Monograph",
    "grid": "16-Column High-Precision Aeronautical Grid",
    "typography": {
      "display": "Space Grotesk (800 Bold)",
      "body": "Inter (500, 600)",
      "technical": "JetBrains Mono (700 Bold)"
    },
    "palette": [
      {
        "name": "Anodized Titanium",
        "hex": "#8E9399",
        "role": "Aerodynamic Exterior Cladding"
      },
      {
        "name": "Glacier White",
        "hex": "#FFFFFF",
        "role": "Reflective Thermal Insulation"
      },
      {
        "name": "Alpine Basalt",
        "hex": "#222326",
        "role": "Pin-Foundation Anchorage"
      },
      {
        "name": "Rescue Signal",
        "hex": "#E04E39",
        "role": "Aeronautical Contrast Accent"
      }
    ],
    "key_proof_elements": "Thermal bridge-free envelope details, 250 km/h wind deflection aerodynamic profiles, helicopter-drop assembly sequencing diagrams."
  }
};

  const lookTabs = document.querySelectorAll('.look-tab');
  const lookTitle = document.getElementById('look-title');
  const lookArchetype = document.getElementById('look-archetype');
  const lookIdeal = document.getElementById('look-ideal');
  const lookSwatches = document.getElementById('look-swatches');
  const lookFontDisplay = document.getElementById('look-font-display');
  const lookFontBody = document.getElementById('look-font-body');
  const lookFontTech = document.getElementById('look-font-tech');
  const lookAspect = document.getElementById('look-aspect');
  const lookGrid = document.getElementById('look-grid');
  const lookProof = document.getElementById('look-proof');
  const copyLookBtn = document.getElementById('copy-look-btn');
  const copyLookLabel = document.getElementById('copy-look-label');

  let activeLookKey = 'swiss_editorial';

  function renderLook(key) {
    const l = PORTFOLIO_LOOKS_DATA[key] || PORTFOLIO_LOOKS_DATA.swiss_editorial;
    activeLookKey = key;

    if (lookTitle) lookTitle.textContent = l.title;
    if (lookArchetype) lookArchetype.textContent = l.archetype;
    if (lookIdeal) lookIdeal.textContent = l.ideal_for;
    if (lookFontDisplay) lookFontDisplay.textContent = l.typography.display;
    if (lookFontBody) lookFontBody.textContent = l.typography.body;
    if (lookFontTech) lookFontTech.textContent = l.typography.technical;
    if (lookAspect) lookAspect.textContent = l.spread_aspect;
    if (lookGrid) lookGrid.textContent = l.grid;
    if (lookProof) lookProof.textContent = l.key_proof_elements;

    if (lookSwatches) {
      lookSwatches.innerHTML = l.palette.map(p => `
        <div class="flex items-center justify-between p-2 rounded-lg bg-studio-bone border border-studio-border">
          <div class="flex items-center gap-2.5">
            <span class="w-6 h-6 rounded border border-studio-border shadow-2xs" style="background-color: ${p.hex}"></span>
            <div class="flex flex-col">
              <span class="font-bold text-[11px] text-studio-textPrimary">${p.name}</span>
              <span class="text-[10px] text-studio-textMuted">${p.role}</span>
            </div>
          </div>
          <code class="text-[10px] font-bold text-studio-textPrimary px-1.5 py-0.5 rounded bg-white border border-studio-border cursor-pointer hover:bg-studio-subtle" onclick="navigator.clipboard.writeText('${p.hex}')" title="Click to copy hex">${p.hex}</code>
        </div>
      `).join('');
    }
  }

  lookTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      lookTabs.forEach(t => {
        t.className = "look-tab px-3.5 py-1.5 rounded-lg bg-white text-studio-textSecondary hover:text-studio-textPrimary border border-studio-border transition whitespace-nowrap";
      });
      tab.className = "look-tab active px-3.5 py-1.5 rounded-lg bg-studio-graphite text-white font-bold transition shadow-xs whitespace-nowrap";
      renderLook(tab.getAttribute('data-look'));
    });
  });

  if (copyLookBtn) {
    copyLookBtn.addEventListener('click', () => {
      const l = PORTFOLIO_LOOKS_DATA[activeLookKey];
      const payload = {
        look: l.title,
        aspect_ratio: l.spread_aspect,
        grid_system: l.grid,
        typography: l.typography,
        color_palette: l.palette
      };
      navigator.clipboard.writeText(JSON.stringify(payload, null, 2)).then(() => {
        if (copyLookLabel) copyLookLabel.textContent = "Copied Config!";
        setTimeout(() => {
          if (copyLookLabel) copyLookLabel.textContent = "Copy Design Palette";
        }, 2000);
      });
    });
  }

  
  // --- Portfolio Looks Discipline Filtering ---
  const lookFilterBtns = document.querySelectorAll('.look-filter-btn');
  lookFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.getAttribute('data-filter');
      lookFilterBtns.forEach(b => {
        b.className = "look-filter-btn px-3.5 py-1.5 rounded-full bg-white hover:bg-studio-subtle text-studio-textSecondary hover:text-studio-textPrimary border border-studio-border font-semibold transition text-[11px]";
      });
      btn.className = "look-filter-btn active px-3.5 py-1.5 rounded-full bg-studio-graphite text-white font-semibold transition text-[11px] shadow-xs";

      let firstVisibleTab = null;
      lookTabs.forEach(tab => {
        const disc = tab.getAttribute('data-discipline') || '';
        if (filter === 'all' || disc.includes(filter)) {
          tab.style.display = 'inline-block';
          if (!firstVisibleTab) firstVisibleTab = tab;
        } else {
          tab.style.display = 'none';
        }
      });

      // If active tab is hidden, switch to first visible
      const currentActiveTab = document.querySelector('.look-tab.active');
      if (currentActiveTab && currentActiveTab.style.display === 'none' && firstVisibleTab) {
        firstVisibleTab.click();
      }
    });
  });

  // --- Movements Group Filtering ---
  const movementFilterBtns = document.querySelectorAll('.movement-filter-btn');
  const movementCards = document.querySelectorAll('.movement-card');
  movementFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.getAttribute('data-filter');
      movementFilterBtns.forEach(b => {
        b.className = "movement-filter-btn px-3.5 py-1.5 rounded-full bg-white hover:bg-studio-subtle text-studio-textSecondary hover:text-studio-textPrimary border border-studio-border font-semibold transition text-[11px]";
      });
      btn.className = "movement-filter-btn active px-3.5 py-1.5 rounded-full bg-studio-graphite text-white font-semibold transition text-[11px] shadow-xs";

      movementCards.forEach(card => {
        const grp = card.getAttribute('data-group');
        if (filter === 'all' || grp === filter) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // --- Copy Agent System Prompt Handler ---
  const copyPromptBtns = document.querySelectorAll('.copy-agent-prompt-btn');
  copyPromptBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const prompt = btn.getAttribute('data-prompt');
      const label = btn.querySelector('.prompt-btn-label');
      if (!prompt) return;

      navigator.clipboard.writeText(prompt).then(() => {
        if (label) label.textContent = "✓ Prompt Copied!";
        btn.classList.add('bg-studio-graphite', 'text-white');
        btn.classList.remove('bg-white', 'text-studio-textSecondary');

        setTimeout(() => {
          if (label) label.textContent = "Copy Agent Prompt";
          btn.classList.remove('bg-studio-graphite', 'text-white');
          btn.classList.add('bg-white', 'text-studio-textSecondary');
        }, 2000);
      });
    });
  });

  renderLook('swiss_editorial');

  if (window.lucide) {
    lucide.createIcons();
  }
});

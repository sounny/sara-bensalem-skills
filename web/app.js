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
  timber: "A contemporary timber cultural pavilion featuring cantilevered oak glulam rafters, cross-laminated timber roof panels, full-height double-glazed fenestration, polished terrazzo floors, and an accessible garden terrace.",
  glass: "A 24-story urban high-rise commercial tower with a frameless unitized glass curtain wall, core-driven egress stairs, concrete shear walls, and a multi-level atrium.",
  render: "A luxury private villa in the hills documented through photorealistic Lumion and Midjourney renders, highlighting atmospheric sunset lighting, mood boards, and textured materiality.",
  pmr: "A municipal urban library with a 1500mm entrance airlock, wide 1800mm bookstack corridors, dual panic-bar egress stairs, and an acoustic wood-slat atrium ceiling."
};

document.addEventListener('DOMContentLoaded', () => {

  // 1. MISTRAL / ANTIGRAVITY ANIMATED DRAFTING CANVAS & CLICK-TO-DRAFT
  const canvas = document.getElementById('drafting-canvas');
  const hud = document.getElementById('crosshair-hud');
  const hudX = document.getElementById('hud-x');
  const hudY = document.getElementById('hud-y');
  const hudScale = document.getElementById('hud-scale');
  let currentScale = '1:20';

  // Scale toggles
  const scaleBtns = document.querySelectorAll('.scale-toggle');
  scaleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      scaleBtns.forEach(b => {
        b.className = "scale-toggle px-1.5 py-0.5 rounded text-[10px] font-mono text-studio-textSecondary hover:text-studio-textPrimary";
      });
      btn.className = "scale-toggle px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-studio-graphite text-white";
      currentScale = btn.getAttribute('data-scale');
      if (hudScale) hudScale.textContent = `${currentScale} SNAP`;
    });
  });

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

      if (hud) {
        hud.style.display = 'block';
        hud.style.left = `${e.clientX}px`;
        hud.style.top = `${e.clientY}px`;
        const multiplier = currentScale === '1:20' ? 2.5 : (currentScale === '1:50' ? 6.25 : 12.5);
        if (hudX) hudX.textContent = Math.round(mouseX * multiplier);
        if (hudY) hudY.textContent = Math.round(mouseY * multiplier);
      }
    });

    canvas.parentElement.addEventListener('mouseleave', () => {
      mouseX = -1000;
      mouseY = -1000;
      if (hud) hud.style.display = 'none';
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

          // Dimension text
          const midX = (a0.x + a1.x) / 2;
          const midY = (a0.y + a1.y) / 2;
          const dist = Math.round(Math.hypot(a1.x - a0.x, a1.y - a0.y) * 2.5);
          ctx.fillStyle = 'rgba(22, 22, 21, 0.8)';
          ctx.font = '10px JetBrains Mono';
          ctx.fillText(`${dist} MM`, midX + 6, midY - 6);
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

        if (text.includes('lumion') || text.includes('midjourney') || text.includes('render') && !text.includes('wall section')) {
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

  if (window.lucide) {
    lucide.createIcons();
  }
});

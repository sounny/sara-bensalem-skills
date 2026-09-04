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

const SAMPLE_SPREAD_SVG = `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FFFFFF; font-family:Inter, sans-serif;">
  <!-- Grid Layer (Architectural Drafting Hairlines) -->
  <g id="preview-grid-cols" opacity="0.45">
    <rect x="64" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="212" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="360" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="508" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="656" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="804" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="952" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="1100" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="1248" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="1396" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="1544" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
    <rect x="1692" y="64" width="124" height="952" fill="#F8F8F5" stroke="#E8E5DC" stroke-dasharray="2 4" />
  </g>
  <g id="preview-grid-margins">
    <rect x="64" y="64" width="1792" height="952" fill="none" stroke="#111110" stroke-width="1" stroke-opacity="0.25" />
    <circle cx="64" cy="64" r="2.5" fill="#111110" />
    <circle cx="1856" cy="64" r="2.5" fill="#111110" />
    <circle cx="64" cy="1016" r="2.5" fill="#111110" />
    <circle cx="1856" cy="1016" r="2.5" fill="#111110" />
  </g>

  <!-- Folio Header -->
  <text x="64" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#55544E" letter-spacing="1">PROJECT MONOGRAPH: MAISON BRETONNE ADAPTIVE REUSE</text>
  <text x="1856" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#111110" font-weight="700" text-anchor="end">ACT 4 // CONSTRUCTIVE PROOF (1:20)</text>
  <line x1="64" y1="64" x2="1856" y2="64" stroke="#E8E5DC" stroke-width="1" />

  <!-- Left Technical Column: Material Callouts -->
  <g transform="translate(64, 120)">
    <text x="0" y="28" font-size="24" font-weight="800" fill="#111110">1:20 Wall Section Detail</text>
    <text x="0" y="52" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#55544E">SCALE 1:20 @ A3 // DIMENSIONS IN MM // STRASBOURG ATELIER</text>

    <g transform="translate(0, 84)">
      <rect x="0" y="0" width="24" height="24" fill="#111110" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">01</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Breton Granite Ashlar (180mm)</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Consolidated lime mortar joints, exterior breathability</text>
    </g>

    <g transform="translate(0, 144)">
      <rect x="0" y="0" width="24" height="24" fill="#55544E" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">02</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Lime-Hemp Biotamping (140mm)</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Hygrothermal monolithic insulation, λ = 0.076 W/m·K</text>
    </g>

    <g transform="translate(0, 204)">
      <rect x="0" y="0" width="24" height="24" fill="#111110" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">03</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Thermal Break & EPDM Flashing</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Continuous capillary moisture seal at plinth threshold</text>
    </g>

    <g transform="translate(0, 264)">
      <rect x="0" y="0" width="24" height="24" fill="#55544E" />
      <text x="12" y="16" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">04</text>
      <text x="36" y="12" font-size="13" font-weight="700" fill="#111110">Oak Glulam Post & Beam (160x280)</text>
      <text x="36" y="28" font-size="11" fill="#55544E">Concealed steel plate flitch connector w/ dowels</text>
    </g>

    <g transform="translate(0, 680)">
      <rect x="0" y="0" width="560" height="120" fill="#F8F8F5" stroke="#E8E5DC" />
      <text x="16" y="28" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#111110">CONSTRUCTIVE PROOF GUARANTEE</text>
      <text x="16" y="48" font-size="12" fill="#111110">Individual Line-Item Work: Envelope detailing &</text>
      <text x="16" y="66" font-size="12" fill="#111110">construction administration documentation.</text>
      <text x="16" y="94" font-family="'IBM Plex Mono', monospace" font-size="10" fill="#55544E">ANTI-RENDER-TRAP COMPLIANT • 100% BUILDABLE</text>
    </g>
  </g>

  <!-- Right Technical Canvas: 1:20 Detailing -->
  <g transform="translate(680, 120)">
    <rect x="0" y="0" width="1176" height="820" fill="#FFFFFF" stroke="#E8E5DC" stroke-width="1" />
    <rect x="180" y="520" width="860" height="130" fill="#F4F4F0" stroke="#111110" stroke-width="2" />
    <line x1="190" y1="560" x2="1030" y2="560" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />
    <line x1="190" y1="620" x2="1030" y2="620" stroke="#84827A" stroke-width="1" stroke-dasharray="8 6" />

    <rect x="180" y="40" width="180" height="480" fill="#EAEAE5" stroke="#111110" stroke-width="2" />
    <line x1="180" y1="120" x2="360" y2="120" stroke="#111110" stroke-width="1" />
    <line x1="180" y1="200" x2="360" y2="200" stroke="#111110" stroke-width="1" />
    <line x1="180" y1="280" x2="360" y2="280" stroke="#111110" stroke-width="1" />
    <line x1="180" y1="360" x2="360" y2="360" stroke="#111110" stroke-width="1" />
    <line x1="180" y1="440" x2="360" y2="440" stroke="#111110" stroke-width="1" />

    <rect x="360" y="40" width="120" height="480" fill="#F8F8F5" stroke="#111110" stroke-width="1.5" stroke-dasharray="4 2" />
    <rect x="480" y="40" width="20" height="480" fill="#FFFFFF" stroke="#111110" stroke-width="1" />

    <rect x="500" y="160" width="540" height="260" fill="#F8F8F5" stroke="#111110" stroke-width="2" />
    <line x1="500" y1="290" x2="1040" y2="290" stroke="#111110" stroke-width="1.5" />
    <text x="770" y="278" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#111110" text-anchor="middle">TRIPLE GLAZED TIMBER-ALU ENVELOPE // Uw = 0.78 W/m²K</text>

    <!-- Dimension Strings -->
    <g stroke="#111110" stroke-width="1.25">
      <line x1="120" y1="40" x2="120" y2="520" />
      <line x1="108" y1="40" x2="132" y2="40" />
      <line x1="108" y1="520" x2="132" y2="520" />
      <line x1="112" y1="44" x2="128" y2="36" stroke-width="2" />
      <line x1="112" y1="524" x2="128" y2="516" stroke-width="2" />
    </g>
    <text x="100" y="290" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#111110" text-anchor="middle" transform="rotate(-90 100 290)">4800 MM CLEARANCE</text>

    <g stroke="#111110" stroke-width="1.25">
      <line x1="180" y1="18" x2="500" y2="18" />
      <line x1="180" y1="8" x2="180" y2="28" />
      <line x1="500" y1="8" x2="500" y2="28" />
      <line x1="176" y1="22" x2="184" y2="14" stroke-width="2" />
      <line x1="496" y1="22" x2="504" y2="14" stroke-width="2" />
    </g>
    <text x="340" y="12" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#111110" text-anchor="middle">320 MM COMPOSITE ENVELOPE</text>
  </g>

  <!-- Folio Footer -->
  <line x1="64" y1="1008" x2="1856" y2="1008" stroke="#E8E5DC" stroke-width="1" />
  <text x="64" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#55544E">LEAD ARCHITECT: SARA BENSALEM • 48°35'05"N 07°45'02"E</text>
  <text x="960" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#55544E" text-anchor="middle">WORK RIGHTS: EU CITIZEN // ZERO VISA SPONSORSHIP REQUIRED</text>
  <text x="1856" y="1034" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#111110" text-anchor="end">SPREAD 04</text>
</svg>`;

// Preset submissions for Grill My Design
const GRILL_PRESETS = {
  timber: "A contemporary timber cultural pavilion featuring cantilevered oak glulam rafters, cross-laminated timber roof panels, full-height double-glazed fenestration, polished terrazzo floors, and an accessible garden terrace.",
  glass: "A 24-story urban high-rise commercial tower with a frameless unitized glass curtain wall, core-driven egress stairs, concrete shear walls, and a multi-level atrium.",
  render: "A luxury private villa in the hills documented through photorealistic Lumion and Midjourney renders, highlighting atmospheric sunset lighting, mood boards, and textured materiality."
};

document.addEventListener('DOMContentLoaded', () => {

  // 1. MISTRAL / ANTIGRAVITY ANIMATED DRAFTING CANVAS
  const canvas = document.getElementById('drafting-canvas');
  const hud = document.getElementById('crosshair-hud');
  const hudX = document.getElementById('hud-x');
  const hudY = document.getElementById('hud-y');

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
        if (hudX) hudX.textContent = Math.round(mouseX * 2.5);
        if (hudY) hudY.textContent = Math.round(mouseY * 2.5);
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

      // Draw subtle connection hairlines between nearby nodes
      for (let i = 0; i < particles.length; i++) {
        const p1 = particles[i];

        // Update position
        p1.x += p1.vx;
        p1.y += p1.vy;
        if (p1.x < 0 || p1.x > width) p1.vx *= -1;
        if (p1.y < 0 || p1.y > height) p1.vy *= -1;

        // Interactive mouse repulsion/interaction (Antigravity physics)
        const dxMouse = mouseX - p1.x;
        const dyMouse = mouseY - p1.y;
        const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
        if (distMouse < 140) {
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(mouseX, mouseY);
          ctx.strokeStyle = `rgba(22, 22, 21, ${0.18 * (1 - distMouse / 140)})`;
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

  // 3. GRILL MY DESIGN INTERACTIVE JURY SANDBOX
  const grillInput = document.getElementById('grill-input');
  const runGrillBtn = document.getElementById('run-grill-btn');
  const grillResult = document.getElementById('grill-result');
  const grillVerdict = document.getElementById('grill-verdict-badge');
  const grillScore = document.getElementById('grill-score-badge');
  const grillQuestion = document.getElementById('grill-question');
  const grillVuln = document.getElementById('grill-vulnerability');
  const grillRemedy = document.getElementById('grill-remedy');
  const presetBtns = document.querySelectorAll('.preset-btn');

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

        // Socratic critique evaluation
        let verdict = "CONDITIONAL PASS";
        let score = 74;
        let q = "Where is the continuous thermal break at your cantilevered glulam-to-slab junction? How do you prevent interstitial condensation during winter freeze-thaw cycles?";
        let vuln = "Uninsulated envelope penetration risking thermal bridging and structural degradation.";
        let remedy = "Detail a modular structural thermal break connector (e.g. Isokorb) with 120mm continuous exterior stone-wool wrapping.";

        if (text.includes('lumion') || text.includes('midjourney') || text.includes('render') && !text.includes('wall section')) {
          verdict = "RENDER TRAP ALERT";
          score = 42;
          q = "I have 15 seconds to review this portfolio: you showcase atmospheric 3D sunset renderings, but where is your 1:20 constructive proof? How does this wall envelope meet the ground plane?";
          vuln = "Over-reliance on photorealistic 3D imagery with zero verified constructive drawings.";
          remedy = "Dedicate Plate IV to an uncropped 1:20 wall section with material callouts, EPDM flashing, and dimension chains.";
        } else if (text.includes('high-rise') || text.includes('curtain wall') || text.includes('glass')) {
          verdict = "REWORK REQUIRED";
          score = 58;
          q = "With a frameless unitized glass curtain wall, what is your calculated Solar Heat Gain Coefficient (SHGC) on the south and west facades, and where are your mechanical air shafts located?";
          vuln = "Unprotected large-span glazing risks extreme summer solar overheating and excessive chiller loads.";
          remedy = "Integrate integrated vertical exterior fins or micro-perforated louvers with Uw <= 0.8 W/m²K triple glazing.";
        } else if (text.includes('terrace') || text.includes('accessible')) {
          verdict = "STRONG CANDIDATE";
          score = 86;
          q = "Your spatial sequence is clear. Show me how your universal accessibility turning circle (1500mm) functions at the entrance airlock without obstructing egress door swing.";
          vuln = "Entrance vestibule depth requires verified 1500mm PMR clearance circles.";
          remedy = "Widen entry vestibule to 1800mm and offset secondary swing door 300mm from corner.";
        }

        if (grillVerdict) grillVerdict.textContent = verdict;
        if (grillScore) grillScore.textContent = `SCORE: ${score}/100`;
        if (grillQuestion) grillQuestion.textContent = `"${q}"`;
        if (grillVuln) grillVuln.textContent = vuln;
        if (grillRemedy) grillRemedy.textContent = remedy;

        runGrillBtn.innerHTML = `<i data-lucide="flame" class="w-4 h-4"></i><span>Grill My Design</span>`;
        if (window.lucide) lucide.createIcons();

        grillResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 450);
    });
  }

  // 4. Spread Preview & Grid Toggle
  const previewCanvas = document.getElementById('preview-canvas');
  const toggleGridBtn = document.getElementById('toggle-grid-btn');
  const downloadSvgBtn = document.getElementById('download-svg-btn');
  let gridVisible = true;

  if (previewCanvas) {
    previewCanvas.innerHTML = SAMPLE_SPREAD_SVG;
  }

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
      const blob = new Blob([SAMPLE_SPREAD_SVG], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "sara_bensalem_1_20_wall_section.svg";
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

// Sara Bensalem Design Skills — Interactive Studio Application

// 1. MCP CONFIGURATIONS FOR QUICK INSTALL
const MCP_CONFIGS = {
  claude: `{
  "mcpServers": {
    "sara-bensalem-design-skills": {
      "command": "python",
      "args": [
        "path/to/sara-bensalem-skills/mcp-server/server.py"
      ]
    }
  }
}`,
  cursor: `{
  "mcpServers": {
    "sara-bensalem-design-skills": {
      "command": "python",
      "args": [
        "path/to/sara-bensalem-skills/mcp-server/server.py"
      ]
    }
  }
}`,
  antigravity: `{
  "mcp": {
    "servers": {
      "sara-bensalem-skills": {
        "command": "python",
        "args": ["mcp-server/server.py"]
      }
    }
  }
}`,
  cli: `# Run the MCP server directly via stdio JSON-RPC:
git clone https://github.com/sounny/sara-bensalem-skills.git
cd sara-bensalem-skills/mcp-server
pip install -r requirements.txt
python server.py`
};

// 2. DESIGN SKILLS SUITE DATA
const DESIGN_SKILLS_SUITE = [
  {
    id: "portfolio-design",
    number: "01",
    title: "Spatial Portfolio Architecture & Curation",
    status: "Available Now",
    statusBg: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    dotColor: "bg-emerald-400",
    badge: "Flagship Skill",
    desc: "Swiss editorial typography, 10 layout archetypes, 5-act spatial case study structure, and 100-point audit rubric to eliminate render traps.",
    tags: ["Swiss Grid", "PDF Curation", "Tectonic Proof", "Interactive Auditor"],
    actionText: "Launch Auditor & Archetypes",
    actionLink: "#auditor",
    active: true
  },
  {
    id: "heritage-adaptive-reuse",
    number: "02",
    title: "Heritage Longère & Vernacular Adaptive Reuse",
    status: "In Development",
    statusBg: "bg-amber-500/10 text-amber-300 border-amber-500/30",
    dotColor: "bg-amber-400",
    badge: "Vernacular Systems",
    desc: "Breton vernacular masonry, lime-hemp mortars, timber roof truss stabilization, thermal envelopes, and glazed modern transitions.",
    tags: ["Heritage Masonry", "Thermal Envelope", "Hempcrete", "Adaptive Reuse"],
    actionText: "Preview Methodology",
    actionLink: "#skills-portfolio",
    active: false
  },
  {
    id: "interior-joinery-scenography",
    number: "03",
    title: "Interior Joinery & Tactile Scenography",
    status: "In Development",
    statusBg: "bg-amber-500/10 text-amber-300 border-amber-500/30",
    dotColor: "bg-amber-400",
    badge: "Material & Detail",
    desc: "Bespoke architectural millwork details, material triptych curation, warm greige atmospheric palettes, and luminaire schedules.",
    tags: ["Millwork & Joinery", "Material Boards", "Lighting Schedules", "Sensory Interiors"],
    actionText: "Preview Methodology",
    actionLink: "#skills-portfolio",
    active: false
  },
  {
    id: "gender-equitable-urbanism",
    number: "04",
    title: "Gender-Equitable Public Realm & Safety",
    status: "In Development",
    statusBg: "bg-amber-500/10 text-amber-300 border-amber-500/30",
    dotColor: "bg-amber-400",
    badge: "Civic Research",
    desc: "Empirical civic safety auditing, 24/7 natural surveillance sightlines, bio-buffered pedestrian boulevards, and inclusive streetscapes.",
    tags: ["Civic Safety Audits", "Inclusive Typologies", "Pedestrian Comfort", "Public Space"],
    actionText: "Preview Methodology",
    actionLink: "#skills-portfolio",
    active: false
  }
];

// 3. 100-POINT AUDIT RUBRIC DATA
const RUBRIC_DATA = [
  {
    id: "narrative",
    title: "1. Narrative & Strategic Curation",
    max_points: 20,
    items: [
      { id: "passports", label: "Project Passport Clarity", points: 5, desc: "Role, tools, location, year, and 2-sentence executive challenge on spread 1." },
      { id: "problem_solving", label: "Problem-to-Solution Framing", points: 5, desc: "Clear ecological, structural, or programmatic dilemma before showing finished form." },
      { id: "scannability", label: "30-Second Scannable Hierarchy", points: 5, desc: "Bold headings, short spec blurbs, callouts. Zero long dense text blocks." },
      { id: "hook_pacing", label: "Hero Hook & Project Pacing", points: 5, desc: "First spread commands immediate authority. Smooth rhythm across 3–4 spreads." }
    ]
  },
  {
    id: "constructive",
    title: "2. Constructive Rigor & Technical Proof",
    max_points: 25,
    items: [
      { id: "scaled_drawings", label: "Scaled Working Drawings (1:20 to 1:100)", points: 10, desc: "Dimensioned floor plans, elevations, or structural sections with graphic scale bars." },
      { id: "wall_sections", label: "Layered Construction Wall Sections", points: 5, desc: "Multi-layered material callouts (waterproofing, insulation, anchors, finishes)." },
      { id: "cotations", label: "Legible Cotations & Grid Axes", points: 5, desc: "Dimension chains exported with calibrated line weights (no 4pt blurry lines)." },
      { id: "codes_egress", label: "Code & Structural Reality", points: 5, desc: "Real-world fire egress, PMR-ADA clearances, shear walls, and MEP plant spaces." }
    ]
  },
  {
    id: "grid_type",
    title: "3. Layout, Typography & Swiss Grid",
    max_points: 20,
    items: [
      { id: "margins", label: "Consistent Swiss Grid & Margins", points: 5, desc: "Rigid modular column grid and generous outer margins consistent across all spreads." },
      { id: "type_scale", label: "Restrained Typographic Scale", points: 5, desc: "Maximum 2 font families (clean sans + subtle serif/mono), 3 clear weight steps." },
      { id: "white_space", label: "Generous White Space (35%+)", points: 5, desc: "Page breathes; avoids overcrowded 6-box collage grids." },
      { id: "pacing_rhythm", label: "Rhythm & Spread Balance", points: 5, desc: "Alternates between full-bleed cinematic hero spreads and disciplined technical plates." }
    ]
  },
  {
    id: "multiscale",
    title: "4. Multi-Scale Spatial Fluency",
    max_points: 15,
    items: [
      { id: "macro_site", label: "Macro Urban & Environmental Integration", points: 5, desc: "Master plan, climatic sun/wind vectors, hydrology, or contextual city fabric." },
      { id: "meso_building", label: "Meso Building-Scale Circulation", points: 5, desc: "Clear user journey paths, vertical cores, daylight atriums, and room adjacencies." },
      { id: "micro_joinery", label: "Micro Joinery, Hardware, or Tectonic Joint", points: 5, desc: "1:5 bespoke interior millwork, facade bracket, stair nosing, or custom fixture." }
    ]
  },
  {
    id: "materiality",
    title: "5. Materiality, Light & Sensory Scenography",
    max_points: 10,
    items: [
      { id: "triptych", label: "Tactile Material Palette / Triptych", points: 3, desc: "Curated texture samples (e.g. travertine, lime plaster, fluted oak, bronze)." },
      { id: "lighting", label: "Daylight Scenography & Illumination", points: 3, desc: "Diurnal light filtration (sawtooth roof, deep reveals) and artificial lighting balance." },
      { id: "restraint", label: "Color Restraint (No Neon Saturation)", points: 4, desc: "Sophisticated mineral greige and earthy tone palette avoiding hyper-saturated render presets." }
    ]
  },
  {
    id: "validation",
    title: "6. Professional Delivery & Integrity",
    max_points: 10,
    items: [
      { id: "pdf_optimization", label: "PDF Container Integrity (<50 MB)", points: 3, desc: "Properly compressed raster assets that pass email filters without pixelation." },
      { id: "real_proof", label: "Real-World Proof & Validation", points: 4, desc: "On-site construction photos, client commissions, competitions, or academic honors." },
      { id: "colophon", label: "Clean Colophon, Bio & Contact Matrix", points: 3, desc: "Restrained concluding page with software competencies, contact details, and dates." }
    ]
  }
];

// 4. ARCHETYPES DATA (SANITIZED & TYPOLOGICAL)
const ARCHETYPES_DATA = [
  {
    id: "01",
    title: "The Swiss Editorial Landscape",
    category: "Architecture",
    budget: "24 Spreads (48 Pages)",
    format: "16:9 / A4 Landscape",
    typology: "Contemporary European Agency & Field Practice",
    target: "European design consultancies & international agencies",
    summary: "Panoramic double-spread balance, large 20% opacity display numbers (01-06), circular vignettes, and on-site construction drone photography."
  },
  {
    id: "02",
    title: "The Technical Office Working Set",
    category: "Technical",
    budget: "30-35 Pages",
    format: "A3 / A4 Landscape",
    typology: "Tectonic Detailing, Working Sets & Execution Engineering",
    target: "General contractors & engineering consultancies (AECOM, Bouygues, Dar Al-Handasah)",
    summary: "Reverses the render trap completely (90% technical working drawings, 10% renders), parapet waterproofing, mechanical stone anchor brackets."
  },
  {
    id: "03",
    title: "The French Luxury Minimalist Book",
    category: "Interior",
    budget: "28-32 Pages",
    format: "A4 Landscape",
    typology: "Parisian High-End Residential & Heritage Longère Ateliers",
    target: "Parisian interior architecture ateliers & luxury hospitality studios",
    summary: "Custom monogram branding, warm greige minimalism, historic stone longère conversions, and custom timber furniture prototyping."
  },
  {
    id: "04",
    title: "The Phenomenological Storyboard",
    category: "Architecture",
    budget: "26 Spreads (52 Pages)",
    format: "A4 Landscape",
    typology: "Cultural Memorials & Phenomenological Spatial Storytelling",
    target: "Cultural institutions, memorial design studios, narrative firms",
    summary: "6-panel comic-strip graphic narrative walking reviewers through sensory and psychological user journeys, physical clay study models."
  },
  {
    id: "05",
    title: "The Feminist Urbanist & Researcher",
    category: "Urban",
    budget: "24-30 Pages",
    format: "A4 Landscape",
    typology: "Inclusive Urbanism, Empirical Safety Audits & Healing Environments",
    target: "Civic design foundations & progressive urban planning consultancies",
    summary: "Empirical safety audit of public transit corridors, 12-factor inclusive urban design typology, and circular before/after comparative isometrics."
  },
  {
    id: "06",
    title: "The Vernacular & Ecological Monograph",
    category: "Architecture",
    budget: "30-36 Pages",
    format: "Square (1:1) / A4 Portrait",
    typology: "Bioclimatic Earth Craft & Architectural Research Monographs",
    target: "Bioclimatic practices, tropical institutes, research foundations",
    summary: "Restrained square format, terracotta/clay massing diagrams, graphite isometrics, and published research monographs."
  },
  {
    id: "07",
    title: "The Regenerative Environmental Systems",
    category: "Urban",
    budget: "50-60 Pages",
    format: "A4 Landscape",
    typology: "Climate Resilience, Agro-Industrial Hubs & Water Infrastructure",
    target: "Global concept consultancies (BIG, Foster + Partners, Snøhetta)",
    summary: "Aquatic remediation infrastructure, vertical automated hydroponics, salinity mitigation systems, and international competition awards."
  },
  {
    id: "08",
    title: "The Commercial Interior Specifier",
    category: "Interior",
    budget: "45-52 Pages",
    format: "A4 Landscape",
    typology: "Commercial Retail Showrooms, Hospitality & Lighting Execution",
    target: "Commercial retail agencies & exhibition stand architects",
    summary: "Tender-ready specification sheets with luminaire schedules (L1-L29), exact material pricing (€/m²), and high-end showroom pavilions."
  },
  {
    id: "09",
    title: "The Multi-Scale Infrastructure Architect",
    category: "Architecture",
    budget: "18-22 Pages",
    format: "A4 Landscape",
    typology: "Multi-Modal Transit Terminals & Tectonic Joinery",
    target: "Multidisciplinary consultancies & state transit infrastructure agencies",
    summary: "Balanced agility moving from macro LRT transit terminal stations to exploded structural skin axonometrics down to bespoke interior joinery."
  },
  {
    id: "10",
    title: "The Industrial Housing & Net-Zero BIM",
    category: "Technical",
    budget: "20-24 Pages",
    format: "A4 Landscape",
    typology: "Net-Zero Multi-Family Housing & Parametric BIM Façades",
    target: "Multi-family residential developers & computational design studios",
    summary: "Modular workforce housing clusters, Solar Decathlon Net-Zero team leadership, built residential commissions, and parametric solar screens."
  }
];

// 5. 5-ACT SPREAD METHODOLOGY DATA
const ACTS_DATA = [
  {
    id: "act1",
    tag: "Act I — The Hook & Project Passport",
    spreadLabel: "Spread 1 (Opening)",
    title: "Act I: The Hook & Project Passport",
    desc: "Anchor the project immediately with scannable executive metadata and a 2-sentence thesis stating the core challenge.",
    leftTitle: "Executive Project Passport",
    leftElements: [
      "Typology, Location, Year, Client/Studio",
      "Software Stack: Revit, Rhino, V-Ray",
      "2-Sentence Problem Statement",
      "Key Area Metric (e.g. 1,000 m²)"
    ],
    rightTitle: "Cinematic Atmosphere Hero",
    rightElements: [
      "Hero atmospheric rendering or twilight view",
      "Subtle architectural scale bar & north arrow",
      "Muted display title (Tracking -0.02em)",
      "Zero clutter or secondary thumbnails"
    ]
  },
  {
    id: "act2",
    tag: "Act II — Contextual Conflict & Site",
    spreadLabel: "Spread 1 Right & Spread 2 Left",
    title: "Act II: The Contextual Conflict & Environmental Site",
    desc: "Prove you understand the constraints of the terrain, climate, or socioeconomic fabric before drawing any forms.",
    leftTitle: "Climatic & Topographic Vectors",
    leftElements: [
      "Solar radiation & shadow simulation",
      "Prevailing wind breeze corridors",
      "Topographic contour clearing & slope",
      "Hydrological drainage & water table"
    ],
    rightTitle: "Empirical Context Mapping",
    rightElements: [
      "Regional connectivity & transport nodes",
      "Socioeconomic or historic footprint map",
      "Programmatic zoning constraints",
      "Site boundary cotations"
    ]
  },
  {
    id: "act3",
    tag: "Act III — Spatial Strategy & Volumetric Evolution",
    spreadLabel: "Spread 2 (Evolution)",
    title: "Act III: Spatial Strategy & Volumetric Evolution",
    desc: "Demystify your design thinking through a disciplined 3-to-4-step massing evolution or exploded architectural axonometric.",
    leftTitle: "4-Step Massing Evolution",
    leftElements: [
      "Step 1: Zoning envelope & setback limit",
      "Step 2: Carving central daylight atrium",
      "Step 3: Stepped terracing for wind flow",
      "Step 4: Facade envelope & shading louvers"
    ],
    rightTitle: "Exploded Structural Axonometric",
    rightElements: [
      "Substructure & foundation piers",
      "Concrete structural shear cores",
      "Vierendeel transfer trusses",
      "Layered skin & circulation paths"
    ]
  },
  {
    id: "act4",
    tag: "Act IV — Constructive Proof (The Anti-Trap)",
    spreadLabel: "Spread 3 (Tectonic Proof)",
    title: "Act IV: Constructive Proof & Layered Wall Sections",
    desc: "This is the spread that eliminates the Render Trap. Reviewers look here to verify whether you can actually build.",
    leftTitle: "Scaled 1:50 / 1:100 Floor Plans",
    leftElements: [
      "Legible dimension chains & structural axes",
      "Fire egress stairwells & PMR-ADA radii",
      "Room names, finish codes, and net m²",
      "Section cut lines A-A' and B-B'"
    ],
    rightTitle: "Layered 1:20 Technical Wall Section",
    rightElements: [
      "Parapet flashing & waterproofing membrane",
      "Thermal break double-glazing callout",
      "Mechanical stone/GFRC anchor brackets",
      "Foundation perimeter drainage gravel"
    ]
  },
  {
    id: "act5",
    tag: "Act V — Sensory Atmosphere & Resolution",
    spreadLabel: "Spread 4 (Sensory Climax)",
    title: "Act V: Sensory Atmosphere, Materiality & Light",
    desc: "Conclude with tactile material resonance, lighting scenography (day vs. night), and the verified socio-ecological impact.",
    leftTitle: "Tactile Material Triptych",
    leftElements: [
      "Natural honed travertine sample",
      "Fluted acoustic white oak paneling",
      "Champagne bronze anodized hardware",
      "Micro-terrazzo blush floor finish"
    ],
    rightTitle: "Atmospheric Lighting Study",
    rightElements: [
      "Natural daylight filtration study",
      "Artificial luminaire schedule callouts (L1-L29)",
      "Vignette view of public interaction",
      "Verified outcome / competition award stamp"
    ]
  }
];

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initMcpTabs();
  initSkillsSuite();
  initAuditor();
  initArchetypes();
  initSpreadSimulator();
  initTerminalSimulator();
  initCoArchitectDrawer();
  initPortfolioStitchStudio();
  
  if (window.lucide) {
    lucide.createIcons();
  }
});

// 0. THEME TOGGLE (Google Labs / Mistral Light & Antigravity Dark)
function initThemeToggle() {
  const btn = document.getElementById('theme-toggle-btn');
  if (!btn) return;

  const savedTheme = localStorage.getItem('sara_theme');
  if (savedTheme === 'light') {
    document.documentElement.classList.add('light');
  }

  btn.addEventListener('click', () => {
    document.documentElement.classList.toggle('light');
    const isLight = document.documentElement.classList.contains('light');
    localStorage.setItem('sara_theme', isLight ? 'light' : 'dark');
    if (window.lucide) {
      lucide.createIcons();
    }
  });
}

// 0.1 CO-ARCHITECT DRAWER MODAL
function initCoArchitectDrawer() {
  const openBtn = document.getElementById('open-coarchitect-btn');
  const drawer = document.getElementById('coarchitect-drawer');
  const closeBtn = document.getElementById('close-drawer-btn');
  const form = document.getElementById('coarchitect-form');
  if (!drawer) return;

  if (openBtn) {
    openBtn.addEventListener('click', () => drawer.classList.remove('hidden'));
  }
  if (closeBtn) {
    closeBtn.addEventListener('click', () => drawer.classList.add('hidden'));
  }
  drawer.addEventListener('click', (e) => {
    if (e.target === drawer) drawer.classList.add('hidden');
  });
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      alert('Thank you! Your proposed spatial skill has been submitted to the Paris atelier.');
      drawer.classList.add('hidden');
      form.reset();
    });
  }
}


// 1. MCP TABS & QUICK INSTALL
function initMcpTabs() {
  const codeEl = document.getElementById('mcp-code-snippet');
  const copyBtn = document.getElementById('copy-mcp-btn');
  const copyLabel = document.getElementById('copy-mcp-label');
  const tabBtns = document.querySelectorAll('.mcp-tab');

  function setSnippet(key) {
    if (!codeEl) return;
    codeEl.textContent = MCP_CONFIGS[key] || MCP_CONFIGS.claude;
  }

  // Initial set
  setSnippet('claude');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => {
        b.classList.remove('active', 'bg-bronze-600', 'text-white', 'font-semibold');
        b.classList.add('text-slate-400');
      });
      btn.classList.add('active', 'bg-bronze-600', 'text-white', 'font-semibold');
      btn.classList.remove('text-slate-400');

      const target = btn.getAttribute('data-target');
      setSnippet(target);
    });
  });

  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      if (!codeEl) return;
      navigator.clipboard.writeText(codeEl.textContent).then(() => {
        const originalText = copyLabel.textContent;
        copyLabel.textContent = "Copied to Clipboard!";
        copyBtn.classList.add('bg-emerald-600', 'text-white');
        setTimeout(() => {
          copyLabel.textContent = originalText;
          copyBtn.classList.remove('bg-emerald-600', 'text-white');
        }, 2000);
      });
    });
  }
}

// 2. SKILLS SUITE GENERATOR
function initSkillsSuite() {
  const container = document.getElementById('skills-suite-container');
  if (!container) return;

  container.innerHTML = DESIGN_SKILLS_SUITE.map(skill => `
    <div class="rounded-2xl bg-dark-900 border ${skill.active ? 'border-bronze-500/40 shadow-xl shadow-bronze-900/20' : 'border-white/5'} p-6 flex flex-col justify-between hover:border-bronze-400/50 transition group relative overflow-hidden">
      ${skill.active ? '<div class="absolute top-0 right-0 w-24 h-24 bg-bronze-500/10 rounded-full blur-xl pointer-events-none"></div>' : ''}
      <div>
        <div class="flex items-center justify-between gap-2 mb-4">
          <span class="font-mono font-bold text-xs text-bronze-400 tracking-widest">SKILL ${skill.number}</span>
          <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border ${skill.statusBg}">
            <span class="w-1.5 h-1.5 rounded-full ${skill.dotColor} ${skill.active ? 'animate-pulse' : ''}"></span>
            ${skill.status}
          </span>
        </div>

        <h3 class="font-display font-bold text-lg text-white group-hover:text-bronze-300 transition-colors mb-2">
          ${skill.title}
        </h3>

        <p class="text-xs text-slate-400 leading-relaxed mb-6">
          ${skill.desc}
        </p>

        <div class="flex flex-wrap gap-1.5 mb-6">
          ${skill.tags.map(t => `<span class="px-2 py-0.5 rounded bg-dark-800 text-[11px] text-slate-300 border border-white/5 font-mono">${t}</span>`).join('')}
        </div>
      </div>

      <div>
        <a href="${skill.actionLink}" class="w-full py-2.5 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition ${skill.active ? 'bg-gradient-to-r from-bronze-600 to-bronze-500 hover:from-bronze-500 hover:to-bronze-400 text-white shadow-md' : 'bg-dark-800 hover:bg-dark-750 text-slate-300 border border-white/10'}">
          <span>${skill.actionText}</span>
          <i data-lucide="${skill.active ? 'arrow-right' : 'eye'}" class="w-3.5 h-3.5"></i>
        </a>
      </div>
    </div>
  `).join('');
}

// 3. 100-POINT AUDITOR & INTERACTIVE SCORECARD
function initAuditor() {
  const container = document.getElementById('rubric-container');
  if (!container) return;

  container.innerHTML = RUBRIC_DATA.map(cat => `
    <div class="p-6 rounded-2xl bg-dark-900 border border-white/5 space-y-4">
      <div class="flex items-center justify-between border-b border-white/5 pb-3">
        <h3 class="font-display font-bold text-white text-base sm:text-lg">${cat.title}</h3>
        <span class="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-bronze-500/10 text-bronze-300 border border-bronze-500/20">${cat.max_points} pts</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        ${cat.items.map(item => `
          <label class="flex items-start gap-3 p-3 rounded-xl bg-dark-850/80 border border-white/5 hover:border-white/15 cursor-pointer transition select-none">
            <input type="checkbox" id="check-${item.id}" class="rubric-check mt-1 rounded border-slate-700 text-bronze-500 focus:ring-bronze-500 focus:ring-offset-dark-950 w-4 h-4 bg-dark-900" data-id="${item.id}" data-points="${item.points}" data-cat="${cat.id}">
            <div>
              <div class="text-xs font-bold text-white flex items-center justify-between">
                <span>${item.label}</span>
                <span class="text-[11px] text-bronze-400 font-mono">+${item.points}</span>
              </div>
              <p class="text-[11px] text-slate-400 mt-0.5 leading-relaxed">${item.desc}</p>
            </div>
          </label>
        `).join('')}
      </div>
    </div>
  `).join('');

  // Attach change listeners
  document.querySelectorAll('.rubric-check').forEach(cb => {
    cb.addEventListener('change', updateScore);
  });

  // Preset Buttons
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const preset = btn.getAttribute('data-preset');
      applyPreset(preset);
    });
  });

  // Export summary button
  const copySummaryBtn = document.getElementById('copy-audit-summary-btn');
  const copySummaryLabel = document.getElementById('copy-audit-label');
  if (copySummaryBtn) {
    copySummaryBtn.addEventListener('click', () => {
      exportAuditMarkdown(copySummaryLabel);
    });
  }

  // Initial score
  updateScore();
}

function updateScore() {
  let totalScore = 0;
  const catScores = {};
  RUBRIC_DATA.forEach(c => catScores[c.id] = 0);

  document.querySelectorAll('.rubric-check:checked').forEach(cb => {
    const pts = parseInt(cb.getAttribute('data-points'), 10);
    const cat = cb.getAttribute('data-cat');
    totalScore += pts;
    if (catScores[cat] !== undefined) {
      catScores[cat] += pts;
    }
  });

  // Update DOM Elements
  const scoreDisplay = document.getElementById('score-display');
  const circleSvg = document.getElementById('score-circle-svg');
  const gradeBadge = document.getElementById('grade-badge');
  const adviceEl = document.getElementById('score-advice');
  const breakdownEl = document.getElementById('category-breakdown');

  if (scoreDisplay) scoreDisplay.textContent = totalScore;
  
  // Update circular SVG progress
  // Circumference = 2 * PI * 50 = 314.159
  if (circleSvg) {
    const circumference = 314.159;
    const offset = circumference - (totalScore / 100) * circumference;
    circleSvg.style.strokeDashoffset = offset;
    
    // Colorize circle
    if (totalScore >= 90) {
      circleSvg.setAttribute('class', 'score-circle-meter text-emerald-400');
    } else if (totalScore >= 80) {
      circleSvg.setAttribute('class', 'score-circle-meter text-bronze-400');
    } else if (totalScore >= 70) {
      circleSvg.setAttribute('class', 'score-circle-meter text-amber-400');
    } else {
      circleSvg.setAttribute('class', 'score-circle-meter text-red-400');
    }
  }

  let grade = "Unrated";
  let gradeClass = "bg-slate-800 text-slate-300";
  let advice = "";

  if (totalScore >= 90) {
    grade = "Elite Hire (Top 5%)";
    gradeClass = "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
    advice = "Your portfolio demonstrates world-class balance across narrative, tectonic proof, and Swiss typography. Ready for immediate partner-level review at Foster + Partners, BIG, Snøhetta, or Parisian luxury ateliers.";
  } else if (totalScore >= 80) {
    grade = "Competitive Contender";
    gradeClass = "bg-bronze-500/20 text-bronze-300 border border-bronze-500/30";
    advice = "Strong architectural foundation. Reviewers will advance this to the interview pile. To reach Elite status, sharpen your 1:20 wall section callouts and add on-site fabrication proof.";
  } else if (totalScore >= 70) {
    grade = "Needs Constructive Polish";
    gradeClass = "bg-amber-500/20 text-amber-300 border border-amber-500/30";
    advice = "Borderline status. Good visual ideas, but lacking sufficient working drawings and tectonic cotations. Reviewers may diagnose this as 'creative but unbuildable'.";
  } else {
    grade = "Render Trap Alert (<70)";
    gradeClass = "bg-red-500/20 text-red-300 border border-red-500/30";
    advice = "Critical Action Needed: 75% rejection risk in the 15-second scan. Replace 3D perspectives with dimensioned plans, 1:20 wall sections, and adopt a structured layout archetype.";
  }

  if (gradeBadge) {
    gradeBadge.textContent = grade;
    gradeBadge.className = `text-xs font-mono font-semibold px-2.5 py-1 rounded-full ${gradeClass}`;
  }

  if (adviceEl) {
    adviceEl.innerHTML = `
      <div class="font-bold text-white flex items-center gap-1.5 mb-1">
        <i data-lucide="info" class="w-3.5 h-3.5 text-bronze-400"></i>
        <span>Diagnostic: ${grade}</span>
      </div>
      <p class="text-slate-300 leading-relaxed">${advice}</p>
    `;
    if (window.lucide) lucide.createIcons();
  }

  if (breakdownEl) {
    breakdownEl.innerHTML = RUBRIC_DATA.map(c => `
      <div class="space-y-1">
        <div class="flex items-center justify-between text-slate-400 text-[11px] font-mono">
          <span class="truncate max-w-[170px]">${c.title.split('.')[1] || c.title}</span>
          <span class="font-bold text-slate-200">${catScores[c.id]} / ${c.max_points}</span>
        </div>
        <div class="w-full h-1 bg-dark-800 rounded-full overflow-hidden">
          <div class="h-full bg-bronze-500 rounded-full" style="width: ${(catScores[c.id] / c.max_points) * 100}%"></div>
        </div>
      </div>
    `).join('');
  }
}

function applyPreset(preset) {
  // Clear all first
  document.querySelectorAll('.rubric-check').forEach(cb => cb.checked = false);

  if (preset === 'reset') {
    updateScore();
    return;
  }

  if (preset === 'junior') {
    // 83 pts
    const checked = [
      'passports', 'problem_solving', 'scannability', 'hook_pacing', // 20
      'scaled_drawings', 'wall_sections', 'cotations', // 20
      'margins', 'type_scale', 'white_space', 'pacing_rhythm', // 20
      'macro_site', 'meso_building', // 10
      'triptych', 'restraint', // 7
      'pdf_optimization', 'colophon' // 6
    ];
    checked.forEach(id => {
      const el = document.getElementById(`check-${id}`);
      if (el) el.checked = true;
    });
  } else if (preset === 'elite') {
    // 95 pts (all except micro_joinery or real_proof)
    document.querySelectorAll('.rubric-check').forEach(cb => cb.checked = true);
    const uncheck = document.getElementById('check-micro_joinery');
    if (uncheck) uncheck.checked = false;
  } else if (preset === 'rendertrap') {
    // 46 pts (only visuals, no wall sections, no cotations, no code)
    const checked = [
      'hook_pacing', // 5
      'pacing_rhythm', 'white_space', // 10
      'macro_site', // 5
      'triptych', 'lighting', 'restraint', // 10
      'pdf_optimization', 'colophon' // 6
    ];
    checked.forEach(id => {
      const el = document.getElementById(`check-${id}`);
      if (el) el.checked = true;
    });
  }

  updateScore();
}

function exportAuditMarkdown(labelEl) {
  const scoreDisplay = document.getElementById('score-display');
  const gradeBadge = document.getElementById('grade-badge');
  const score = scoreDisplay ? scoreDisplay.textContent : '0';
  const grade = gradeBadge ? gradeBadge.textContent : 'Unrated';

  let md = `# Sara Bensalem Portfolio Audit Report\n\n`;
  md += `**Overall Score:** ${score} / 100 PTS (${grade})\n`;
  md += `**Audited Date:** ${new Date().toISOString().split('T')[0]}\n`;
  md += `**Studio Platform:** https://skills.sarabensalem.com\n\n`;
  md += `## Category Breakdown\n\n`;

  RUBRIC_DATA.forEach(cat => {
    md += `### ${cat.title} (Max ${cat.max_points} pts)\n`;
    cat.items.forEach(item => {
      const el = document.getElementById(`check-${item.id}`);
      const checked = el && el.checked;
      md += `- [${checked ? 'X' : ' '}] **${item.label}** (${item.points} pts) — ${item.desc}\n`;
    });
    md += `\n`;
  });

  navigator.clipboard.writeText(md).then(() => {
    if (labelEl) {
      const orig = labelEl.textContent;
      labelEl.textContent = "Report Copied to Clipboard!";
      setTimeout(() => { labelEl.textContent = orig; }, 2000);
    }
  });
}

// 4. ARCHETYPES GALLERY & FILTERING
function initArchetypes() {
  const grid = document.getElementById('archetypes-grid');
  const filters = document.getElementById('archetype-filters');
  if (!grid) return;

  function renderArchetypes(filter = 'all') {
    const filtered = filter === 'all' 
      ? ARCHETYPES_DATA 
      : ARCHETYPES_DATA.filter(a => a.category.toLowerCase().includes(filter.toLowerCase()));

    grid.innerHTML = filtered.map(a => `
      <div class="p-6 rounded-2xl bg-dark-900 border border-white/5 hover:border-bronze-500/40 transition flex flex-col justify-between group">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-bronze-500/10 text-bronze-300 border border-bronze-500/20">ARCHETYPE ${a.id}</span>
            <span class="text-[11px] text-slate-400 font-medium font-mono">${a.category}</span>
          </div>
          <h3 class="font-display font-bold text-lg text-white mb-2 group-hover:text-bronze-300 transition">${a.title}</h3>
          <p class="text-xs text-slate-400 leading-relaxed mb-4">${a.summary}</p>
          
          <div class="space-y-2 pt-3 border-t border-white/5 text-[11px] font-mono">
            <div class="flex items-center justify-between text-slate-400">
              <span>Budget:</span>
              <span class="font-semibold text-slate-200">${a.budget}</span>
            </div>
            <div class="flex items-center justify-between text-slate-400">
              <span>Format:</span>
              <span class="font-semibold text-slate-200">${a.format}</span>
            </div>
            <div class="text-slate-400 pt-1">
              <span class="block text-slate-500 mb-0.5">Typology Focus:</span>
              <span class="text-bronze-300 font-medium">${a.typology}</span>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-white/5">
          <a href="#framework" class="block w-full py-2 rounded-lg bg-dark-800 hover:bg-bronze-600 text-slate-200 hover:text-white text-center text-xs font-semibold transition">
            View Spread Structure &rarr;
          </a>
        </div>
      </div>
    `).join('');
  }

  renderArchetypes();

  if (filters) {
    filters.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        filters.querySelectorAll('.filter-btn').forEach(b => {
          b.className = "filter-btn text-xs font-mono px-3 py-1.5 rounded-lg bg-dark-850 hover:bg-dark-800 text-slate-300 transition";
        });
        btn.className = "filter-btn active text-xs font-mono px-3 py-1.5 rounded-lg bg-bronze-500 text-white transition";
        renderArchetypes(btn.getAttribute('data-filter'));
      });
    });
  }
}

// 5. 5-ACT SPREAD SIMULATOR
function initSpreadSimulator() {
  const stepsContainer = document.getElementById('act-steps-container');
  const spreadTag = document.getElementById('spread-act-tag');
  const leftWireframe = document.getElementById('wireframe-left');
  const rightWireframe = document.getElementById('wireframe-right');
  if (!stepsContainer) return;

  function renderAct(actIndex) {
    const act = ACTS_DATA[actIndex];
    if (!act) return;

    if (spreadTag) spreadTag.textContent = act.tag;

    // Update Left Wireframe
    if (leftWireframe) {
      leftWireframe.innerHTML = `
        <div class="border-b border-white/10 pb-2 mb-2">
          <span class="text-[9px] font-mono text-bronze-400 uppercase tracking-wider block mb-0.5">Left Spread Plate</span>
          <strong class="text-white text-xs block">${act.leftTitle}</strong>
        </div>
        <div class="space-y-1.5">
          ${act.leftElements.map(e => `
            <div class="p-1.5 rounded bg-dark-900 border border-white/5 text-[10px] text-slate-300 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-bronze-400"></span>
              <span>${e}</span>
            </div>
          `).join('')}
        </div>
        <div class="pt-2 mt-auto border-t border-white/5 text-[9px] text-slate-500 font-mono">
          Swiss Grid: 3-Col Modular Unit
        </div>
      `;
    }

    // Update Right Wireframe
    if (rightWireframe) {
      rightWireframe.innerHTML = `
        <div class="border-b border-white/10 pb-2 mb-2">
          <span class="text-[9px] font-mono text-emerald-400 uppercase tracking-wider block mb-0.5">Right Spread Plate</span>
          <strong class="text-white text-xs block">${act.rightTitle}</strong>
        </div>
        <div class="space-y-1.5">
          ${act.rightElements.map(e => `
            <div class="p-1.5 rounded bg-dark-900 border border-white/5 text-[10px] text-slate-300 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
              <span>${e}</span>
            </div>
          `).join('')}
        </div>
        <div class="pt-2 mt-auto border-t border-white/5 text-[9px] text-slate-500 font-mono">
          Swiss Grid: Hero Display Anchor
        </div>
      `;
    }

    // Update Step Selection Styles
    document.querySelectorAll('.act-step-btn').forEach((b, idx) => {
      if (idx === actIndex) {
        b.className = "act-step-btn active w-full p-3.5 rounded-xl bg-dark-850 border border-bronze-500/50 text-left transition flex items-center justify-between";
        b.querySelector('.act-step-number').className = "act-step-number text-xs font-mono font-bold text-bronze-300";
      } else {
        b.className = "act-step-btn w-full p-3.5 rounded-xl bg-dark-900 border border-white/5 hover:border-white/15 text-left transition flex items-center justify-between";
        b.querySelector('.act-step-number').className = "act-step-number text-xs font-mono font-bold text-slate-400";
      }
    });
  }

  stepsContainer.innerHTML = ACTS_DATA.map((act, idx) => `
    <button class="act-step-btn ${idx === 0 ? 'active border-bronze-500/50 bg-dark-850' : 'bg-dark-900 border-white/5'} w-full p-3.5 rounded-xl border text-left transition flex items-center justify-between" data-index="${idx}">
      <div>
        <span class="act-step-number text-xs font-mono font-bold ${idx === 0 ? 'text-bronze-300' : 'text-slate-400'}">${act.tag.split('—')[0]}</span>
        <h4 class="font-display font-bold text-sm text-white mt-0.5">${act.title.split(':')[1] || act.title}</h4>
      </div>
      <i data-lucide="chevron-right" class="w-4 h-4 text-slate-500"></i>
    </button>
  `).join('');

  stepsContainer.querySelectorAll('.act-step-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = parseInt(btn.getAttribute('data-index'), 10);
      renderAct(idx);
    });
  });

  // Initial render Act 0
  renderAct(0);
}

// 6. LIVE MCP TERMINAL SANDBOX
function initTerminalSimulator() {
  const terminalScreen = document.getElementById('terminal-screen');
  const toolBtns = document.querySelectorAll('.terminal-tool-btn');
  if (!terminalScreen) return;

  const TOOL_RESPONSES = {
    list_skills: `&gt; tools/call {"name": "list_sara_skills"}
&lt; 200 OK (Response time: 42ms)
{
  "active_skills": [
    {
      "id": "portfolio-design",
      "name": "Spatial Portfolio Architecture & Curation",
      "status": "PRODUCTION",
      "deliverables": ["PDF Monographs", "100-pt Audit Rubric", "10 Archetypes", "5-Act Framework"]
    },
    {
      "id": "heritage-adaptive-reuse",
      "name": "Heritage Longère & Vernacular Adaptive Reuse",
      "status": "DEVELOPMENT",
      "deliverables": ["Breton Granite Detailing", "Hempcrete Envelopes", "Truss Consolidation"]
    },
    {
      "id": "interior-joinery-scenography",
      "name": "Interior Joinery & Tactile Scenography",
      "status": "DEVELOPMENT",
      "deliverables": ["1:5 Millwork Blueprints", "Tactile Triptychs", "Luminaire Schedules"]
    }
  ]
}`,
    audit_pdf: `&gt; tools/call {"name": "audit_portfolio", "arguments": {"pdf_path": "sample_portfolio.pdf"}}
&lt; 200 OK (Inspecting PDF binary...)
{
  "filename": "sample_portfolio.pdf",
  "page_count": 48,
  "aspect_ratio": "16:9 Landscape (Consistent)",
  "file_size_mb": 24.8,
  "preliminary_score": 92,
  "status": "ELITE_HIRE_TIER",
  "constructive_proof_found": true,
  "wall_sections_detected": 4,
  "render_trap_risk": "LOW (Constructive proof ratio > 35%)",
  "recommendation": "Passes 30-second hiring screening. Ready for international agency submission."
}`,
    recommend_archetype: `&gt; tools/call {"name": "recommend_archetype", "arguments": {"discipline": "Interior Architecture", "target_firms": "Parisian luxury ateliers"}}
&lt; 200 OK
{
  "matched_archetype": {
    "id": "03_french_luxury_minimalist",
    "name": "The French Luxury Minimalist Book",
    "recommended_page_budget": "28-32 Pages",
    "format": "A4 Landscape",
    "typology_focus": "Parisian High-End Residential & Heritage Longère Ateliers",
    "key_proof_elements": [
      "Monogram branding",
      "Warm greige minimalism",
      "Historic stone longère conversions",
      "Custom bespoke furniture prototype fabrication"
    ]
  }
}`,
    generate_5act: `&gt; tools/call {"name": "generate_5act_structure", "arguments": {"project_name": "Rosetta Coastal Hotel", "typology": "Resort"}}
&lt; 200 OK (Generating 5-act markdown framework...)
{
  "framework": {
    "Act_I": "Project Passport & Mediterranean Wave Dynamic Hero (Spread 1)",
    "Act_II": "Coastal Erosion & Sea Breeze Venting Analysis (Spread 1-2)",
    "Act_III": "Stepped Single-Loaded Terrace Massing & Structural Cores (Spread 2)",
    "Act_IV": "1:20 GFRC Curved Louver Wall Section & Saline Protection Detail (Spread 3)",
    "Act_V": "Twilight Scenography, Infinity Reflection Pool & Diurnal Sun Path (Spread 4)"
  }
}`
  };

  toolBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tool = btn.getAttribute('data-tool');
      const response = TOOL_RESPONSES[tool];
      if (!response) return;

      terminalScreen.innerHTML = `
        <div class="text-slate-500">// Executing simulated tool call via stdio JSON-RPC...</div>
        <div class="text-amber-300 font-semibold mt-2">${response}</div>
        <div class="text-emerald-400 mt-2">&gt; Execution complete. Ready for next query.</div>
      `;
    });
  });
}

// =========================================================================
// 7. PORTFOLIO STITCH STUDIO (Google Stitch for Spatial Portfolios)
// =========================================================================

const STITCH_SPREADS = {
  THE_CONSTRUCTIVE_PROOF: {
    title: "Plate IV: 1:20 Constructive Wall Section & Envelope Detailing",
    prompt: "Act 4: 1:20 Wall Section showing Breton granite masonry, lime-hemp biotamping, triple-glazed thermal breaks, and PMR clearances.",
    score: 100,
    rank: "ELITE HIRE",
    svg: `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FBFBF8; font-family:Inter, sans-serif;">
      <!-- Grid Layer Overlay (Toggled via JS) -->
      <g id="stitch-grid-cols" class="stitch-grid-layer" opacity="0.35">
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
      <g id="stitch-grid-margins" class="stitch-grid-layer">
        <rect x="64" y="64" width="1792" height="952" fill="none" stroke="#FFAF01" stroke-width="1" stroke-opacity="0.4" />
        <!-- Crosshairs -->
        <circle cx="64" cy="64" r="3" fill="#FFAF01" />
        <circle cx="1856" cy="64" r="3" fill="#FFAF01" />
        <circle cx="64" cy="1016" r="3" fill="#FFAF01" />
        <circle cx="1856" cy="1016" r="3" fill="#FFAF01" />
      </g>

      <!-- Folio Header -->
      <text x="64" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470" letter-spacing="1">PROJECT MONOGRAPH: MAISON BRETONNE ADAPTIVE REUSE</text>
      <text x="1856" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#FFAF01" font-weight="700" text-anchor="end">ACT 4 // CONSTRUCTIVE PROOF (1:20)</text>
      <line x1="64" y1="64" x2="1856" y2="64" stroke="#E6E2DA" stroke-width="1" />

      <!-- Left Technical Column: Material Callout Schedule (Cols 1-4) -->
      <g transform="translate(64, 120)">
        <text x="0" y="28" font-family="Inter, sans-serif" font-size="24" font-weight="800" fill="#090B0E">1:20 Wall Section Detail</text>
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

        <!-- Guarantee Stamp -->
        <g transform="translate(0, 680)">
          <rect x="0" y="0" width="560" height="120" fill="#E6E2DA" fill-opacity="0.35" stroke="#E6E2DA" />
          <text x="16" y="28" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="bold" fill="#FFAF01">CONSTRUCTIVE PROOF GUARANTEE</text>
          <text x="16" y="48" font-size="12" fill="#090B0E">Individual Line-Item Work: Envelope detailing &</text>
          <text x="16" y="66" font-size="12" fill="#090B0E">construction administration documentation.</text>
          <text x="16" y="94" font-family="'IBM Plex Mono', monospace" font-size="10" fill="#5C6470">ANTI-RENDER-TRAP COMPLIANT • 100% BUILDABLE</text>
        </g>
      </g>

      <!-- Right Technical Canvas: 1:20 Construction Detailing Plate (Cols 5-12) -->
      <g transform="translate(680, 120)">
        <rect x="0" y="0" width="1176" height="820" fill="#FFFFFF" stroke="#E6E2DA" stroke-width="1" />
        <!-- Floor Slab cut (Reinforced Concrete) -->
        <rect x="180" y="520" width="860" height="130" fill="#EAE6DF" stroke="#090B0E" stroke-width="2.5" />
        <line x1="190" y1="560" x2="1030" y2="560" stroke="#5C6470" stroke-width="1" stroke-dasharray="8 6" />
        <line x1="190" y1="620" x2="1030" y2="620" stroke="#5C6470" stroke-width="1" stroke-dasharray="8 6" />

        <!-- Vertical Exterior Masonry Wall -->
        <rect x="180" y="40" width="180" height="480" fill="#DFD9D0" stroke="#090B0E" stroke-width="2.5" />
        <line x1="180" y1="120" x2="360" y2="120" stroke="#090B0E" stroke-width="1" />
        <line x1="180" y1="200" x2="360" y2="200" stroke="#090B0E" stroke-width="1" />
        <line x1="180" y1="280" x2="360" y2="280" stroke="#090B0E" stroke-width="1" />
        <line x1="180" y1="360" x2="360" y2="360" stroke="#090B0E" stroke-width="1" />
        <line x1="180" y1="440" x2="360" y2="440" stroke="#090B0E" stroke-width="1" />

        <!-- Internal Lime-Hemp Insulation -->
        <rect x="360" y="40" width="120" height="480" fill="#F4EFE6" stroke="#090B0E" stroke-width="1.5" stroke-dasharray="4 2" />
        <!-- Plaster Finish -->
        <rect x="480" y="40" width="20" height="480" fill="#FBFBF8" stroke="#090B0E" stroke-width="1" />

        <!-- Triple Glazed Curtain Wall Profile -->
        <rect x="500" y="160" width="540" height="260" fill="#E8F1F5" fill-opacity="0.4" stroke="#002B49" stroke-width="2" />
        <line x1="500" y1="290" x2="1040" y2="290" stroke="#002B49" stroke-width="2" />
        <text x="770" y="278" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#002B49" text-anchor="middle">TRIPLE GLAZED TIMBER-ALU ENVELOPE // Uw = 0.78 W/m²K</text>

        <!-- Dimension Strings in Mistral Amber -->
        <g stroke="#FFAF01" stroke-width="1.5">
          <line x1="120" y1="40" x2="120" y2="520" />
          <line x1="108" y1="40" x2="132" y2="40" />
          <line x1="108" y1="520" x2="132" y2="520" />
          <line x1="112" y1="44" x2="128" y2="36" stroke-width="2.5" />
          <line x1="112" y1="524" x2="128" y2="516" stroke-width="2.5" />
        </g>
        <text x="100" y="290" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="bold" fill="#FFAF01" text-anchor="middle" transform="rotate(-90 100 290)">4800 MM CLEARANCE</text>

        <!-- Horizontal thickness string -->
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
    </svg>`
  },
  THE_PASSPORT: {
    title: "Plate I: The Project Passport & Individual Attribution",
    prompt: "Act 1: Standardized Project Passport with uncropped site section, line-item attribution, and work rights status.",
    score: 96,
    rank: "ELITE HIRE",
    svg: `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FBFBF8; font-family:Inter, sans-serif;">
      <!-- Grid Layer Overlay -->
      <g id="stitch-grid-cols" class="stitch-grid-layer" opacity="0.35">
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
      <g id="stitch-grid-margins" class="stitch-grid-layer">
        <rect x="64" y="64" width="1792" height="952" fill="none" stroke="#FFAF01" stroke-width="1" stroke-opacity="0.4" />
      </g>
      <text x="64" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">PROJECT PASSPORT DOSSIER // VOL. 01</text>
      <text x="1856" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#FFAF01" font-weight="700" text-anchor="end">ACT 1 // THE HOOK & PASSPORT</text>
      <line x1="64" y1="64" x2="1856" y2="64" stroke="#E6E2DA" stroke-width="1" />

      <!-- Left Column: Passport Metadata (Cols 1-5) -->
      <g transform="translate(64, 120)">
        <text x="0" y="32" font-family="Inter, sans-serif" font-size="36" font-weight="800" fill="#090B0E">Maison Bretonne</text>
        <text x="0" y="64" font-size="15" fill="#5C6470">Vernacular stone longère adaptive reuse w/ bioclimatic pavilion.</text>
        
        <g transform="translate(0, 110)">
          <text x="0" y="0" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="600" fill="#5C6470">TYPOLOGY</text>
          <text x="0" y="18" font-size="13" font-weight="700" fill="#090B0E">Heritage Adaptive Reuse & Contemporary Extension</text>
          <line x1="0" y1="28" x2="680" y2="28" stroke="#E6E2DA" stroke-width="1" />
        </g>
        <g transform="translate(0, 164)">
          <text x="0" y="0" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="600" fill="#5C6470">LOCATION & COORDINATES</text>
          <text x="0" y="18" font-size="13" font-weight="700" fill="#090B0E">Finistère, Brittany, France (48°14'12"N 04°08'44"W)</text>
          <line x1="0" y1="28" x2="680" y2="28" stroke="#E6E2DA" stroke-width="1" />
        </g>
        <g transform="translate(0, 218)">
          <text x="0" y="0" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="600" fill="#5C6470">STAGE & DELIVERY</text>
          <text x="0" y="18" font-size="13" font-weight="700" fill="#090B0E">RIBA Stage 4 / Permis de Construire Obtenu</text>
          <line x1="0" y1="28" x2="680" y2="28" stroke="#E6E2DA" stroke-width="1" />
        </g>
        <g transform="translate(0, 272)">
          <text x="0" y="0" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="600" fill="#5C6470">TEAM SCALE & INDIVIDUAL ROLE</text>
          <text x="0" y="18" font-size="13" font-weight="700" fill="#090B0E">4 Architects • Lead Project Architect & Envelope Detailing</text>
          <line x1="0" y1="28" x2="680" y2="28" stroke="#E6E2DA" stroke-width="1" />
        </g>
        <g transform="translate(0, 326)">
          <text x="0" y="0" font-family="'IBM Plex Mono', monospace" font-size="10" font-weight="600" fill="#5C6470">WORK RIGHTS STATUS</text>
          <text x="0" y="18" font-size="13" font-weight="700" fill="#059669">Permanent EU Citizen // Zero Visa Sponsorship Required</text>
          <line x1="0" y1="28" x2="680" y2="28" stroke="#E6E2DA" stroke-width="1" />
        </g>
      </g>

      <!-- Right Column: Site Section Diagram (Cols 6-12) -->
      <g transform="translate(804, 120)">
        <rect x="0" y="0" width="1052" height="820" fill="#FFFFFF" stroke="#E6E2DA" />
        <!-- Topo Curves -->
        <path d="M 0,380 Q 300,320 600,420 T 1052,360" fill="none" stroke="#E6E2DA" stroke-width="2" />
        <rect x="180" y="240" width="480" height="300" fill="#F4F1EB" stroke="#090B0E" stroke-width="2.5" />
        <polygon points="180,240 420,120 660,240" fill="#E4DEC8" stroke="#090B0E" stroke-width="2.5" />
        <rect x="660" y="290" width="280" height="250" fill="#E8F1F5" fill-opacity="0.5" stroke="#002B49" stroke-width="2" />
        <text x="210" y="320" font-family="'IBM Plex Mono', monospace" font-size="13" font-weight="bold" fill="#FFAF01">CONSOLIDATED GRANITE</text>
        <text x="680" y="340" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#002B49">GLAZED PAVILION</text>
      </g>
      <line x1="64" y1="1008" x2="1856" y2="1008" stroke="#E6E2DA" stroke-width="1" />
      <text x="64" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">SWISS 12-COLUMN MODULAR SYSTEM</text>
      <text x="1856" y="1034" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#090B0E" text-anchor="end">SPREAD 01</text>
    </svg>`
  },
  THE_SPATIAL_ANATOMY: {
    title: "Plate III: 1:100 Ground Floor Spatial Anatomy",
    prompt: "Act 3: Scaled 1:100 Ground Floor Plan with structural columns, PMR corridor clearances, and programmatic fills.",
    score: 94,
    rank: "ELITE HIRE",
    svg: `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FBFBF8; font-family:Inter, sans-serif;">
      <text x="64" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">PROJECT: MAISON BRETONNE // SCALE 1:100 @ A3</text>
      <text x="1856" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#FFAF01" font-weight="700" text-anchor="end">ACT 3 // SPATIAL ANATOMY</text>
      <line x1="64" y1="64" x2="1856" y2="64" stroke="#E6E2DA" stroke-width="1" />

      <rect x="64" y="100" width="1792" height="840" fill="#FFFFFF" stroke="#E6E2DA" />
      <rect x="220" y="240" width="1480" height="560" fill="none" stroke="#090B0E" stroke-width="2.5" />
      <line x1="680" y1="240" x2="680" y2="800" stroke="#090B0E" stroke-width="2.5" />
      <line x1="1220" y1="240" x2="1220" y2="800" stroke="#090B0E" stroke-width="2.5" />

      <text x="450" y="520" font-size="18" font-weight="800" fill="#090B0E" text-anchor="middle">ATELIER PUBLIC / CAFE</text>
      <text x="450" y="546" font-family="'IBM Plex Mono', monospace" font-size="12" fill="#5C6470" text-anchor="middle">140 m² • 1500MM PMR CIRCULATION</text>

      <text x="950" y="520" font-size="18" font-weight="800" fill="#090B0E" text-anchor="middle">CENTRAL GLAZED CLOISTER</text>
      <text x="950" y="546" font-family="'IBM Plex Mono', monospace" font-size="12" fill="#FFAF01" font-weight="bold" text-anchor="middle">BIO-MICROCLIMATE CORE</text>

      <text x="1460" y="520" font-size="18" font-weight="800" fill="#090B0E" text-anchor="middle">VERNACULAR RESIDENCE</text>
      <text x="1460" y="546" font-family="'IBM Plex Mono', monospace" font-size="12" fill="#5C6470" text-anchor="middle">180 m² • RESTORED TIMBER FRAME</text>

      <line x1="64" y1="1008" x2="1856" y2="1008" stroke="#E6E2DA" stroke-width="1" />
      <text x="64" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">SCALE BAR 1:100 // ACCESSIBILITY COMPLIANT</text>
      <text x="1856" y="1034" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#090B0E" text-anchor="end">SPREAD 03</text>
    </svg>`
  },
  THE_ENVIRONMENTAL_ENGINE: {
    title: "Plate II: Bioclimatic Microclimate Modeling",
    prompt: "Act 2: Environmental flow modeling with vector sun path arc, prevailing wind vectors, and thermal stack discharge.",
    score: 95,
    rank: "ELITE HIRE",
    svg: `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FBFBF8; font-family:Inter, sans-serif;">
      <text x="64" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">MICROCLIMATE FLOW MODELING // VOL. 01</text>
      <text x="1856" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#FFAF01" font-weight="700" text-anchor="end">ACT 2 // ENVIRONMENTAL ENGINE</text>
      <line x1="64" y1="64" x2="1856" y2="64" stroke="#E6E2DA" stroke-width="1" />

      <rect x="64" y="100" width="1792" height="840" fill="#FFFFFF" stroke="#E6E2DA" />
      <path d="M 160,720 Q 960,80 1760,720" fill="none" stroke="#FFAF01" stroke-width="3" stroke-dasharray="8 4" />
      <circle cx="680" cy="240" r="32" fill="#FFAF01" />
      <text x="680" y="246" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#FBFBF8" text-anchor="middle">SUMMER +68°</text>

      <polygon points="500,720 500,440 960,300 1420,440 1420,720" fill="#F0EDE6" stroke="#090B0E" stroke-width="2.5" />
      <path d="M 200,600 Q 400,580 580,560 T 960,380" fill="none" stroke="#002B49" stroke-width="3.5" />
      <text x="320" y="570" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#002B49">PREVAILING S-W BREEZE (4.2 m/s)</text>
      <text x="960" y="360" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#002B49">THERMAL STACK EFFECT</text>

      <line x1="64" y1="1008" x2="1856" y2="1008" stroke="#E6E2DA" stroke-width="1" />
      <text x="64" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">PASSIVE SOLAR REDUCTION: 34% HEATING DEMAND SAVINGS</text>
      <text x="1856" y="1034" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#090B0E" text-anchor="end">SPREAD 02</text>
    </svg>`
  },
  THE_TECTONIC_TRIPTYCH: {
    title: "Plate V: 1:5 Bespoke Joinery Details & Material Triptych",
    prompt: "Act 5: 1:5 joinery fabrication details, shadow reveal tolerances, bush-hammered granite plinth, and marine zinc cladding.",
    score: 98,
    rank: "ELITE HIRE",
    svg: `<svg viewBox="0 0 1920 1080" width="100%" height="100%" style="background:#FBFBF8; font-family:Inter, sans-serif;">
      <text x="64" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">TECTONIC FABRICATION // VOL. 01</text>
      <text x="1856" y="48" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#FFAF01" font-weight="700" text-anchor="end">ACT 5 // 1:5 JOINERY & MATERIAL TRIPTYCH</text>
      <line x1="64" y1="64" x2="1856" y2="64" stroke="#E6E2DA" stroke-width="1" />

      <!-- Panel 1 -->
      <g transform="translate(64, 120)">
        <rect x="0" y="0" width="560" height="820" fill="#FFFFFF" stroke="#E6E2DA" />
        <rect x="40" y="40" width="480" height="420" fill="#D7C4A5" stroke="#090B0E" stroke-width="2" />
        <rect x="440" y="140" width="12" height="180" fill="#090B0E" />
        <text x="40" y="520" font-size="18" font-weight="bold" fill="#090B0E">01. 8mm Shadow Reveal</text>
        <text x="40" y="550" font-size="13" fill="#5C6470">Solid French Oak Joinery w/ Blum Clip-Top tolerances</text>
      </g>
      <!-- Panel 2 -->
      <g transform="translate(680, 120)">
        <rect x="0" y="0" width="560" height="820" fill="#FFFFFF" stroke="#E6E2DA" />
        <rect x="40" y="40" width="480" height="420" fill="#C2BBB0" stroke="#090B0E" stroke-width="2" />
        <circle cx="160" cy="180" r="2.5" fill="#5C6470" />
        <circle cx="260" cy="240" r="3" fill="#5C6470" />
        <circle cx="360" cy="160" r="2.5" fill="#5C6470" />
        <text x="40" y="520" font-size="18" font-weight="bold" fill="#090B0E">02. Bush-Hammered Granite</text>
        <text x="40" y="550" font-size="13" fill="#5C6470">Tactile rusticated plinth resisting water splash-back</text>
      </g>
      <!-- Panel 3 -->
      <g transform="translate(1296, 120)">
        <rect x="0" y="0" width="560" height="820" fill="#FFFFFF" stroke="#E6E2DA" />
        <rect x="40" y="40" width="480" height="420" fill="#9DA7B2" stroke="#090B0E" stroke-width="2" />
        <line x1="120" y1="40" x2="120" y2="460" stroke="#090B0E" stroke-width="2.5" />
        <line x1="240" y1="40" x2="240" y2="460" stroke="#090B0E" stroke-width="2.5" />
        <line x1="360" y1="40" x2="360" y2="460" stroke="#090B0E" stroke-width="2.5" />
        <text x="40" y="520" font-size="18" font-weight="bold" fill="#090B0E">03. Pre-Weathered Zinc</text>
        <text x="40" y="550" font-size="13" fill="#5C6470">Standing seam roof cladding w/ ventilated air gap</text>
      </g>

      <line x1="64" y1="1008" x2="1856" y2="1008" stroke="#E6E2DA" stroke-width="1" />
      <text x="64" y="1034" font-family="'IBM Plex Mono', monospace" font-size="11" fill="#5C6470">MATERIALITY & TACTILE CRAFT DOSSIER</text>
      <text x="1856" y="1034" font-family="'IBM Plex Mono', monospace" font-size="12" font-weight="bold" fill="#090B0E" text-anchor="end">SPREAD 05</text>
    </svg>`
  }
};

function initPortfolioStitchStudio() {
  const viewport = document.getElementById('stitch-canvas-viewport');
  const promptInput = document.getElementById('stitch-prompt-input');
  const generateBtn = document.getElementById('stitch-generate-btn');
  const auditScoreEl = document.getElementById('stitch-audit-score');
  const variantsContainer = document.getElementById('stitch-variants-container');
  const archetypeTabs = document.querySelectorAll('.stitch-archetype-tab');
  const chipBtns = document.querySelectorAll('.stitch-chip-btn');
  const rangeBtns = document.querySelectorAll('.stitch-range-btn');
  
  const toggleCols = document.getElementById('stitch-toggle-cols');
  const toggleMargins = document.getElementById('stitch-toggle-margins');
  const exportSvgBtn = document.getElementById('stitch-export-svg-btn');
  const openPrintBtn = document.getElementById('stitch-open-print-btn');

  if (!viewport) return;

  let currentArch = "THE_CONSTRUCTIVE_PROOF";
  let currentRange = "REFINE";
  let showCols = true;
  let showMargins = true;

  function renderSpread(archKey) {
    const spread = STITCH_SPREADS[archKey] || STITCH_SPREADS.THE_CONSTRUCTIVE_PROOF;
    currentArch = archKey;
    viewport.innerHTML = spread.svg;

    if (auditScoreEl) {
      auditScoreEl.textContent = `${spread.score} / 100 PTS (${spread.rank})`;
    }

    // Apply overlay visibility
    updateOverlays();

    // Render variants for current archetype
    renderVariants(spread);
  }

  function updateOverlays() {
    const cols = viewport.querySelector('#stitch-grid-cols');
    const margins = viewport.querySelector('#stitch-grid-margins');
    if (cols) cols.style.display = showCols ? 'block' : 'none';
    if (margins) margins.style.display = showMargins ? 'block' : 'none';
  }

  function renderVariants(baseSpread) {
    if (!variantsContainer) return;
    const variants = [
      { id: "var-1", name: "Variant 1: Swiss Refine", desc: "Tighter 16-col baseline snap & 4pt micro-typography", score: 100, arch: currentArch },
      { id: "var-2", name: "Variant 2: Plan Exploration", desc: "Dual spatial anatomy & 1:100 circulation overlay", score: 95, arch: "THE_SPATIAL_ANATOMY" },
      { id: "var-3", name: "Variant 3: Dark Atelier", desc: "High-contrast dark titanium tectonic presentation", score: 98, arch: "THE_TECTONIC_TRIPTYCH" }
    ];

    variantsContainer.innerHTML = variants.map((v, i) => `
      <div class="stitch-variant-card p-3 rounded-xl bg-dark-950 border ${i === 0 ? 'active border-amber-500/80 bg-dark-850' : 'border-white/5'} transition flex items-center justify-between" data-arch="${v.arch}">
        <div>
          <span class="text-[10px] font-mono font-bold text-amber-400 block">${v.name}</span>
          <span class="text-[11px] text-slate-400 leading-tight block mt-0.5">${v.desc}</span>
        </div>
        <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-bold">${v.score}</span>
      </div>
    `).join('');

    variantsContainer.querySelectorAll('.stitch-variant-card').forEach(card => {
      card.addEventListener('click', () => {
        variantsContainer.querySelectorAll('.stitch-variant-card').forEach(c => {
          c.classList.remove('active', 'border-amber-500/80', 'bg-dark-850');
          c.classList.add('border-white/5');
        });
        card.classList.add('active', 'border-amber-500/80', 'bg-dark-850');
        card.classList.remove('border-white/5');

        const targetArch = card.getAttribute('data-arch');
        renderSpread(targetArch);
      });
    });
  }

  // Archetype tab switching
  archetypeTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      archetypeTabs.forEach(t => {
        t.classList.remove('active', 'bg-amber-500', 'text-slate-950', 'font-bold');
        t.classList.add('bg-dark-900', 'text-slate-300');
      });
      tab.classList.add('active', 'bg-amber-500', 'text-slate-950', 'font-bold');
      tab.classList.remove('bg-dark-900', 'text-slate-300');

      const arch = tab.getAttribute('data-arch');
      if (promptInput && STITCH_SPREADS[arch]) {
        promptInput.value = STITCH_SPREADS[arch].prompt;
      }
      renderSpread(arch);
    });
  });

  // Quick preset chips
  chipBtns.forEach(chip => {
    chip.addEventListener('click', () => {
      const p = chip.getAttribute('data-preset');
      if (p === 'wall_section') {
        renderSpread('THE_CONSTRUCTIVE_PROOF');
        if (promptInput) promptInput.value = STITCH_SPREADS.THE_CONSTRUCTIVE_PROOF.prompt;
      } else if (p === 'passport') {
        renderSpread('THE_PASSPORT');
        if (promptInput) promptInput.value = STITCH_SPREADS.THE_PASSPORT.prompt;
      } else if (p === 'plan') {
        renderSpread('THE_SPATIAL_ANATOMY');
        if (promptInput) promptInput.value = STITCH_SPREADS.THE_SPATIAL_ANATOMY.prompt;
      } else if (p === 'bioclimatic') {
        renderSpread('THE_ENVIRONMENTAL_ENGINE');
        if (promptInput) promptInput.value = STITCH_SPREADS.THE_ENVIRONMENTAL_ENGINE.prompt;
      }
    });
  });

  // Range buttons
  rangeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      rangeBtns.forEach(b => {
        b.classList.remove('active', 'bg-amber-500', 'text-slate-950', 'font-bold');
        b.classList.add('text-slate-400');
      });
      btn.classList.add('active', 'bg-amber-500', 'text-slate-950', 'font-bold');
      btn.classList.remove('text-slate-400');
      currentRange = btn.getAttribute('data-range');
      renderVariants(STITCH_SPREADS[currentArch]);
    });
  });

  // Toggle Grid Overlays
  if (toggleCols) {
    toggleCols.addEventListener('click', () => {
      showCols = !showCols;
      toggleCols.className = showCols
        ? "px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-semibold transition"
        : "px-2.5 py-1 rounded bg-dark-800 text-slate-400 border border-white/5 font-semibold transition";
      updateOverlays();
    });
  }

  if (toggleMargins) {
    toggleMargins.addEventListener('click', () => {
      showMargins = !showMargins;
      toggleMargins.className = showMargins
        ? "px-2.5 py-1 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-semibold transition"
        : "px-2.5 py-1 rounded bg-dark-800 text-slate-400 border border-white/5 font-semibold transition";
      updateOverlays();
    });
  }

  // Generate Button Animation
  if (generateBtn) {
    generateBtn.addEventListener('click', () => {
      const originalText = generateBtn.innerHTML;
      generateBtn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i><span>Synthesizing Vector Spread...</span>`;
      generateBtn.disabled = true;

      setTimeout(() => {
        renderSpread(currentArch);
        generateBtn.innerHTML = `<i data-lucide="check" class="w-4 h-4 text-emerald-400"></i><span>Spread Generated!</span>`;
        if (window.lucide) lucide.createIcons();

        setTimeout(() => {
          generateBtn.innerHTML = originalText;
          generateBtn.disabled = false;
          if (window.lucide) lucide.createIcons();
        }, 1500);
      }, 700);
    });
  }

  // Export SVG
  if (exportSvgBtn) {
    exportSvgBtn.addEventListener('click', () => {
      const svgData = viewport.innerHTML;
      const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sara_bensalem_monograph_${currentArch.toLowerCase()}.svg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  // Open Print View
  if (openPrintBtn) {
    openPrintBtn.addEventListener('click', () => {
      const svgData = viewport.innerHTML;
      const printWin = window.open('', '_blank');
      printWin.document.write(`<!DOCTYPE html>
<html>
<head>
  <title>Sara Bensalem Monograph Spread — 16:9 Landscape</title>
  <style>
    @page { size: landscape; margin: 0; }
    body { margin: 0; padding: 0; background: #EAEAEA; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    .print-canvas { width: 100vw; height: 56.25vw; max-height: 100vh; max-width: 177.78vh; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
    svg { width: 100%; height: 100%; display: block; }
  </style>
</head>
<body>
  <div class="print-canvas">${svgData}</div>
  <script>window.onload = function() { window.print(); };</script>
</body>
</html>`);
      printWin.document.close();
    });
  }

  // Initial render
  renderSpread("THE_CONSTRUCTIVE_PROOF");
}

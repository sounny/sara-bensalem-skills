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
  initMcpTabs();
  initSkillsSuite();
  initAuditor();
  initArchetypes();
  initSpreadSimulator();
  initTerminalSimulator();
  
  if (window.lucide) {
    lucide.createIcons();
  }
});

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

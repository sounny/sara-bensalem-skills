// Sara Bensalem Skills Application Logic
document.addEventListener('DOMContentLoaded', () => {
  initSkillsSuite();
  initAuditor();
  initArchetypes();
  initCopyButtons();
});

// RUBRIC DATA DEFINITION
const RUBRIC_DATA = [
  {
    id: "narrative_curation",
    title: "1. Narrative & Strategic Curation",
    max_points: 20,
    items: [
      { id: "p1", points: 5, label: "Project Passport Clarity", desc: "Clear Title, Location, Role, Typology, and Software Matrix on spread 1." },
      { id: "p2", points: 5, label: "Problem-Solution Arc", desc: "Explicitly states the spatial/climatic conflict, not just visual forms." },
      { id: "p3", points: 5, label: "Scannable Typography", desc: "Headings, short blurbs, and callouts readable within 30 seconds." },
      { id: "p4", points: 5, label: "First-Spread Pacing & Hook", desc: "First spread immediately hooks the reviewer with decisive clarity." }
    ]
  },
  {
    id: "constructive_rigor",
    title: "2. Constructive Rigor & Technical Proof (Anti-Trap)",
    max_points: 25,
    items: [
      { id: "p5", points: 10, label: "Scaled Technical Plans", desc: "Scaled CAD plans (1:20 to 1:100) with calibrated lineweights." },
      { id: "p6", points: 5, label: "Layered Wall Sections", desc: "Wall sections showing waterproofing, insulation, and mechanical anchors." },
      { id: "p7", points: 5, label: "Legible Dimension Chains", desc: "Accurate cotations, level markers (NGF/TN), and graphic scale bars." },
      { id: "p8", points: 5, label: "Accessibility & Code Compliance", desc: "PMR/ADA turning circles, egress corridors, and MEP coordination." }
    ]
  },
  {
    id: "swiss_grid",
    title: "3. Layout, Typography & Swiss Grid Discipline",
    max_points: 20,
    items: [
      { id: "p9", points: 5, label: "Consistent Multi-Column Grid", desc: "Unified margin and baseline grid across all spreads." },
      { id: "p10", points: 5, label: "Disciplined Type Hierarchy", desc: "Max 2 font families and 3 weight variations across the book." },
      { id: "p11", points: 5, label: "Generous White Space", desc: "At least 30-35% negative space avoiding claustrophobic clutter." },
      { id: "p12", points: 5, label: "Visual Rhythm", desc: "Rhythmic balance between full-bleed hero spreads and dense technical plates." }
    ]
  },
  {
    id: "multi_scale",
    title: "4. Multi-Scale Spatial Fluency",
    max_points: 15,
    items: [
      { id: "p13", points: 5, label: "Macro Urban Context", desc: "Site plans, topography contours, transit networks, or regional context." },
      { id: "p14", points: 5, label: "Meso Architectural Scale", desc: "Building volumes, massing evolution diagrams, and spatial circulation." },
      { id: "p15", points: 5, label: "Micro Joinery / Product Detail", desc: "Bespoke joinery, lighting prototype, or tectonic hardware joint." }
    ]
  },
  {
    id: "materiality",
    title: "5. Materiality, Light & Sensory Quality",
    max_points: 10,
    items: [
      { id: "p16", points: 3, label: "Tactile Material Triptych", desc: "Physical texture swatches, tactile finishes, or sample boards." },
      { id: "p17", points: 3, label: "Lighting Scenography", desc: "Deliberate daylight penetration and day vs. night artificial lighting." },
      { id: "p18", points: 4, label: "Restrained Color Palette", desc: "Warm greiges, noble minerals, and muted natural tones (no neon saturation)." }
    ]
  },
  {
    id: "professional_delivery",
    title: "6. Professional Validation & Delivery",
    max_points: 10,
    items: [
      { id: "p19", points: 3, label: "Optimized Binary PDF", desc: "Crisp vector lines and file size under 50 MB to prevent email bounce." },
      { id: "p20", points: 4, label: "Real-World Execution Proof", desc: "On-site photos, built freelance work, competition awards, or honors." },
      { id: "p21", points: 3, label: "Clean Colophon & Contact", desc: "Professional contact details, CV matrix, and software skill badges." }
    ]
  }
];

// ARCHETYPES DEFINITION
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

// INITIALIZE AUDITOR
// DESIGN SKILLS SUITE DATA
const DESIGN_SKILLS_SUITE = [
  {
    id: "portfolio-design",
    number: "01",
    title: "Spatial Portfolio Architecture & Curation",
    status: "Available Now",
    statusBg: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    dotColor: "bg-emerald-400",
    badge: "Flagship Skill",
    desc: "Swiss editorial typography, 10 layout archetypes, 5-act case study structure, and 100-point audit rubric to eliminate render traps.",
    tags: ["InDesign / Figma", "Swiss Grid", "PDF Curation", "Interactive Auditor"],
    actionText: "Explore Skill & Auditor",
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
    tags: ["Heritage Masonry", "Thermal Envelope", "PMR Standards", "Adaptive Reuse"],
    actionText: "Request Early Access",
    actionLink: "#storefront",
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
    actionText: "Request Early Access",
    actionLink: "#storefront",
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
    actionText: "Request Early Access",
    actionLink: "#storefront",
    active: false
  }
];

function initSkillsSuite() {
  const container = document.getElementById('skills-suite-container');
  if (!container) return;

  container.innerHTML = DESIGN_SKILLS_SUITE.map(skill => `
    <div class="rounded-2xl bg-dark-900 border ${skill.active ? 'border-brand-500/40 shadow-xl shadow-brand-900/20' : 'border-slate-800'} p-6 flex flex-col justify-between hover:border-brand-400/60 transition group relative overflow-hidden">
      ${skill.active ? '<div class="absolute top-0 right-0 w-24 h-24 bg-brand-500/10 rounded-full blur-xl pointer-events-none"></div>' : ''}
      <div>
        <div class="flex items-center justify-between gap-2 mb-4">
          <span class="font-display font-bold text-xs text-brand-400 tracking-widest">SKILL ${skill.number}</span>
          <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border ${skill.statusBg}">
            <span class="w-1.5 h-1.5 rounded-full ${skill.dotColor} ${skill.active ? 'animate-pulse' : ''}"></span>
            ${skill.status}
          </span>
        </div>

        <h3 class="font-display font-bold text-lg text-white group-hover:text-brand-300 transition-colors mb-2">
          ${skill.title}
        </h3>

        <p class="text-xs text-slate-400 leading-relaxed mb-6">
          ${skill.desc}
        </p>

        <div class="flex flex-wrap gap-1.5 mb-6">
          ${skill.tags.map(t => `<span class="px-2 py-0.5 rounded bg-dark-800 text-[11px] text-slate-300 border border-slate-700/60">${t}</span>`).join('')}
        </div>
      </div>

      <div>
        <a href="${skill.actionLink}" class="w-full py-2.5 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 transition ${skill.active ? 'bg-brand-600 hover:bg-brand-500 text-white shadow-md shadow-brand-600/30' : 'bg-dark-800 hover:bg-dark-750 text-slate-300 border border-slate-700'}">
          <span>${skill.actionText}</span>
          <i data-lucide="${skill.active ? 'arrow-right' : 'bell'}" class="w-3.5 h-3.5"></i>
        </a>
      </div>
    </div>
  `).join('');

  if (window.lucide) {
    lucide.createIcons();
  }
}


function initAuditor() {
  const container = document.getElementById('rubric-container');
  if (!container) return;

  container.innerHTML = RUBRIC_DATA.map(cat => `
    <div class="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
        <h3 class="font-display font-bold text-white text-base sm:text-lg">${cat.title}</h3>
        <span class="text-xs font-semibold px-2 py-0.5 rounded bg-brand-500/10 text-brand-300 border border-brand-500/20">${cat.max_points} pts</span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        ${cat.items.map(item => `
          <label class="flex items-start gap-3 p-3 rounded-xl bg-dark-900 border border-slate-800/80 hover:border-slate-700 cursor-pointer transition select-none">
            <input type="checkbox" class="rubric-check mt-1 rounded border-slate-700 text-brand-500 focus:ring-brand-500 focus:ring-offset-dark-950 w-4 h-4" data-points="${item.points}" data-cat="${cat.id}">
            <div>
              <div class="text-xs font-bold text-white flex items-center justify-between">
                <span>${item.label}</span>
                <span class="text-[11px] text-brand-400 font-mono">+${item.points}</span>
              </div>
              <p class="text-[11px] text-slate-400 mt-0.5">${item.desc}</p>
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

  // Update DOM
  const scoreDisplay = document.getElementById('score-display');
  const progressBar = document.getElementById('score-progress');
  const gradeBadge = document.getElementById('grade-badge');
  const adviceEl = document.getElementById('score-advice');
  const breakdownEl = document.getElementById('category-breakdown');

  if (scoreDisplay) scoreDisplay.textContent = totalScore;
  if (progressBar) progressBar.style.width = `${totalScore}%`;

  let grade = "Unrated";
  let gradeClass = "bg-slate-800 text-slate-300";
  let advice = "";

  if (totalScore >= 90) {
    grade = "Elite Hire (Top 5%)";
    gradeClass = "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
    advice = "Exceptional portfolio. Your work demonstrates complete multi-scale agility, rigorous constructive proof, and Swiss grid discipline.";
  } else if (totalScore >= 80) {
    grade = "Competitive (Top 20%)";
    gradeClass = "bg-blue-500/20 text-blue-300 border border-blue-500/30";
    advice = "Strong foundation. Sharpen your wall section callouts and ensure white space is at least 30% on complex technical spreads.";
  } else if (totalScore >= 65) {
    grade = "Needs Polish";
    gradeClass = "bg-amber-500/20 text-amber-300 border border-amber-500/30";
    advice = "Warning: Reviewers may flag render trap hazards. Add scaled CAD working drawings ($1:20-1:50) and reduce dense narrative blocks.";
  } else {
    grade = "Critical Redline Traps";
    gradeClass = "bg-red-500/20 text-red-300 border border-red-500/30";
    advice = "Critical Action Needed: High rejection risk in the 15-second scan. Adopt a proven layout archetype and add constructive proof immediately.";
  }

  if (gradeBadge) {
    gradeBadge.textContent = grade;
    gradeBadge.className = `text-xs font-semibold px-2.5 py-1 rounded-full ${gradeClass}`;
  }

  if (adviceEl) {
    adviceEl.innerHTML = `
      <div class="font-bold text-white flex items-center gap-1.5">
        <i data-lucide="info" class="w-3.5 h-3.5 text-brand-400"></i> ${grade}
      </div>
      <p>${advice}</p>
    `;
    if (window.lucide) lucide.createIcons();
  }

  if (breakdownEl) {
    breakdownEl.innerHTML = RUBRIC_DATA.map(c => `
      <div class="flex items-center justify-between text-slate-400">
        <span class="truncate max-w-[180px]">${c.title.split('.')[1] || c.title}</span>
        <span class="font-mono font-bold text-slate-200">${catScores[c.id]} / ${c.max_points}</span>
      </div>
    `).join('');
  }
}

// INITIALIZE ARCHETYPES GALLERY
function initArchetypes() {
  const grid = document.getElementById('archetypes-grid');
  const filters = document.getElementById('archetype-filters');
  if (!grid) return;

  function renderArchetypes(filter = 'all') {
    const filtered = filter === 'all' 
      ? ARCHETYPES_DATA 
      : ARCHETYPES_DATA.filter(a => a.category.toLowerCase().includes(filter.toLowerCase()));

    grid.innerHTML = filtered.map(a => `
      <div class="p-6 rounded-2xl bg-dark-900 border border-slate-800 hover:border-brand-500/40 transition flex flex-col justify-between group">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-brand-500/10 text-brand-300 border border-brand-500/20">ARCHETYPE ${a.id}</span>
            <span class="text-[11px] text-slate-400 font-medium">${a.category}</span>
          </div>
          <h3 class="font-display font-bold text-lg text-white mb-2 group-hover:text-brand-300 transition">${a.title}</h3>
          <p class="text-xs text-slate-400 leading-relaxed mb-4">${a.summary}</p>
          
          <div class="space-y-2 pt-3 border-t border-slate-800/80 text-[11px]">
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
              <span class="text-brand-300 font-medium">${a.typology}</span>
            </div>
          </div>
        </div>

        <div class="mt-6 pt-4 border-t border-slate-800/60">
          <a href="#storefront" class="block w-full py-2 rounded-lg bg-dark-800 hover:bg-brand-600 text-slate-200 hover:text-white text-center text-xs font-semibold transition">
            Use This Template &rarr;
          </a>
        </div>
      </div>
    `).join('');
  }

  renderArchetypes();

  if (filters) {
    filters.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        filters.querySelectorAll('.filter-btn').forEach(b => {
          b.className = "filter-btn text-xs font-semibold px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-700 text-slate-300 transition";
        });
        btn.className = "filter-btn active text-xs font-semibold px-3 py-1.5 rounded-lg bg-brand-500 text-white transition";
        renderArchetypes(btn.getAttribute('data-filter'));
      });
    });
  }
}

// COPY BUTTONS
function initCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-copy');
      const el = document.getElementById(targetId);
      if (el) {
        navigator.clipboard.writeText(el.innerText || el.textContent).then(() => {
          const original = btn.innerHTML;
          btn.innerHTML = `<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> Copied!`;
          if (window.lucide) lucide.createIcons();
          setTimeout(() => {
            btn.innerHTML = original;
            if (window.lucide) lucide.createIcons();
          }, 2000);
        });
      }
    });
  });
}

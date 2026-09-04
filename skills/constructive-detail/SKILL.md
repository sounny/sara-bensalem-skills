---
name: constructive-detail
description: >-
  Draws publication-grade 1:20 constructive wall sections with calibrated lineweights,
  continuous thermal breaks, EPDM flashings, and hygrothermal calculations (U-value, condensation dew points)
  to establish undeniable constructive competence and eliminate the 3D render trap.
author: Sara Bensalem <sara@sarabensalem.com>
website: https://skills.sarabensalem.com
github: https://github.com/sounny/sara-bensalem-skills
---

# Constructive Detail (`/constructive-detail`)
### *The Anti-Render-Trap 1:20 Wall Section & Construction Detailing Engine*
**Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]**

> *"When a technical partner opens your portfolio, they do not admire your Lumion sky. They zoom straight into the parapet, the plinth, and the window sill. If the thermal break is missing, the candidate is discarded."*

`constructive-detail` is the constructive proof engine of Sara Bensalem Skills. It equips AI agents with the ability to compute, detail, and compile **1:20 buildable wall assemblies**, eliminating the fatal "render trap" that causes 75% of architectural portfolio rejections.

---

## 🏛️ The Constructive Hierarchy & Drafting Standards

### 1. Calibrated Drafting Lineweights (ISO / DIN Standard):
- **0.50mm (Solid Dark Graphite `#111110`)**: Heavy primary cut lines through loadbearing structural elements (concrete floor slab, timber columns, masonry ashlar).
- **0.25mm (Medium `#55544E`)**: Secondary assembly boundaries, window profiles, and insulation bounding boxes.
- **0.13mm (Hairline `#84827A` / `#DDD9D0`)**: Material hatching, vapor barriers, air cavities, and dimension projection strings.
- **Dashed `#111110` (Stroke 1.2px, Dash `4 2`)**: Acoustic seals, elastomeric EPDM waterproofing flashings, and structural thermal breaks.

### 2. Standard Multi-Layer Wall Assembly:
Every 1:20 constructive wall section follows a verified hygrothermal sequence from exterior to interior:
1. **Rainscreen Outer Leaf**: 180mm Breton Granite Ashlar with recessed breathable lime joints.
2. **Ventilated Drainage Cavity**: 40mm continuous ventilation zone with weep holes and insect mesh.
3. **Breather Membrane**: Micro-perforated water-resistant barrier ($S_d \le 0.05\text{ m}$).
4. **Hygrothermal Monolithic Core**: 140mm Lime-Hemp Biotamping ($\\lambda = 0.076\text{ W/m}\\cdot\\text{K}$, vapor-open $\\mu = 5\\text{--}10$).
5. **Continuous Thermal Break & EPDM Flashing**: Plinth threshold decoupling preventing capillary rise.
6. **Primary Mass Timber Structure**: 160x280 French Oak Glulam column / lintel bents (Eurocode 5).
7. **Triple-Glazed Fenestration Unit**: $U_w \le 0.78\text{ W/m}^2\\cdot\\text{K}$ with insulated warm-edge perimeter seal.
8. **Interior Finish**: 15mm breathable lime plaster with concealed joint reveals.

---

## 📐 Algorithmic Hygrothermal Formulas

The engine evaluates wall assemblies against international standards (Passivhaus, RT2020 / RE2020, Eurocode 5):

$$\\text{Total Thermal Resistance } R_{tot} = R_{si} + \\sum_{i=1}^n \\frac{d_i}{\\lambda_i} + R_{se}$$

$$\\text{Overall Heat Transfer Coefficient } U = \\frac{1}{R_{tot}} \\quad [\\text{W/m}^2\\cdot\\text{K}]$$

- **Passivhaus Wall Standard**: $U \le 0.15\text{ W/m}^2\\cdot\\text{K}$
- **RE2020 Bio-Composite Standard**: $U \le 0.20\text{ W/m}^2\\cdot\\text{K}$
- **Embodied Carbon Metric**: Net negative sequestration calculation ($\\text{kgCO}_2\text{e/m}^2$) for mass timber and hempcrete cores.

---

## 💬 How to Use in Antigravity, Claude & Cursor

```bash
# Generate a complete 1:20 Wall Section Vector Drawing:
/constructive-detail generate --assembly granite-hemp --scale 1:20 --output wall_section_1_20.svg

# Calculate U-value and Dew Point Risk:
/constructive-detail audit --thicknesses 180,140,20,160 --conductivities 2.1,0.076,0.031,0.13
```

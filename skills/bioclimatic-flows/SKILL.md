---
name: bioclimatic-flows
description: >-
  Calculates passive solar angles, thermodynamic stack ventilation loops, and diurnal thermal mass damping,
  generating publication-grade bioclimatic vector diagrams grounded in building physics.
author: Sara Bensalem <sara@sarabensalem.com>
website: https://skills.sarabensalem.com
github: https://github.com/sounny/sara-bensalem-skills
---

# Bioclimatic Flows (`/bioclimatic-flows`)
### *Thermodynamic Simulation & Passive Solar Vector Engine*
**Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]**

> *"True sustainability is not green paint or decorative solar panels. It is the geometric alignment of building mass, solar angles, and natural pressure buoyancy loops."*

`bioclimatic-flows` equips AI agents with building physics principles for environmental architectural design:
- **Solar Geometry**: Latitude-calibrated solar altitude angles (Summer Solstice $65^\circ$ vs Winter Solstice $18^\circ$ at $48^\circ\text{N}$ Strasbourg).
- **Stack-Effect Buoyancy (Chimney Effect)**: Neutral pressure planes, natural airflow rates ($\\Delta T$), and high-level operable relief louvers.
- **Diurnal Thermal Damping**: Phase lag ($\\phi = 8\\text{--}12\\text{ hours}$) of heavyweight mass walls (rammed earth, stone masonry, hempcrete monolith).
- **Calculated Solar Heat Gain**: Facade $g$-values, Solar Heat Gain Coefficient (SHGC), and passive solar aperture sizing.

---

## 📐 Thermodynamic Governing Equations

### 1. Thermal Stack Ventilation Volume Flow:
$$Q = C_d \\cdot A \\cdot \\sqrt{2 \\cdot g \\cdot h \\cdot \\frac{T_{in} - T_{out}}{T_{in}}}$$
Where:
- $Q$ = Airflow volume rate [$\\text{m}^3/\\text{s}$]
- $C_d$ = Discharge orifice coefficient (typically 0.60–0.65)
- $A$ = Free operable opening area [$\\text{m}^2$]
- $h$ = Height distance between lower intake and upper chimney exhaust [$\\text{m}$]
- $T_{in}, T_{out}$ = Absolute indoor/outdoor temperatures [$\\text{K}$]

### 2. Thermal Mass Phase Shift (Time Lag $\phi$):
$$\phi = \frac{d}{2} \cdot \sqrt{\frac{24}{\pi \cdot \alpha}} \quad [\text{hours}]$$
Where $d$ is thickness in meters and $\alpha$ is thermal diffusivity ($k / \rho c_p$).

### 3. Kinetic Hybrid Microgrid Sizing (The Solaura Formulation):
For kinetic building-integrated photovoltaics (BIPV) and micro-wind harvesting modules:
$$E_{\text{daily, solar}} = A_{\text{pv}} \cdot I_{\text{daily}} \cdot \eta_{\text{pv}} \quad [\text{kWh/day}]$$
$$P_{\text{wind, module}} = \frac{1}{2} \cdot \rho_{\text{air}} \cdot A_{\text{frontal}} \cdot v_{\text{wind}}^3 \cdot \eta_{\text{turbine}} \quad [\text{W}]$$
$$E_{\text{daily, wind}} = P_{\text{wind, module}} \cdot 24\,\text{h} \cdot N_{\text{modules}} \cdot 10^{-3} \quad [\text{kWh/day}]$$
Where $\rho_{\text{air}} = 1.225\,\text{kg/m}^3$, $\eta_{\text{turbine}} \le 0.593$ (Betz limit, typically $0.25\text{--}0.35$), and $I_{\text{daily}}$ is regional solar insolation [$\text{kWh/m}^2/\text{day}$].

### 4. Hydrological Root-Zone Rain Garden Stratification:
Stratifying bioswales and retention gardens into distinct hygrothermal and moisture-tolerance layers:
- **Upper Aerobic Tier ($15\text{--}30\text{cm}$ depth)**: Drought-tolerant native shrubs and flowering species with deep root penetration for soil stabilization.
- **Lower Saturated Hydric Basin ($30\text{--}45\text{cm}$ depth)**: Flooding-resilient wetland macrophytes (*Colocasia*, *Carex*, *Ipomoea pes-caprae*) designed for anaerobic water retention and bio-filtration of storm runoff ($10,000\,\text{L/day}$).

---

## 💬 How to Use in Antigravity, Claude & Cursor

```bash
# Calculate Solar Vectors & Ventilation Flow for Strasbourg:
/bioclimatic-flows calculate --latitude 48.58 --chimney-height 9.2 --vent-area 4.5

# Generate Bioclimatic Vector Spread SVG:
/bioclimatic-flows generate --output bioclimatic_flow_plate.svg
```

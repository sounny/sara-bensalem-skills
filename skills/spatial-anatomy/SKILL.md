---
name: spatial-anatomy
description: >-
  Generates verified 1:100 architectural plans and validates universal accessibility (PMR/ADA)
  and emergency code egress compliance, checking 1500mm wheelchair turning circles, 900mm door clearances,
  and travel distance corridors.
author: Sara Bensalem <sara@sarabensalem.com>
website: https://skills.sarabensalem.com
github: https://github.com/sounny/sara-bensalem-skills
---

# Spatial Anatomy (`/spatial-anatomy`)
### *1:100 Floor Plan Generation, Universal Accessibility (PMR) & Code Egress Engine*
**Sara Bensalem Studio • Strasbourg Atelier [48°35'05"N 07°45'02"E]**

> *"Architecture begins with the plan. If the plan fails universal accessibility, egress corridors, or acoustic buffering, the building is dead on arrival regardless of the envelope."*

`spatial-anatomy` equips coding agents with geometric rigor for interior architecture, space planning, and international code compliance:
- **French PMR**: Arrêté du 24 décembre 2015 (Accessibilité des personnes à mobilité réduite).
- **US ADA**: 2010 ADA Standards for Accessible Design.
- **IBC Chapter 10**: Means of Egress, occupant load factors, and exit discharge distances.

---

## 🏛️ Key Spatial Compliance Mandates

### 1. The 1500mm Wheelchair Turning Circle:
- In every entrance airlock, accessible toilet, primary corridor intersection, and public service counter, an unobstructed $\varnothing 1500\text{ mm}$ rotation circle must be guaranteed clear of door swing arcs.

### 2. Door Clearances & Approaches:
- **Nominal Leaf Width**: $\ge 900\text{ mm}$.
- **Clear Passage Width ($L_u$)**: $\ge 830\text{ mm}$ with door open at $90^\circ$.
- **Latching Side Clearance**: Minimum $300\text{ mm}$ strike edge clearance on pull side for wheelchair approach.

### 3. Egress Corridors:
- **Single Wheelchair Corridor**: Minimum $1200\text{ mm}$.
- **Two-Way Passing Corridor**: Minimum $1400\text{ mm}$ (recommended $1800\text{ mm}$).
- **Maximum Dead-End Corridor**: $\le 12\text{ m}$ (French ERP) / $\le 20\text{ ft}$ (IBC).

---

## 💬 How to Use in Antigravity, Claude & Cursor

```bash
# Audit an architectural plan for PMR & Egress:
/spatial-anatomy audit --doors 900,830 --vestibule 1800,2100 --corridor 1400

# Generate an accessible 1:100 Plan Vector SVG:
/spatial-anatomy generate --typology library --scale 1:100 --output plan_1_100.svg
```

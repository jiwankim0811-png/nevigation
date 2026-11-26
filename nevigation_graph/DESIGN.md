---
name: Algorithmic Graph Studio
colors:
  surface: '#0d1322'
  surface-dim: '#0d1322'
  surface-bright: '#33394a'
  surface-container-lowest: '#080e1d'
  surface-container-low: '#151b2b'
  surface-container: '#191f2f'
  surface-container-high: '#242a3a'
  surface-container-highest: '#2f3445'
  on-surface: '#dde2f8'
  on-surface-variant: '#bdc8d1'
  inverse-surface: '#dde2f8'
  inverse-on-surface: '#2a3040'
  outline: '#87929a'
  outline-variant: '#3e484f'
  surface-tint: '#7bd0ff'
  primary: '#8ed5ff'
  on-primary: '#00354a'
  primary-container: '#38bdf8'
  on-primary-container: '#004965'
  inverse-primary: '#00668a'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffc174'
  on-tertiary: '#472a00'
  tertiary-container: '#f59e0b'
  on-tertiary-container: '#613b00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#c4e7ff'
  primary-fixed-dim: '#7bd0ff'
  on-primary-fixed: '#001e2c'
  on-primary-fixed-variant: '#004c69'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0d1322'
  on-background: '#dde2f8'
  surface-variant: '#2f3445'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 14px
  code-inline:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-lg: 1.5rem
  margin: 1rem
  margin-lg: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system is tailored for computer science students, researchers, and software engineers analyzing graph theory and pathfinding mechanics. The brand aesthetic merges the clarity of modern developer environments with the precision of interactive mathematical instrumentation.

### Style Directives
- **Aesthetic Movement:** Technical Minimalism infused with Terminal Cybernetics. Crisp, high-contrast vector lines, structural geometry, and selective luminous accents.
- **Atmospheric Depth:** Deep oceanic slate backgrounds evoke late-night focus and IDE-like familiarity, while glowing nodes and analytical metrics establish clear cognitive hierarchies without visual fatigue.
- **Mental Model:** A flight simulator for graph traversal. Every color token maps to a specific computational state (unvisited, evaluating, visited, optimal path), treating visual attributes strictly as informational syntax.

## Colors

The color palette directly mirrors Dijkstra's state machine:

- **Primary (`#38bdf8` / Cyan-Sky):** The confirmed shortest path, active edge traversal, and primary navigation calls to action.
- **Secondary (`#10b981` / Emerald):** Settled nodes, finalized set $S$, optimal weights, and execution success metrics.
- **Tertiary (`#f59e0b` / Amber):** The currently evaluated vertex/edge, relax operation in flight, and execution playback controls.
- **Semantic Accents:** 
  - Indigo/Violet (`#818cf8` / `#6366f1`): Priority queue (`min-heap`) indices and memory allocations.
  - Crimson/Rose (`#f43f5e`): Unreachable nodes, infinite distance ($\infty$), and cycle warnings.
- **Base Surfaces:**
  - Canvas Background: `#0b1120` (Obsidian Navy)
  - Surface Panel / Cards: `#131d33` (Slate Navy)
  - Elevated Container / Hover States: `#1e293b` (Subtle Muted Slate)
  - Structural Hairlines: `#1e293b` with localized state-tinted borders at 40% opacity.

## Typography

Typography balances structural geometric authority with absolute tabular precision:

- **Headlines (Space Grotesk):** Engineered, tech-forward proportions with tight tracking for dashboard headers, module titles, and algorithm status readouts.
- **Body & Prose (Geist):** High-legibility neutral sans-serif built specifically for technical tooling, documentation sidebars, and contextual helper dialogs.
- **Labels, Tables & Pseudocode (JetBrains Mono):** Dedicated to the interactive priority queue, adjacency matrix displays, coordinate markers, and live code inspection panels. Tabular numeric alignment ensures data values do not shift during real-time animation.

## Layout & Spacing

The dashboard employs a **Modular Split-Screen Dashboard Layout** centered around high-density data and interactive canvas regions.

### Screen Layout Architecture
- **Desktop (≥ 1280px):** 
  - Left Panel (280px–340px): Graph generation parameters, input matrix, and step-by-step playback controls.
  - Central Canvas (Flexible 1fr): WebGL/SVG interactive graph view with infinite pan/zoom coordinates.
  - Right Panel (320px–380px): Min-priority heap visualization, visited node table, and live complexity diagnostics ($O((V + E) \log V)$).
- **Tablet (768px – 1279px):**
  - Graph canvas occupies the top tier (height: 55vh).
  - Controls and Priority Queue collapse into a synchronized dual-column drawer below.
- **Mobile (< 768px):**
  - Single-column stacked mode. Bottom floating sheet hosts scrubber playback and execution logs.

### Rhythm & Alignment
Spacing adheres to a strict 4px/8px modular scale. Spacing within code metrics and data tables defaults to `space-xs` and `space-sm` for maximum informational density, while layout canvas margins use `space-lg` and `space-xl` to prevent claustrophobia.

## Elevation & Depth

Visual hierarchy does not rely on soft real-world dropshadows, but rather on **Layered Dark-Luminance and Luminescent Outlines**.

- **Level 0 (Canvas Base):** Deepest `#0b1120`. Sub-grid guidelines rendered at 8% opacity.
- **Level 1 (Panels & Toolbars):** `#131d33` surface bounded by a crisp 1px stroke of `#1e293b`.
- **Level 2 (Active Nodes & Hover Cards):** `#18243e` overlay with a soft 0 0 16px glow reflecting the state's hue:
  - Evaluation glow: `rgba(245, 158, 11, 0.15)`
  - Active path glow: `rgba(56, 189, 248, 0.25)`
  - Visited settled glow: `rgba(16, 185, 129, 0.15)`
- **Level 3 (Modals, Overlays & Dragged Nodes):** `#1e293b` with a solid 1px border of `#334155` and a tight drop shadow (`0 10px 25px -5px rgba(0, 0, 0, 0.6)`).

## Shapes

The shape system utilizes **Soft (`roundedness: 1`)** rounding. This maintains the crisp architectural discipline demanded by developer interfaces, avoiding childish bubble aesthetics while softening sharp terminal edges.

- **Base Elements (Buttons, Inputs, Metric Badges):** 0.25rem (`rounded-sm`).
- **Cards, Code Containers, Split Panels:** 0.5rem (`rounded-lg`).
- **Graph Nodes:** Strict geometric circles (`50%` / circular border-radius) with 2px concentric state rings.
- **Weight Badges on Edges:** Pill-shaped (`9999px`) micro-containers centered over graph vectors for legible edge weights.

## Components

### Buttons & Playback Controls
- **Primary Execution (Run / Step):** Background `#38bdf8`, label in `#0b1120` (Space Grotesk, 600 weight). Hover: `#7dd3fc`.
- **Secondary (Reset / Clear Graph):** Background transparent, 1px border of `#1e293b`, text `#94a3b8`. Hover: `#1e293b` with text `#f8fafc`.
- **Icon Transport Controls (Step Back, Pause, Play, Step Next):** Squircle icon toggles inside `#131d33` with JetBrains Mono tooltips indicating hotkeys (`Space`, `→`, `R`).

### Interactive Graph Nodes & Edges
- **Unvisited Node:** Surface `#131d33`, border 1.5px `#475569`, text `#94a3b8`.
- **Current Candidate Node:** Surface `#f59e0b` at 15% opacity, border 2px `#f59e0b`, text `#fef3c7`.
- **Finalized Path Node:** Surface `#38bdf8`, text `#0b1120`, glowing outer halo.
- **Edge Weight Labels:** Monospaced numbers encapsulated in a high-contrast pill badge (`#0b1120` fill, 1px `#334155` border).

### Priority Queue Table (Min-Heap Viewer)
- Monospaced table headers (`Node ID`, `Tentative Dist`, `Predecessor`).
- Heap rows dynamically reorder with transition keyframes. Active extraction row highlights in `#818cf8` tint with a left-accent 3px bar.

### Input Fields & Sliders
- **Matrix / Node Inputs:** Dark inputs (`#0b1120`), 1px outline `#1e293b`, focus state shifts border to `#38bdf8` with no native browser outline.
- **Speed Slider:** 4px rail (`#1e293b`) with a glowing `#38bdf8` thumb marker and realtime numeric frequency counter (`"50ms / step"`).

### Informational Chips & Status Pills
- Compact tags with `label-sm` JetBrains Mono text.
- Visited counter: Background `rgba(16, 185, 129, 0.1)`, text `#10b981`, 1px border `rgba(16, 185, 129, 0.2)`.

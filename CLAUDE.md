# CLAUDE.md — dunwoody_tools

This file gives Claude Code context about the project so it can assist effectively.

---

## Project Overview

**dunwoody_tools** is a collection of engineering calculators for [dunwoodyengineering.com](https://dunwoodyengineering.com), a personal hobby site focused on bulk materials handling and conveyor design. Tools are hosted on GitHub Pages and embedded in WordPress via iframes.

The project is in active transition:
- **Legacy tools** are Python/Marimo notebooks (`.py` files in `apps/`)
- **New tools** are plain HTML/CSS/JS files (`.html` files in `apps/`) — this is the preferred format going forward

---

## Repository Structure

```
dunwoody_tools/
├── apps/                          # All calculator tools (Marimo .py and new .html)
│   ├── static/
│   │   ├── theme.css              # Nord colour palette, font vars, semantic tokens
│   │   └── calculator.css         # Shared component styles for all HTML tools
│   ├── lifting-lug-check.html     # Lifting lug evaluation tool
│   └── de-calculator-template.html  # Blank starter template
├── scripts/                       # Build/utility scripts
├── .devcontainer/                 # VS Code Dev Container config (Python + Marimo)
├── .github/workflows/             # GitHub Actions (GitHub Pages deployment)
├── pyproject.toml                 # Python dependencies for Marimo tools
├── CLAUDE.md                      # This file
└── README.md
```

---

## Tool Architecture

### New tools (HTML/JS — preferred)
- **Single self-contained `.html` files** in `apps/`
- No build step, no dependencies, no server required
- All calculation logic in vanilla JavaScript
- Styled with the Nord colour palette (see Design System below)
- Deployed automatically to GitHub Pages on push to `main`
- Embedded in WordPress via iframe:
  ```html
  <iframe src="https://pdunwoody.github.io/dunwoody_tools/apps/tool-name.html"
          style="width:100%; height:900px; border:none; border-radius:8px;"
          loading="lazy"></iframe>
  ```

### Legacy tools (Python/Marimo)
- Marimo notebooks in `apps/` as `.py` files
- Run locally via Dev Container or `marimo run apps/<tool>.py`
- Some are exported to static HTML for GitHub Pages via the build scripts
- Being replaced by native HTML tools over time

---

## Design System

All new HTML tools use the **Nord colour palette** and a shared CSS stack. The canonical template is `apps/de-calculator-template.html`.

### CSS files

Every tool links both shared stylesheets in `<head>`, in this order:
```html
<link rel="stylesheet" href="static/theme.css" />
<link rel="stylesheet" href="static/calculator.css" />
```

| File | Purpose |
|---|---|
| `apps/static/theme.css` | Nord palette (`--nord0`–`--nord15`), font variables (`--text-font`, `--monospace-font`), semantic tokens (`--background`, `--foreground`, `--accent`, `--success`, `--destructive`, `--action`, `--ring`, `--radius`, etc.) |
| `apps/static/calculator.css` | All shared component styles: layout, cards, inputs, button, results grid, status badge, result table, divider, disclaimer. Also overrides `--card`, `--border`, and `--gap` to calculator-appropriate values. |

Tool-specific styles (e.g. a diagram wrapper, a custom list) go in a `<style>` block in the tool file itself. Most tools need no local styles at all.

### Key component classes (from `calculator.css`)
| Class | Purpose |
|---|---|
| `.calc-header` | Left-accented page header with `h1` and `.subtitle` |
| `.card` | Rounded card container |
| `.card-title` | Uppercase accent-coloured section label |
| `.card-subtitle` | Uppercase muted sub-section label |
| `.info-box` | Tinted informational card |
| `details.collapsible` | Expandable reference/notes section |
| `.input-grid` | Responsive grid for input fields |
| `.input-group` | Label + input + hint stacked vertically |
| `.input-field` | Styled `<input>` or `<select>` |
| `.btn-calculate` | Full-width calculate button |
| `.results-grid` | Responsive grid for result cards |
| `.result-card` | Single result display (label / value / unit) |
| `.result-value.pass/warn/fail` | Colour-coded result value |
| `.result-table` | Tabular breakdown with pass/warn/fail colouring |
| `#status-badge` | Coloured overall pass/warn/fail banner |
| `hr.divider` | Horizontal rule within a card |
| `.disclaimer` | Small-print disclaimer block |

### JS helpers (in every tool)
- `setStatus(type, msg)` — drives the status badge; type = `'pass'|'warn'|'fail'|'info'`
- `setOutputFOS(id, fos)` — writes a factor-of-safety value with colour coding
- `buildTable(rows)` — populates the result table from an array of `{name, actual, allow, pass}`

---

## Adding a New Tool

1. Copy `apps/de-calculator-template.html` and rename it (kebab-case, e.g. `belt-capacity.html`)
2. Update `<title>`, the `<h1>`, and the `.subtitle` text
3. Replace the input section with your fields using `.input-group` pattern
4. Replace the output section with your result cards
5. Write your `calculate()` function — keep all maths in JS
6. Add a `<style>` block only if the tool needs styles beyond what `calculator.css` provides
7. Push to `main`; GitHub Actions deploys to Pages automatically
8. Add a WordPress page on dunwoodyengineering.com embedding the tool via iframe
9. Update this file to add the tool to the inventory below

---

## Tool Inventory

| File | Description | Method/Reference | Status |
|---|---|---|---|
| `apps/lifting-lug-check.html` | Overhead lifting lug evaluation | Rajendra – PDHonline S106 | ✅ Live |
| `apps/de-calculator-template.html` | Blank starter template | — | ✅ Template |

*(Add new tools here as they are created)*

---

## Engineering Domain Context

The site focuses on **bulk materials handling** — specifically:
- Belt conveyor design (CEMA 7th Edition methodology)
- Conveyor component sizing (idlers, pulleys, drives, take-ups)
- Structural checks for conveyor steel (lifting lugs, etc.)
- DEM / FEA analysis (articles, not tools)

Most calculations follow **CEMA 7th Edition** (*Belt Conveyors for Bulk Materials*) or referenced PDH/industry standards. Always note the standard/reference in the tool's subtitle and collapsible reference section.

**Unit convention:** Imperial (US customary) unless the tool explicitly states otherwise. Use kip, ksi, ft, in, lbs/ft, tph etc.

---

## Local Development

### With Dev Container (recommended)
1. Install VS Code + Docker
2. Clone the repo and open in VS Code
3. Accept the "Reopen in Container" prompt
4. The container installs all Python deps automatically
5. Use the Marimo extension to run/edit `.py` notebooks

### Without Dev Container
```bash
pip install marimo
git clone https://github.com/pdunwoody/dunwoody_tools.git
cd dunwoody_tools
pip install .
marimo run apps/lifting_lug_check.py   # example
```

### HTML tools
No build step needed. Open any `.html` file directly in a browser, or use the VS Code Live Server extension.

---

## Deployment

GitHub Actions automatically deploys the `main` branch to GitHub Pages at:
**https://pdunwoody.github.io/dunwoody_tools/**

Individual tools are accessible at:
**https://pdunwoody.github.io/dunwoody_tools/apps/\<filename\>.html**

No manual deployment steps required — push to `main` and it goes live.

---

## Constraints

- **No paid services** — everything must be free to host (GitHub Pages, no backend servers)
- **No npm/build pipeline for HTML tools** — single-file, zero-dependency HTML only
- **No external CDN fonts or tracking** — system fonts only in tools; no analytics scripts inside tool files
- Tools must work when embedded in an iframe on WordPress (no `localStorage`, no cookies required)

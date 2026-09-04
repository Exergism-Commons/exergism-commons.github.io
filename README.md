# www.exergism.org

Public-facing website for **Exergism Commons**.

This repository serves `https://www.exergism.org/` through GitHub Pages. It is a presentation layer only: canonical philosophical, legal, semantic, funding, governance, and registry authority remains in the repositories and adopted artifacts that own those layers.

## Web architecture

- `www.exergism.org` — public/institutional website and ecosystem entry point (this repository)
- `exergism.org` — intended apex redirect to `www.exergism.org`
- `governance.exergism.org` — human-facing guide to Exergism Commons governance; the governance repository and valid adoption records remain authoritative
- `funding.exergism.org` — public funding intelligence, strategy, opportunities, and funding-governance presentation
- `id.exergism.org` — persistent semantic identifier resolution and vocabulary/ontology access
- project repositories — canonical source, version history, machine-readable records, and domain-specific authority

The website must not become a second source of truth for Exergism, ECL, ECL-PL, Funding, Governance, or persistent identifiers.

The intended separation is:

```text
www.exergism.org
  public presentation / ecosystem navigation

governance.exergism.org
  how Exergism Commons is governed

funding.exergism.org
  how Exergism Commons builds and governs institutional funding capacity

id.exergism.org
  persistent identifiers and dereferenceable semantic resources

GitHub repositories
  canonical source, history, records, validators and domain authority
```

## Brand assets

The public site uses the maintained Exergism Commons and Exergism symbols under `assets/brand/` rather than generated placeholder marks. Their use here is presentational and does not alter project-specific authority, licensing, or semantic identity.

- `commons-symbol.webp` — compact Exergism Commons mark for navigation and small surfaces.
- `commons-crest.webp` — institutional Exergism Commons crest for prominent presentation and social previews.
- `exergism-symbol.webp` — Exergism project symbol used to identify the canonical framework.

## Implementation

The site is intentionally static and dependency-free:

- semantic HTML;
- plain CSS;
- minimal progressive JavaScript;
- no framework or build step;
- GitHub Pages deployment from the default branch.

This keeps the public site replaceable without coupling persistent identifiers or canonical artifacts to a web framework.

# www.exergism.org

Public-facing website for **Exergism Commons**.

This repository serves `https://www.exergism.org/` through GitHub Pages. It is a presentation layer only: canonical philosophical, legal, semantic, governance, and registry authority remains in the repositories that own those layers.

## Web architecture

- `www.exergism.org` — public/institutional website (this repository)
- `exergism.org` — intended apex redirect to `www.exergism.org`
- `id.exergism.org` — persistent semantic identifier authority
- project repositories — canonical source and version history

The website must not become a second source of truth for Exergism, ECL, ECL-PL, or governance artifacts.

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

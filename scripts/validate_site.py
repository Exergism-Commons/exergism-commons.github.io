from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HOST = "www.exergism.org"
EXPECTED_CANONICAL = f"https://{EXPECTED_HOST}/"
BRAND_IMAGES = (
    "assets/brand/commons-symbol.webp",
    "assets/brand/commons-crest.webp",
    "assets/brand/exergism-symbol.webp",
)


class RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refs: list[tuple[str, str]] = []
        self.canonical: str | None = None
        self.description: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for attr in ("href", "src"):
            value = values.get(attr)
            if value:
                self.refs.append((attr, value))
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href")
        if tag == "meta" and values.get("name") == "description":
            self.description = values.get("content")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def resolve_local(path: str) -> Path | None:
    parsed = urlparse(path)
    if parsed.scheme or parsed.netloc or path.startswith("#") or path.startswith("mailto:"):
        return None
    clean = parsed.path
    if not clean.startswith("/"):
        return None
    if clean == "/":
        return ROOT / "index.html"
    candidate = ROOT / clean.lstrip("/")
    if clean.endswith("/"):
        candidate = candidate / "index.html"
    return candidate


def validate_html(file: Path, require_canonical: bool = False) -> None:
    parser = RefParser()
    parser.feed(file.read_text(encoding="utf-8"))

    if require_canonical and parser.canonical != EXPECTED_CANONICAL:
        fail(f"{file.name}: canonical must be {EXPECTED_CANONICAL!r}, got {parser.canonical!r}")
    if require_canonical and not parser.description:
        fail(f"{file.name}: missing meta description")

    for _, ref in parser.refs:
        local = resolve_local(ref)
        if local is not None and not local.exists():
            fail(f"{file.name}: local reference {ref!r} resolves to missing {local.relative_to(ROOT)}")


def validate_brand_assets() -> None:
    required = {*BRAND_IMAGES, "assets/brand.css"}
    missing = [path for path in sorted(required) if not (ROOT / path).exists()]
    if missing:
        fail(f"missing required brand asset(s): {', '.join(missing)}")

    dimensions: dict[str, tuple[int, int]] = {}
    for relative_path in BRAND_IMAGES:
        path = ROOT / relative_path
        try:
            with Image.open(path) as image:
                if image.format != "WEBP":
                    fail(f"{relative_path}: expected WebP, got {image.format!r}")
                image.load()
                if image.width < 128 or image.height < 128:
                    fail(f"{relative_path}: image dimensions are unexpectedly small: {image.size}")
                dimensions[relative_path] = image.size
        except (UnidentifiedImageError, OSError) as exc:
            fail(f"{relative_path}: image cannot be decoded: {exc}")

    index = (ROOT / "index.html").read_text(encoding="utf-8")
    brand_css = (ROOT / "assets/brand.css").read_text(encoding="utf-8")
    crest_dimensions = dimensions["assets/brand/commons-crest.webp"]

    if '<meta name="twitter:card" content="summary_large_image">' in index and crest_dimensions[0] < 300:
        fail(f"summary_large_image requires a social image at least 300px wide, got {crest_dimensions}")

    forbidden_page_treatments = (
        'class="hero-crest"',
        'class="exergism-section-logo"',
        'class="brand-mark"',
        '>EC</span>',
        'Identity is not presentation.',
        '<strong>www.exergism.org</strong>',
    )
    for token in forbidden_page_treatments:
        if token in index:
            fail(f"deprecated visual/copy treatment remains in index.html: {token!r}")

    required_markup = (
        'class="hero-field"',
        'class="framework-field"',
        'class="identifier-domain"',
        'class="identity-principle"',
    )
    for token in required_markup:
        if token not in index:
            fail(f"missing required public-facing treatment in index.html: {token!r}")

    for selector in (".hero-field", ".framework-field", ".identifier-domain", ".identity-principle"):
        if selector not in brand_css:
            fail(f"brand.css is missing required design selector {selector!r}")


def validate_progressive_navigation() -> None:
    css = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
    javascript = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")

    for selector in (".js .nav-toggle", ".js .site-nav", ".js .site-nav.is-open"):
        if selector not in css:
            fail(f"mobile navigation must be progressively enhanced via {selector!r}")

    marker = "document.documentElement.classList.add('js')"
    handler = "toggle.addEventListener('click'"
    if marker not in javascript:
        fail("site.js must mark the page as enhanced before collapsed-nav CSS can apply")
    if handler not in javascript or javascript.index(marker) < javascript.index(handler):
        fail("the enhanced-nav marker must only be added after the navigation handler is installed")


def main() -> None:
    cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    if cname != EXPECTED_HOST:
        fail(f"CNAME must be {EXPECTED_HOST!r}, got {cname!r}")

    index = ROOT / "index.html"
    if not index.exists():
        fail("index.html is missing")
    validate_html(index, require_canonical=True)
    validate_brand_assets()

    error_page = ROOT / "404.html"
    if error_page.exists():
        validate_html(error_page)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if EXPECTED_CANONICAL not in sitemap:
        fail("sitemap.xml does not contain the canonical homepage URL")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {EXPECTED_CANONICAL}sitemap.xml" not in robots:
        fail("robots.txt does not reference the canonical sitemap")

    validate_progressive_navigation()
    print("site validation passed")


if __name__ == "__main__":
    main()

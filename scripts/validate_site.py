from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_HOST = "www.exergism.org"
EXPECTED_CANONICAL = f"https://{EXPECTED_HOST}/"


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


def main() -> None:
    cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    if cname != EXPECTED_HOST:
        fail(f"CNAME must be {EXPECTED_HOST!r}, got {cname!r}")

    index = ROOT / "index.html"
    if not index.exists():
        fail("index.html is missing")
    validate_html(index, require_canonical=True)

    error_page = ROOT / "404.html"
    if error_page.exists():
        validate_html(error_page)

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if EXPECTED_CANONICAL not in sitemap:
        fail("sitemap.xml does not contain the canonical homepage URL")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {EXPECTED_CANONICAL}sitemap.xml" not in robots:
        fail("robots.txt does not reference the canonical sitemap")

    print("site validation passed")


if __name__ == "__main__":
    main()

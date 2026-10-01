"""Validate the static site's local links; optionally check external URLs."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1] / "site"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.references = []
        self.errors = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate id: {attrs['id']}")
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.references.append(attrs[name])
        if tag == "img" and "alt" not in attrs:
            self.errors.append("Image has no alt attribute")


def check(external=False):
    pages = {p.resolve(): Page(p) for p in ROOT.rglob("*.html")}
    errors = []
    urls = set()
    for path, page in pages.items():
        errors.extend(f"{path.name}: {error}" for error in page.errors)
        for reference in page.references:
            url = urlsplit(reference)
            if url.scheme in ("https", "http"):
                urls.add(reference.split("#", 1)[0])
                continue
            if url.scheme:
                errors.append(f"Unexpected URL scheme: {reference}")
                continue
            if url.netloc or url.path.startswith("/"):
                errors.append(f"Use project-relative links for GitHub Pages: {reference}")
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
                errors.append(f"Missing or out-of-site target: {reference}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"Missing fragment: {reference}")
    for css in ROOT.rglob("*.css"):
        for reference in re.findall(r"url\(['\"]?([^)'\"]+)", css.read_text(encoding="utf-8")):
            if not (css.parent / reference).is_file():
                errors.append(f"Missing CSS asset: {reference}")
    if external:
        for url in sorted(urls):
            try:
                request = Request(url, headers={"User-Agent": "ChainOSCPad-Portal-LinkCheck/1.0"})
                with urlopen(request, timeout=30) as response:
                    print(f"{response.status} {url}")
            except Exception as error:
                errors.append(f"External link failed: {url}: {error}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(pages)} HTML page(s), local assets/fragments, {len(urls)} external URLs" +
          (" checked" if external else " listed (use --external to check HTTP responses)"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--external", action="store_true")
    check(parser.parse_args().external)

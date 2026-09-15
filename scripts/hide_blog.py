"""Post-render step: remove blog pages from sitemap.xml while the blog is hidden.

Runs automatically after `quarto render` (see `post-render` in _quarto.yml).
Delete that line in _quarto.yml when the blog launches.
"""
import os
import re
from pathlib import Path

out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
sitemap = out_dir / "sitemap.xml"

if sitemap.exists():
    xml = sitemap.read_text(encoding="utf-8")
    xml = re.sub(r"\s*<url>\s*<loc>[^<]*/blog/[^<]*</loc>.*?</url>", "", xml, flags=re.S)
    sitemap.write_text(xml, encoding="utf-8")

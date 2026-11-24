#!/usr/bin/env python3
"""Copia a cada skill las guías de docs/ que cita, para que funcione fuera del repositorio.

La fuente sigue siendo docs/: no edites las copias. Copia la versión en inglés (la lengua
de las skills). Las rutas a scripts de la propia skill pasan a <skill-dir>/…, los enlaces
a otras copias quedan locales y el resto de enlaces relativos apunta a GitHub.

Uso:
    python3 scripts/sync_skill_references.py           # escribe las copias
    python3 scripts/sync_skill_references.py --check   # sale con 1 si alguna no está al día

Solo necesita Python 3.
"""
import posixpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins/video-studio/skills"
GITHUB = "https://github.com/SantipBarber/haividio/blob/main/"
COPIES = {
    "choose-video-tool": ["docs/workflows/05-product-demo.en.md", "docs/windows.en.md", "docs/tools.en.md"],
    "faceless-video": ["docs/editing-and-verification.en.md"],
    "pencil-to-hyperframes": ["docs/workflows/06-pencil-to-hyperframes.en.md", "docs/style/tokens.css"],
    "publish-youtube": ["docs/workflows/04-publish-youtube.en.md"],
    "visual-identity": ["docs/style/identity.en.md", "docs/style/tokens.css", "docs/open-resources.en.md"],
}


def target(src: str) -> str:
    return posixpath.basename(src).replace(".en.md", ".md")


def render(skill: str, src: str) -> str:
    text = (ROOT / src).read_text(encoding="utf-8")
    if not src.endswith(".md"):
        return text
    local = {s: target(s) for s in COPIES[skill]}

    def link(m):
        url, _, anchor = m.group(1).partition("#")
        if not url or re.match(r"[a-z]+:", url):
            return m.group(0)
        path = posixpath.normpath(posixpath.join(posixpath.dirname(src), url))
        new = local.get(path) or GITHUB + path
        return f"]({new}{'#' + anchor if anchor else ''})"

    text = re.sub(r"^\*\[Español\]\([^)]*\)\*\n\n?", "", text, flags=re.M)
    text = re.sub(r"\]\(([^)\s]+)\)", link, text)
    if "docs/style/tokens.css" in local:
        text = text.replace("docs/style/tokens.css", "<skill-dir>/references/tokens.css")
    own = f"plugins/video-studio/skills/{skill}/"
    text = re.sub(r"(?<!blob/main/)" + re.escape(own), "<skill-dir>/", text)
    return f"<!-- Copy of {src}. Edit it there and run scripts/sync_skill_references.py. -->\n\n{text}"


def main():
    check, stale = "--check" in sys.argv[1:], []
    for skill, sources in COPIES.items():
        for src in sources:
            out = SKILLS / skill / "references" / target(src)
            new = render(skill, src)
            if not out.exists() or out.read_text(encoding="utf-8") != new:
                stale.append(out.relative_to(ROOT))
                if not check:
                    out.parent.mkdir(exist_ok=True)
                    out.write_text(new, encoding="utf-8", newline="\n")
    for p in stale:
        print(("desfasada: " if check else "escrita: ") + str(p))
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()

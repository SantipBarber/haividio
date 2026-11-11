#!/usr/bin/env python3
"""Convierte fotogramas exportados de Pencil (pen.dev) en una composición de HyperFrames lista para animar.

Pencil exporta HTML con estilos en línea, posiciones absolutas y el nombre de cada capa
(`data-pencil-name`). Ya se parece mucho a una escena de HyperFrames; lo que falta, y
este script hace:

- ids estables a partir de los nombres de capa («Tracker/Paso 01» → #kf-tracker-paso-01),
  para que el agente anime cada elemento por su nombre de diseño;
- fuentes locales: descarga de Google Fonts los subconjuntos latin y latin-ext a
  assets/fonts/ y los declara con @font-face (HyperFrames no admite fuentes por CDN y
  Geist no viene incluida);
- imágenes: copia las que referencia el diseño a assets/pencil/ y reescribe las rutas
  (las busca junto al HTML exportado y, con --pen-dir, junto al .pen);
- colores: con --tokens, cada color literal que esté en la paleta pasa a
  var(--nombre, #hex), así un cambio de identidad llega también a lo importado;
- el envoltorio de HyperFrames: <template>, #root con data-composition-id y una línea
  de tiempo vacía registrada en window.__timelines, donde va la animación.

Varios fotogramas (un storyboard): el primero es la composición; los demás son
estados del mismo diseño. Para cada elemento, por su id, <nombre>.states.json guarda
qué cambia respecto al primero (estilos y texto) y qué elementos entran o salen, y
pencil/<nombre>/ guarda el HTML de cada fotograma, ya convertido y con los mismos
ids, para copiar de ahí las capas que entran. Pencil exporta varios fotogramas
dentro de un lienzo sin nombre, cada uno con su left: el script lo quita. Los
fotogramas son estados de una animación, no diapositivas: se anima de uno a otro.

Exportar desde Pencil (por MCP, con la ruta explícita del .pen):
    Export(["<id fotograma 1>", "<id fotograma 2>"], "html-css", "<ruta>/frames.html")

Uso:
    python3 scripts/pencil_to_hyperframes.py frames.html --project animations/mi-video \\
        --name buscar --pen-dir design/ --tokens docs/style/tokens.css [--duration 8]

Escribe compositions/<nombre>.html (y <nombre>.states.json si hay más de un fotograma)
e imprime el fragmento para montarla en index.html. Solo necesita Python 3; descargar
las fuentes necesita red la primera vez.
"""
import argparse
import html
import html.parser
import json
import re
import shutil
import sys
import unicodedata
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
SUBSETS = ("latin", "latin-ext")  # el español cabe en latin; latin-ext cubre flechas y signos de más


def slug(text):
    t = unicodedata.normalize("NFD", text.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "capa"


class Frames(html.parser.HTMLParser):
    """Recorre el <body> exportado y vuelve a escribirlo igual, con un id en cada capa con nombre.

    Usa el texto original de cada etiqueta (get_starttag_text) para no tocar mayúsculas de SVG
    (viewBox) ni el escapado."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self, prefix):
        super().__init__(convert_charrefs=False)
        self.prefix = prefix
        self.in_body = False
        self.stack = []        # (tag, nombre de capa o None, id o None)
        self.frames = []       # [{"name", "html": [trozos], "elements": {id: {...}}}]
        self.fonts_href = []
        self.used = {}

    def _frame(self):
        return self.frames[-1] if self.frames else None

    def _emit(self, text):
        if self.frames and any(e != "wrap" for _, _, e in self.stack):
            self.frames[-1]["html"].append(text)

    def handle_starttag(self, tag, attrs):
        raw = self.get_starttag_text()
        a = dict(attrs)
        if tag == "link" and "fonts.googleapis.com/css" in (a.get("href") or ""):
            self.fonts_href.append(html.unescape(a["href"]))
        if tag == "body":
            self.in_body = True
            return
        if not self.in_body:
            return
        name = a.get("data-pencil-name")
        if all(e == "wrap" for _, _, e in self.stack) and name is None:
            # Con varios fotogramas, Pencil los mete en un lienzo sin nombre: no es un fotograma.
            self.stack.append((tag, None, "wrap"))
            return
        if all(e == "wrap" for _, _, e in self.stack):  # un fotograma de primer nivel
            # Dentro del lienzo, cada fotograma lleva su left: en la composición va a 0.
            raw = re.sub(r"\b(left|top):\s*-?[\d.]+px", r"\1: 0px", raw)
            self.frames.append({"name": name or f"Fotograma {len(self.frames) + 1}", "html": [], "elements": {}})
            self.used = {}
        if name is not None:
            inner = [x for x in self.stack if x[2] != "wrap"]
            path = [n for _, n, _ in inner[1:] if n] + ([name] if inner else [])
            base = f"{self.prefix}-" + ("-".join(slug(p) for p in path) if path else "frame")
            count = self.used.get(base, 0) + 1
            self.used[base] = count
            eid = base if count == 1 else f"{base}-{count}"
            if "id" not in a:
                raw = re.sub(r"^<(\w+)", lambda m: f'<{m.group(1)} id="{eid}"', raw, count=1)
            else:
                eid = a["id"]
            style = a.get("style", "") if path else re.sub(r"\b(left|top):\s*-?[\d.]+px", r"\1: 0px", a.get("style", ""))
            self._frame()["elements"][eid] = {"name": name, "path": "/".join(path), "style": style,
                                              "text": ""}
        self.stack.append((tag, name, eid if name is not None else None))
        self._emit(raw)
        if tag in self.VOID:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        # <link … />, <path … />, <img … />: misma lógica que una etiqueta de apertura, sin cierre.
        depth = len(self.stack)
        self.handle_starttag(tag, attrs)
        if len(self.stack) > depth:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
            return
        if not self.in_body or not self.stack:
            return
        if self.stack[-1][2] != "wrap":
            self._emit(f"</{tag}>")
        while self.stack:
            t = self.stack.pop()[0]
            if t == tag:
                break

    def handle_data(self, data):
        if self.in_body and self.stack:
            self._emit(data)
            if data.strip():
                # El texto pertenece a la capa con nombre más cercana.
                owner = next((e for _, _, e in reversed(self.stack) if e), None)
                if owner is not None:
                    el = self._frame()["elements"][owner]
                    el["text"] = (el["text"] + " " + data.strip()).strip()

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        self.handle_data(f"&#{name};")

    def handle_comment(self, data):
        self._emit(f"<!--{data}-->")


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def local_fonts(hrefs, project):
    """Descarga los subconjuntos latin y latin-ext y devuelve las reglas @font-face con rutas locales."""
    rules = []
    for href in hrefs:
        css = fetch(href)
        for subset, body in re.findall(r"/\* ([\w-]+) \*/\s*@font-face\s*{([^}]*)}", css):
            if subset not in SUBSETS:
                continue
            family = re.search(r"font-family:\s*'([^']+)'", body).group(1)
            style = re.search(r"font-style:\s*(\w+)", body).group(1)
            weight = re.search(r"font-weight:\s*([\d ]+)", body).group(1).strip()
            url = re.search(r"src:\s*url\(([^)]+)\)", body).group(1)
            rng = re.search(r"unicode-range:\s*([^;]+)", body).group(1).strip()
            fname = f"{slug(family)}-{subset}-{weight.replace(' ', '-')}-{style}.woff2"
            dest = project / "assets" / "fonts" / fname
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(fetch(url, binary=True))
                print(f"fuente: {dest.relative_to(project)}")
            rules.append(f'@font-face {{ font-family: "{family}"; font-style: {style}; font-weight: {weight}; '
                         f'src: url("assets/fonts/{fname}") format("woff2"); unicode-range: {rng}; }}')
    return rules


def palette(tokens_css):
    """Colores literales de tokens.css: {"#d4ff3a": "lime", ...}; gana el primer nombre de cada color."""
    out = {}
    for name, hexv in re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})\b", Path(tokens_css).read_text(encoding="utf-8")):
        out.setdefault(hexv.lower(), name)
    return out


def tokenize_colors(text, pal):
    if not pal:
        return text, 0
    count = 0

    def sub(m):
        nonlocal count
        name = pal.get(m.group(0).lower())
        if not name:
            return m.group(0)
        count += 1
        return f"var(--{name}, {m.group(0)})"

    # Solo dentro de style="…": un color en el texto visible no se toca.
    return re.sub(r'style="([^"]*)"', lambda m: 'style="' + re.sub(r"#[0-9a-fA-F]{6}\b", sub, m.group(1)) + '"', text), count


def copy_assets(text, bases, project):
    """Copia las imágenes a assets/pencil/. Una ruta relativa se busca junto al export y junto al .pen."""
    copied = []

    def sub(m):
        quote, ref = m.group(1), m.group(2)
        if re.match(r"^(https?:|data:)", ref):
            return m.group(0)
        # Pencil ha exportado la misma imagen como «../assets/x.png» (relativa al HTML) y como
        # «assets/x.png» (relativa al .pen): se prueba en los dos sitios.
        src = next(((b / ref).resolve() for b in bases if (b / ref).is_file()), None)
        if src is None and (project / ref).is_file():
            return m.group(0)
        if src is None:
            print(f"aviso: no encuentro {ref} (ni junto al export ni junto al .pen)", file=sys.stderr)
            return m.group(0)
        dest = project / "assets" / "pencil" / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(dest.relative_to(project))
        return f"url({quote}assets/pencil/{src.name}{quote})"

    text = re.sub(r"url\((['\"]?)([^'\")]+)\1\)", sub, text)
    text = re.sub(r'(<img\b[^>]*\bsrc=")([^"]+)"',
                  lambda m: m.group(1) + sub(re.match(r"url\((['\"]?)([^'\")]+)\1\)", f"url({m.group(2)})"))[4:-1] + '"',
                  text)
    return text, copied


def style_props(style):
    return {k.strip(): v.strip() for k, v in (p.split(":", 1) for p in style.split(";") if ":" in p)}


def states(frames):
    """Qué cambia en cada fotograma respecto al primero, por id."""
    first = frames[0]["elements"]
    out = {"frames": [f["name"] for f in frames], "changes": {}, "enter": {}, "exit": {}}
    for f in frames[1:]:
        cur = f["elements"]
        changes = {}
        for eid, el in cur.items():
            if eid not in first:
                continue
            a, b = style_props(first[eid]["style"]), style_props(el["style"])
            diff = {k: b.get(k) for k in set(a) | set(b) if a.get(k) != b.get(k)}
            if first[eid]["text"] != el["text"]:
                diff["text"] = el["text"]
            if diff:
                changes[eid] = diff
        out["changes"][f["name"]] = changes
        out["enter"][f["name"]] = [k for k in cur if k not in first]
        out["exit"][f["name"]] = [k for k in first if k not in cur]
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("export", help="HTML exportado de Pencil con html-css")
    p.add_argument("--project", required=True, help="carpeta del proyecto de HyperFrames")
    p.add_argument("--name", required=True, help="nombre de la composición (y data-composition-id)")
    p.add_argument("--prefix", help="prefijo de los ids (por defecto, el nombre)")
    p.add_argument("--pen-dir", help="carpeta del .pen, por si una imagen no está junto al export")
    p.add_argument("--tokens", help="tokens.css de la identidad: los colores de la paleta pasan a variables")
    p.add_argument("--duration", type=float, default=5.0, help="s de la composición")
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--no-fonts", action="store_true", help="no descargar fuentes")
    a = p.parse_args()

    project = Path(a.project)
    export = Path(a.export)
    name = slug(a.name)
    parser = Frames(slug(a.prefix or a.name))
    parser.feed(export.read_text(encoding="utf-8"))
    if not parser.frames:
        sys.exit("No hay fotogramas en el <body> del export.")
    frame = parser.frames[0]
    body = "".join(frame["html"])

    bases = [export.parent] + ([Path(a.pen_dir)] if a.pen_dir else [])
    pal = palette(a.tokens) if a.tokens else {}
    body, copied = copy_assets(body, bases, project)
    body, ncolors = tokenize_colors(body, pal)
    fonts = [] if a.no_fonts else local_fonts(parser.fonts_href, project)

    font_css = "\n".join("    " + r for r in fonts)
    tokens_note = "" if not a.tokens else "\n    /* Colores de la paleta como var(--nombre, #hex): enlaza assets/tokens.css en index.html. */"
    out = f"""<template>
  <style>
{font_css}{tokens_note}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
  </style>
  <!-- Importado de Pencil: «{frame['name']}» ({export.name}). Cada capa lleva un id a partir de su nombre. -->
  <div id="root" data-composition-id="{name}" data-width="{a.width}" data-height="{a.height}">
    {body.strip()}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      // La animación va aquí, con los ids de las capas. Ejemplo:
      // tl.from("#{parser.prefix}-...", {{ opacity: 0, y: 24, duration: 0.6, ease: "expo.out" }}, 0.2);
      tl.to({{}}, {{ duration: {a.duration} }}, 0);
      window.__timelines = window.__timelines || {{}};
      window.__timelines["{name}"] = tl;
    }})();
  </script>
</template>
"""
    dest = project / "compositions" / f"{name}.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")

    ids = list(frame["elements"])
    print(f"composición: {dest} · {len(ids)} capas con id · {ncolors} colores a variables · {len(copied)} imágenes")
    if len(parser.frames) > 1:
        st = states(parser.frames)
        # El HTML de cada fotograma, ya convertido y con los mismos ids: de ahí se copian las capas que entran.
        ref_dir = project / "pencil" / name
        ref_dir.mkdir(parents=True, exist_ok=True)
        st["html"] = {}
        for i, f in enumerate(parser.frames, 1):
            fhtml, _ = copy_assets("".join(f["html"]), bases, project)
            fhtml, _ = tokenize_colors(fhtml, pal)
            fpath = ref_dir / f"{i:02d}-{slug(f['name'])}.html"
            fpath.write_text(fhtml.strip() + "\n", encoding="utf-8")
            st["html"][f["name"]] = str(fpath.relative_to(project))
        sdest = project / "compositions" / f"{name}.states.json"
        sdest.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
        for fname in st["frames"][1:]:
            print(f"  «{fname}»: {len(st['changes'][fname])} capas cambian, {len(st['enter'][fname])} entran, "
                  f"{len(st['exit'][fname])} salen")
        print(f"estados: {sdest}")
        print(f"HTML de cada fotograma (para copiar las capas que entran): {ref_dir}")
    print("\nIds (capa → id):")
    for eid in ids[:40]:
        print(f"  {frame['elements'][eid]['path'] or frame['name']} → #{eid}")
    if len(ids) > 40:
        print(f"  … y {len(ids) - 40} más")
    print(f"""
Para montarla en index.html:
  <div id="{name}-host" data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="0" data-duration="{a.duration}" data-track-index="1"></div>
Después: npx hyperframes check y npx hyperframes snapshot --at <s>.""")


if __name__ == "__main__":
    main()

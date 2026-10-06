#!/usr/bin/env python3
"""Genera el fondo vivo de Leon: atlas de fotogramas + shader + still.

Uso:
  leon-wallpaper.py <mark-animated.svg> <leon-dir> <leon-light-dir>

Entrada: `brand/logo/final/mark-animated.svg` del repo de Leon (SMIL, 26 s,
parpadeos y miradas). Salida por variante, dentro de cada directorio de tema:

  backgrounds/02-mark-live.png   postura de reposo a tamaño de pantalla
  tools/mark-grid.png            atlas de 96 fotogramas de 256 px en 16x6
  tools/mark.frag.qsb            shader compilado con la timeline

Necesita: python3 con Pillow, rsvg-convert y qsb (qt6-shadertools).
El shader resultante espera el parche de atlas descrito en
`tools/background-live-atlas.md`.
"""
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

TILE = 256          # px por casilla del atlas
COLS = 16
FPS = 24.0          # muestreo de los tramos en movimiento
LOOP = 26.0         # duración del ciclo, en segundos (dur="26s")
BOX = 0.30          # lado del logo respecto al lado menor de la pantalla
SCREEN = (3440, 1440)

VARIANTS = {
    "dark": {"bg": "#0A0A0A", "fg": "#FFEA00"},
    "light": {"bg": "#FAFAF9", "fg": "#0A0A0A"},
}


def main(svg_path, dark_dir, light_dir):
    src = open(svg_path).read()
    kt = [float(x) for x in re.search(r'keyTimes="([^"]+)"', src).group(1).split(';')]
    vals = re.search(r'values="([^"]+)"', src).group(1).split(';')
    rest = vals[0]

    def lerp_path(a, b, f):
        out, i = [], 0
        for tok in re.split(r'(-?\d+\.?\d*)', a):
            if re.fullmatch(r'-?\d+\.?\d*', tok):
                na = float(tok)
                nb = float(re.split(r'(-?\d+\.?\d*)', b)[i * 2 + 1])
                v = na + (nb - na) * f
                out.append(f"{v:.3f}".rstrip('0').rstrip('.'))
                i += 1
            else:
                out.append(tok)
        return ''.join(out)

    bursts = []
    for i in range(len(vals) - 1):
        if vals[i] != vals[i + 1]:
            if bursts and i == bursts[-1][1] + 1:
                bursts[-1][1] = i
            else:
                bursts.append([i, i])

    frames = [rest]
    segments = []
    for a, b in bursts:
        t0, t1 = kt[a] * LOOP, kt[b + 1] * LOOP
        n = int(math.ceil((t1 - t0) * FPS)) + 1
        first = len(frames)
        for j in range(n):
            f = j / (n - 1) if n > 1 else 0.0
            pos = a + f * (b + 1 - a)
            k0 = min(int(math.floor(pos)), len(vals) - 2)
            frames.append(lerp_path(vals[k0], vals[k0 + 1], pos - k0))
        segments.append((t0, t1, first, n))

    rows = math.ceil(len(frames) / COLS)
    if rows * COLS < len(frames):
        sys.exit("atlas sin sitio")
    print(f"frames={len(frames)} atlas={COLS}x{rows} segmentos={len(segments)}")

    def render(path_data, size, fill, bg):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
               f'<rect width="64" height="64" fill="{bg}"/>'
               f'<path fill="{fill}" fill-rule="evenodd" d="{path_data}"/></svg>')
        with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as f:
            f.write(svg)
            tmp = f.name
        out = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-o", out, tmp],
                       check=True)
        os.unlink(tmp)
        return Image.open(out).convert("RGB")

    qsb = shutil.which("qsb") or "/usr/lib/qt6/bin/qsb"

    for name, v in VARIANTS.items():
        theme_dir = dark_dir if name == "dark" else light_dir
        bgrs = os.makedirs(os.path.join(theme_dir, "backgrounds"), exist_ok=True)
        os.makedirs(os.path.join(theme_dir, "tools"), exist_ok=True)

        atlas = Image.new("RGB", (COLS * TILE, rows * TILE), v["bg"])
        for idx, p in enumerate(frames):
            atlas.paste(render(p, TILE, v["fg"], v["bg"]),
                        ((idx % COLS) * TILE, (idx // COLS) * TILE))
        atlas.save(os.path.join(theme_dir, "tools", "mark-grid.png"), optimize=True)

        sw, sh = SCREEN
        box = int(round(BOX * min(sw, sh)))
        still = Image.new("RGB", SCREEN, v["bg"])
        still.paste(render(rest, box, v["fg"], v["bg"]),
                    ((sw - box) // 2, (sh - box) // 2))
        still.save(os.path.join(theme_dir, "backgrounds", "02-mark-live.png"),
                   optimize=True)

        segs = ",\n  ".join(f"vec4({t0:.4f}, {t1:.4f}, {float(fr)}, {float(n)})"
                            for t0, t1, fr, n in segments)
        pr, pg, pb = (int(v['bg'][i:i + 2], 16) / 255 for i in (1, 3, 5))
        shader = SHADER.format(LOOP=LOOP, BOX=BOX, COLS=COLS, ROWS=rows,
                               PAGE=f"vec3({pr:.4f}, {pg:.4f}, {pb:.4f})",
                               SEGN=len(segments), SEGS=segs)
        frag = os.path.join(theme_dir, "tools", "mark.frag")
        open(frag, "w").write(shader)
        subprocess.run([qsb, "--glsl", "100es,120,150,300es", "--hlsl", "50",
                        "--msl", "12", "-o", frag + ".qsb", frag], check=True)
        print(f"{name}: {theme_dir}")


SHADER = """#version 440

// Leon — marca viva para el fondo del escritorio.
//
// Generado por tools/leon-wallpaper.py a partir de
// brand/logo/final/mark-animated.svg del repositorio de Leon. Solo dibuja
// parpadeos y miradas (los gestos del logo vivo de la app); entre gesto y
// gesto la postura es la de reposo. Fuera de cada tramo la textura no se
// muestrea: se pinta el fondo del tema.
//
// El PNG hermano (`...-live.png`) es la postura de reposo a tamaño de
// pantalla; el plugin de fondo lo deja debajo del shader y lo muestra cuando
// el shader se apaga (portátil con batería), así que la transición no se nota.

layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {{
    mat4  qt_Matrix;
    float qt_Opacity;
    float uTime;
    vec2  uResolution;
}};

layout(binding = 1) uniform sampler2D uAtlas;

const float LOOP   = {LOOP:.1f};
const float BOX    = {BOX:.2f};
const int   COLS   = {COLS};
const int   ROWS   = {ROWS};
const vec3  PAGE   = {PAGE};
// Corrección de orientación vertical del atlas, según backend gráfico.
const bool  FLIP_Y = false;

// Gestos: (t0, t1, primer frame, nº de frames).
const int   SEGN = {SEGN};
const vec4  SEGS[SEGN] = vec4[SEGN](
  {SEGS}
);

float frameIndex(float t) {{
    for (int i = 0; i < SEGN; i++) {{
        vec4 s = SEGS[i];
        if (t >= s.x && t < s.y) {{
            float f = (t - s.x) / max(1e-5, s.y - s.x);
            return s.z + floor(f * (s.w - 1.0) + 0.5);
        }}
    }}
    return 0.0;
}}

void main() {{
    vec2 res = uResolution;
    float box = BOX * min(res.x, res.y);
    vec2 px = qt_TexCoord0 * res;
    vec2 local = (px - res * 0.5) / box + 0.5;

    vec3 colour = PAGE;
    if (local.x > 0.0 && local.x < 1.0 && local.y > 0.0 && local.y < 1.0) {{
        float fi = frameIndex(mod(uTime, LOOP));
        float col = mod(fi, float(COLS));
        float row = floor(fi / float(COLS));
        float v = local.y;
        if (FLIP_Y) v = 1.0 - v;
        vec2 uv = (vec2(col, row) + vec2(local.x, v)) / vec2(float(COLS), float(ROWS));
        colour = texture(uAtlas, uv).rgb;
    }}

    fragColor = vec4(colour, 1.0) * qt_Opacity;
}}
"""

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

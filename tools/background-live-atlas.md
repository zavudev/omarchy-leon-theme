# Live wallpaper: el parche del plugin de fondo

Los fondos `*-live.png` de este repositorio resuelven, en el plugin de fondo
de Omarchy, al shader `tools/<nombre>.frag.qsb` del tema. El parche original
(del tema Zavu) solo pasa `uTime` y `uResolution`; la marca de Leon necesita
además **una textura**: un atlas de fotogramas en `tools/<nombre>-grid.png`.

Con el plugin stock, el shader se carga pero el atlas no llega: se ve una
caja negra (o nada). Añade esto a tu copia del plugin:

```bash
omarchy plugin clone omarchy.background   # si aún no lo has clonado
# edita ~/.config/omarchy/plugins/<usuario>.background/Background.qml
```

## 1. Propiedades (junto a `liveShaderUrl`)

```qml
readonly property url liveAtlasUrl: liveShaderName === ""
  ? ""
  : Util.fileUrl(stateHome + "/omarchy/current/theme/tools/" + liveShaderName + "-grid.png")
```

## 2. Textura y ShaderEffect (junto al `ShaderEffect` del fondo)

```qml
Image {
  id: liveAtlasImage
  source: root.liveAtlasUrl
  width: implicitWidth
  height: implicitHeight
  cache: true
  smooth: true
  onStatusChanged: if (status === Image.Ready) liveAtlasSource.scheduleUpdate()
}

ShaderEffectSource {
  id: liveAtlasSource
  sourceItem: liveAtlasImage
  hideSource: true
  live: false
  recursive: false
}

ShaderEffect {
  id: liveShader
  anchors.fill: parent
  visible: root.liveShaderUrl != "" && root.liveShaderAllowed
  blending: false
  fragmentShader: root.liveShaderUrl
  property real uTime: 43.0
  property vector2d uResolution: Qt.vector2d(width, height)
  property variant uAtlas: liveAtlasSource   // <- la textura
}
```

`live: false` + `scheduleUpdate()` capturan el atlas una sola vez (el atlas no
cambia). Con la batería puesta el shader se apaga y queda el PNG
`*-live.png`, renderizado en la misma postura de reposo: el escritorio deja
de moverse, no cambia de aspecto.

**Nota:** al guardar el plugin, el shell puede no recargar un *service* de
verdad; si el cambio no se aplica, `omarchy restart shell`.

## Regenerar el atlas

```bash
tools/leon-wallpaper.py <repo-leon>/brand/logo/final/mark-animated.svg \
                        leon leon-light
```

Necesita `rsvg-convert`, Pillow y `qsb` (qt6-shadertools). El script muestrea
los 12 gestos del SVG animado (3,2 s de movimiento en un ciclo de 26 s) a
24 fps y hornea la línea de tiempo en el shader; el resto del ciclo es la
postura de reposo.

# Omarchy Leon themes

Leon (by Zavu) applied to the Omarchy desktop: stone neutrals, hairlines,
and one acid-yellow signal (`#FFEA00`) spent only on focus, selection and
active state — the same discipline as the Leon app theme
(`crates/app/src/theme/leon.rs`).

| Theme | Mode | Page | Signal |
|---|---|---|---|
| `leon` | dark | `#0A0A0A` near-black | `#FFEA00` acid yellow |
| `leon-light` | light | `#FAFAF9` paper | `#756600` olive (5.5:1 on paper) |

The wallpaper is the Leon mark itself — animated, when the background
plugin can run the live shader (see [the live wallpaper](#the-live-wallpaper)).

Warning is orange (`#FF9500` / `#A06000`): yellow terminal text is never
mistaken for the acid-yellow cursor. ANSI red/green/yellow/cyan are the four
state colours, so a state means the same in a terminal and in the app.

## Install

```bash
omarchy theme install https://github.com/zavudev/omarchy-leon-theme.git
omarchy theme set leon
```

## What's in here

| Path | Drives |
|---|---|
| `leon/colors.toml`, `leon-light/colors.toml` | The palettes. Terminals, editor and browser configs are generated from these alone. |
| `leon/shell.toml`, `leon-light/shell.toml` | Bar, menus, notifications, launcher, lock screen. |
| `leon/hyprland.lua`, `leon-light/hyprland.lua` | 1 px hairline borders, 6 px corners, no shadows, one instrument easing. |
| `leon/hyprlock.conf`, `leon-light/hyprlock.conf` | Lock screen input field. |
| `leon/backgrounds/`, `leon-light/backgrounds/` | Wallpapers: `01-void` / `01-paper` (plain) and `02-mark-live.png`, the Leon mark. The `-live` name makes it a live wallpaper where the background plugin supports it (below). |
| `leon/tools/mark.frag.qsb` + `mark-grid.png` | The compiled live shader and its 96-frame atlas (16×6 tiles). |
| `tools/background-live-atlas.md` | How to teach the background plugin to pass the atlas to the shader (one Image + one ShaderEffectSource + one property). |
| `tools/leon-wallpaper.py` | Regenerates the atlas, still and shader from Leon's `mark-animated.svg` (`rsvg-convert` + Pillow + `qsb`). |
| `tools/leon-sync` | `theme-set` hook: regenerates Leon's own `omarchy` theme from the active Omarchy palette, so the app follows `omarchy theme set <anything>`. Install with `omarchy hook install theme-set tools/leon-sync`. |
| `tools/leon-sessions` | Bar command widget: agent sessions touched in 24 h (reads `leon.db` read-only). Copy to `~/.config/omarchy/bar/scripts/` and add the entry to `shell.json` (see repo docs or the installed example). |
| `tools/hyprland-leon.lua` | Window rule (opaque Leon window) + `SUPER + SHIFT + L` launcher binding. |

## The live wallpaper

`02-mark-live.png` is the Leon mark at rest. In the background plugin it
resolves, by name, to `tools/mark.frag.qsb`: a shader that plays the mark's
own gestures — blinks and glances, the same animation as the app's live
logo — from the atlas next to it. Between gestures the mark is still, and
off battery (a laptop unplugged) the shader switches itself off, leaving
the PNG in the very same pose.

The stock plugin only passes `uTime`; the atlas needs the small patch in
[`tools/background-live-atlas.md`](tools/background-live-atlas.md). Then
`omarchy theme bg next` selects it like any other background.

## Note for installed copies

A theme cloned by `omarchy theme install` is held to the stranger list:
any `*.lua`, terminal configs and `vscode.json` it ships are dropped and
regenerated from `colors.toml` through the stock templates (named on
stderr). Everything else — including `shell.toml` — is kept. That means an
installed copy wears the stock Hyprland geometry with Leon colours. To get
the full `hyprland.lua` (6 px corners, custom curves) from the repo copy:

```bash
rm -rf ~/.config/omarchy/themes/leon/.git   # mine, ya no "de un extraño"
omarchy theme set leon
```

## License

MIT. The Zavu/Leon brand identity (logo, isotype, wordmark, names) is not
covered and remains the property of Zavu.

# Omarchy Leon themes

Leon (by Zavu) applied to the Omarchy desktop: stone neutrals, hairlines,
and one acid-yellow signal (`#FFEA00`) spent only on focus, selection and
active state — the same discipline as the Leon app theme
(`crates/app/src/theme/leon.rs`).

| Theme | Mode | Page | Signal |
|---|---|---|---|
| `leon` | dark | `#0A0A0A` near-black | `#FFEA00` acid yellow |
| `leon-light` | light | `#FAFAF9` paper | `#756600` olive (5.5:1 on paper) |

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
| `leon/backgrounds/`, `leon-light/backgrounds/` | Wallpapers (placeholder stills; replace with your own). |
| `tools/leon-sync` | `theme-set` hook: regenerates Leon's own `omarchy` theme from the active Omarchy palette, so the app follows `omarchy theme set <anything>`. Install with `omarchy hook install theme-set tools/leon-sync`. |
| `tools/leon-sessions` | Bar command widget: agent sessions touched in 24 h (reads `leon.db` read-only). Copy to `~/.config/omarchy/bar/scripts/` and add the entry to `shell.json` (see repo docs or the installed example). |
| `tools/hyprland-leon.lua` | Window rule (opaque Leon window) + `SUPER + SHIFT + L` launcher binding. |

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

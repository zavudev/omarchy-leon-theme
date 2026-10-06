-- Leon — geometry and motion for Omarchy/Hyprland.
-- Editorial hairline (1px), 6px corners on controls/windows (radius_cell 0 is
-- the app's terminal grids; desktop windows take the control radius), no
-- shadows. Acid yellow marks the focused window and nothing else.
-- Motion: calm, mechanical, instrument-like — one easing, no overshoot, no spring.

local signal = "rgba(ffea00ff)"
local border = "rgba(262626ff)"

hl.config({
  general = {
    col = {
      active_border = signal,
      inactive_border = border,
    },
    gaps_in = 5,
    gaps_out = 10,
    border_size = 1,
  },
  group = {
    col = {
      border_active = signal,
      border_inactive = border,
    },
  },
  decoration = {
    rounding = 6,
    shadow = {
      enabled = false,
    },
  },
  animations = {
    enabled = true,
  },
})

hl.curve("leonStandard", { type = "bezier", points = { { 0.22, 1.00 }, { 0.36, 1.00 } } })
hl.curve("leonAccel", { type = "bezier", points = { { 0.40, 0.00 }, { 1.00, 1.00 } } })

hl.animation({ leaf = "windowsIn", enabled = true, speed = 4, bezier = "leonStandard", style = "popin 97%" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 3, bezier = "leonAccel", style = "popin 97%" })
hl.animation({ leaf = "windowsMove", enabled = true, speed = 4, bezier = "leonStandard" })
hl.animation({ leaf = "border", enabled = true, speed = 8, bezier = "leonStandard" })
hl.animation({ leaf = "layersIn", enabled = true, speed = 3, bezier = "leonStandard", style = "fade" })
hl.animation({ leaf = "layersOut", enabled = true, speed = 3, bezier = "leonAccel", style = "fade" })
hl.animation({ leaf = "fadeLayersIn", enabled = true, speed = 3, bezier = "leonStandard" })
hl.animation({ leaf = "fadeLayersOut", enabled = true, speed = 3, bezier = "leonAccel" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 5, bezier = "leonStandard", style = "slide" })
hl.animation({ leaf = "specialWorkspaceIn", enabled = true, speed = 4, bezier = "leonStandard", style = "slidevert" })
hl.animation({ leaf = "specialWorkspaceOut", enabled = true, speed = 3, bezier = "leonAccel", style = "slidevert" })

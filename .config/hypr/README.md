# Hyprland Config

Personal Hyprland 0.55+ setup (Lua config) with Omarchy-style keybindings. Shared across machines; per-machine settings live in `hosts/`.

## Structure

```
~/.config/hypr/
├── hyprland.lua        # Main config: monitors, autostart, env, look & feel, input
├── keybinds.lua        # All keybindings (loaded with require("keybinds"))
├── hosts/
│   └── l33t.lua        # Machine-specific: monitors, NVIDIA env vars
└── scripts/
    └── powermenu.sh    # Super + Escape system menu
```

## Dependencies

```zsh
sudo pacman -S waybar wofi dunst hyprpaper hyprlock hyprpicker grim slurp wl-clipboard jq btop impala bluetui playerctl brightnessctl
```

## Shortcuts

### Apps & menus
| Keys | Action |
|---|---|
| Super + Return | Terminal |
| Super + Shift + Return | Chrome |
| Super + Shift + F | File manager (Nemo) |
| Super + Space | App launcher |
| Super + Escape | Power menu |
| Super + Ctrl + L | Lock screen |
| Super + Ctrl + B / W / T | Bluetooth / Wi-Fi / btop |
| Super + Shift + Space | Toggle Waybar |

### Windows
| Keys | Action |
|---|---|
| Super + W | Close window |
| Ctrl + Alt + Delete | Close all windows |
| Super + T | Toggle floating |
| Super + F | Fullscreen |
| Super + Alt + F | Maximize (keeps the bar) |
| Super + P | Pseudo-tile |
| Super + J | Flip split direction |
| Super + Backspace | Toggle transparency |
| Super + Arrows | Move focus |
| Super + Shift + Arrows | Swap window |
| Super + − / = | Shrink / grow width |
| Super + Shift + − / = | Shrink / grow height |
| Super + Left drag | Move window |
| Super + Right drag | Resize window |

### Groups
| Keys | Action |
|---|---|
| Super + G | Make or undo a group |
| Super + Alt + G | Pull window out of group |
| Super + Alt + Arrows | Move window into group in that direction |
| Super + Alt + Tab, Super + Ctrl + ← / → | Cycle tabs in a group |

### Workspaces
| Keys | Action |
|---|---|
| Super + 1–0 | Go to workspace |
| Super + Shift + 1–0 | Move window there and follow |
| Super + Shift + Alt + 1–0 | Move window there, stay put |
| Super + Tab / Shift + Tab | Next / previous workspace |
| Super + Ctrl + Tab | Last-used workspace |
| Super + Scroll | Cycle workspaces |
| Super + Shift + Alt + ← / → | Send workspace to other monitor |
| Super + S | Show or hide the scratchpad |
| Super + Alt + S | Send window to the scratchpad |

### Screenshots & misc
| Keys | Action |
|---|---|
| Print | Region screenshot to clipboard |
| Shift + Print | Full screenshot to clipboard |
| Super + Print | Color picker |
| Media keys | Volume, mute, play/pause, next/previous |
| Super + Shift + Escape | Quit Hyprland |

## Notes

- After editing: `hyprctl reload && hyprctl configerrors`
- Format Lua files: `stylua ~/.config/hypr/`
- New machine: add `hosts/<hostname>.lua` for its monitors and GPU settings.
- If a monitor shows up at 640x480, its EDID read failed. Replug the DP cable.

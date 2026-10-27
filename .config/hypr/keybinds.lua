-- ~/.config/hypr/keybinds.lua
-- Omarchy-style keybindings, adapted for a plain Hyprland 0.55+ Lua setup.
-- Load it from hyprland.lua with: require("keybinds")

local mod = "SUPER"
local terminal = "gnome-terminal"
local fileManager = "nemo"
local browser = "google-chrome-stable"
local launcher = "wofi --show drun"
local scripts = os.getenv("HOME") .. "/.config/hypr/scripts"


-- Dispatchers without a known Lua wrapper go through hyprctl
local function dispatch(cmd)
	return hl.dsp.exec_cmd("hyprctl dispatch " .. cmd)
end


local function in_terminal(cmd)
	return hl.dsp.exec_cmd(terminal .. " -- " .. cmd)
end


-----------------------
---- APPS & MENUS ----
-----------------------
hl.bind(mod .. " + return", hl.dsp.exec_cmd(terminal))
hl.bind(mod .. " + SHIFT + return", hl.dsp.exec_cmd(browser))
hl.bind(mod .. " + SHIFT + F", hl.dsp.exec_cmd(fileManager))
hl.bind(mod .. " + space", hl.dsp.exec_cmd(launcher))
hl.bind(mod .. " + escape", hl.dsp.exec_cmd(scripts .. "/powermenu.sh"))
hl.bind(mod .. " + CTRL + L", hl.dsp.exec_cmd("hyprlock"))

-- Control menu, plus a shortcut straight to its Capture section
hl.bind(mod .. " + ALT + space", hl.dsp.exec_cmd(scripts .. "/menu.sh"))
hl.bind(mod .. " + CTRL + C", hl.dsp.exec_cmd(scripts .. "/menu.sh capture"))

-- TUI tools (bluetui, impala, btop)
hl.bind(mod .. " + CTRL + B", in_terminal("bluetui"))
hl.bind(mod .. " + CTRL + W", in_terminal("impala"))
hl.bind(mod .. " + CTRL + T", in_terminal("btop"))

-- Toggle the top bar
hl.bind(mod .. " + SHIFT + space", hl.dsp.exec_cmd("pkill -SIGUSR1 waybar"))

-------------------
---- WINDOWS ----
-------------------
hl.bind(mod .. " + W", hl.dsp.window.close())
hl.bind("CTRL + ALT + delete", hl.dsp.exec_cmd("hyprctl clients -j | jq -r '.[].address' "
	.. "| xargs -I{} hyprctl dispatch closewindow address:{}"))
hl.bind(mod .. " + T", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mod .. " + F", hl.dsp.window.fullscreen())
hl.bind(mod .. " + ALT + F", dispatch("fullscreen 1"))
hl.bind(mod .. " + P", hl.dsp.window.pseudo())
hl.bind(mod .. " + J", hl.dsp.layout("togglesplit"))
hl.bind(mod .. " + backspace", dispatch("setprop active opaque toggle"))

-- Focus and swap with arrows
local arrows = {
	left = "l",
	right = "r",
	up = "u",
	down = "d",
}

for key, dir in pairs(arrows) do
	hl.bind(mod .. " + " .. key, dispatch("movefocus " .. dir))
	hl.bind(mod .. " + SHIFT + " .. key, dispatch("swapwindow " .. dir))
end

-- Resize: Super + minus/equal (width), Super + Shift + minus/equal (height)
local held = { repeating = true }
hl.bind(mod .. " + minus", dispatch("resizeactive -100 0"), held)
hl.bind(mod .. " + equal", dispatch("resizeactive 100 0"), held)
hl.bind(mod .. " + SHIFT + minus", dispatch("resizeactive 0 -100"), held)
hl.bind(mod .. " + SHIFT + equal", dispatch("resizeactive 0 100"), held)

-- Mouse: drag to move, right-drag to resize
hl.bind(mod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind(mod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

------------------
---- GROUPS ----
------------------
hl.bind(mod .. " + G", dispatch("togglegroup"))
hl.bind(mod .. " + ALT + G", dispatch("moveoutofgroup"))
hl.bind(mod .. " + ALT + tab", dispatch("changegroupactive f"))
hl.bind(mod .. " + CTRL + left", dispatch("changegroupactive b"))
hl.bind(mod .. " + CTRL + right", dispatch("changegroupactive f"))

for key, dir in pairs(arrows) do
	hl.bind(mod .. " + ALT + " .. key, dispatch("moveintogroup " .. dir))
end

----------------------
---- WORKSPACES ----
----------------------
-- Super + N: go to workspace
-- Super + Shift + N: move window there and follow
-- Super + Shift + Alt + N: move window there silently
for i = 1, 10 do
	local key = i % 10

	hl.bind(mod .. " + " .. key, hl.dsp.focus({ workspace = i }))
	hl.bind(mod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
	hl.bind(mod .. " + SHIFT + ALT + " .. key, dispatch("movetoworkspacesilent " .. i))
end

hl.bind(mod .. " + tab", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mod .. " + SHIFT + tab", hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mod .. " + CTRL + tab", dispatch("workspace previous"))
hl.bind(mod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mod .. " + mouse_up", hl.dsp.focus({ workspace = "e-1" }))

-- Move the whole workspace to the other monitor
hl.bind(mod .. " + SHIFT + ALT + left", dispatch("movecurrentworkspacetomonitor l"))
hl.bind(mod .. " + SHIFT + ALT + right", dispatch("movecurrentworkspacetomonitor r"))

-- Scratchpad
hl.bind(mod .. " + S", dispatch("togglespecialworkspace scratchpad"))
hl.bind(mod .. " + ALT + S", dispatch("movetoworkspacesilent special:scratchpad"))

-----------------------
---- SCREENSHOTS ----
-----------------------
hl.bind("Print", hl.dsp.exec_cmd('grim -g "$(slurp)" - | wl-copy'))
hl.bind("SHIFT + Print", hl.dsp.exec_cmd("grim - | wl-copy"))
hl.bind(mod .. " + Print", hl.dsp.exec_cmd("hyprpicker -a"))

-----------------
---- MEDIA ----
-----------------
local media = { locked = true, repeating = true }
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), media)
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), media)
hl.bind("XF86AudioMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), media)
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("brightnessctl set 5%+"), media)
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl set 5%-"), media)

hl.bind("XF86AudioPlay", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioNext", hl.dsp.exec_cmd("playerctl next"), { locked = true })
hl.bind("XF86AudioPrev", hl.dsp.exec_cmd("playerctl previous"), { locked = true })

-- Exit Hyprland
hl.bind(mod .. " + SHIFT + escape", hl.dsp.exit())

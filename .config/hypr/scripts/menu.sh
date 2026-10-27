#!/usr/bin/env bash
# ~/.config/hypr/scripts/menu.sh — Omarchy-style control menu
# Usage: menu.sh            -> main menu
#        menu.sh capture    -> jump straight to a submenu (capture, toggle, setup, install, remove)

TERMINAL="gnome-terminal"
EDITOR_CMD="${EDITOR:-nvim}"
HYPR="$HOME/.config/hypr"
SCRIPTS="$HYPR/scripts"
SHOTS="$HOME/Pictures/Screenshots"
VIDEOS="$HOME/Videos/Recordings"


# Pressing the menu key again closes it, like Omarchy
if pkill -x wofi; then
	exit 0
fi


menu() {
	local prompt="$1"
	local options="$2"

	printf "%b" "$options" | wofi --dmenu --insensitive --prompt "$prompt" --width 320
}


run_in_terminal() {
	"$TERMINAL" -- bash -c "$1; echo; read -n 1 -s -r -p 'Press any key to close...'"
}


edit() {
	"$TERMINAL" -- "$EDITOR_CMD" "$1"
}


aur_helper() {
	if command -v yay >/dev/null; then
		echo yay
	elif command -v paru >/dev/null; then
		echo paru
	fi
}


toggle_process() {
	local name="$1"
	local label="$2"

	shift 2

	if pgrep -x "$name" >/dev/null; then
		pkill -x "$name"
		notify-send "$label off"
	else
		setsid -f "$@" >/dev/null 2>&1
		notify-send "$label on"
	fi
}


show_capture_menu() {
	mkdir -p "$SHOTS" "$VIDEOS"

	local stamp
	stamp=$(date +%Y-%m-%d_%H-%M-%S)

	local choice
	choice=$(menu "Capture" "Screenshot region\nScreenshot full\nRecord region\nRecord full\nStop recording\nColor picker")

	# Let wofi close before grabbing the screen
	sleep 0.2

	case "$choice" in
		"Screenshot region")
			local region
			region=$(slurp) || return

			grim -g "$region" - | tee "$SHOTS/$stamp.png" | wl-copy
			notify-send "Screenshot saved and copied"
			;;
		"Screenshot full")
			grim - | tee "$SHOTS/$stamp.png" | wl-copy
			notify-send "Screenshot saved and copied"
			;;
		"Record region")
			local region
			region=$(slurp) || return

			setsid -f wf-recorder -g "$region" -f "$VIDEOS/$stamp.mp4" >/dev/null 2>&1
			notify-send "Recording… (menu → Capture → Stop recording)"
			;;
		"Record full")
			setsid -f wf-recorder -f "$VIDEOS/$stamp.mp4" >/dev/null 2>&1
			notify-send "Recording… (menu → Capture → Stop recording)"
			;;
		"Stop recording")
			pkill -INT -x wf-recorder && notify-send "Recording saved to $VIDEOS"
			;;
		"Color picker")
			hyprpicker -a
			;;
		*)
			show_main_menu
			;;
	esac
}


show_toggle_menu() {
	case $(menu "Toggle" "Top bar\nNight light\nIdle lock\nDo not disturb") in
		"Top bar")
			pkill -SIGUSR1 waybar
			;;
		"Night light")
			toggle_process hyprsunset "Night light" hyprsunset -t 4500
			;;
		"Idle lock")
			toggle_process hypridle "Idle lock" hypridle
			;;
		"Do not disturb")
			dunstctl set-paused toggle
			;;
		*)
			show_main_menu
			;;
	esac
}


show_setup_menu() {
	local host_file="$HYPR/hosts/$(</etc/hostname).lua"

	if [ ! -f "$host_file" ]; then
		host_file="$HYPR/hyprland.lua"
	fi

	case $(menu "Setup" "Audio\nWifi\nBluetooth\nMonitors\nKeybindings\nHyprland\nWaybar\nThis menu") in
		"Audio") setsid -f pavucontrol >/dev/null 2>&1 ;;
		"Wifi") "$TERMINAL" -- impala ;;
		"Bluetooth") "$TERMINAL" -- bluetui ;;
		"Monitors") edit "$host_file" ;;
		"Keybindings") edit "$HYPR/keybinds.lua" ;;
		"Hyprland") edit "$HYPR/hyprland.lua" ;;
		"Waybar") edit "$HOME/.config/waybar/config.jsonc" ;;
		"This menu") edit "$SCRIPTS/menu.sh" ;;
		*) show_main_menu ;;
	esac
}


show_install_menu() {
	local helper
	helper=$(aur_helper)

	local options="Package"

	if [ -n "$helper" ]; then
		options="$options\nAUR package"
	fi

	case $(menu "Install" "$options") in
		"Package")
			run_in_terminal "pacman -Slq | fzf --multi --preview 'pacman -Si {}' | xargs -ro sudo pacman -S"
			;;
		"AUR package")
			run_in_terminal "$helper -Slqa | fzf --multi --preview '$helper -Si {}' | xargs -ro $helper -S"
			;;
		*)
			show_main_menu
			;;
	esac
}


show_remove_menu() {
	case $(menu "Remove" "Package") in
		"Package")
			run_in_terminal "pacman -Qqe | fzf --multi --preview 'pacman -Qi {}' | xargs -ro sudo pacman -Rns"
			;;
		*)
			show_main_menu
			;;
	esac
}


run_update() {
	local helper
	helper=$(aur_helper)

	if [ -n "$helper" ]; then
		run_in_terminal "$helper -Syu"
	else
		run_in_terminal "sudo pacman -Syu"
	fi
}


show_main_menu() {
	case $(menu "Menu" "Apps\nCapture\nToggle\nSetup\nInstall\nRemove\nUpdate\nAbout\nSystem") in
		"Apps") wofi --show drun ;;
		"Capture") show_capture_menu ;;
		"Toggle") show_toggle_menu ;;
		"Setup") show_setup_menu ;;
		"Install") show_install_menu ;;
		"Remove") show_remove_menu ;;
		"Update") run_update ;;
		"About") run_in_terminal "fastfetch" ;;
		"System") "$SCRIPTS/powermenu.sh" ;;
	esac
}


case "$1" in
	capture) show_capture_menu ;;
	toggle) show_toggle_menu ;;
	setup) show_setup_menu ;;
	install) show_install_menu ;;
	remove) show_remove_menu ;;
	*) show_main_menu ;;
esac

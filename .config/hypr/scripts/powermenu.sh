#!/usr/bin/env bash
# ~/.config/hypr/scripts/powermenu.sh — Omarchy-style system menu (Super + Escape)

choice=$(printf "Lock\nSuspend\nLog out\nRestart\nShut down" | wofi --dmenu --insensitive --prompt "System")

case "$choice" in
	"Lock") hyprlock ;;
	"Suspend") systemctl suspend ;;
	"Log out") hyprctl dispatch exit ;;
	"Restart") systemctl reboot ;;
	"Shut down") systemctl poweroff ;;
esac

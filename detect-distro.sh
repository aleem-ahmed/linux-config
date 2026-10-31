get_os_field()
{
	local field="$1"

	grep -E "^${field}=" /etc/os-release 2>/dev/null \
		| head -n1 \
		| cut -d= -f2- \
		| tr -d '"' \
		| tr '[:upper:]' '[:lower:]'
}

detect_distro()
{
	local id
	local id_like

	id=$(get_os_field ID)
	id_like=$(get_os_field ID_LIKE)

	case "$id" in
		arch)
			echo "arch"
			;;
		linuxmint)
			echo "mint"
			;;
		*)
			if [[ "$id_like" == *arch* ]]; then
				echo "arch"
			elif [[ "$id_like" == *ubuntu* || "$id_like" == *debian* ]]; then
				echo "mint"
			else
				echo "unknown"
			fi
			;;
	esac
}

DISTRO=$(detect_distro)

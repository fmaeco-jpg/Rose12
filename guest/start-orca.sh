#!/bin/sh
# Launch the actual Linux desktop application in the already-running XFCE/X11 session.
set -eu
[ "$(id -u)" -ne 0 ] || { echo 'Start ORCA as the regular desktop user, not root.' >&2; exit 1; }
[ -n "${DISPLAY:-}" ] || { echo 'DISPLAY is not set; start the XFCE desktop first.' >&2; exit 1; }
command -v orca-ide >/dev/null 2>&1 || { echo 'orca-ide is not installed or not on PATH.' >&2; exit 1; }
# Deliberately do not disable Chromium sandbox security by default.
exec orca-ide "$@"

#!/bin/sh
# Install a separately obtained, checksum-verified ORCA ARM64 package inside Ubuntu.
set -eu

usage() { echo "Usage: $0 --confirm-guest ORCA.deb SHA256" >&2; exit 2; }
[ "$#" -eq 3 ] && [ "$1" = "--confirm-guest" ] || usage
package=$2
expected=$3
case "$expected" in *[!0-9a-fA-F]*|'') usage ;; esac
[ "${#expected}" -eq 64 ] || usage
[ "$(id -u)" -eq 0 ] || { echo 'Run as root inside the Ubuntu guest.' >&2; exit 1; }
[ "$(dpkg --print-architecture)" = arm64 ] || { echo 'An ARM64 Ubuntu guest is required.' >&2; exit 1; }
[ -f "$package" ] || { echo 'Package file not found.' >&2; exit 1; }
actual=$(sha256sum "$package" | cut -d ' ' -f 1)
[ "$(printf '%s' "$actual" | tr 'A-F' 'a-f')" = "$(printf '%s' "$expected" | tr 'A-F' 'a-f')" ] || { echo 'SHA-256 mismatch; installation stopped.' >&2; exit 1; }
name=$(dpkg-deb -f "$package" Package)
arch=$(dpkg-deb -f "$package" Architecture)
[ "$name" = orca-ide ] && [ "$arch" = arm64 ] || { echo "Unexpected package identity: $name ($arch)." >&2; exit 1; }
echo "Installing $name ($arch) into the confirmed guest..."
apt-get update
# apt resolves the package's declared dependencies as well as installing the local file.
# An absolute path prevents apt interpreting a relative filename as a package name.
package=$(realpath "$package")
DEBIAN_FRONTEND=noninteractive apt-get install -y "$package"
echo 'Installed. Launch ORCA as the regular guest user within the X11 desktop.'

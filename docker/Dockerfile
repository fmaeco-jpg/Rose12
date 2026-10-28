# Research prototype: ARM64 Ubuntu XFCE desktop with the official ORCA package.
# Build only on an ARM64 host or with an explicitly configured ARM64 build emulator.
FROM lscr.io/linuxserver/webtop:ubuntu-xfce
ARG ORCA_DEB_SHA256
COPY orca-ide_arm64.deb /tmp/orca-ide.deb
RUN set -eu; \
    test "$(dpkg --print-architecture)" = arm64; \
    test "${#ORCA_DEB_SHA256}" -eq 64; \
    echo "$ORCA_DEB_SHA256  /tmp/orca-ide.deb" | sha256sum -c -; \
    test "$(dpkg-deb -f /tmp/orca-ide.deb Package)" = orca-ide; \
    test "$(dpkg-deb -f /tmp/orca-ide.deb Architecture)" = arm64; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y /tmp/orca-ide.deb; \
    rm -f /tmp/orca-ide.deb; \
    rm -rf /var/lib/apt/lists/*

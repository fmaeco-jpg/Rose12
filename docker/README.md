# Docker-Testumgebung (noch nicht auf Android integriert)

Erster Prototyp auf Basis des öffentlichen [LinuxServer-Webtop-Images](https://github.com/linuxserver/docker-webtop), Ubuntu/XFCE, arm64. Das ist der vollständige Linux-Desktop, nicht nur der ORCA-Remote-Client. Ein Docker-Image allein ist keine Android-App: Auf Android wäre eine lokale Linux-VM samt Docker-Laufzeit und eine eingebettete Oberfläche zusätzlich erforderlich. Docker/Podroid, Webtop und ORCA sind hier noch nicht zusammen getestet.

## Vorbereitung auf einem geeigneten ARM64-Docker-Host

1. Das offizielle `orca-ide_*_arm64.deb` aus einem ORCA-Release herunterladen und als `docker/orca-ide_arm64.deb` ablegen. Eine unabhängig vertrauenswürdige SHA-256-Prüfsumme prüfen; ein selber aus derselben ungesicherten Quelle berechneter Hash bestätigt die Herkunft nicht.
2. Die Umgebung setzen, ohne Zugangsdaten in Git abzulegen:

```sh
export ORCA_DEB_SHA256='VERTRAUENSWUERDIGE_SHA256_PRUEFSUMME'
export ORCA_DESKTOP_USER='DEIN_BENUTZERNAME'
# Passwort sicher im eigenen Terminal setzen, nicht in Git eintragen.
export ORCA_DESKTOP_PASSWORD='DEIN_PASSWORT'
docker compose -f docker/compose.yaml up --build
```

3. Auf demselben Docker-Host `https://localhost:3001/` öffnen und das selbstsignierte Zertifikat prüfen. ORCA über das Desktop-Menü starten. Es wird kein Chromium-Sandbox- oder Docker-Seccomp-Schutz automatisch deaktiviert.

Die Oberfläche wird nur an die Loopback-Adresse des Docker-Hosts gebunden und über Webtop authentifiziert. Um sie in einer Android-VM zu erreichen, ist ein sicher konfiguriertes Port-Forwarding und eine geeignete Darstellung einschließlich Zertifikatshandhabung notwendig; Android-`localhost` ist nicht automatisch die VM. Kein Docker-Socket oder priviligierter Modus wird eingebunden. Standard-Webtop und sein Browserzugang dürfen nicht ungeschützt im Netzwerk veröffentlicht werden.

`orca-config` speichert Nutzerdaten persistent. Die Zugangsdaten werden zur Laufzeit als Container-Umgebungsvariablen übergeben und sind für Personen mit Docker-Zugriff einsehbar. Das Base-Image-Tag ist für diesen Prototyp noch nicht auf ein Digest eingefroren. Ein echter Build, Größenmessungen, ARM64-Laufzeit und Android-Test stehen aus.

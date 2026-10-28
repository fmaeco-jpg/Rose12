# ORCA auf Android – Machbarkeitsprototyp

Ziel ist eine eigenständige Android-App ab Android 13 mit dem vollständigen ORCA-Desktop. Als erste technische Grundlage ist [FluxLinux Ubuntu Edition](https://github.com/akane599/fluxlinux-ubuntufied) vorgesehen (untersucht: Commit `ab73309f5303dc3e7550caef366d1917ec6a8d6c`). Der Linux-Unterbau soll 200–300 MB groß sein; ORCA, App und KI-Modelle zählen separat. Derzeit ist **noch keine APK gebaut oder auf einem Gerät getestet**. Siehe [PLAN.md](PLAN.md).

## Erster Schritt: ORCA im Ubuntu-Gast

Die Skripte in `guest/` sind Vorarbeiten für den Test in einem bereits eingerichteten ARM64-Ubuntu-Gast mit XFCE/X11. Sie ersetzen noch keine Integration in FluxLinux. ORCA-Paket und eine unabhängig vertrauenswürdig bestätigte SHA-256-Prüfsumme müssen bereitgestellt werden; eine selbst vom gleichen ungesicherten Download berechnete Prüfsumme belegt dessen Herkunft nicht.

Als Root **ausschließlich im Gast**, nicht auf dem Host:

```sh
./guest/install-orca.sh --confirm-guest /pfad/zum/orca-ide_arm64.deb VERTRAUENSWUERDIGER_SHA256_WERT
```

Das Skript prüft Architektur, Paketname und Hash und installiert über APT inklusive Abhängigkeiten. Dieser Vorgang verändert das Gast-System und benötigt Netzwerkzugriff. Danach im laufenden XFCE-Desktop als normaler Gast-Benutzer:

```sh
./guest/start-orca.sh
```

Die Skripte setzen keinen unsicheren Chromium-Sandbox-Schalter. Dass ORCA unter PRoot und dem integrierten X11 tatsächlich läuft, ist noch nicht erwiesen.

## Tests

```sh
python3 -m unittest discover -s tests -v
sh -n guest/*.sh
```

Die Tests simulieren Systemprogramme; sie installieren nichts und sind **keine** Android- oder ORCA-Laufzeittests.

## Docker-Alternative

Unter [`docker/`](docker/README.md) liegt ein ungetesteter ARM64-Docker-Prototyp, der einen fertigen Ubuntu-XFCE-Webtop mit ORCAs Desktop-Paket kombiniert. Er ist noch keine Android-Ein-App-Lösung und benötigt für den Build und Betrieb einen Docker-Host.

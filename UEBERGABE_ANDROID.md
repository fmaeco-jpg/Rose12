# Übergabe: ORCA Desktop auf Android

**Stand:** 28.10.2026  
**Repository:** [fmaeco-jpg/Rose12](https://github.com/fmaeco-jpg/Rose12)  
**Vorhandener Pull Request:** [#1](https://github.com/fmaeco-jpg/Rose12/pull/1)

## 1. Produktauftrag

Eine **einzige Android-App für den persönlichen Gebrauch** entwickeln, die ORCAs vollständigen Desktop-Funktionsumfang einschließlich aller Einstellungen lokal auf dem Gerät bereitstellt. Die bestehende ORCA-Mobile-App ist nicht die Funktionsgrenze: Sie darf als UI-Vorlage dienen, ist aber als reine Fernsteuerung nicht ausreichend.

- **Mindestversion:** Android 13 / API 33.
- **Ein Installationserlebnis:** Keine separat zu installierende VM-App, Termux, VNC-App oder Desktop-Verbindung. Beim ersten Start dürfen notwendige Komponenten heruntergeladen werden.
- **Online und offline:** Online-Dienste und unterstützte Coding-Agenten sollen verfügbar sein; zusätzlich soll ein geeignetes lokales Modell auf dem Android-Gerät auch ohne Internet genutzt werden können.
- **Größe:** Ziel für den Linux-/VM-Unterbau sind etwa **200–300 MB**. Diese Grenze gilt ausdrücklich **nicht** für die gesamte App, ORCA oder separat heruntergeladene Modelle. Download- und installierte Größe getrennt messen.
- **Voller Umfang ist Ziel, kein verifiziertes Ergebnis:** Desktop-Funktionen einzeln gegen das Linux-Original prüfen und fehlende/auf Android nicht unterstützte Funktionen dokumentieren.

## 2. Ist-Zustand im Repository

Das Projekt ist ein **Machbarkeitsprototyp**, keine fertige Android-App:

| Pfad | Inhalt / Status |
| --- | --- |
| `PLAN.md` | Vorläufige Architektur, Test- und Sicherheitsplanung. |
| `guest/install-orca.sh` | Installiert ein lokal bereitgestelltes Debian-Paket im bereits eingerichteten ARM64-Gast nach ausdrücklicher Bestätigung, Prüfsummen-, Paketnamen- und Architekturprüfung. Keine Android-Integration. |
| `guest/start-orca.sh` | Startet `orca-ide` als Nicht-root-Nutzer bei gesetztem `DISPLAY`. |
| `tests/test_guest_scripts.py` | Sieben Host-Tests mit simulierten Systembefehlen; keine echten Paket-, Android- oder ORCA-Tests. |
| `docker/` | Experimentelles Dockerfile/Compose auf Basis LinuxServer Webtop Ubuntu/XFCE; verwendet ein separat bereitzustellendes, per SHA-256 geprüftes ORCA-Deb. Nicht gebaut, nicht deployed und nicht in Android integriert. |
| `README.md` | Nutzung und bekannte Einschränkungen. |

**Nicht vorhanden:** Android-Projekt, Gradle-Konfiguration, SDK-Build, APK, automatische Integration von Linux oder Docker, funktionierender ORCA-Start, Nachweis auf einem Android-Gerät. API 33 ist eine Produktanforderung, noch keine implementierte `minSdk`-Einstellung. Frühere Arbeiten wurden nicht auf einem physischen Gerät getestet.

Zuletzt ausgeführte Host-Prüfungen:

```sh
python3 -m unittest discover -s tests -v  # 7 Tests bestanden
sh -n guest/*.sh                         # Syntaxprüfung bestanden
```

Die Entwicklungsumgebung hatte kein Java, Android SDK, ADB oder Docker. Der Download des ORCA-Release-Assets schlug fehl; deshalb wurden dessen Paketinhalt und Ausführbarkeit nicht verifiziert. Die Tests simulieren `apt-get`, `dpkg` und den Launcher.

## 3. Kandidaten und Entscheidungsrahmen

### Erster Kandidat: FluxLinux Ubuntu Edition

- [Quelle](https://github.com/akane599/fluxlinux-ubuntufied), untersuchter Commit `ab73309f5303dc3e7550caef366d1917ec6a8d6c`, Release `v2.1.8`.
- Laut Projekt eine Android-App mit eingebettetem PRoot, Ubuntu ARM64, XFCE und integriertem X11. **PRoot ist keine VM.**
- Vorteil: glibc-Ubuntu passt grundsätzlich eher zum offiziellen ORCA-Deb; X11 ist bereits integriert. Der Quellstand des Kandidaten ist GPL-3.0; vollständige Lizenzprüfung einschließlich Drittkomponenten erforderlich.
- Die untersuchte Upstream-Konfiguration hatte `minSdk = 26`; unser Derivat muss mindestens API 33 setzen und testen. Package-ID und Bootstrap-Pfade nicht naiv umbenennen: der Upstream-Build koppelt native Assets und Pfade an die Application-ID.
- Laut Upstream enthält das APK die Host-Laufzeit, während das Rootfs bei Bedarf nachgeladen wird. Die tatsächlich installierte Größe nach XFCE und Abhängigkeiten ist **unbekannt**.

### Alternative: Podroid + VM

- [Podroid](https://github.com/ExTV/Podroid): laut Projekt echte Alpine-VM via QEMU, auf unterstützten Geräten optional AVF, mit integriertem Desktop und Container-Laufzeit. GPL-2.0 bzw. jeweilige Komponentenlizenzen prüfen.
- Falls PRoot/Electron oder benötigte Kernel-Funktionen scheitern: prototypisch eine glibc-basierte ORCA-Umgebung in der VM erproben. Alpine verwendet musl; ein Debian-/Ubuntu-Deb ist nicht ohne Weiteres kompatibel.
- QEMU ohne Hardwarebeschleunigung kann erhebliche Leistungskosten verursachen. AVF-Verfügbarkeit und Berechtigungen sind geräteabhängig. Eine VM mit Docker erhöht Komplexität und Ressourcenverbrauch; keine Funktionstüchtigkeit voraussetzen.

### Docker-Prototyp

- [`docker/README.md`](docker/README.md) beschreibt das optionale Webtop-Experiment. Ein Image/Container ist **keine** Android-App und bietet nicht selbst die Linux-VM auf Android.
- [LinuxServer Webtop](https://github.com/linuxserver/docker-webtop) bietet Ubuntu/XFCE und ARM64; `docker/Dockerfile` ergänzt das offizielle ORCA-Paket. Das Basisimage ist derzeit **nicht digest-gepinnt**.
- Bei einem VM-Test: Android-`localhost`, VM und Container sind unterschiedliche Netzwerk-Namensräume. Weiterleitung, Authentifizierung und Zertifikatsprüfung vor Zugriff implementieren. Kein Docker-Socket an untrusted Desktop durchreichen. Bestehende Compose-Konfiguration bindet an die Loopback-Adresse des Docker-Hosts.

**Entscheidung noch nicht getroffen:** FluxLinux ist der erste Kandidat, nicht der Nachweis einer geeigneten endgültigen Architektur. Der native Android-Coder soll das Ergebnis anhand tatsächlicher Tests entscheiden; falls Docker/VM einfacher ist, diesen Weg mit gemessener Größe und Leistung begründen.

## 4. ORCA-Referenz

- [ORCA-Repository](https://github.com/stablyai/orca), Lizenz MIT; Native- und Drittanbieter-Bestandteile gesondert prüfen.
- [Release v1.4.243](https://github.com/stablyai/orca/releases/tag/v1.4.243): `orca-ide_1.4.243_arm64.deb`, laut GitHub-Metadaten 178.719.524 Byte. Das ist **ORCA selbst**, nicht die Linux-Unterbaugröße.
- Mobile verwendet laut Projekt React Native/Expo und RPC zu einem Host. Native Chat bezeichnet eine Chat-Ansicht und beweist für sich keinen auf dem Handy ausgeführten Agenten. Aktuelle mobile Oberfläche und vom Desktop bezogene Web-Bundles reichen allein nicht für die Desktop-Funktionsparität.
- Vor einem neuen Test Versionen/Commits der verwendeten Quellen und Images festhalten. Paket und Rootfs ausschließlich aus vertrauenswürdigen Quellen beziehen und ihre Integrität anhand einer vertrauenswürdigen Prüfsumme verifizieren.

## 5. Erste Aufgaben – in dieser Reihenfolge

1. **Umgebung reproduzieren:** ARM64-Gerät mit Android 13+ und verfügbarem RAM/Speicher dokumentieren; Java, Android SDK/NDK, Gradle und ADB gemäß gewähltem Kandidaten einrichten. Lizenz- und Build-Anforderungen prüfen.
2. **Kandidaten isoliert starten:** FluxLinux Ubuntu/XFCE auf dem Testgerät installieren, Erstinstallation, lokales Dateisystem, Neustart und X11 prüfen. Aufbaugröße separat messen. Das ist ein Testkandidat, noch nicht die spätere Nutzerinstallation.
3. **ORCA installieren und starten:** offizielles ARM64-Deb und alle Abhängigkeiten verifizieren, unter PRoot/X11 ausführen. Logs, Architektur, Befehle und Fehlermeldungen ohne Zugangsdaten erfassen. Bei Chromium-Sandbox- oder Kernel-Problemen nicht stillschweigend `--no-sandbox`, `--privileged` oder `seccomp=unconfined` als finale Lösung verwenden; Risiken und Alternativen dokumentieren.
4. **Desktop-Funktionsmatrix anlegen:** Referenz unter normalem Linux gegen Android vergleichen. Insbesondere Einstellungen, Sessions, parallele Agenten, Terminal/PTY, lokale Dateien, Git/Worktrees, Web-/Preview, Berechtigungen, Anhänge, Benachrichtigungen und Persistenz testen. Abweichungen offen benennen.
5. **Android-App integrieren:** nach erfolgreichem Laufzeittest Linux/VM und ORCA in einem Build und einem Einrichtungsablauf verbinden. Hintergrundbetrieb, Touch, Fenstergröße, Tastatur, Dateizugriff und Wiederaufnahme nach Prozessende implementieren und testen.
6. **Offline-Pfad:** lokale Inferenz und ein geeignetes Modell als optionalen Download einbinden; Flugmodus-Test einschließlich Agenten-Tools. Cloud-Dienste bleiben nur mit Internet und ggf. eigenen Accounts nutzbar. Modellqualität, Speicher, Wärme, Akku und Geschwindigkeit messen.
7. **Release-Härtung:** reproduzierbare Quellen und Images pinnen, Lizenzpflichten erfüllen, Updates/Recovery, Datenmigration, Schutz von Schlüsseln und lokale Schnittstellen prüfen. APK und Erststart-Assets signiert/verifiziert bereitstellen.

## 6. Testnachweise / Abnahmekriterien

- Ein APK auf Android 13+ installieren; keine zweite App und kein Desktop-Rechner nötig.
- Linux-Unterbau einmalig einrichten, Größe des Downloads und des installierten Unterbaus dokumentieren. ORCA und Modellgrößen separat ausweisen.
- ORCA startet lokal, die Desktop-Einstellungen sind zugänglich und bleiben nach Neustart erhalten.
- Desktop-Funktionsmatrix mit bestanden / fehlgeschlagen / nicht unterstützt, Android-Version, Gerät und Logs; keine pauschale Aussage „volle Parität“ ohne Nachweis.
- Online-Agent mit gültiger Nutzeranmeldung testen; optionales lokales Modell im Flugmodus testen. Secrets nicht in Logs oder Repository aufnehmen.
- App-Hintergrund, Akkusparmodus, Prozessabbruch und Recovery prüfen; Grenzen von Android offenlegen.
- Keine Annahme, dass die aktuellen Mock-Tests die Android-Laufzeit oder Sicherheit belegen.

## 7. Für die nächste Sitzung benötigte Angaben

Gerätemodell, Android-Version, RAM, freier Speicher und ob USB-/ADB-Zugriff möglich ist. Zugangsdaten nicht in Chat oder Repository ablegen. Kein Root voraussetzen.

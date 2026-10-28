# Plan: ORCA Desktop auf Android

## Ziel

Eine einzige Android-App für den persönlichen Gebrauch: ORCA Desktop und seine Einstellungen sollen lokal auf dem Gerät verfügbar sein. Die bisherige Mobile-App ist keine funktionale Obergrenze. Online-Agenten und optional ein lokales Offline-Modell sollen unterstützt werden. Android 13 (API 33) ist die Mindestversion. Zielgröße für den Linux-Unterbau: 200–300 MB; ORCA, die Android-App und Modelldateien werden separat gemessen.

## Technische Entscheidung für den ersten Versuch

[FluxLinux Ubuntu Edition](https://github.com/akane599/fluxlinux-ubuntufied), Stand Release v2.1.8, als Prototyp-Basis: Android-App mit eingebettetem PRoot, Ubuntu ARM64, XFCE und X11. Kein zusätzliches Termux, kein separater VNC-Client. PRoot ist keine VM. Alternativ kommt [Podroid](https://github.com/ExTV/Podroid) mit echter Linux-VM infrage, falls die PRoot-/Chromium-Einschränkungen den Desktop verhindern.

ORCA zunächst unverändert als offizielles ARM64-Deb-Paket aus Release v1.4.243 im Ubuntu-Gast ausführen. Die echte Desktop-Oberfläche wird über das integrierte X11 dargestellt. Ein mobil angepasstes Interface darf erst ergänzt werden, wenn die Desktop-Funktionen verfügbar und vergleichbar sind; es darf die Einstellungen nicht ersetzen oder verstecken.

## Bisher überprüft – Stand 28.10.2026

- ORCA v1.4.243 bietet `orca-ide_1.4.243_arm64.deb` (178.719.524 Byte) an. ORCAs Build-Konfiguration definiert Linux ARM64, Electron und weitere native Linux-Ressourcen.
- FluxLinux Ubuntu Edition v2.1.8 bietet eine Release-APK von ca. 62,2 MiB; laut Repository lädt sie Ubuntu beim ersten Start nach und startet XFCE mit integriertem X11. Quellcode und GPL-3.0-Lizenz sind öffentlich.
- Diese beiden Dateien allein entsprechen zusammen rund 232,6 MiB Download. Linux-Image, Abhängigkeiten und ggf. Updates kommen hinzu. Die 200–300-MB-Grenze gilt nur für den Linux-Unterbau, nicht für die Gesamt-App. Die Größe des Linux-Unterbaus ist erst zu messen. Installationsgröße und lokal heruntergeladene Modelle sind nicht in dieser Zahl enthalten.
- Der direkte Download des ORCA-Deb-Pakets in dieser Arbeitsumgebung scheiterte beim GitHub-Release-Asset-Host; eine Paket- oder Laufzeitprüfung wurde nicht durchgeführt. Die Umgebung ist x86_64 und bietet weder `adb` noch einen Android-Emulator. Es gibt bisher keinen Gerätetest und keinen Nachweis, dass ORCA auf FluxLinux startet.

## Phasen und verbindliche Prüfpunkte

### 1. Reproduzierbare Grundlage und Lizenzprüfung

- Passende Quellstände von FluxLinux und ORCA festhalten; Builds, Ursprung und Prüfsummen protokollieren. Lizenzen aller eingebundenen Komponenten und Pflichten bei Weitergabe prüfen (FluxLinux GPL-3.0, ORCA MIT, Drittabhängigkeiten gesondert).
- FluxLinux unverändert auf einem ARM64-Android-Gerät installieren und Ubuntu samt XFCE starten. Ein-APK-Anforderung, Downloads, entpackte Größe und Android-Version dokumentieren.
- **Bestanden:** Linux-Terminal, Netzwerk, persistente Dateien und XFCE funktionieren ohne zusätzliche App. Größen aufzeichnen.

### 2. ORCA-Desktop unverändert starten

- ORCA-Deb kontrolliert installieren, Paketabhängigkeiten und ARM64-Binärdateien prüfen; X11, D-Bus, Chromium/Electron und PRoot-Verträglichkeit untersuchen. Fehler und Logs sichern.
- **Bestanden:** ORCA-Fenster öffnet sich, bleibt stabil, alle Einstellungsseiten sind erreichbar und Einstellungen überleben einen Neustart. Sicherheitsrelevante Workarounds wie deaktivierte Chromium-Sandbox nicht ungeprüft als endgültige Lösung übernehmen.
- **Abbruch-/Alternativpfad:** Scheitert dies grundlegend an PRoot oder Chromium, dieselben Tests in Podroids VM mit geeignetem glibc-Linux-Gast durchführen; Größe und Performance vergleichen. Ein erfolgreicher Start ist keine Garantie für vollen Funktionsumfang.

### 3. Desktop-Funktionen systematisch abdecken

- Desktop-Funktionsinventar aus ORCA-Dokumentation und Code mit konkreten Testfällen und Ergebnissen erstellen.
- Prüfen: lokale Projekte und Dateizugriff, Terminal/PTY, Git-Clone und Worktrees, mehrere parallele Sessions/Agenten, Einstellungen, Persistenz, Anhänge, Browser/Vorschau, Benachrichtigungen und Bildschirm-/Hintergrundverhalten.
- Online-Agenten nur mit vorhandener gültiger Anmeldung und nach jeweiliger Anbieterunterstützung testen. Kein vollständiges Funktionsversprechen, bevor Funktionen einzeln bestanden haben; nicht portable Desktop-Funktionen explizit ausweisen und Lösungen definieren.
- **Bestanden:** priorisierte Tests laufen auf dem Zielgerät, Fehlschläge und Unterschiede zum Desktop sind dokumentiert.

### 4. Offline-KI

- Separat Android- oder Linux-taugliches `llama.cpp` und ein kleines lokal gespeichertes Modell prüfen; passende Agenten-/Provider-Anbindung und Tool-Calling verifizieren.
- Im Flugmodus Start, Chat, Dateiarbeit und Agentenwerkzeuge testen. RAM, Modellgröße, Geschwindigkeit, Temperatur und Akkuverbrauch messen.
- Modelle als optionalen separaten Download behandeln; keine Aussage, dass Cloud-Agenten oder deren Abonnements offline funktionieren.

### 5. Eine integrierte App

- Auf Basis der Messergebnisse Linux und ORCA vorkonfigurieren, Systemstart und Wiederherstellung automatisieren, mobile Bedienung (Skalierung, Tastatur, Touch, Dateiauswahl) verbessern und die ursprünglichen Desktop-Einstellungen erhalten.
- Größen separat für APK, Linux-Unterbau, ORCA, Updates und optionale Modelle ausweisen; Abhängigkeiten nicht doppelt paketieren. Falls der Linux-Unterbau 300 MB überschreitet, Optimierung messen und Zielkonflikt offenlegen.
- Security: Integritätsprüfung der Downloads, app-private Speicherung, restriktive Berechtigungen, lokale Dienste möglichst nur lokal erreichbar, keine Zugangsdaten in Logs; Updates und Wiederherstellung testen.
- **Bestanden:** eine APK, keine zusätzlichen Apps, Einrichtungsablauf und Offline-Neustart funktionieren; Funktionsmatrix, Ressourcenverbrauch und bekannte Einschränkungen sind dokumentiert.

## Offene Voraussetzung

Für einen aussagekräftigen Android-Test werden ein ARM64-Zielgerät mit Modell, Android-Version, freiem Speicher und RAM sowie eine sichere Möglichkeit zur Installation und zum Erfassen der Logs benötigt. Ohne ein angeschlossenes oder anderweitig erreichbares Gerät können lediglich Quellcode, Builds und Host-Tests geprüft werden, kein praktisches Android-Verhalten.

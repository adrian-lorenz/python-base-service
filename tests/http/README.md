# HTTP-Tests für die User Service API

Diese Verzeichnis enthält HTTP-Testdateien, die mit verschiedenen HTTP-Clients verwendet werden können,
um die API-Endpunkte manuell zu testen.

## Verfügbare Testdateien

- `base.http` - Grundlegende Konfiguration und Variablen
- `users.http` - Grundlegende CRUD-Operationen für Benutzer
- `error_scenarios.http` - Tests für Fehlerszenarien
- `user_lifecycle.http` - Sequentielle Tests für den vollständigen Benutzer-Lebenszyklus
- `performance.http` - Tests mit mehreren Benutzern für Performance-Überprüfungen

## Verwendung

### In JetBrains IDEs (IntelliJ IDEA, PyCharm, etc.)

1. Öffne eine der .http-Dateien
2. Klicke auf den grünen "Run"-Button neben einer Anfrage, um sie auszuführen
3. Die Antwort wird im rechten Panel angezeigt

JetBrains HTTP-Client kann Variablen zwischen Anfragen teilen und
unterstützt automatische Extraktion von Daten aus vorherigen Antworten.

### In Visual Studio Code

1. Installiere die "REST Client" Erweiterung (von Huachao Mao)
2. Öffne eine der .http-Dateien
3. Klicke auf "Send Request" über einer Anfrage, um sie auszuführen
4. Die Antwort wird in einem neuen Tab angezeigt

### In anderen Umgebungen

Du kannst die Anfragen aus den .http-Dateien auch in andere HTTP-Clients wie Postman oder Insomnia kopieren.

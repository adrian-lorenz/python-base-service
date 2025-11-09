# User Service mit FastAPI und MySQL



`uvicorn src.app.main:app --reload`

## Environment Variables
```
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD="xxx"
DB_NAME=user_service_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```


## Architekturübersicht

Nachfolgend findest du eine visuelle Übersicht der Architektur dieses User-Services. Die Diagramme sind in Mermaid geschrieben und werden auf GitHub automatisch gerendert.

### Komponenten-/Datenflussdiagramm
```mermaid
flowchart LR
    subgraph Client
        U[Browser / HTTP-Client]
    end

    subgraph API["FastAPI App<br/>src/app/main.py"]
        M["Main & Router-Setup"]
        C["UsersController<br/>src/domains/user/api/users_contoller.py"]
    end

    subgraph Domain["Domain-Schicht"]
        S["UserService<br/>src/domains/user/user_service.py"]
        R["UserRepository<br/>src/domains/user/repository/user_repository.py"]
        Models["SQLAlchemy Models & Schemas<br/>src/domains/user/models/"]
    end

    subgraph Infra["Infrastruktur"]
        DB[(MySQL)]
        SQLA["SQLAlchemy Engine & Session<br/>src/app/database.py"]
        CFG["Settings & Env<br/>src/app/config/settings.py"]
    end

    U -->|HTTP REST| M --> C
    C -->|ruft Methoden| S
    S -->|CRUD-Operationen| R
    R -->|ORM-Queries| SQLA
    SQLA --> DB
    Models <-->|Mapping/Validation| R
    CFG --> M
    CFG --> SQLA
```

### Sequenzdiagramm: Beispiel GET /api/users
```mermaid
sequenceDiagram
    participant U as Client
    participant A as FastAPI Router ("/api")
    participant C as UsersController
    participant S as UserService
    participant R as UserRepository
    participant D as MySQL

    U->>A: HTTP GET /api/users
    A->>C: Route-Handler
    C->>S: get_users(skip, limit)
    S->>R: get_users(skip, limit)
    R->>D: SELECT * FROM users LIMIT ... OFFSET ...
    D-->>R: Resultset
    R-->>S: User-Model-Objekte
    S-->>C: Liste<UserResponse>
    C-->>U: 200 OK (JSON)
```

### Schichten & Verantwortlichkeiten (kurz)
- API/Controller: Endpunkte definieren, Request/Response binden, Fehler in HTTP-Status übersetzen.
- Service: Geschäftslogik, Validierungen (z. B. E-Mail/Username-Kollisionen), Aggregation.
- Repository: Datenzugriff via SQLAlchemy (Sessions, Queries, Transaktionen).
- Modelle/Schemas: Persistenz-Modelle (ORM) und Pydantic-Schemas für IO.
- Infrastruktur: App-Start, DB-Engine/Session, Konfiguration aus Umgebungsvariablen.

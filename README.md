```mermaid
flowchart TD
    A[Stundenplandaten] --> B

    subgraph B["ha-stundenplan – Home Assistant Custom Integration"]
        C[Datenmodell]
        D[Zeitberechnung]
        E[Aktueller Block]
        F[Nächster Block]
        G[Tages- und Wochenplan]
    end

    B --> H[Home Assistant]

    H --> I[Sensoren]
    H --> J[Calendar]
    H --> K[Automationen]

    I --> L[Dashboard]
    J --> L
    K --> M[Geräte & Aktionen]

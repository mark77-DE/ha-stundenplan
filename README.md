Stundenplandaten
       │
       ▼
┌───────────────────────┐
│ ha-stundenplan        │
│ Custom Integration    │
├───────────────────────┤
│ Datenmodell           │
│ Zeitberechnung        │
│ aktueller Block       │
│ nächster Block        │
│ Tages-/Wochenplan     │
└───────────┬───────────┘
            │
            ├──────────────► Sensoren
            │
            ├──────────────► Calendar
            │
            └──────────────► Automationen
                              │
                              ▼
                         Home Assistant

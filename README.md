# Stundenplan for Home Assistant

This custom integration creates a sensor and a calendar for each person in a
local school schedule. The schedule is read from `/config/schedules.yaml` when
Home Assistant starts.

## Installation

Copy `custom_components/stundenplan` into the `custom_components` directory
under your Home Assistant configuration directory. Add this to
`configuration.yaml` to enable the integration:

```yaml
stundenplan: {}
```

Create `schedules.yaml` next to `configuration.yaml` (that is, at
`/config/schedules.yaml`). For example:

```yaml
persons:
  - id: paulina
    name: Paulina
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: Mathe
        tuesday:
          start: "07:40"
          end: "08:20"
          subject: Deutsch
      HT:
        monday:
          start: "09:10"
          end: "09:50"
          subject: HT
```

Each person needs a unique `id`, a display `name`, and a `schedule`. Each
schedule key is a block ID; under it, add lowercase English weekday names and
`start`, `end`, and `subject` values. Times use 24-hour `HH:MM` format. The
integration uses Home Assistant's configured time zone for calendar events.

Restart Home Assistant after installing the integration or changing
`schedules.yaml`.

## Entities

For a person with ID `paulina`, the integration creates:

- `sensor.stundenplan_paulina`: current subject, or `frei` when no lesson is
  active. Attributes include the current block and the next lesson.
- `calendar.stundenplan_paulina`: lesson events, including the subject and
  block. The calendar reflects the schedule and is read-only.

Entity IDs use each person's `id`, so choose IDs that remain stable if you want
to preserve Home Assistant entity history and automations.

## Development

Run the tests with:

```bash
python -m pytest --asyncio-mode=auto
```

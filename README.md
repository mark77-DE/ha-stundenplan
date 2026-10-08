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
  - id: student_a
    name: Student A
    schedule:
      "1":
        monday:
          start: "07:40"
          end: "08:20"
          subject: Subject A
        tuesday:
          start: "07:40"
          end: "08:20"
          subject: Subject B
      HT:
        monday:
          start: "09:10"
          end: "09:50"
          subject: HT
```

Each person needs a unique `id`, a display `name`, and a `schedule`. Each
schedule key is a block ID; under it, add lowercase weekday names and
`start`, `end`, and `subject` values. Times use 24-hour `HH:MM` format. The
integration uses Home Assistant's configured time zone for calendar events.

Restart Home Assistant after installing the integration or changing
`schedules.yaml`.

## Entities

For a person with ID `student_a`, the integration creates:

- `sensor.stundenplan_student_a`: current subject, or `frei` when no lesson is
  active. Attributes include the current block, the next lesson, and complete
  `today_lessons` and `tomorrow_lessons` lists. Each list item has a block,
  subject, start, and end.
- `calendar.stundenplan_student_a`: lesson events, including the subject and
  block. The calendar reflects the schedule and is read-only.

Entity IDs use each person's `id`, so choose IDs that remain stable if you want
to preserve Home Assistant entity history and automations.

## Dashboard overview

The sensor attributes can be used in Markdown cards for a complete list of
today's and tomorrow's lessons. Replace `student_a` with another person's ID:

```yaml
type: markdown
title: Stundenplan Student A
content: |
  ## Heute ({{ state_attr('sensor.stundenplan_student_a', 'today_date') }})
  {% set lessons = state_attr('sensor.stundenplan_student_a', 'today_lessons') or [] %}
  {% for lesson in lessons %}
  - {{ lesson.start }}–{{ lesson.end }} **{{ lesson.subject }}**
  {% else %}
  - Frei
  {% endfor %}

  ## Morgen ({{ state_attr('sensor.stundenplan_student_a', 'tomorrow_date') }})
  {% set lessons = state_attr('sensor.stundenplan_student_a', 'tomorrow_lessons') or [] %}
  {% for lesson in lessons %}
  - {{ lesson.start }}–{{ lesson.end }} **{{ lesson.subject }}**
  {% else %}
  - Frei
  {% endfor %}
```

For a rolling seven-day weekly overview, add a Calendar card with both calendar
entities and set its initial view to `listWeek`:

```yaml
type: calendar
initial_view: listWeek
entities:
  - calendar.stundenplan_student_a
  - calendar.stundenplan_student_b
```

The Calendar card's `listWeek` view displays the next seven days.

## Development

Run the tests with:

```bash
python -m pytest --asyncio-mode=auto
```

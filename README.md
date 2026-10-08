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
  active. Attributes include the current block, the next lesson, the complete
  `today_lessons` and `tomorrow_lessons` lists, and `week_lessons` for the
  Monday-to-Sunday week containing today. Each lesson has a block, subject,
  start, and end.
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

### Optional color helpers for the combined daily card

The integration creates schedule sensors automatically. The colors are
dashboard preferences, so use editable `input_text` helpers rather than adding
fixed color sensors to the integration. Add these entries to
`configuration.yaml` (merge them into an existing `input_text:` section if you
already have one):

```yaml
input_text:
  stundenplan_student_a_farbe:
    name: Stundenplan Student A Farbe
    initial: "#C47FF5"
    max: 7
  stundenplan_student_b_farbe:
    name: Stundenplan Student B Farbe
    initial: "#F25AE5"
    max: 7
```

Reload the `input_text` helpers or restart Home Assistant. In the combined
daily card, mark the active student's table cell with `valign="student_a"` or
`valign="student_b"`. Then add this `card_mod` block to the card to read the
colors from the helpers:

```yaml
card_mod:
  style:
    ha-markdown$: |
      td[valign="student_a"] {
        background-color: {{ states('input_text.stundenplan_student_a_farbe') }} !important;
      }
      td[valign="student_b"] {
        background-color: {{ states('input_text.stundenplan_student_b_farbe') }} !important;
      }
```

For a weekly overview with a separate table for each person, add a new dashboard
view and place two Markdown cards in it. Use a vertical stack to give each table
the full view width. Add this `tap_action` to the existing daily Markdown card
to open that view (replace the path if your dashboard has another URL):

```yaml
tap_action:
  action: navigate
  navigation_path: /dashboard-flur/wochenplan
```

Example Markdown card for one person:

```yaml
type: markdown
title: Stundenplan Student A
entity_id: sensor.stundenplan_student_a
content: |
  {% set week = state_attr('sensor.stundenplan_student_a', 'week_lessons') or [] %}
  {% set slots = state_attr('sensor.stundenplan_student_a', 'week_time_slots') or [] %}
  {% set weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'] %}
  {% set focus_index = now().weekday() %}
  {% if now().hour >= 17 %}{% set focus_index = focus_index + 1 %}{% endif %}
  {% if focus_index >= 5 %}{% set focus_index = 0 %}{% endif %}
  {% set focus_weekday = weekdays[focus_index] %}
  {% set day_names = {'monday': 'Montag', 'tuesday': 'Dienstag', 'wednesday': 'Mittwoch', 'thursday': 'Donnerstag', 'friday': 'Freitag', 'saturday': 'Samstag', 'sunday': 'Sonntag'} %}
  <table width="100%">
  <thead><tr><th align="left">Zeit</th>{% for day in week %}<th align="left" valign="{{ day.weekday }}">{% if day.weekday == focus_weekday %}{% if now().hour < 17 %}Heute{% else %}Nächster Schultag{% endif %}<br>{{ day_names[day.weekday] }}{% else %}{{ day_names[day.weekday] }}{% endif %}</th>{% endfor %}</tr></thead>
  <tbody>
  {% for slot in slots %}
  {% set slot_index = loop.index0 %}
  <tr><td>{{ slot.start }}–{{ slot.end }}</td>
  {% for day in week %}
  {% set cell = day.grid_cells[slot_index] %}
  {% if cell is not none %}<td valign="{{ day.weekday }}"{% if cell.rowspan > 1 %} rowspan="{{ cell.rowspan }}"{% endif %}>{% if cell.subject %}{{ cell.subject }}{% else %}&nbsp;{% endif %}</td>{% endif %}
  {% endfor %}
  </tr>
  {% endfor %}
  </tbody>
  </table>
card_mod:
  style:
    ha-markdown$: |
      {% set weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'] %}
      {% set focus_index = now().weekday() %}
      {% if now().hour >= 17 %}{% set focus_index = focus_index + 1 %}{% endif %}
      {% if focus_index >= 5 %}{% set focus_index = 0 %}{% endif %}
      {% set focus_weekday = weekdays[focus_index] %}
      th[valign="{{ focus_weekday }}"],
      td[valign="{{ focus_weekday }}"] {
        background-color: #fff2cc !important;
      }
```

Duplicate the Markdown card for each child and change its title and sensor ID.
The second card's `card_mod` template should use that child's sensor ID and
`#ffe0b2` for orange. The `valign` attributes identify the weekday column because
the Markdown card removes inline `style` attributes; card-mod applies the color
to every header and lesson cell in the selected column. Install card-mod through
HACS for the coloring. Until 17:00 the table selects today; after 17:00 it
selects the next school day. On weekends it selects Monday. Adjacent lessons
with the same subject are combined vertically.

## Development

Run the tests with:

```bash
python -m pytest --asyncio-mode=auto
```

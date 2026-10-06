"""Configuration handling for the Stundenplan integration."""

from pathlib import Path

import yaml

from datetime import time

from .models import Block, DaySchedule, Person, Schedule, ScheduleManager
from .parser import parse_legacy_schedule


def create_schedule_manager(
    persons: list[dict],
) -> ScheduleManager:
    """Create a schedule manager from legacy configuration data."""
    manager = ScheduleManager()
     

    for person_data in persons:
        person = Person(
            id=person_data["id"],
            name=person_data["name"],
            schedule=parse_legacy_schedule(person_data["schedule"]),
        )

        manager.add_person(person)

    return manager


def create_schedule_manager_from_config(
    config: dict,
) -> ScheduleManager:
    """Create a schedule manager from the new configuration format."""
    if "persons" not in config:
        raise ValueError("Configuration must contain 'persons'.")

    if not isinstance(config["persons"], list):
        raise ValueError("Configuration 'persons' must be a list.")

    manager = ScheduleManager()
    person_ids: set[str] = set()

    for person_data in config["persons"]:
        if not isinstance(person_data, dict):
            raise ValueError(
                "Each person configuration must be a dictionary."
            )

        # Person ID
        if "id" not in person_data:
            raise ValueError(
                "Each person configuration must contain 'id'."
            )

        person_id = str(person_data["id"]).strip()

        if not person_id:
            raise ValueError("Person ID must not be empty.")

        if person_id in person_ids:
            raise ValueError(
                f"Duplicate person ID: {person_id}"
            )

        person_ids.add(person_id)

        # Person name
        if "name" not in person_data:
            raise ValueError(
                "Each person configuration must contain 'name'."
            )

        person_name = str(person_data["name"]).strip()

        if not person_name:
            raise ValueError("Person name must not be empty.")

        # Schedule
        if "schedule" not in person_data:
            raise ValueError(
                f"Person '{person_id}' must contain 'schedule'."
            )

        if not isinstance(person_data["schedule"], dict):
            raise ValueError(
                f"Schedule for person '{person_id}' must be a dictionary."
            )

        blocks: list[Block] = []

        for block_id, block_data in person_data["schedule"].items():
            block_id = str(block_id).strip()

            if not block_id:
                raise ValueError("Block ID must not be empty.")

            if not isinstance(block_data, dict):
                raise ValueError(
                    f"Block '{block_id}' must be a dictionary."
                )

            days: dict[str, DaySchedule] = {}

            for day, day_data in block_data.items():
                if not isinstance(day_data, dict):
                    raise ValueError(
                        f"Day '{day}' in block '{block_id}' "
                        "must be a dictionary."
                    )

                if "start" not in day_data:
                    raise ValueError(
                        f"Missing start time for block '{block_id}' "
                        f"on {day}."
                    )

                if "end" not in day_data:
                    raise ValueError(
                        f"Missing end time for block '{block_id}' "
                        f"on {day}."
                    )

                if "subject" not in day_data:
                    raise ValueError(
                        f"Missing subject for block '{block_id}' "
                        f"on {day}."
                    )

                start = time.fromisoformat(day_data["start"])
                end = time.fromisoformat(day_data["end"])

                if end <= start:
                    raise ValueError(
                        f"Invalid time range for block {block_id} "
                        f"on {day}: "
                        f"{day_data['start']} - {day_data['end']}"
                    )

                days[day] = DaySchedule(
                    start=start,
                    end=end,
                    subject=day_data["subject"],
                )

            blocks.append(
                Block(
                    id=block_id,
                    days=days,
                )
            )

        schedule = Schedule(blocks=blocks)

        person = Person(
            id=person_id,
            name=person_name,
            schedule=schedule,
        )

        manager.add_person(person)

    return manager
    
    
def load_schedule_manager_from_yaml(
    path: str | Path,
) -> ScheduleManager:
    """Load a schedule manager from a YAML configuration file."""
    with Path(path).open(encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return create_schedule_manager_from_config(config)    
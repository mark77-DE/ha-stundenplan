"""Parsing helpers for Stundenplan data."""

from datetime import time

from .models import Block, DaySchedule, Schedule


def parse_schedule(data: dict) -> Schedule:
    """Parse a normalized schedule dictionary."""
    blocks: list[Block] = []

    for block_data in data["blocks"]:
        days: dict[str, DaySchedule] = {}

        for day, day_data in block_data["days"].items():
            if not day_data.get("start") or not day_data.get("end"):
                continue

            days[day] = DaySchedule(
                start=time.fromisoformat(day_data["start"]),
                end=time.fromisoformat(day_data["end"]),
                subject=day_data["subject"],
            )

        blocks.append(
            Block(
                id=str(block_data["id"]),
                days=days,
            )
        )

    return Schedule(blocks=blocks)


def parse_legacy_schedule(data: list[dict]) -> Schedule:
    """Parse the legacy Home Assistant schedule format."""
    blocks: list[Block] = []

    for block_data in data:
        block_id = str(block_data["block"])

        start_times = block_data["start"]
        end_times = block_data["end"]
        subjects = block_data["class"]

        days: dict[str, DaySchedule] = {}

        for day in start_times:
            start = start_times.get(day)
            end = end_times.get(day)
            subject = subjects.get(day)

            if not start or not end or not subject:
                continue

            days[day] = DaySchedule(
                start=time.fromisoformat(start),
                end=time.fromisoformat(end),
                subject=subject,
            )

        blocks.append(
            Block(
                id=block_id,
                days=days,
            )
        )

    return Schedule(blocks=blocks)
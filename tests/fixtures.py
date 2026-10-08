"""Test fixtures for the Stundenplan integration."""


def create_student_a_new_config() -> dict:
    """Return Student A's schedule in the new configuration format."""
    return {
        "persons": [
            {
                "id": "student_a",
                "name": "Student A",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject J",
                        },
                        "tuesday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                        "wednesday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject A",
                        },
                        "thursday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject B",
                        },
                        "friday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject C",
                        },
                    },
                    "2": {
                        "monday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject J",
                        },
                        "tuesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject A",
                        },
                        "wednesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject A",
                        },
                        "thursday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject B",
                        },
                        "friday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject C",
                        },
                    },
                    "Subject AA": {
                        "monday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                        "tuesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                        "wednesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "KR",
                        },
                        "thursday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                        "friday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                    },
                    "3": {
                        "monday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject D",
                        },
                        "tuesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject E",
                        },
                        "wednesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject H",
                        },
                        "thursday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject V",
                        },
                        "friday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject J",
                        },
                    },
                    "4": {
                        "monday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject D",
                        },
                        "tuesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject E",
                        },
                        "wednesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject H",
                        },
                        "thursday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject V",
                        },
                        "friday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject J",
                        },
                    },
                    "5": {
                        "monday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject B",
                        },
                        "tuesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject F",
                        },
                        "wednesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject D",
                        },
                        "thursday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject K",
                        },
                        "friday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject G",
                        },
                    },
                    "6": {
                        "monday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject B",
                        },
                        "tuesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject L",
                        },
                        "wednesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject D",
                        },
                        "thursday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject K",
                        },
                        "friday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject G",
                        },
                    },
                    "7": {
                        "tuesday": {
                            "start": "13:40",
                            "end": "14:20",
                            "subject": "Subject I",
                        },
                        "friday": {
                            "start": "13:20",
                            "end": "14:00",
                            "subject": "Subject K",
                        },
                    },
                    "8": {
                        "tuesday": {
                            "start": "14:20",
                            "end": "15:00",
                            "subject": "Subject I",
                        },
                    },
                },
            }
        ]
    }
    
def create_student_b_new_config() -> dict:
    """Return Student B's schedule in the new configuration format."""
    return {
        "persons": [
            {
                "id": "student_b",
                "name": "Student B",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject O",
                        },
                        "wednesday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject Z",
                        },
                        "thursday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject W",
                        },
                        "friday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Subject V",
                        },
                    },
                    "2": {
                        "monday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject A",
                        },
                        "tuesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject V",
                        },
                        "wednesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject P",
                        },
                        "thursday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject W",
                        },
                        "friday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Subject V",
                        },
                    },
                    "Subject AA": {
                        "monday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject N",
                        },
                        "tuesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                        "wednesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                        "thursday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                        "friday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "Subject AA",
                        },
                    },
                    "3": {
                        "monday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject H",
                        },
                        "tuesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject X",
                        },
                        "wednesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject Q",
                        },
                        "thursday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject I",
                        },
                        "friday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Subject O",
                        },
                    },
                    "4": {
                        "monday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject H",
                        },
                        "tuesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject X",
                        },
                        "wednesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject Q",
                        },
                        "thursday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject I",
                        },
                        "friday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Subject O",
                        },
                    },
                    "5": {
                        "monday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject Y",
                        },
                        "tuesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject O",
                        },
                        "wednesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject R",
                        },
                        "thursday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "frei",
                        },
                        "friday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Subject S",
                        },
                    },
                    "6": {
                        "monday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject Y",
                        },
                        "tuesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject Z/Subject L",
                        },
                        "wednesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject U",
                        },
                        "thursday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject X",
                        },
                        "friday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Subject T",
                        },
                    },
                    "7": {
                        "monday": {
                            "start": "13:20",
                            "end": "14:00",
                            "subject": "Subject Q",
                        },
                        "tuesday": {
                            "start": "13:40",
                            "end": "14:20",
                            "subject": "Subject W",
                        },
                        "thursday": {
                            "start": "13:20",
                            "end": "14:00",
                            "subject": "Subject A",
                        },
                    },
                    "8": {
                        "monday": {
                            "start": "14:00",
                            "end": "14:40",
                            "subject": "Subject Q",
                        },
                        "thursday": {
                            "start": "14:00",
                            "end": "14:40",
                            "subject": "Subject A",
                        },
                    },
                },
            }
        ]
    }
    
 


def create_complete_new_config() -> dict:
    """Return the complete schedule configuration for all persons."""
    student_a = create_student_a_new_config()["persons"][0]
    student_b = create_student_b_new_config()["persons"][0]

    return {
        "persons": [
            student_a,
            student_b,
        ]
    } 
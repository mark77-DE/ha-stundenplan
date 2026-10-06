"""Test fixtures for the Stundenplan integration."""


def create_paulina_new_config() -> dict:
    """Return Paulina's schedule in the new configuration format."""
    return {
        "persons": [
            {
                "id": "paulina",
                "name": "Paulina",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "WP1",
                        },
                        "tuesday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Mathe",
                        },
                        "wednesday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Mathe",
                        },
                        "thursday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Deutsch",
                        },
                        "friday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Physik",
                        },
                    },
                    "2": {
                        "monday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "WP1",
                        },
                        "tuesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Mathe",
                        },
                        "wednesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Mathe",
                        },
                        "thursday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Deutsch",
                        },
                        "friday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Physik",
                        },
                    },
                    "HT": {
                        "monday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                        "tuesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                        "wednesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "KR",
                        },
                        "thursday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                        "friday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                    },
                    "3": {
                        "monday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Englisch",
                        },
                        "tuesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Chemie",
                        },
                        "wednesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Geo",
                        },
                        "thursday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Bio",
                        },
                        "friday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "WP1",
                        },
                    },
                    "4": {
                        "monday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Englisch",
                        },
                        "tuesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Chemie",
                        },
                        "wednesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Geo",
                        },
                        "thursday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Bio",
                        },
                        "friday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "WP1",
                        },
                    },
                    "5": {
                        "monday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Deutsch",
                        },
                        "tuesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Sport",
                        },
                        "wednesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Englisch",
                        },
                        "thursday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "WP2",
                        },
                        "friday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Geschichte",
                        },
                    },
                    "6": {
                        "monday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Deutsch",
                        },
                        "tuesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Hosp.",
                        },
                        "wednesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Englisch",
                        },
                        "thursday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "WP2",
                        },
                        "friday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Geschichte",
                        },
                    },
                    "7": {
                        "tuesday": {
                            "start": "13:40",
                            "end": "14:20",
                            "subject": "WiPo",
                        },
                        "friday": {
                            "start": "13:20",
                            "end": "14:00",
                            "subject": "WP2",
                        },
                    },
                    "8": {
                        "tuesday": {
                            "start": "14:20",
                            "end": "15:00",
                            "subject": "WiPo",
                        },
                    },
                },
            }
        ]
    }
    
def create_johanna_new_config() -> dict:
    """Return Johanna's schedule in the new configuration format."""
    return {
        "persons": [
            {
                "id": "johanna",
                "name": "Johanna",
                "schedule": {
                    "1": {
                        "monday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "SpanA",
                        },
                        "wednesday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Che",
                        },
                        "thursday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Deu",
                        },
                        "friday": {
                            "start": "07:40",
                            "end": "08:20",
                            "subject": "Bio",
                        },
                    },
                    "2": {
                        "monday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Mathe",
                        },
                        "tuesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Bio",
                        },
                        "wednesday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Inform",
                        },
                        "thursday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Deu",
                        },
                        "friday": {
                            "start": "08:20",
                            "end": "09:00",
                            "subject": "Bio",
                        },
                    },
                    "HT": {
                        "monday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "BeOr",
                        },
                        "tuesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                        "wednesday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                        "thursday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                        "friday": {
                            "start": "09:10",
                            "end": "09:50",
                            "subject": "HT",
                        },
                    },
                    "3": {
                        "monday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Geo",
                        },
                        "tuesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "Eng",
                        },
                        "wednesday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "SpoP",
                        },
                        "thursday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "WiPo",
                        },
                        "friday": {
                            "start": "10:10",
                            "end": "10:50",
                            "subject": "SpanA",
                        },
                    },
                    "4": {
                        "monday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Geo",
                        },
                        "tuesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "Eng",
                        },
                        "wednesday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "SpoP",
                        },
                        "thursday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "WiPo",
                        },
                        "friday": {
                            "start": "10:50",
                            "end": "11:30",
                            "subject": "SpanA",
                        },
                    },
                    "5": {
                        "monday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Ges",
                        },
                        "tuesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "SpanA",
                        },
                        "wednesday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Reli",
                        },
                        "thursday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "frei",
                        },
                        "friday": {
                            "start": "11:50",
                            "end": "12:30",
                            "subject": "Musik/Kunst",
                        },
                    },
                    "6": {
                        "monday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Ges",
                        },
                        "tuesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Che/Hosp.",
                        },
                        "wednesday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Philo",
                        },
                        "thursday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Eng",
                        },
                        "friday": {
                            "start": "12:30",
                            "end": "13:10",
                            "subject": "Kunst/DSp.",
                        },
                    },
                    "7": {
                        "monday": {
                            "start": "13:20",
                            "end": "14:00",
                            "subject": "SpoP",
                        },
                        "tuesday": {
                            "start": "13:40",
                            "end": "14:20",
                            "subject": "Deu",
                        },
                        "thursday": {
                            "start": "13:20",
                            "end": "14:00",
                            "subject": "Mathe",
                        },
                    },
                    "8": {
                        "monday": {
                            "start": "14:00",
                            "end": "14:40",
                            "subject": "SpoP",
                        },
                        "thursday": {
                            "start": "14:00",
                            "end": "14:40",
                            "subject": "Mathe",
                        },
                    },
                },
            }
        ]
    }
    
 


def create_complete_new_config() -> dict:
    """Return the complete schedule configuration for all persons."""
    paulina = create_paulina_new_config()["persons"][0]
    johanna = create_johanna_new_config()["persons"][0]

    return {
        "persons": [
            paulina,
            johanna,
        ]
    } 
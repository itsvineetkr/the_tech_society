STATUS_CHOICES = [(1, "Accepted"), (0, "Req Pending")]

EVENT_TYPE_CHOICES = [
    ("normal", "Normal Event"),
    ("individual", "Individual Participation Event"),
    ("team", "Team Participation Event"),
]

CLUBS_CHOICES = [
    ("all", "All"),
    ("insaniax", "Insaniax"),
    ("parmarth", "Parmarth"),
    ("fractal", "Fractal"),
    ("robotics", "Robotics"),
    ("excelsior", "Excelsior"),
    ("mirage", "Mirage"),
    ("ecell", "E-Cell"),
    ("nnf", "NNF"),
]

INDIVIDUAL_REGISTRAION_DATA_COLUMNS_FOR_XLSX = [
    "Event Name",
    "Email",
    "Name",
    "Year",
    "Branch",
    "Rollno",
]

TEAM_REGISTRAION_DATA_COLUMNS_FOR_XLSX = [
    "Event Name",
    "Team Name",
    "User Name",
    "Roll no",
    "Year",
    "Branch",
    "Email",
    "Phone No",
    "Position",
]

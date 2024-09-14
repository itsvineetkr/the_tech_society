# All the constants are stored here
BRANCH_CHOICES = [
    ("CSE", "CSE Regular"),
    ("CSEAI", "CSE AI"),
    ("CSESF", "CSE SF"),
    ("ECE", "Electronics"),
    ("EE", "Electrical"),
    ("MEC", "Mechanical"),
    ("CVL", "Civil"),
    ("CHE", "Chemical"),
    ("ADMIN", "AdminUser")
]
    
YEAR_CHOICES = [
    ("1", "First Year"),
    ("2", "Second Year"),
    ("3", "Third Year"),
    ("4", "Fourth Year"),
    ("ADMIN", "AdminUser")
]

from events.constants import CLUBS_CHOICES
CLUB_ADMIN_CHOICES = CLUBS_CHOICES[1:] + [("NORMAL", "Student")]
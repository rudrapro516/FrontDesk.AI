import pandas as pd
from datetime import datetime

SYMPTOM_MAP = {
    "ear pain": "ENT",
    "hearing loss": "ENT",
    "fever": "General Medicine",
    "child fever": "Pediatrics",
    "kidney stone": "Urology",
    "heart": "Cardiology",
    "chest pain": "Cardiology",
    "bone": "Orthopaedics",
    "fracture": "Orthopaedics",
    "headache": "Neurology",
    "brain": "Neurology",
    "skin": "Dermatology",
    "stomach": "Gastroenterology",
    "eye": "Ophthalmology",
    "vision": "Ophthalmology",
    "tooth": "Dentistry",
    "pregnancy": "Obstetrics & Gynecology"
}

def identify_department(query):
    query = query.lower()
    for symptom, dept in SYMPTOM_MAP.items():
        if symptom in query:
            return dept
    return None

def extract_day(query):
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    query_lower = query.lower()
    for day in days:
        if day in query_lower:
            return day.capitalize()
    if "today" in query_lower:
        return datetime.now().strftime("%A")
    if "tomorrow" in query_lower:
        from datetime import timedelta
        return (datetime.now() + timedelta(days=1)).strftime("%A")
    return None

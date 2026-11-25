"""Application rules; independent of Streamlit."""
from datetime import datetime, timezone
from . import database

CATEGORIES = ('Unclassified', 'Flooding', 'Medical assistance', 'Relief supplies', 'Other')
URGENCIES = ('Not assessed', 'High', 'Medium', 'Low')

def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def submit_report(location, report):
    location, report = location.strip(), report.strip()
    if not location or not report:
        raise ValueError('Please enter both location and report.')
    if len(location) > 200 or len(report) > 3000:
        raise ValueError('Location must be at most 200 characters and report at most 3000.')
    return database.insert_report(report, location, now())

def review_incident(incident_id, category, urgency):
    if category not in CATEGORIES or urgency not in URGENCIES:
        raise ValueError('Invalid category or urgency.')
    database.save_review(incident_id, category, urgency, now())

def list_incidents():
    return database.list_incidents()

def list_audit():
    return database.list_audit()

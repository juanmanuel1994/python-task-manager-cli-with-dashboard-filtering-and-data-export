"""
seed.py  —  Populate the task manager with realistic demo data.
Run once before recording: python seed.py
"""

import os
import storage
from models import Task

# wipe existing data for a clean demo
if os.path.exists("tasks.json"):
    os.remove("tasks.json")

tasks = [
    # Work
    Task(title="Prepare Q3 financial report",    category="work",    priority="critical", status="in_progress", due_date="2025-07-01",  description="Consolidate data from all departments and present to CFO"),
    Task(title="Review pull requests on GitHub", category="work",    priority="high",     status="pending",     due_date="2026-06-07",  description="At least 5 PRs waiting for review"),
    Task(title="Update project documentation",   category="work",    priority="medium",   status="pending",     due_date="2026-06-20",  description="Add API docs and deployment guide"),
    Task(title="Onboard new developer",          category="work",    priority="high",     status="in_progress", due_date="2026-06-10",  description="Set up access, walk through codebase"),
    Task(title="Weekly team sync",               category="work",    priority="low",      status="done",        description="Regular Monday standup"),

    # Personal
    Task(title="Book dentist appointment",       category="health",  priority="high",     status="pending",     due_date="2025-06-05",  description="Overdue checkup"),
    Task(title="30-minute run",                  category="health",  priority="medium",   status="done",        description="Morning jog around the park"),
    Task(title="Meal prep for the week",         category="health",  priority="low",      status="pending",     due_date="2026-06-08"),
    Task(title="Read 'Clean Code' chapter 5",    category="learning",priority="medium",   status="in_progress", due_date="2026-06-15"),
    Task(title="Complete Python course module",  category="learning",priority="high",     status="pending",     due_date="2026-06-12",  description="Async/await section"),

    # Home
    Task(title="Pay electricity bill",           category="finance", priority="critical", status="pending",     due_date="2025-06-01",  description="Last warning notice received"),
    Task(title="Renew car insurance",            category="finance", priority="high",     status="pending",     due_date="2026-06-30"),
    Task(title="Fix leaking kitchen faucet",     category="home",    priority="medium",   status="pending",     due_date="2026-06-18"),
    Task(title="Clean garage",                   category="home",    priority="low",      status="cancelled",   description="Postponed until summer"),
    Task(title="Buy groceries",                  category="home",    priority="medium",   status="done",        description="Weekly shopping done"),
]

for t in tasks:
    storage.add(t)

print(f"[OK] Seeded {len(tasks)} tasks into tasks.json")

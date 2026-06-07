#!/usr/bin/env python3
"""
Task Manager CLI  v2.0
A full-featured command-line task manager.
"""

import sys
import time
from datetime import datetime

import storage
from models import Task, RESET, BOLD, PRIORITIES
from models import R, B, C_WHITE, C_CYAN, C_GREEN, C_YELLOW, C_RED, C_MAGENTA, C_BLUE, C_GRAY, BG_HEADER
from utils import (
    header, section_header, success, error, info, warn, hr, hr_thin,
    print_table, print_stats, export_csv,
    choose, ask, loading, spinner, clear,
)

# -- splash screen -------------------------------------------------------------

LOGO = f"""
{C_CYAN}{B}
  ████████╗ █████╗ ███████╗██╗  ██╗    ███╗   ███╗ ██████╗ ██████╗
     ██╔══╝██╔══██╗██╔════╝██║ ██╔╝    ████╗ ████║██╔════╝ ██╔══██╗
     ██║   ███████║███████╗█████╔╝     ██╔████╔██║██║  ███╗██████╔╝
     ██║   ██╔══██║╚════██║██╔═██╗     ██║╚██╔╝██║██║   ██║██╔══██╗
     ██║   ██║  ██║███████║██║  ██╗    ██║ ╚═╝ ██║╚██████╔╝██║  ██║
     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝
{R}"""

LOGO_SIMPLE = f"""
{C_CYAN}{B}
  +--------------------------------------------------+
  |                                                  |
  |          TASK  MANAGER  CLI   v2.0               |
  |       Organize. Track. Get things done.          |
  |                                                  |
  +--------------------------------------------------+
{R}"""


def splash():
    clear()
    # try fancy logo first, fall back to simple if encoding fails
    try:
        print(LOGO)
    except UnicodeEncodeError:
        print(LOGO_SIMPLE)

    print(f"  {C_GRAY}Organize. Track. Get things done.{R}")
    print(f"  {C_GRAY}{'-' * 50}{R}\n")

    # boot sequence
    steps = [
        ("Initializing system", 0.35),
        ("Loading task database", 0.45),
        ("Applying theme", 0.3),
        ("Ready", 0.2),
    ]
    for label, duration in steps:
        _animate_boot(label, duration)

    time.sleep(0.2)
    print(f"\n  {C_GREEN}{B}System ready!{R}  Press Enter to continue...")
    input()
    clear()


def _animate_boot(label: str, duration: float):
    frames = ["[.  ]", "[.. ]", "[...]", "[ ..]", "[  .]"]
    import sys, time
    end = time.time() + duration
    i = 0
    while time.time() < end:
        f = frames[i % len(frames)]
        sys.stdout.write(f"\r  {C_CYAN}{f}{R}  {label}...")
        sys.stdout.flush()
        time.sleep(0.07)
        i += 1
    sys.stdout.write(f"\r  {C_GREEN}[OK ]{R}  {label}          \n")
    sys.stdout.flush()


# -- menu ----------------------------------------------------------------------

def print_menu(count: int, overdue: int):
    clear()
    try:
        print(f"\n{C_CYAN}{B}  +================================================+")
        print(f"  |          TASK MANAGER  CLI   v2.0              |")
        print(f"  +================================================+{R}\n")
    except UnicodeEncodeError:
        print(f"\n{C_CYAN}{B}  TASK MANAGER CLI  v2.0{R}\n")

    # status bar
    print(f"  {BG_HEADER}{C_WHITE}  Tasks: {B}{count}{R}{BG_HEADER}{C_WHITE}   "
          + (f"{C_RED}{B}  Overdue: {overdue}  {R}{BG_HEADER}" if overdue else f"  Overdue: 0  ")
          + f"{C_WHITE}  {R}\n")

    options = [
        ("1", "Add Task",         C_GREEN),
        ("2", "List All Tasks",   C_CYAN),
        ("3", "Update Task",      C_YELLOW),
        ("4", "Complete Task",    C_GREEN),
        ("5", "Delete Task",      C_RED),
        ("6", "Search Tasks",     C_BLUE),
        ("7", "Filter Tasks",     C_MAGENTA),
        ("8", "Statistics",       C_CYAN),
        ("9", "Export to CSV",    C_YELLOW),
        ("0", "Exit",             C_GRAY),
    ]

    print(f"  {C_WHITE}{B}  MENU{R}")
    hr_thin()
    for key, label, color in options:
        bullet = f"{color}{B}[{key}]{R}"
        print(f"  {bullet}  {C_WHITE}{label}{R}")
    hr_thin()
    print()


# -- commands ------------------------------------------------------------------

def cmd_add():
    section_header("ADD NEW TASK", "++")
    loading("Preparing form")

    title       = ask("Title", required=True)
    category    = ask("Category", required=True, default="general")
    description = ask("Description", required=False)
    priority    = choose("Priority", ["low", "medium", "high", "critical"], default="medium")
    due_raw     = ask("Due date (YYYY-MM-DD)", required=False)

    due_date = None
    if due_raw:
        try:
            datetime.strptime(due_raw, "%Y-%m-%d")
            due_date = due_raw
        except ValueError:
            error("Invalid date format — due date ignored.")

    spinner("Saving task")
    task = Task(
        title=title,
        category=category,
        description=description,
        priority=priority,
        due_date=due_date,
    )
    storage.add(task)
    success(f"Task [{C_CYAN}{task.id}{R}] '{C_WHITE}{B}{task.title}{R}' created successfully!")


def cmd_list(tasks=None):
    section_header("ALL TASKS", "**")
    loading("Fetching tasks")
    if tasks is None:
        tasks = storage.load_all()
    tasks.sort(key=lambda t: (
        not t.is_overdue(),
        -PRIORITIES.get(t.priority, 0),
        t.created_at,
    ))
    print_table(tasks)


def cmd_update():
    section_header("UPDATE TASK", "//")
    task_id = ask("Task ID to update", required=True)
    loading("Looking up task")
    task = storage.find_by_id(task_id)

    if not task:
        error(f"No task found with ID '{task_id}'.")
        return

    print(f"  {C_CYAN}Found:{R}  {B}{task.title}{R}  {task.status_label()}  {task.priority_label()}\n")
    print(f"  {C_GRAY}Press Enter to keep the current value.{R}\n")

    new_title    = ask("Title",       required=False, default=task.title)
    new_cat      = ask("Category",    required=False, default=task.category)
    new_desc     = ask("Description", required=False, default=task.description)
    new_priority = choose("Priority", ["low", "medium", "high", "critical"], default=task.priority)
    new_status   = choose("Status",   ["pending", "in_progress", "done", "cancelled"], default=task.status)
    due_raw      = ask("Due date (YYYY-MM-DD)", required=False, default=task.due_date or "")

    due_date = task.due_date
    if due_raw and due_raw != task.due_date:
        try:
            datetime.strptime(due_raw, "%Y-%m-%d")
            due_date = due_raw
        except ValueError:
            error("Invalid date — keeping original.")

    task.title       = new_title
    task.category    = new_cat
    task.description = new_desc
    task.priority    = new_priority
    task.status      = new_status
    task.due_date    = due_date or None
    task.updated_at  = datetime.now().isoformat()

    spinner("Saving changes")
    storage.update(task)
    success(f"Task [{C_CYAN}{task.id}{R}] updated successfully!")


def cmd_complete():
    section_header("COMPLETE TASK", "OK")
    task_id = ask("Task ID to mark as done", required=True)
    loading("Looking up task")
    task = storage.find_by_id(task_id)

    if not task:
        error(f"No task found with ID '{task_id}'.")
        return
    if task.status == "done":
        warn(f"Task [{task.id}] is already marked as done.")
        return

    task.status     = "done"
    task.updated_at = datetime.now().isoformat()
    spinner("Marking as done")
    storage.update(task)
    success(f"Task [{C_CYAN}{task.id}{R}] '{C_WHITE}{B}{task.title}{R}' completed!")


def cmd_delete():
    section_header("DELETE TASK", "XX")
    task_id = ask("Task ID to delete", required=True)
    loading("Looking up task")
    task = storage.find_by_id(task_id)

    if not task:
        error(f"No task found with ID '{task_id}'.")
        return

    print(f"  {C_YELLOW}About to delete:{R}  {B}{task.title}{R}  {task.priority_label()}\n")
    confirm = choose("Are you sure?", ["yes", "no"], default="no")
    if confirm != "yes":
        info("Deletion cancelled.")
        return

    spinner("Deleting task")
    storage.delete(task_id)
    success(f"Task [{C_CYAN}{task_id}{R}] permanently deleted.")


def cmd_search():
    section_header("SEARCH TASKS", "??")
    query = ask("Search keyword", required=True).lower()
    loading("Searching")
    tasks = storage.load_all()
    results = [
        t for t in tasks
        if query in t.title.lower() or query in t.description.lower()
    ]
    if results:
        info(f"Found {C_GREEN}{B}{len(results)}{R} result(s) for '{C_YELLOW}{query}{R}':\n")
        print_table(results)
    else:
        warn(f"No tasks match '{query}'.")


def cmd_filter():
    while True:
        section_header("FILTER TASKS", "//")
        print(f"  {C_WHITE}{B}Filter by:{R}\n")
        print(f"  {C_GREEN}{B}[1]{R}  Status")
        print(f"  {C_YELLOW}{B}[2]{R}  Priority")
        print(f"  {C_CYAN}{B}[3]{R}  Category")
        print(f"  {C_RED}{B}[4]{R}  Overdue only")
        print(f"  {C_GRAY}{B}[0]{R}  Back to menu\n")

        choice = input(f"  {C_CYAN}{B}Filter option:{R} ").strip()
        tasks  = storage.load_all()

        if choice == "1":
            status = choose("Status", ["pending", "in_progress", "done", "cancelled"])
            loading(f"Filtering by status: {status}")
            cmd_list([t for t in tasks if t.status == status])

        elif choice == "2":
            priority = choose("Priority", ["low", "medium", "high", "critical"])
            loading(f"Filtering by priority: {priority}")
            cmd_list([t for t in tasks if t.priority == priority])

        elif choice == "3":
            cats = sorted(set(t.category for t in tasks))
            if not cats:
                warn("No categories found.")
                continue
            print(f"\n  {C_CYAN}{B}Available categories:{R}")
            for i, cat in enumerate(cats, 1):
                print(f"    {C_WHITE}{i}.{R} {cat}")
            print()
            cat_input = ask("Category name", required=True)
            loading(f"Filtering by category: {cat_input}")
            cmd_list([t for t in tasks if t.category.lower() == cat_input.lower()])

        elif choice == "4":
            loading("Finding overdue tasks")
            overdue = [t for t in tasks if t.is_overdue()]
            if overdue:
                section_header(f"OVERDUE TASKS  ({len(overdue)})", "!!")
                print_table(overdue)
            else:
                success("No overdue tasks! You're all caught up.")

        elif choice == "0":
            break
        else:
            error("Invalid option. Enter 1-4 or 0.")

        input(f"\n  {C_GRAY}Press Enter to continue...{R}")


def cmd_stats():
    loading("Analyzing tasks")
    tasks = storage.load_all()
    print_stats(tasks)


def cmd_export():
    section_header("EXPORT TO CSV", ">>")
    tasks    = storage.load_all()
    filename = ask("Output filename", required=False, default="tasks_export.csv")
    spinner("Exporting data")
    path = export_csv(tasks, filename)
    success(f"Exported {C_CYAN}{B}{len(tasks)}{R} task(s) to:\n\n     {C_GREEN}{path}{R}")


# -- main loop -----------------------------------------------------------------

COMMANDS = {
    "1": cmd_add,
    "2": cmd_list,
    "3": cmd_update,
    "4": cmd_complete,
    "5": cmd_delete,
    "6": cmd_search,
    "7": cmd_filter,
    "8": cmd_stats,
    "9": cmd_export,
}


def main():
    splash()

    while True:
        tasks   = storage.load_all()
        count   = len(tasks)
        overdue = sum(1 for t in tasks if t.is_overdue())
        print_menu(count, overdue)

        choice = input(f"  {C_CYAN}{B}Select option:{R} ").strip()

        if choice == "0":
            clear()
            print(f"\n  {C_CYAN}{B}Thanks for using Task Manager!{R}")
            print(f"  {C_GRAY}See you next time.{R}\n")
            sys.exit(0)

        cmd = COMMANDS.get(choice)
        if cmd:
            try:
                print()
                cmd()
            except KeyboardInterrupt:
                print()
                info("Operation cancelled.")
        else:
            error("Invalid option. Enter a number from 0 to 9.")

        input(f"\n  {C_GRAY}Press Enter to return to menu...{R}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C_CYAN}{B}Goodbye!{R}\n")
        sys.exit(0)

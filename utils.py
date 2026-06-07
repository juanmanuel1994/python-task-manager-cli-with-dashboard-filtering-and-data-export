import csv
import os
import sys
import time
from collections import Counter
from typing import List

from models import Task, RESET, BOLD, PRIORITIES
from models import (
    R, B, DIM, C_WHITE, C_CYAN, C_GREEN, C_YELLOW,
    C_RED, C_MAGENTA, C_BLUE, C_GRAY, C_ORANGE,
    BG_DARK, BG_HEADER,
)

# -- animation -----------------------------------------------------------------

def loading(label: str = "Loading", steps: int = 5, delay: float = 0.09):
    frames = [".  ", ".. ", "..."]
    sys.stdout.write(f"\n  {C_CYAN}{B}{label}{R}")
    sys.stdout.flush()
    for i in range(steps):
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r  {C_CYAN}{B}{label}{R} {C_YELLOW}{frame}{R}")
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(f"\r  {C_GREEN}{B}{label} done!{R}          \n")
    sys.stdout.flush()
    time.sleep(0.08)


def spinner(label: str = "Processing", duration: float = 0.5):
    frames = ["|", "/", "-", "\\"]
    end = time.time() + duration
    i = 0
    sys.stdout.write("\n")
    while time.time() < end:
        sys.stdout.write(f"\r  {C_CYAN}{frames[i % 4]}{R}  {B}{label}...{R}")
        sys.stdout.flush()
        time.sleep(0.07)
        i += 1
    sys.stdout.write(f"\r  {C_GREEN}{B}Done!{R}                    \n\n")
    sys.stdout.flush()


# -- terminal helpers ----------------------------------------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def hr(char="=", width=62, color=C_BLUE):
    print(f"{color}{char * width}{R}")


def hr_thin(width=62):
    print(f"{C_GRAY}{'-' * width}{R}")


def section_header(text: str, icon: str = ">>"):
    width = 62
    print()
    hr(color=C_CYAN)
    padding = (width - len(text) - len(icon) - 3) // 2
    print(f"{BG_HEADER}{C_WHITE}{B}  {icon}  {' ' * padding}{text}{' ' * padding}  {R}")
    hr(color=C_CYAN)
    print()


def header(text: str):
    section_header(text)


def success(msg: str):
    print(f"\n  {C_GREEN}{B}  SUCCESS  {R}  {C_WHITE}{msg}{R}\n")


def error(msg: str):
    print(f"\n  {C_RED}{B}  ERROR  {R}  {C_WHITE}{msg}{R}\n")


def info(msg: str):
    print(f"  {C_CYAN}>{R}  {msg}")


def warn(msg: str):
    print(f"  {C_YELLOW}{B}  WARN  {R}  {C_WHITE}{msg}{R}")


def label_val(label: str, value: str, label_color=C_CYAN):
    print(f"  {label_color}{B}{label:<18}{R}  {C_WHITE}{value}{R}")


# -- table renderer ------------------------------------------------------------

def print_table(tasks: List[Task]):
    if not tasks:
        print(f"\n  {C_YELLOW}No tasks found.{R}\n")
        return

    col_id    = 8
    col_title = 26
    col_cat   = 11
    col_pri   = 16
    col_stat  = 18
    col_due   = 13

    # header row
    print(f"  {BG_HEADER}{C_WHITE}{B}"
          f"  {'ID':<{col_id}}  {'TITLE':<{col_title}}  {'CATEGORY':<{col_cat}}"
          f"  {'PRIORITY':<{col_pri}}  {'STATUS':<{col_stat}}  {'DUE DATE':<{col_due}}"
          f"  {R}")
    hr_thin()

    for i, t in enumerate(tasks):
        title = (t.title[:col_title - 1] + ".") if len(t.title) > col_title else t.title
        row_color = f"\033[48;5;236m" if i % 2 == 0 else ""
        print(
            f"  {row_color}"
            f"{C_GRAY}{t.id:<{col_id}}{R}  "
            f"{row_color}{C_WHITE}{title:<{col_title}}{R}  "
            f"{row_color}{C_CYAN}{t.category:<{col_cat}}{R}  "
            f"{t.priority_label():<{col_pri + 20}}"
            f"{t.status_label():<{col_stat + 20}}"
            f"{t.due_label()}"
            f"{R}"
        )

    hr_thin()
    print(f"  {C_CYAN}{B}{len(tasks)}{R}{C_GRAY} task(s) found{R}\n")


# -- statistics ----------------------------------------------------------------

def print_stats(tasks: List[Task]):
    total = len(tasks)
    if total == 0:
        info("No tasks to analyze.")
        return

    by_status   = Counter(t.status for t in tasks)
    by_priority = Counter(t.priority for t in tasks)
    by_category = Counter(t.category for t in tasks)
    overdue     = sum(1 for t in tasks if t.is_overdue())
    done_pct    = round(by_status.get("done", 0) / total * 100)

    section_header("STATISTICS", "##")

    # summary boxes
    print(f"  {C_CYAN}{B}Total Tasks   {R}{C_WHITE}{B}{total}{R}   "
          f"{C_GREEN}{B}Done   {R}{C_WHITE}{B}{by_status.get('done', 0)}{R}   "
          f"{C_YELLOW}{B}Pending   {R}{C_WHITE}{B}{by_status.get('pending', 0)}{R}   "
          f"{C_RED}{B}Overdue   {R}{C_WHITE}{B}{overdue}{R}")
    print()

    # progress bar
    filled  = done_pct // 4
    empty   = 25 - filled
    bar     = f"{C_GREEN}{B}{'#' * filled}{R}{C_GRAY}{'.' * empty}{R}"
    print(f"  {C_CYAN}{B}Completion{R}  [{bar}]  {C_WHITE}{B}{done_pct}%{R}")
    print()

    # by status
    print(f"  {C_WHITE}{B}By Status{R}")
    status_colors = {"pending": C_YELLOW, "in_progress": C_CYAN, "done": C_GREEN, "cancelled": C_GRAY}
    for status in ("pending", "in_progress", "done", "cancelled"):
        count = by_status.get(status, 0)
        bar   = "#" * count
        col   = status_colors.get(status, C_WHITE)
        pct   = round(count / total * 100) if total else 0
        print(f"    {col}{status.replace('_',' '):<14}{R}  {col}{bar:<15}{R}  {C_WHITE}{count}{R}  {C_GRAY}({pct}%){R}")

    print()

    # by priority
    print(f"  {C_WHITE}{B}By Priority{R}")
    pri_colors = {"critical": C_MAGENTA, "high": C_RED, "medium": C_YELLOW, "low": C_BLUE}
    for pri in ("critical", "high", "medium", "low"):
        count = by_priority.get(pri, 0)
        bar   = "#" * count
        col   = pri_colors.get(pri, C_WHITE)
        print(f"    {col}{pri:<14}{R}  {col}{bar:<15}{R}  {C_WHITE}{count}{R}")

    print()

    # by category
    print(f"  {C_WHITE}{B}By Category{R}")
    cat_colors = [C_CYAN, C_GREEN, C_YELLOW, C_MAGENTA, C_ORANGE, C_BLUE]
    for idx, (cat, count) in enumerate(by_category.most_common()):
        bar = "#" * count
        col = cat_colors[idx % len(cat_colors)]
        print(f"    {col}{cat:<14}{R}  {col}{bar:<15}{R}  {C_WHITE}{count}{R}")

    print()


# -- CSV export ----------------------------------------------------------------

def export_csv(tasks: List[Task], filename: str = "tasks_export.csv") -> str:
    fields = ["id", "title", "category", "priority", "status",
              "description", "due_date", "created_at", "updated_at"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for t in tasks:
            writer.writerow(t.to_dict())
    return os.path.abspath(filename)


# -- input helpers -------------------------------------------------------------

def choose(prompt: str, options: list, default: str = "") -> str:
    opts_str = "  /  ".join(
        f"{C_GREEN}{B}{o}{R}" if o == default else f"{C_WHITE}{o}{R}"
        for o in options
    )
    while True:
        val = input(f"  {C_CYAN}{B}{prompt}{R}  [{opts_str}{R}]: ").strip().lower()
        if val == "" and default:
            return default
        if val in options:
            return val
        error(f"Please choose one of: {', '.join(options)}")


def ask(prompt: str, required: bool = True, default: str = "") -> str:
    if default:
        hint = f"{C_GRAY} (default: {default}){R}"
    elif required:
        hint = f"{C_RED} *{R}"
    else:
        hint = f"{C_GRAY} (optional){R}"

    while True:
        val = input(f"  {C_CYAN}{B}{prompt}{R}{hint}: ").strip()
        if val == "" and default:
            return default
        if val or not required:
            return val
        error("This field is required.")

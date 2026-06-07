╔══════════════════════════════════════════════════════════════╗
║              TASK MANAGER CLI  v2.0                          ║
║          Organize. Track. Get things done.                   ║
╚══════════════════════════════════════════════════════════════╝

A full-featured command-line task manager built in pure Python.
No external packages required — only Python standard library.


════════════════════════════════════════════════════════════════
  WHAT IT DOES
════════════════════════════════════════════════════════════════

Task Manager CLI lets you create, organize, and track tasks
directly from your terminal. It features:

  - Animated splash screen with boot sequence on startup
  - Color-coded interactive menu
  - Full CRUD: add, list, update, complete, delete tasks
  - Priority levels: low / medium / high / critical
  - Status tracking: pending / in_progress / done / cancelled
  - Due date support with overdue detection (highlighted in red)
  - Search tasks by keyword (title + description)
  - Filter tasks by status, priority, category, or overdue
  - Statistics dashboard with ASCII bar charts + completion %
  - Export all tasks to a CSV file
  - Data stored locally in tasks.json (no database needed)
  - Alternating row colors in task table for readability
  - Confirmation prompt before destructive actions (delete)


════════════════════════════════════════════════════════════════
  REQUIREMENTS
════════════════════════════════════════════════════════════════

  - Python 3.8 or higher
  - No external packages (uses standard library only)

To check your Python version:

    python --version


════════════════════════════════════════════════════════════════
  HOW TO RUN
════════════════════════════════════════════════════════════════

Step 1 — Open a terminal inside the task-manager folder.

Step 2 — (Optional but recommended) Load demo data first:

    python seed.py

  This creates 15 realistic sample tasks across categories like
  work, health, finance, learning, and home — great for testing
  and demonstrations.

Step 3 — Launch the app:

    python taskmanager.py

  The app will show an animated splash screen, then take you
  to the main interactive menu.


════════════════════════════════════════════════════════════════
  MENU OPTIONS
════════════════════════════════════════════════════════════════

  [1]  Add Task
       Create a new task. You will be prompted for:
         - Title        (required)
         - Category     (required, e.g. work / health / home)
         - Description  (optional)
         - Priority     (low / medium / high / critical)
         - Due date     (optional, format: YYYY-MM-DD)

  [2]  List All Tasks
       Shows all tasks sorted by urgency (overdue first),
       then by priority, then creation date.
       Color-coded columns: ID, title, category, priority,
       status, and due date.

  [3]  Update Task
       Enter a Task ID to edit any field.
       Press Enter to keep the current value for any field.

  [4]  Complete Task
       Enter a Task ID to mark it as done instantly.
       Shows a warning if the task is already completed.

  [5]  Delete Task
       Enter a Task ID to delete it permanently.
       Requires confirmation before deleting (yes / no).

  [6]  Search Tasks
       Enter any keyword to search across task titles
       and descriptions. Case-insensitive.

  [7]  Filter Tasks
       Sub-menu to filter by:
         1. Status      (pending / in_progress / done / cancelled)
         2. Priority    (low / medium / high / critical)
         3. Category    (shows available categories dynamically)
         4. Overdue only

  [8]  Statistics
       Dashboard showing:
         - Total tasks, done count, pending count, overdue count
         - Completion progress bar (percentage)
         - Bar charts by status, by priority, by category

  [9]  Export to CSV
       Saves all tasks to a .csv file (default: tasks_export.csv)
       You can enter a custom filename when prompted.
       File includes all fields: id, title, category, priority,
       status, description, due date, created_at, updated_at.

  [0]  Exit
       Exits the application cleanly.


════════════════════════════════════════════════════════════════
  TASK FIELDS
════════════════════════════════════════════════════════════════

  Field         Description
  ────────────  ─────────────────────────────────────────────
  id            Auto-generated 8-character unique ID
  title         Short name for the task (required)
  category      Group label (e.g. work, health, finance)
  priority      low / medium / high / critical
  status        pending / in_progress / done / cancelled
  description   Optional longer description
  due_date      Optional deadline in YYYY-MM-DD format
  created_at    Auto-set timestamp when task is created
  updated_at    Auto-updated timestamp on every edit


════════════════════════════════════════════════════════════════
  PRIORITY COLORS & ICONS
════════════════════════════════════════════════════════════════

  low       →  Blue      [ v ]
  medium    →  Yellow    [ - ]
  high      →  Red       [ ! ]
  critical  →  Magenta   [ !! ]


════════════════════════════════════════════════════════════════
  STATUS COLORS & ICONS
════════════════════════════════════════════════════════════════

  pending      →  Yellow    [ ]
  in_progress  →  Cyan      [~]
  done         →  Green     [x]
  cancelled    →  Gray      [-]


════════════════════════════════════════════════════════════════
  FILE STRUCTURE
════════════════════════════════════════════════════════════════

  task-manager/
  ├── taskmanager.py    Main entry point — splash screen, menu, commands
  ├── models.py         Task dataclass, color constants, priority/status helpers
  ├── storage.py        JSON read/write layer (load, save, add, update, delete)
  ├── utils.py          Table renderer, stats dashboard, CSV export, input helpers
  ├── seed.py           Generates 15 demo tasks for testing/recording
  ├── tasks.json        Auto-created data file — do not edit manually
  ├── HOW_TO_RUN.txt    Quick start reference
  └── README 2.txt      This file


════════════════════════════════════════════════════════════════
  DATA STORAGE
════════════════════════════════════════════════════════════════

All tasks are saved automatically to tasks.json in the same
folder. The file is created on first run. It is a plain JSON
file — human-readable but should not be edited manually as
it may corrupt the data.

If tasks.json becomes corrupted or unreadable, delete it and
run seed.py again to start fresh.


════════════════════════════════════════════════════════════════
  QUICK EXAMPLE SESSION
════════════════════════════════════════════════════════════════

  # Seed demo data
  python seed.py

  # Launch the app
  python taskmanager.py

  # From the menu:
  #   Press 1 → add a task called "Fix login bug", category "work",
  #              priority "high", due date 2026-06-15
  #   Press 2 → see all tasks listed with colors
  #   Press 8 → view statistics dashboard
  #   Press 4 → complete the task by entering its ID
  #   Press 9 → export everything to tasks_export.csv
  #   Press 0 → exit


════════════════════════════════════════════════════════════════
  NOTES
════════════════════════════════════════════════════════════════

  - Color output requires a terminal that supports ANSI codes.
    Works on: Linux, macOS, Windows Terminal, VS Code terminal.
    May not render correctly in basic Windows cmd.exe.

  - The app runs fully offline. No internet connection needed.

  - seed.py is safe to re-run. It deletes tasks.json and
    regenerates it with fresh demo data each time.

  - Pressing Ctrl+C at any prompt cancels the current operation
    and returns to the menu safely.

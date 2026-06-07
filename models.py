from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

PRIORITIES = {"low": 1, "medium": 2, "high": 3, "critical": 4}

# -- colors --------------------------------------------------------------------
R  = "\033[0m"       # reset
B  = "\033[1m"       # bold
DIM = "\033[2m"

# backgrounds
BG_DARK   = "\033[48;5;235m"
BG_HEADER = "\033[48;5;24m"

# foregrounds
C_WHITE   = "\033[97m"
C_CYAN    = "\033[96m"
C_GREEN   = "\033[92m"
C_YELLOW  = "\033[93m"
C_RED     = "\033[91m"
C_MAGENTA = "\033[95m"
C_BLUE    = "\033[94m"
C_GRAY    = "\033[90m"
C_ORANGE  = "\033[38;5;208m"

RESET = R
BOLD  = B

PRIORITY_STYLES = {
    "low":      f"{C_BLUE}{B}",
    "medium":   f"{C_YELLOW}{B}",
    "high":     f"{C_RED}{B}",
    "critical": f"{C_MAGENTA}{B}",
}
PRIORITY_ICONS = {
    "low":      "v",
    "medium":   "-",
    "high":     "!",
    "critical": "!!",
}
STATUS_STYLES = {
    "pending":     f"{C_YELLOW}",
    "in_progress": f"{C_CYAN}{B}",
    "done":        f"{C_GREEN}{B}",
    "cancelled":   f"{C_GRAY}",
}
STATUS_ICONS = {
    "pending":     "[ ]",
    "in_progress": "[~]",
    "done":        "[x]",
    "cancelled":   "[-]",
}

PRIORITY_COLORS = PRIORITY_STYLES
STATUS_COLORS   = STATUS_STYLES


@dataclass
class Task:
    title: str
    category: str
    priority: str = "medium"
    status: str = "pending"
    description: str = ""
    due_date: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> dict:
        return {
            "id":          self.id,
            "title":       self.title,
            "category":    self.category,
            "priority":    self.priority,
            "status":      self.status,
            "description": self.description,
            "due_date":    self.due_date,
            "created_at":  self.created_at,
            "updated_at":  self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            category=data["category"],
            priority=data.get("priority", "medium"),
            status=data.get("status", "pending"),
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
        )

    def is_overdue(self) -> bool:
        if not self.due_date or self.status in ("done", "cancelled"):
            return False
        return self.due_date < datetime.now().strftime("%Y-%m-%d")

    def priority_label(self) -> str:
        style = PRIORITY_STYLES.get(self.priority, "")
        icon  = PRIORITY_ICONS.get(self.priority, "")
        return f"{style}{icon} {self.priority.upper()}{R}"

    def status_label(self) -> str:
        style = STATUS_STYLES.get(self.status, "")
        icon  = STATUS_ICONS.get(self.status, "")
        label = self.status.replace("_", " ").upper()
        return f"{style}{icon} {label}{R}"

    def due_label(self) -> str:
        if not self.due_date:
            return f"{C_GRAY}  none{R}"
        if self.is_overdue():
            return f"{C_RED}{B}[!] {self.due_date}{R}"
        return f"{C_GREEN}{self.due_date}{R}"

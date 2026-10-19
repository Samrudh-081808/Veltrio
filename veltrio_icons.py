
from pathlib import Path

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QToolButton


class VeltrioIcons:
    """
    Loads and applies Veltrio SVG icons.

    Default variants:
        teal      -> name.svg
        charcoal  -> name_charcoal.svg
    """

    ICON_DIR = (
        Path(__file__).resolve().parent
        / "resources"
        / "veltrio-icons"
    )

    ICON_NAMES = {
        "add_task",
        "calendar",
        "close",
        "complete_task",
        "dashboard",
        "date_custom",
        "date_deadline",
        "date_next_week",
        "date_today",
        "date_tomorrow",
        "decrease_time",
        "delete",
        "dropdown_chevron",
        "edit",
        "export_summary",
        "focus",
        "health",
        "holiday_trip",
        "inbox",
        "increase_time",
        "list_selector",
        "more_options",
        "next",
        "notes",
        "notifications",
        "previous",
        "profile",
        "search",
        "settings",
        "study",
        "task_submit",
        "task_unchecked",
        "tasks",
        "theme",
        "timer_pause",
        "timer_reset",
        "timer_start",
        "work",
        "workspace",
        "theme_day",
        "theme_night",
    }

    DEFAULT_SIZE = QSize(20, 20)

    @classmethod
    def path(cls, name, variant="teal"):
        """Return the path to an icon variant."""
        if name not in cls.ICON_NAMES:
            raise ValueError(f"Unknown Veltrio icon: {name}")

        if variant not in {"teal", "charcoal"}:
            raise ValueError(
                "Variant must be 'teal' or 'charcoal'."
            )

        filename = (
            f"{name}.svg"
            if variant == "teal"
            else f"{name}_charcoal.svg"
        )

        return cls.ICON_DIR / filename

    @classmethod
    def get(cls, name, variant="teal"):
        """Load and return a QIcon."""
        icon_path = cls.path(name, variant)

        if not icon_path.is_file():
            raise FileNotFoundError(
                f"Icon file not found: {icon_path}"
            )

        icon = QIcon(str(icon_path))

        if icon.isNull():
            raise ValueError(
                f"Qt could not load the icon: {icon_path}"
            )

        return icon

    @classmethod
    def apply(
        cls,
        widget,
        name,
        variant="teal",
        size=None,
    ):
        """Apply an icon to an existing button."""
        icon = cls.get(name, variant)
        icon_size = size or cls.DEFAULT_SIZE

        if isinstance(widget, QPushButton):
            widget.setIcon(icon)
            widget.setIconSize(icon_size)

        elif isinstance(widget, QToolButton):
            widget.setIcon(icon)
            widget.setIconSize(icon_size)

        else:
            raise TypeError(
                "VeltrioIcons.apply() expects a QPushButton "
                "or QToolButton."
            )

        return widget

    @classmethod
    def validate_all(cls):
        """Check whether all 78 SVG files exist and load."""
        missing = []
        invalid = []

        for name in sorted(cls.ICON_NAMES):
            for variant in ("teal", "charcoal"):
                icon_path = cls.path(name, variant)

                if not icon_path.is_file():
                    missing.append(str(icon_path))
                    continue

                if QIcon(str(icon_path)).isNull():
                    invalid.append(str(icon_path))

        return {
            "total_expected": len(cls.ICON_NAMES) * 2,
            "missing": missing,
            "invalid": invalid,
        }
    @staticmethod
    def apply_stateful(button, icon_name):
        def update_icon(checked=False):
            color = "" if checked else "_charcoal"
            button.setIcon(
                QIcon(str(VeltrioIcons.ICON_DIR / f"{icon_name}{color}.svg"))
            )

        update_icon(button.isChecked())
        button.toggled.connect(update_icon)

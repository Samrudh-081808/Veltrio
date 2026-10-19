# Veltrio icon audit and integration

## Scope

Audited the full supplied Python source text (1,434 lines) and the existing `outputs/veltrio-icons` folder. No actual project checkout or `Resources` directory was supplied, so resource files and any other modules, menus, or dialogs could not be inspected. Previously generated icons were retained and reused; only missing assets identified from this source were added.

## Inventory

| Icon | UI location | Current symbol / visual | Required states or variants | Status | Suggested asset |
|---|---|---|---|---|---|
| Window icon | Application window | veltrio.ico path referenced; actual ICO not supplied | App icon / OS rendering | Required | veltrio.ico — missing |
| Brand mark | Header brand | Existing PNG logo referenced, preserved | Existing teal ribbon art | Required | existing logo PNG — not supplied |
| Dashboard | Sidebar | Text only | Selected / unselected | Required | dashboard.svg |
| Tasks | Sidebar | Text only | Selected / unselected | Required | tasks.svg |
| Calendar | Sidebar | Text only | Selected / unselected | Required | calendar.svg |
| Notes | Sidebar | Text only | Selected / unselected | Required | notes.svg |
| Inbox | My Lists | Text only; also task destination | Selected / unselected | Required | inbox.svg |
| Work | My Lists | Text only | Selected / unselected | Required | work.svg |
| Study | My Lists | Text only | Selected / unselected | Required | study.svg |
| Health | My Lists | Text only | Selected / unselected | Required | health.svg |
| Holiday Trip | My Lists | Text only | Selected / unselected | Required | holiday_trip.svg |
| Workspace | Workspace entries | Text only | Selected / unselected | Required | workspace.svg |
| Add list / workspace | Sidebar section headers | + | Shared add symbol | Required | add_task.svg |
| Search | Top bar field | Placeholder only; no icon in supplied code | Optional adornment | Required by audit checklist, not currently rendered | search.svg |
| Export Summary | Top bar | 📂 | Neutral / hover | Required | export_summary.svg |
| Theme toggle | Top bar | 🌗 | Light/dark state | Required | theme.svg |
| Notifications | Top bar | 🔔 | Badge is not shown in supplied code | Required | notifications.svg |
| Profile | Top bar | 👤 | Profile dropdown not shown | Required | profile.svg |
| Submit task | Task input | ➣ | Enabled / disabled button | Required | task_submit.svg |
| List selector | Task input options | 🔵 Inbox ▾ | Dropdown open / closed; current list can be indicated by UI styling | Required | list_selector.svg + dropdown_chevron.svg |
| Now / Today | Task date shortcuts | Text button | Selected / unselected | Required | date_today.svg |
| Tomorrow | Task date shortcuts | Text button | Selected / unselected | Required | date_tomorrow.svg |
| Next Week | Task date shortcuts | Text button | Selected / unselected | Required | date_next_week.svg |
| Custom Date | Task date shortcuts | Text button | Selected / unselected | Required | date_custom.svg |
| Task checkbox | Today task list | QCheckBox; no custom glyph | Unchecked / checked | Required | task_unchecked.svg + complete_task.svg |
| Timer decrease | Focus timer | − | Enabled / disabled | Required | decrease_time.svg |
| Timer increase | Focus timer | + | Enabled / disabled | Required | increase_time.svg |
| Timer start / pause | Focus timer | ▶ / Ⅱ | Play / pause state | Required | timer_start.svg + timer_pause.svg |
| Timer reset | Focus timer | ↺ | Enabled / disabled | Required | timer_reset.svg |
| Previous month | Calendar header | ‹ | Hover / pressed | Required | previous.svg |
| Next month | Calendar header | › | Hover / pressed | Required | next.svg |

## Missing-icon report

- The supplied code references `Resources/veltrio-icons/veltrio.ico`, but no ICO or original project resource folder was supplied. The existing ribbon logo is separately referenced as a PNG; it was not modified or recreated.
- The supplied code references PNG landscape and timer backgrounds; these are artwork resources, not icon assets, and were outside this icon generation task.
- The original generated pack had no task-submit glyph, date shortcut symbols, dropdown chevron, or unchecked checkbox. These are now included.
- Theme `theme.svg` represents the light/dark concept. No separate sun and moon state assets exist; the supplied source shows one 🌗 button and no theme-switch implementation.
- The app source does not set icons for sidebar buttons, task checkbox states, date shortcuts, settings/help/error dialogs, expand/collapse, or notification/profile badges. Assets for these only appear where present in existing general-purpose pack; adding them to UI requires code changes.

## Optional future assets

No future-feature icons were added. Candidate-only list from the brief: analytics, charts, search filters, tags, recurring tasks, Pomodoro sessions, task priority, attachments, cloud sync, import, undo/redo, keyboard shortcuts, archived tasks, and trash/recently deleted.

## PyQt5 integration

Assets are in `outputs/veltrio-icons/`. Resolve paths from the application file so the current working directory does not matter:

```python
from pathlib import Path
from PyQt5.QtGui import QIcon

ICON_DIR = Path(__file__).resolve().parent / "Resources" / "Icons"
button.setIcon(QIcon(str(ICON_DIR / "task_submit.svg")))
button.setIconSize(QSize(20, 20))
```

Copy the needed SVGs into the project’s `Resources/Icons/` folder. For the supplied window icon reference, create/provide `Resources/veltrio-icons/veltrio.ico` or update that path to a supplied ICO/PNG. Qt SVG loading requires the Qt SVG image plugin at runtime.

Example timer state change:

```python
self.start_button.setIcon(QIcon(str(ICON_DIR / "timer_start.svg")))
self.start_button.setText("")
def set_running(running):
    name = "timer_pause.svg" if running else "timer_start.svg"
    self.start_button.setIcon(QIcon(str(ICON_DIR / name)))
```

Keep the existing readable button labels; set icons alongside text with `QPushButton.setIcon(...)`. For navigation selected/unselected styling, use the existing checkable button state and palette or select the charcoal/teal asset as needed.

## Validation checklist

- [x] Previously generated 32 icon designs were reused; no duplicates were regenerated.
- [x] The 7 identified missing symbol families were added as teal and charcoal variants.
- [x] All supplied-source icon symbols and calendar arrows appear in the inventory.
- [x] Sidebar navigation labels and workspace controls are inventoried.
- [x] Theme and timer state variants are documented.
- [x] Existing brand logo and landscape artwork were not changed.
- [ ] Actual logo PNG, ICO, landscape, timer background, other source modules, dialogs, and menus could not be validated because only pasted Python source was provided.
- [ ] PNG exports at 16/20/24/32 were not generated; the assets are scalable SVGs.

## Existing reusable assets

The existing set includes dashboard, tasks, calendar, notes, inbox, work, study, health, holiday trip, workspace, search, export summary, theme, notifications, profile, add task, complete task, edit, delete, more options, date deadline, list selector, timer start/pause/reset, increase/decrease time, focus, settings, close, previous, and next, in teal and charcoal variants.

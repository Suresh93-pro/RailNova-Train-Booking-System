<div align="center">

# 🚆 RAILNOVA
### Train Booking & Journey Companion

**Journey, reimagined.**

A neon-inspired Tkinter desktop application for exploring sample train services, saving demo bookings, managing tickets, and counting down to a departure.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-00D9FF?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Type](https://img.shields.io/badge/Type-Academic%20Demo-8A2BE2?style=for-the-badge)

</div>

---

## ✨ Project Overview

RailNova brings train search, demo ticket booking, ticket management, sample station departures and a live-style journey countdown into one desktop application. Its interface uses a dark navy background with neon cyan and magenta accents.

This project demonstrates event-driven GUI programming, navigation between modules, local database persistence, validation, table views and date/time logic.

## 🌌 Features

| Module | Capabilities |
|---|---|
| **Overview Dashboard** | Booking totals, upcoming journeys, cancellations, spend summary and quick search |
| **Book Tickets** | From/To stations, journey date, class, passengers, sample services, estimated fare and passenger details |
| **My Tickets** | Saved demo PNRs, passenger names, route, date, coach/seat labels, class, fare and status |
| **Incoming Trains** | Sample service listings by selected station with departure/arrival times |
| **Upcoming Journeys** | Upcoming, non-cancelled demo bookings |
| **Cancelled Tickets** | Separate cancelled-ticket history |
| **Journey Timer** | Per-second countdown to the selected ticket's departure |
| **Train Explorer** | Instant filtering by train number, name, origin, destination or service type |
| **Help & About** | Workflow, stack, persistence and project limitations |

## 🧰 Built With

- **Python 3** — application logic
- **Tkinter / ttk** — widgets, forms, dialogs, navigation and tables
- **Tkinter Canvas** — drawn visual elements and animated accents
- **SQLite** — local booking records
- **datetime** — date validation and countdown calculations

No third-party `pip` packages are required. Use a Python installation that includes Tkinter.

## 🚀 Run the Project

1. Clone or download this repository.
2. Open the folder in VS Code or a terminal.
3. Run:

   ```bash
   py main.py
   ```

   If the `py` command is unavailable:

   ```bash
   python main.py
   ```

The launcher expands the bundled application source into a readable `railnova_source.py` file on first run, then starts the application. The local SQLite database `railnova.db` is created automatically.

## 🗂️ Repository Layout

```text
RailNova-Train-Booking-System/
├── main.py          # Launches the application
├── README.md        # Project guide
└── .gitignore       # Excludes local DB and Python cache files
```

After the first launch, `railnova_source.py` is generated beside `main.py` so the full application source can be inspected locally.

## 🎓 Academic Project

**Project:** RailNova — Train Booking & Journey Companion  
**Prepared by:** G Suresh Reddy  
**Program:** B.Tech — CSE (Cybersecurity)  
**Course context:** Advanced Programming Practice — Tkinter project

The companion 10-slide presentation covers the overview, application modules, booking workflow, ticket management, journey countdown, technology stack and conclusion. The PowerPoint is currently provided separately from this repository and has not been committed here.

## ⚠️ Important Demo Limitations

RailNova is an **educational prototype**, not a live reservation platform.

- It is **not connected to IRCTC** or any live railway API.
- Train schedules, availability, fares, PNRs, coach and seat labels are sample/demo values.
- No real ticket is issued and no payment is processed.
- The countdown uses the computer's local clock and the selected demo journey date/time.

## 🔭 Future Scope

- Integrate an authorized live train-information API
- Add user accounts and authentication
- Use verified timetables and availability
- Add secure payment integration for a production system
- Add notifications and printable ticket exports

---

<div align="center">

**RAILNOVA** · *Journey, Reimagined* ✦

</div>

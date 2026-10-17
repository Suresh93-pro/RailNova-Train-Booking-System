<div align="center">

# 🚆 RAILNOVA
### Train Booking & Journey Companion

**Plan your route. Organize your tickets. Track your next departure.**

A neon-inspired desktop train-booking demo built with **Python, Tkinter and SQLite**.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-00D9FF?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Academic Project](https://img.shields.io/badge/Project-Academic_Demo-8A2BE2?style=for-the-badge)

</div>

---

## ✨ About RailNova

RailNova is a desktop GUI project that brings train search, demo ticket booking, ticket management, sample station departures and journey countdowns into one application. The interface uses a dark, neon-inspired visual theme with cyan and magenta accents.

The project demonstrates **Tkinter GUI design, event handling, modular navigation, local database persistence and date/time logic**.

## 🌌 Features

| Module | Capabilities |
|---|---|
| **Overview Dashboard** | Booking totals, upcoming journeys, cancellations, travel-spend summary and quick route search |
| **Book Tickets** | From/To stations, journey date, travel class, passenger count, sample train results and passenger-name entry |
| **My Tickets** | Saved demo bookings, PNR, train and route details, passenger names, coach/seat labels, class, fare and status |
| **Incoming Trains** | Sample departures by selected station with scheduled departure and arrival times |
| **Upcoming Journeys** | Upcoming non-cancelled journeys |
| **Cancelled Tickets** | Separate history of cancelled demo bookings |
| **Journey Timer** | Live per-second countdown to the selected journey's departure |
| **Train Explorer** | Instant filtering by train number, train name, origin, destination or service type |
| **Help & About** | Workflow, technology stack, data storage and demo limitations |

## 🧰 Technology Stack

- **Python 3** — application logic
- **Tkinter / ttk** — desktop widgets, forms, navigation, dialogs and tables
- **Tkinter Canvas** — vector-drawn visuals and animated accents
- **SQLite** — local booking persistence
- **datetime** — date validation and departure countdown

No external `pip` packages are required. Use a standard Python installation that includes Tkinter.

## 🚀 Run Locally

1. Clone or download this repository.
2. Open the project folder in VS Code or a terminal.
3. Run:

   ```bash
   py main.py
   ```

   If the `py` command is not available, use:

   ```bash
   python main.py
   ```

The launcher expands the bundled, readable application source to `railnova_source.py` on first run and then starts the app. The SQLite database `railnova.db` is created automatically in the project folder.

## 🗂️ Project Structure

```text
RailNova-Train-Booking-System/
├── main.py                         # Launcher for the application
├── railnova_source.py              # Expanded source, created on first launch
├── README.md
├── .gitignore
└── presentation/
    └── RailNova_Personalized_10_Slides.pptx
```

## 🎓 Academic Project

**Project:** RailNova — Train Booking & Journey Companion  
**Prepared by:** G Suresh Reddy  
**Program:** B.Tech — CSE (Cybersecurity)  
**Course context:** Advanced Programming Practice — Tkinter project

The 10-slide presentation covers the project overview, GUI modules, booking workflow, ticket management, journey timer, technology stack and conclusion. It uses the same neon visual direction and includes project-output screenshot designs.

## ⚠️ Important Demo Limitations

RailNova is an **educational prototype**, not a live railway reservation service.

- It is **not connected to IRCTC** or any live railway API.
- Train names, schedules, availability, fares, PNRs, coach names and seat labels are demonstration data.
- No real ticket is issued and no payment is processed.
- The journey timer uses the computer's local clock and the selected demo journey date/time.

## 🔭 Future Scope

- Connect to an authorized live railway information API
- Add user profiles and authentication
- Use verified schedules and availability
- Add secure payment integration for a production system
- Add notifications and printable ticket exports

---

<div align="center">

**RAILNOVA** · *Journey, Reimagined* ✦

</div>

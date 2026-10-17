<div align="center">

# 🚆 RAILNOVA
### Train Booking & Journey Companion

**Plan your route. Organize your tickets. Track your next departure.**

A neon-inspired desktop train-booking demo built with **Python, Tkinter, and SQLite**.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-00D9FF?style=for-the-badge)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Project](https://img.shields.io/badge/Project-Academic_Demo-8A2BE2?style=for-the-badge)

</div>

---

## ✨ About RailNova

RailNova is a desktop GUI project designed to bring train search, demo ticket booking, ticket management, sample station departures, and journey countdowns into one interface. It uses a dark, neon-inspired visual theme with cyan and magenta accents.

This project demonstrates practical **Tkinter GUI design, event handling, modular navigation, local persistence, and date/time logic**.

## 🌌 Features

| Module | What it does |
|---|---|
| **Overview Dashboard** | Booking overview, upcoming journeys, cancellation summary, spend summary, and quick route search |
| **Book Tickets** | Enter origin, destination, journey date, class, and passenger count; browse sample services and enter passenger names |
| **My Tickets** | View saved demo bookings, PNR, route, passenger details, coach/seat labels, class, and estimated fare |
| **Incoming Trains** | Browse sample services by station with scheduled departure and arrival times |
| **Upcoming Journeys** | Review non-cancelled journeys scheduled for today or a future date |
| **Cancelled Tickets** | Keep cancelled demo tickets in a separate history |
| **Journey Timer** | Live per-second countdown to a selected saved journey departure |
| **Train Explorer** | Filter sample timetable data by train number, name, route, or service type |
| **Help & About** | Project information, technologies, workflow, and limitations |

## 🧰 Technology Stack

- **Python 3** — application logic
- **Tkinter and ttk** — desktop interface, widgets, dialogs, and tables
- **Tkinter Canvas** — drawn visual elements and UI animation
- **SQLite** — persistent local booking storage
- **datetime** — journey-date validation and departure countdown

No additional `pip` packages are required on a standard Windows Python installation that includes Tkinter.

## 🚀 Run Locally

1. Download or clone this repository.
2. Open the project folder in VS Code or a terminal.
3. Run:

   ```bash
   py main.py
   ```

   On systems where `py` is unavailable, try:

   ```bash
   python main.py
   ```

The application creates its local SQLite database automatically when launched.

## 🗂️ Project Structure

```text
RailNova-Train-Booking-System/
├── main.py
├── README.md
├── .gitignore
├── screenshots/
│   ├── overview.png
│   ├── booking.png
│   ├── incoming-trains.png
│   └── help-about.png
└── presentation/
    └── RailNova_Personalized_10_Slides.pptx
```

## 🖼️ Application Screenshots

Screenshots from the project output are included in the `screenshots/` directory. They show the overview dashboard, booking/train results, incoming train list, and Help & About page.

## 🎓 Academic Project

**Project:** RailNova — Train Booking & Journey Companion  
**Prepared by:** G Suresh Reddy  
**Program:** B.Tech — CSE (Cybersecurity)  
**Course context:** Advanced Programming Practice — Tkinter project

The accompanying PowerPoint contains 10 slides covering the overview, GUI modules, booking workflow, ticket management, countdown feature, technology stack, and conclusion.

## ⚠️ Important Demo Limitations

RailNova is an **educational prototype**, not a live railway reservation service.

- It is **not connected to IRCTC** or any live railway API.
- Train schedules, fares, availability, PNRs, coach names, and seat labels are demonstration data.
- No real ticket is issued and no payment is processed.
- The countdown uses the local computer clock and the saved demo journey date/time.

## 🔭 Future Scope

- Integration with an authorized live train information API
- Real user authentication and booking profiles
- Live availability and verified schedules
- Secure payment gateway integration for a production implementation
- Notifications and printable ticket exports

---

<div align="center">

**RAILNOVA** · *Journey, Reimagined* ✦

</div>
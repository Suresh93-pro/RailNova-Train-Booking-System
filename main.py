"""
RAILNOVA — Animated Train Booking & Journey Companion
Python 3.10+ | Tkinter + SQLite (standard library only)
Run: python main.py
Demo booking system for academic use. Train availability/fares are sample data, not live railway data.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, os, random, math, uuid
from datetime import datetime, date, timedelta

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "railnova.db")
BG = "#060B1D"
INK = "#111A2E"
MUTED = "#A7B4CC"
BLUE = "#315EF7"
CYAN = "#37C8D0"
PURPLE = "#8764F8"
PINK = "#FF779A"
WHITE = "#0D1732"
GREEN = "#20A779"
RED = "#E65368"
GOLD = "#F4B942"

TRAIN_DATA = [
    ("12603", "Hyderabad Express", "Chennai Central", "Hyderabad Deccan", "06:15", "14:20", 485, "Daily", "Superfast"),
    ("12604", "Charminar Express", "Chennai Central", "Hyderabad Deccan", "18:10", "06:45", 620, "Daily", "Express"),
    ("12760", "Charminar SF", "Hyderabad Deccan", "Chennai Central", "18:30", "07:05", 640, "Daily", "Superfast"),
    ("12657", "Bengaluru Mail", "Chennai Central", "Bengaluru City", "22:50", "05:45", 410, "Daily", "Mail"),
    ("12028", "Shatabdi Express", "Chennai Central", "Bengaluru City", "06:00", "10:55", 890, "Daily", "Shatabdi"),
    ("12609", "Mysuru Express", "Chennai Central", "Mysuru Junction", "13:35", "22:10", 525, "Daily", "Express"),
    ("12727", "Godavari Express", "Hyderabad Deccan", "Visakhapatnam", "17:15", "06:30", 710, "Daily", "Superfast"),
    ("12723", "Telangana Express", "Hyderabad Deccan", "New Delhi", "06:00", "10:40", 990, "Daily", "Superfast"),
    ("12625", "Kerala Express", "Chennai Central", "Thiruvananthapuram", "11:00", "07:15", 1050, "Daily", "Express"),
    ("12840", "Coromandel Express", "Chennai Central", "Howrah Junction", "07:00", "11:55", 920, "Daily", "Superfast"),
    ("12007", "Deccan Queen", "Mumbai CST", "Pune Junction", "17:10", "20:25", 560, "Daily", "Intercity"),
    ("12951", "Mumbai Rajdhani", "Mumbai Central", "New Delhi", "16:35", "08:30", 1850, "Daily", "Rajdhani"),
    ("12616", "Grand Trunk Express", "Chennai Central", "New Delhi", "18:40", "06:35", 1150, "Daily", "Superfast"),
    ("12785", "Kacheguda Express", "Hyderabad Deccan", "Bengaluru City", "18:20", "07:00", 720, "Daily", "Express"),
    ("12163", "Chennai Express", "Mumbai CST", "Chennai Central", "20:30", "19:15", 880, "Daily", "Superfast"),
]
STATIONS = sorted({x[2] for x in TRAIN_DATA} | {x[3] for x in TRAIN_DATA} | {
    "Vijayawada Junction", "Tirupati", "Coimbatore Junction", "Madurai Junction",
    "Kochi", "Pune Junction", "Ahmedabad Junction", "Kolkata", "Lucknow", "Jaipur",
    "Secunderabad Junction", "Visakhapatnam", "Warangal", "Nellore"
})
CLASSES = {"Sleeper": 1.0, "AC 3 Tier": 2.0, "AC 2 Tier": 3.0, "AC First Class": 4.2, "Chair Car": 1.35, "Executive Chair": 2.8}

class RailDB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT, pnr TEXT UNIQUE, train_no TEXT, train_name TEXT,
            origin TEXT, destination TEXT, journey_date TEXT, depart TEXT, arrive TEXT,
            travel_class TEXT, passengers INTEGER, passenger_names TEXT, total_fare REAL,
            status TEXT, created_at TEXT, coach TEXT, seats TEXT)""")
        self.conn.commit()
    def all(self, status=None):
        if status:
            return self.conn.execute("SELECT * FROM bookings WHERE status=? ORDER BY journey_date, depart", (status,)).fetchall()
        return self.conn.execute("SELECT * FROM bookings ORDER BY created_at DESC").fetchall()
    def add(self, d):
        pnr = str(random.randint(1000000000, 9999999999))
        coach = random.choice(["S1", "S2", "S3", "B1", "B2", "A1", "C1"])
        seats = ", ".join(f"{coach}/{random.randint(1,72)}" for _ in range(d["passengers"]))
        self.conn.execute("""INSERT INTO bookings(pnr,train_no,train_name,origin,destination,journey_date,depart,arrive,travel_class,passengers,passenger_names,total_fare,status,created_at,coach,seats)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (pnr,d["train_no"],d["train_name"],d["origin"],d["destination"],d["journey_date"],d["depart"],d["arrive"],d["travel_class"],d["passengers"],d["passenger_names"],d["total_fare"],"Upcoming",datetime.now().isoformat(timespec="seconds"),coach,seats))
        self.conn.commit()
        return pnr
    def cancel(self, pnr):
        self.conn.execute("UPDATE bookings SET status='Cancelled' WHERE pnr=?", (pnr,))
        self.conn.commit()
    def close(self): self.conn.close()

class RailNova:
    def __init__(self, root):
        self.root = root
        self.root.title("RAILNOVA | Train Booking & Journey Companion")
        self.root.geometry("1420x900")
        self.root.minsize(1120, 740)
        self.root.configure(bg=BG)
        self.db = RailDB()
        self.page = "Overview"
        self.animation_tick = 0
        self.search_results = []
        self.selected_train = None
        self.countdown_job = None
        self.setup_style()
        self.build_shell()
        self.show_page("Overview")
        self.animate_background()
        self.update_clock()
        self.refresh_counts()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_style(self):
        s = ttk.Style()
        try: s.theme_use("clam")
        except tk.TclError: pass
        s.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground="#EDF3FF", rowheight=34, borderwidth=0, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background="#263553", foreground="#EDF3FF", font=("Segoe UI", 10, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", "#35486D")], foreground=[("selected", INK)])
        s.configure("TCombobox", padding=8, fieldbackground="#101C39", background="#101C39", foreground="#EDF3FF")
        s.configure("TEntry", padding=8, fieldbackground="#101C39", foreground="#EDF3FF")

    def build_shell(self):
        self.shell = tk.Frame(self.root, bg=BG)
        self.shell.pack(fill="both", expand=True)
        self.sidebar = tk.Frame(self.shell, bg="#080D25", width=208, highlightbackground="#153D80", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        logo = tk.Frame(self.sidebar, bg="#080D25")
        logo.pack(fill="x", padx=22, pady=(24, 30))
        tk.Canvas(logo, width=42, height=42, bg="#080D25", highlightthickness=0).pack(side="left")
        cv = logo.winfo_children()[0]
        cv.create_oval(3,3,39,39,fill=BLUE,outline="")
        cv.create_line(8,25,18,15,28,25,36,12,fill="white",width=3,smooth=True)
        name = tk.Frame(logo, bg="#080D25"); name.pack(side="left", padx=10)
        tk.Label(name, text="RAILNOVA", bg="#080D25", fg="white", font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(name, text="JOURNEY, REIMAGINED", bg="#080D25", fg="#A8B7D8", font=("Segoe UI", 7, "bold")).pack(anchor="w", pady=(2,0))
        tk.Label(self.sidebar, text="WORKSPACE", bg="#080D25", fg="#8392B4", font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=24, pady=(0,10))
        self.nav_buttons = {}
        navs = [("Overview","◈"),("Book Tickets","＋"),("My Tickets","▤"),("Incoming Trains","◉"),("Upcoming Journeys","◷"),("Cancelled Tickets","⊘"),("Journey Timer","◴"),("Train Explorer","⌕"),("Help & About","?")]
        for label, icon in navs:
            b = tk.Button(self.sidebar, text=f"  {icon}     {label}", anchor="w", command=lambda n=label:self.show_page(n),
                          bg="#080D25", fg="#C6D0E5", activebackground="#2B3B5E", activeforeground="white",
                          relief="flat", bd=0, padx=17, pady=12, font=("Segoe UI", 10), cursor="hand2")
            b.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[label] = b
        spacer = tk.Frame(self.sidebar, bg="#080D25"); spacer.pack(fill="both", expand=True)
        status = tk.Frame(self.sidebar, bg="#1C2942", padx=13, pady=12); status.pack(fill="x", padx=14, pady=18)
        tk.Label(status, text="●  SYSTEM ONLINE", bg="#1C2942", fg="#62E2B5", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(status, text="Local demo database active", bg="#1C2942", fg="#B8C5DD", font=("Segoe UI", 8)).pack(anchor="w", pady=(5,0))
        self.main = tk.Frame(self.shell, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)
        self.topbar = tk.Frame(self.main, bg="#080D25", height=70, highlightbackground="#174B9B", highlightthickness=1)
        self.topbar.pack(fill="x"); self.topbar.pack_propagate(False)
        self.top_title = tk.Label(self.topbar, text="RAILNOVA  /  OVERVIEW", bg="#080D25", fg="#F4F7FF", font=("Segoe UI", 13, "bold"))
        self.top_title.pack(side="left", padx=18)
        self.quicknav = tk.Frame(self.topbar, bg="#080D25")
        self.quicknav.pack(side="left", padx=10)
        for nav_label in ["Book Tickets", "My Tickets", "Incoming Trains", "Upcoming Journeys", "Cancelled Tickets", "Journey Timer", "Train Explorer"]:
            short = {"Book Tickets":"Book","My Tickets":"My Tickets","Incoming Trains":"Incoming","Upcoming Journeys":"Upcoming","Cancelled Tickets":"Cancelled","Journey Timer":"Journey Timer","Train Explorer":"Explorer"}[nav_label]
            b = tk.Button(self.quicknav, text=short, command=lambda n=nav_label:self.show_page(n), bg="#101C42", fg="#DCE8FF",
                          activebackground="#223B79", activeforeground="white", relief="flat", bd=0,
                          font=("Segoe UI", 9, "bold"), padx=10, pady=8, cursor="hand2",
                          highlightbackground="#164C9B", highlightthickness=1)
            b.pack(side="left", padx=3, pady=12)
        self.clock_label = tk.Label(self.topbar, text="", bg="#080D25", fg="#7CE7DE", font=("Segoe UI", 9, "bold"))
        self.clock_label.pack(side="right", padx=16)
        self.page_area = tk.Frame(self.main, bg=BG)
        self.page_area.pack(fill="both", expand=True)
        self.toast = tk.Label(self.main, text="", bg=INK, fg=WHITE, font=("Segoe UI", 10, "bold"), padx=16, pady=10)

    def card(self, parent, bg=WHITE, radius=0, padx=18, pady=16):
        f = tk.Frame(parent, bg=bg, highlightbackground="#2B3852", highlightthickness=1)
        return f
    def label(self, parent, text, size=10, color=INK, bold=False, bg=None, **kw):
        return tk.Label(parent, text=text, font=("Segoe UI", size, "bold" if bold else "normal"), fg=color, bg=bg or parent.cget("bg"), **kw)
    def button(self, parent, text, command, bg=BLUE, fg=WHITE, padx=16, pady=10, **kw):
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
                         relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 10, "bold"), padx=padx, pady=pady, **kw)
    def entry(self, parent, var=None, width=22):
        e = ttk.Entry(parent, textvariable=var, width=width, font=("Segoe UI", 10))
        return e
    def field(self, parent, title, widget, row, col, colspan=1):
        self.label(parent, title.upper(), 8, MUTED, True, bg=parent.cget("bg")).grid(row=row*2, column=col, columnspan=colspan, sticky="w", padx=8, pady=(8,3))
        widget.grid(row=row*2+1, column=col, columnspan=colspan, sticky="ew", padx=8, pady=(0,7))
    def clear_page(self):
        for w in self.page_area.winfo_children(): w.destroy()
    def show_page(self, name):
        self.page = name
        self.top_title.config(text=name)
        for n,b in self.nav_buttons.items():
            b.config(bg="#31466D" if n==name else "#17233D", fg="white" if n==name else "#C6D0E5")
        self.clear_page()
        funcs = {"Overview":self.page_overview,"Book Tickets":self.page_book,"My Tickets":self.page_tickets,
                 "Incoming Trains":self.page_incoming,"Upcoming Journeys":self.page_upcoming,
                 "Cancelled Tickets":self.page_cancelled,"Journey Timer":self.page_timer,
                 "Train Explorer":self.page_explorer,"Help & About":self.page_help}
        funcs.get(name,self.page_overview)()
    def scroll_area(self, parent=None):
        outer = tk.Frame(parent or self.page_area, bg=BG)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
        bar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window_id, width=max(e.width, 900)))
        canvas.configure(yscrollcommand=bar.set)
        canvas.pack(side="left", fill="both", expand=True); bar.pack(side="right", fill="y")
        return inner
    def hero(self, parent, title, subtitle, accent=BLUE):
        f = tk.Frame(parent, bg="#050B24", height=170, highlightbackground="#174C9D", highlightthickness=1)
        f.pack(fill="x", padx=14, pady=(14,14)); f.pack_propagate(False)
        c = tk.Canvas(f, bg="#050B24", height=170, highlightthickness=0)
        c.place(relwidth=1, relheight=1)
        # layered neon atmosphere, city silhouettes and a luminous rail corridor
        c.create_oval(590,-120,980,250, fill="#101E55", outline="")
        c.create_oval(700,-100,1080,260, fill="#11164A", outline="")
        for i in range(18):
            x=590+i*34
            h=22+((i*31)%72)
            c.create_rectangle(x,110-h,x+18,130,fill="#0A1536",outline="#142A63")
            for yy in range(118-h+8,122,12):
                c.create_rectangle(x+5,yy,x+8,yy+3,fill="#1D4F9A",outline="")
        for i in range(5):
            c.create_line(610+i*12,148,880+i*30,100,fill="#123D95",width=2)
        c.create_line(620,154,1090,154,fill="#1748A6",width=2)
        c.create_line(660,159,1110,159,fill="#D52CFF",width=2)
        # stylized futuristic train silhouette
        c.create_polygon(710,122,750,91,820,83,884,101,916,129,908,143,705,143,
                         fill="#0B2E70",outline="#1EDBFF",width=2)
        c.create_polygon(755,96,817,88,861,103,876,121,750,121,fill="#142B67",outline="#38DFFF",width=2)
        c.create_polygon(817,90,860,104,875,121,817,121,fill="#5F8FFF",outline="#C5F9FF",width=1)
        for x in [735,765,795,825,855]:
            c.create_oval(x,132,x+12,144,fill="#061126",outline="#38DFFF",width=2)
        c.create_line(720,127,898,127,fill="#FF36E8",width=3)
        c.create_oval(893,123,902,132,fill="#E6FFFF",outline="#FF3DF0",width=2)
        # animated glints are redrawn by animate_background
        for x,y in [(640,36),(690,62),(900,30),(1020,48),(950,88)]:
            c.create_oval(x,y,x+4,y+4,fill="#58F4FF",outline="")
        c.create_text(24,51,text=title,anchor="w",fill="#F6F8FF",font=("Segoe UI",22,"bold"))
        c.create_text(26,87,text=subtitle,anchor="w",fill="#C3D8FF",font=("Segoe UI",10))
        c.create_text(27,125,text="✦  SMART ROUTES   •   SECURE BOOKINGS   •   LIVE COUNTDOWN",
                      anchor="w",fill="#53EFFF",font=("Segoe UI",8,"bold"))
        c.create_line(20,145,510,145,fill="#143F83",width=1)
        return f
    def stat_card(self, parent, title, value, sub, accent):
        f = tk.Frame(parent, bg=WHITE, highlightbackground="#2B3852", highlightthickness=1, padx=17, pady=14)
        tk.Frame(f, bg=accent, width=4).pack(side="left", fill="y", padx=(0,13))
        right = tk.Frame(f,bg=WHITE); right.pack(side="left",fill="both",expand=True)
        self.label(right,title,9,MUTED,True,bg=WHITE).pack(anchor="w")
        self.label(right,value,23,"#EDF3FF",True,bg=WHITE).pack(anchor="w",pady=(5,2))
        self.label(right,sub,8,MUTED,bg=WHITE).pack(anchor="w")
        return f
    def page_overview(self):
        inner = self.scroll_area()
        self.hero(inner, "Every journey starts here.", "Book smarter. Track your train. Keep every ticket in one beautiful place.", CYAN)
        bookings = self.db.all()
        upcoming = [b for b in bookings if b["status"]=="Upcoming" and b["journey_date"]>=date.today().isoformat()]
        cancelled = [b for b in bookings if b["status"]=="Cancelled"]
        total = sum(b["total_fare"] for b in bookings if b["status"]!="Cancelled")
        stats=tk.Frame(inner,bg=BG); stats.pack(fill="x",padx=24,pady=(0,18))
        for i,(t,v,s,a) in enumerate([("TOTAL BOOKINGS",str(len(bookings)),"All saved tickets",BLUE),("UPCOMING JOURNEYS",str(len(upcoming)),"Ready for departure",CYAN),("CANCELLED TICKETS",str(len(cancelled)),"Kept for your records",PINK),("TRAVEL SPEND",f"₹{total:,.0f}","Non-cancelled bookings",PURPLE)]):
            self.stat_card(stats,t,v,s,a).grid(row=0,column=i,sticky="nsew",padx=(0 if i==0 else 8,0))
            stats.grid_columnconfigure(i,weight=1)
        panel=tk.Frame(inner,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1)
        panel.pack(fill="x",padx=24,pady=(0,16))
        top=tk.Frame(panel,bg=WHITE);top.pack(fill="x",padx=20,pady=(16,10))
        self.label(top,"Find your next connection",14,"#EDF3FF",True,bg=WHITE).pack(side="left")
        self.button(top,"＋  New booking",lambda:self.show_page("Book Tickets"),bg=BLUE).pack(side="right")
        form=tk.Frame(panel,bg=WHITE);form.pack(fill="x",padx=12,pady=(0,14))
        self.from_var=tk.StringVar(value="Chennai Central"); self.to_var=tk.StringVar(value="Hyderabad Deccan")
        self.date_var=tk.StringVar(value=(date.today()+timedelta(days=1)).isoformat())
        self.class_var=tk.StringVar(value="Sleeper"); self.pax_var=tk.StringVar(value="1")
        self.field(form,"From",ttk.Combobox(form,textvariable=self.from_var,values=STATIONS,state="normal"),0,0)
        self.field(form,"To",ttk.Combobox(form,textvariable=self.to_var,values=STATIONS,state="normal"),0,1)
        self.field(form,"Journey date (YYYY-MM-DD)",self.entry(form,self.date_var,16),0,2)
        self.field(form,"Class",ttk.Combobox(form,textvariable=self.class_var,values=list(CLASSES),state="readonly"),0,3)
        self.field(form,"Passengers",ttk.Combobox(form,textvariable=self.pax_var,values=[str(i) for i in range(1,7)],state="readonly"),0,4)
        self.button(form,"Search trains  →",self.search_from_dashboard,bg=INK).grid(row=1,column=5,rowspan=2,padx=8,pady=8,sticky="nsew")
        for i in range(6): form.grid_columnconfigure(i,weight=1)
        lower=tk.Frame(inner,bg=BG);lower.pack(fill="x",padx=24,pady=(0,24))
        left=tk.Frame(lower,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1);left.pack(side="left",fill="both",expand=True,padx=(0,10))
        tk.Label(left,text="YOUR NEXT DEPARTURE",bg=WHITE,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w",padx=18,pady=(16,7))
        if upcoming:
            b=upcoming[0]
            tk.Label(left,text=f"{b['origin']}   →   {b['destination']}",bg=WHITE,fg="#EDF3FF",font=("Segoe UI",15,"bold")).pack(anchor="w",padx=18)
            tk.Label(left,text=f"{b['train_no']} · {b['train_name']}   •   {b['journey_date']} at {b['depart']}",bg=WHITE,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",padx=18,pady=(6,12))
            self.button(left,"Open journey timer  ◷",lambda:self.show_page("Journey Timer"),bg="#263553",fg=BLUE).pack(anchor="w",padx=18,pady=(0,16))
        else:
            tk.Label(left,text="Your next adventure is waiting.",bg=WHITE,fg="#EDF3FF",font=("Segoe UI",14,"bold")).pack(anchor="w",padx=18,pady=(5,5))
            tk.Label(left,text="Book a ticket to see your journey details here.",bg=WHITE,fg=MUTED,font=("Segoe UI",10)).pack(anchor="w",padx=18,pady=(0,14))
        right=tk.Frame(lower,bg="#172E3B",highlightbackground="#28545A",highlightthickness=1,width=300);right.pack(side="left",fill="y");right.pack_propagate(False)
        tk.Label(right,text="✦  RAILNOVA TIP",bg="#172E3B",fg="#178F83",font=("Segoe UI",9,"bold")).pack(anchor="w",padx=17,pady=(16,8))
        tk.Label(right,text="Keep your PNR handy.",bg="#172E3B",fg="#EDF3FF",font=("Segoe UI",14,"bold")).pack(anchor="w",padx=17)
        tk.Label(right,text="Open My Tickets to review passenger names, coach, seat numbers, fare and booking status.",bg="#172E3B",fg="#B4D3D7",wraplength=255,justify="left",font=("Segoe UI",10)).pack(anchor="w",padx=17,pady=(7,15))
    def search_from_dashboard(self):
        self.show_page("Book Tickets")
        self.from_box.set(self.from_var.get()); self.to_box.set(self.to_var.get())
        self.journey_date.set(self.date_var.get()); self.class_box.set(self.class_var.get()); self.passengers.set(self.pax_var.get())
        self.search_trains()

    def page_book(self):
        inner=self.scroll_area()
        self.hero(inner,"Book your next adventure","Choose a route, compare sample services, then save a ticket to your local journey wallet.",PURPLE)
        panel=tk.Frame(inner,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1);panel.pack(fill="x",padx=24,pady=(0,16))
        tk.Label(panel,text="TRIP DETAILS",bg=WHITE,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w",padx=18,pady=(16,0))
        form=tk.Frame(panel,bg=WHITE);form.pack(fill="x",padx=10,pady=8)
        self.from_box=ttk.Combobox(form,values=STATIONS,state="normal")
        self.to_box=ttk.Combobox(form,values=STATIONS,state="normal")
        self.journey_date=tk.StringVar(value=(date.today()+timedelta(days=1)).isoformat())
        self.class_box=ttk.Combobox(form,values=list(CLASSES),state="readonly");self.class_box.set("Sleeper")
        self.passengers=tk.StringVar(value="1")
        self.field(form,"From station",self.from_box,0,0)
        self.field(form,"To station",self.to_box,0,1)
        self.field(form,"Journey date",self.entry(form,self.journey_date),0,2)
        self.field(form,"Travel class",self.class_box,0,3)
        self.field(form,"Passengers",ttk.Combobox(form,textvariable=self.passengers,values=[str(i) for i in range(1,7)],state="readonly"),0,4)
        self.button(form,"Find trains  →",self.search_trains,bg=BLUE).grid(row=1,column=5,rowspan=2,padx=8,pady=8,sticky="nsew")
        for i in range(6):form.grid_columnconfigure(i,weight=1)
        self.label(inner,"Available sample services",14,"#EDF3FF",True,bg=BG).pack(anchor="w",padx=24,pady=(4,10))
        self.results_frame=tk.Frame(inner,bg=BG);self.results_frame.pack(fill="both",expand=True,padx=24,pady=(0,24))
        self.search_trains()

    def search_trains(self):
        origin=self.from_box.get().strip(); dest=self.to_box.get().strip(); d=self.journey_date.get().strip()
        try: date.fromisoformat(d)
        except ValueError:
            messagebox.showerror("Check journey date","Enter the date as YYYY-MM-DD, for example 2026-10-18.");return
        if not origin or not dest or origin.lower()==dest.lower():
            messagebox.showwarning("Route needed","Choose different From and To stations.");return
        for w in self.results_frame.winfo_children():w.destroy()
        matched=[t for t in TRAIN_DATA if t[2].lower()==origin.lower() and t[3].lower()==dest.lower()]
        # If no direct seeded route, offer a demo route so the UI remains useful for entered stations.
        if not matched:
            matched=[(f"{random.randint(12000,12999)}","RailNova Intercity",origin,dest,"08:30","16:45",560,"Daily","Demo Express")]
        self.search_results=matched
        if date.fromisoformat(d)<date.today():
            self.label(self.results_frame,"This date is in the past. You can still inspect sample trains, but booking is disabled.",10,RED,bg=BG).pack(anchor="w",pady=8)
        for t in matched:
            f=tk.Frame(self.results_frame,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1);f.pack(fill="x",pady=6)
            left=tk.Frame(f,bg=WHITE);left.pack(side="left",fill="both",expand=True,padx=17,pady=14)
            self.label(left,f"{t[0]}  ·  {t[1]}",13,"#EDF3FF",True,bg=WHITE).pack(anchor="w")
            route=tk.Frame(left,bg=WHITE);route.pack(anchor="w",pady=(12,5))
            self.label(route,t[2],10,"#EDF3FF",True,bg=WHITE).pack(side="left")
            self.label(route,f"  ━━━━━●━━━━━  {t[3]}",10,BLUE,True,bg=WHITE).pack(side="left",padx=10)
            self.label(left,f"Departure {t[4]}     Arrival {t[5]}     •     {t[7]}     •     {t[8]}",9,MUTED,bg=WHITE).pack(anchor="w",pady=(3,0))
            right=tk.Frame(f,bg=WHITE);right.pack(side="right",padx=18,pady=12)
            fare=round(t[6]*CLASSES.get(self.class_box.get(),1.0)*int(self.passengers.get() or "1"))
            self.label(right,"TOTAL ESTIMATED FARE",8,MUTED,True,bg=WHITE).pack(anchor="e")
            self.label(right,f"₹{fare:,}",19,"#EDF3FF",True,bg=WHITE).pack(anchor="e",pady=(3,7))
            self.button(right,"Select & enter passengers",lambda train=t:self.booking_dialog(train),bg=BLUE,padx=12,pady=8).pack(anchor="e")
    def booking_dialog(self, train):
        d=self.journey_date.get().strip()
        if date.fromisoformat(d)<date.today():
            messagebox.showwarning("Past date","Choose today or a future date.");return
        win=tk.Toplevel(self.root);win.title("Passenger details | RailNova");win.geometry("610x650");win.configure(bg=BG);win.transient(self.root);win.grab_set()
        head=tk.Frame(win,bg=INK,pady=18);head.pack(fill="x")
        tk.Label(head,text="Complete your booking",bg=INK,fg=WHITE,font=("Segoe UI",18,"bold")).pack(anchor="w",padx=22)
        tk.Label(head,text=f"{train[0]} · {train[1]}   |   {train[2]} → {train[3]}",bg=INK,fg="#C5D2ED",font=("Segoe UI",10)).pack(anchor="w",padx=22,pady=(5,0))
        body=tk.Frame(win,bg=BG,padx=22,pady=18);body.pack(fill="both",expand=True)
        pax=max(1,min(6,int(self.passengers.get() or 1)))
        namevars=[]
        for i in range(pax):
            self.label(body,f"Passenger {i+1} full name",9,MUTED,True,bg=BG).pack(anchor="w",pady=(7,3))
            v=tk.StringVar();self.entry(body,v,55).pack(fill="x");namevars.append(v)
        cls=self.class_box.get() or "Sleeper"
        total=round(train[6]*CLASSES.get(cls,1)*pax)
        tk.Label(body,text=f"Class: {cls}     •     Date: {d}     •     Estimated total: ₹{total:,}",bg=BG,fg="#EDF3FF",font=("Segoe UI",11,"bold")).pack(anchor="w",pady=15)
        tk.Label(body,text="Demo project: no real railway reservation or payment is performed.",bg=BG,fg=RED,font=("Segoe UI",9)).pack(anchor="w")
        def confirm():
            names=[v.get().strip() for v in namevars]
            if any(not n for n in names):
                messagebox.showwarning("Passenger names","Enter a name for every passenger.",parent=win);return
            data={"train_no":train[0],"train_name":train[1],"origin":train[2],"destination":train[3],"journey_date":d,"depart":train[4],"arrive":train[5],"travel_class":cls,"passengers":pax,"passenger_names":", ".join(names),"total_fare":total}
            pnr=self.db.add(data);win.destroy();self.refresh_counts()
            messagebox.showinfo("Booking confirmed",f"Your demo ticket is saved!\n\nPNR: {pnr}\nTrain: {train[0]} — {train[1]}\nRoute: {train[2]} → {train[3]}\nDate: {d}\nEstimated fare: ₹{total:,}\n\nOpen My Tickets to view or cancel it.")
            self.show_page("My Tickets")
        self.button(body,"Confirm demo booking  ✓",confirm,bg=GREEN).pack(fill="x",pady=(16,0))

    def ticket_table(self,parent,rows,show_actions=True):
        wrap=tk.Frame(parent,bg=BG);wrap.pack(fill="both",expand=True,padx=24,pady=(0,20))
        cols=("pnr","date","train","route","depart","class","passengers","fare","status")
        tree=ttk.Treeview(wrap,columns=cols,show="headings",height=12)
        headers={"pnr":"PNR","date":"Journey date","train":"Train","route":"From → To","depart":"Departs","class":"Class","passengers":"Pax","fare":"Fare","status":"Status"}
        widths={"pnr":105,"date":105,"train":190,"route":270,"depart":70,"class":105,"passengers":45,"fare":85,"status":90}
        for c in cols:tree.heading(c,text=headers[c]);tree.column(c,width=widths[c],anchor="w")
        for b in rows:
            tree.insert("", "end", iid=str(b["pnr"]), values=(b["pnr"],b["journey_date"],f"{b['train_no']} · {b['train_name']}",f"{b['origin']} → {b['destination']}",b["depart"],b["travel_class"],b["passengers"],f"₹{b['total_fare']:,.0f}",b["status"]))
        tree.pack(fill="both",expand=True)
        actions=tk.Frame(wrap,bg=BG);actions.pack(fill="x",pady=10)
        def selected():
            ids=tree.selection()
            if not ids:messagebox.showinfo("Select a ticket","Select a ticket row first.");return None
            return ids[0]
        self.button(actions,"View ticket details",lambda:self.ticket_detail(selected()),bg=BLUE).pack(side="left",padx=(0,8))
        if show_actions:
            def cancel():
                p=selected()
                if not p:return
                row=next((b for b in rows if b["pnr"]==p),None)
                if row and row["status"]=="Cancelled":messagebox.showinfo("Already cancelled","This ticket is already cancelled.");return
                if messagebox.askyesno("Cancel ticket",f"Cancel demo ticket PNR {p}?\nThis updates the local record only."):
                    self.db.cancel(p);self.refresh_counts();self.show_page(self.page)
                    messagebox.showinfo("Ticket cancelled","The ticket is now listed under Cancelled Tickets.")
            self.button(actions,"Cancel selected ticket",cancel,bg="#3B2437",fg=RED).pack(side="left")
        return tree
    def ticket_detail(self,pnr):
        if not pnr:return
        b=self.db.conn.execute("SELECT * FROM bookings WHERE pnr=?",(pnr,)).fetchone()
        if not b:return
        win=tk.Toplevel(self.root);win.title("Ticket details");win.geometry("560x570");win.configure(bg=BG)
        tk.Frame(win,bg=BLUE,height=7).pack(fill="x")
        card=tk.Frame(win,bg=WHITE,highlightbackground="#34415B",highlightthickness=1,padx=25,pady=22);card.pack(fill="both",expand=True,padx=22,pady=22)
        tk.Label(card,text="RAILNOVA  /  E-TICKET",bg=WHITE,fg=BLUE,font=("Segoe UI",10,"bold")).pack(anchor="w")
        tk.Label(card,text=f"{b['origin']}  →  {b['destination']}",bg=WHITE,fg="#EDF3FF",font=("Segoe UI",18,"bold")).pack(anchor="w",pady=(12,4))
        tk.Label(card,text=f"{b['train_no']} · {b['train_name']}",bg=WHITE,fg=MUTED,font=("Segoe UI",11)).pack(anchor="w")
        tk.Frame(card,bg="#34415B",height=1).pack(fill="x",pady=16)
        details=[("PNR",b["pnr"]),("JOURNEY DATE",b["journey_date"]),("DEPARTURE / ARRIVAL",f"{b['depart']} / {b['arrive']}"),("CLASS",b["travel_class"]),("PASSENGERS",b["passenger_names"]),("COACH / SEATS",f"{b['coach']} · {b['seats']}"),("TOTAL FARE",f"₹{b['total_fare']:,.0f}"),("STATUS",b["status"])]
        for k,v in details:
            row=tk.Frame(card,bg=WHITE);row.pack(fill="x",pady=4)
            tk.Label(row,text=k,bg=WHITE,fg=MUTED,font=("Segoe UI",8,"bold"),width=20,anchor="w").pack(side="left")
            tk.Label(row,text=str(v),bg=WHITE,fg="#EDF3FF",font=("Segoe UI",9,"bold"),wraplength=300,justify="left").pack(side="left")
        self.button(card,"Close ticket",win.destroy,bg=INK).pack(anchor="e",pady=(16,0))
    def page_tickets(self):
        self.hero(self.page_area,"My Tickets","Your complete booking wallet: PNRs, passengers, seat details, fares and status.",BLUE)
        self.ticket_table(self.page_area,self.db.all(),True)
    def page_upcoming(self):
        self.hero(self.page_area,"Upcoming journeys","Everything you have booked and have not cancelled yet.",CYAN)
        rows=[b for b in self.db.all() if b["status"]=="Upcoming" and b["journey_date"]>=date.today().isoformat()]
        if not rows:self.label(self.page_area,"No upcoming journeys yet. Book a trip and it will appear here.",11,MUTED,bg=BG).pack(anchor="w",padx=24,pady=12)
        self.ticket_table(self.page_area,rows,True)
    def page_cancelled(self):
        self.hero(self.page_area,"Cancelled tickets","A transparent history of demo tickets you cancelled.",PINK)
        rows=self.db.all("Cancelled")
        if not rows:self.label(self.page_area,"No cancelled tickets. Your history will appear here if you cancel a booking.",11,MUTED,bg=BG).pack(anchor="w",padx=24,pady=12)
        self.ticket_table(self.page_area,rows,False)
    def page_incoming(self):
        self.hero(self.page_area,"Incoming trains","Explore the next sample departures from your selected station.",PURPLE)
        panel=tk.Frame(self.page_area,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1);panel.pack(fill="x",padx=24,pady=(0,15))
        self.label(panel,"Select station",10,MUTED,True,bg=WHITE).pack(side="left",padx=15,pady=15)
        station=tk.StringVar(value="Chennai Central")
        box=ttk.Combobox(panel,textvariable=station,values=STATIONS,width=32);box.pack(side="left",padx=8,pady=12)
        area=tk.Frame(self.page_area,bg=BG);area.pack(fill="both",expand=True,padx=24)
        def render(*_):
            for w in area.winfo_children():w.destroy()
            matches=[t for t in TRAIN_DATA if t[2].lower()==station.get().lower() or t[3].lower()==station.get().lower()]
            if not matches:matches=[(f"{random.randint(12000,12999)}","RailNova Regional",station.get(),"Nearby Junction","09:15","12:45",350,"Daily","Demo Local")]
            for t in matches:
                f=tk.Frame(area,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1);f.pack(fill="x",pady=5)
                tk.Label(f,text=f"◉  {t[0]}  {t[1]}",bg=WHITE,fg="#EDF3FF",font=("Segoe UI",12,"bold")).pack(side="left",padx=16,pady=15)
                tk.Label(f,text=f"{t[2]} → {t[3]}",bg=WHITE,fg=MUTED,font=("Segoe UI",10)).pack(side="left",padx=12)
                tk.Label(f,text=f"Dep {t[4]}  •  Arr {t[5]}",bg=WHITE,fg=BLUE,font=("Segoe UI",10,"bold")).pack(side="right",padx=18)
        box.bind("<<ComboboxSelected>>",render);box.bind("<Return>",render);self.button(panel,"Refresh",render,bg=INK,pady=7).pack(side="left",padx=8)
        render()
    def page_timer(self):
        self.hero(self.page_area,"Journey countdown","Choose an upcoming ticket and keep an eye on the time until departure.",CYAN)
        rows=[b for b in self.db.all() if b["status"]=="Upcoming" and b["journey_date"]>=date.today().isoformat()]
        panel=tk.Frame(self.page_area,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1,padx=22,pady=20);panel.pack(fill="x",padx=24,pady=(0,16))
        if not rows:
            self.label(panel,"No upcoming ticket found. Book a ticket first to activate your journey timer.",12,"#EDF3FF",True,bg=WHITE).pack(anchor="w")
            self.button(panel,"Book tickets",lambda:self.show_page("Book Tickets"),bg=BLUE).pack(anchor="w",pady=12);return
        options=[f"{b['pnr']} | {b['journey_date']} {b['depart']} | {b['origin']} → {b['destination']}" for b in rows]
        choice=tk.StringVar(value=options[0])
        self.label(panel,"SELECT YOUR JOURNEY",9,MUTED,True,bg=WHITE).pack(anchor="w")
        combo=ttk.Combobox(panel,textvariable=choice,values=options,state="readonly",width=100);combo.pack(anchor="w",fill="x",pady=(6,16))
        timer=tk.Frame(panel,bg=INK,padx=20,pady=20);timer.pack(fill="x")
        tk.Label(timer,text="TIME UNTIL DEPARTURE",bg=INK,fg="#B9C8E7",font=("Segoe UI",9,"bold")).pack(anchor="w")
        digits=tk.Label(timer,text="--  DAYS   --:--:--",bg=INK,fg="#7CE7DE",font=("Consolas",30,"bold"));digits.pack(anchor="w",pady=(8,4))
        route=tk.Label(timer,text="",bg=INK,fg=WHITE,font=("Segoe UI",11));route.pack(anchor="w")
        reminder=tk.Label(panel,text="Timer uses your computer's local time. Keep this window open for a live countdown.",bg=WHITE,fg=MUTED,font=("Segoe UI",9));reminder.pack(anchor="w",pady=(14,0))
        def tick():
            if not win_exists(timer):return
            b=rows[options.index(choice.get())]
            try: target=datetime.strptime(b["journey_date"]+" "+b["depart"],"%Y-%m-%d %H:%M")
            except ValueError: target=datetime.now()
            delta=target-datetime.now()
            if delta.total_seconds()<=0:
                digits.config(text="DEPARTURE TIME",fg=GOLD)
            else:
                days=delta.days; sec=delta.seconds
                digits.config(text=f"{days:02d} DAYS   {sec//3600:02d}:{(sec%3600)//60:02d}:{sec%60:02d}",fg="#7CE7DE")
            route.config(text=f"{b['train_no']} · {b['train_name']}   |   {b['origin']} → {b['destination']}   |   {b['depart']}")
            self.root.after(1000,tick)
        def win_exists(w):
            try:return bool(w.winfo_exists())
            except tk.TclError:return False
        tick()
        self.button(panel,"View selected ticket",lambda:self.ticket_detail(rows[options.index(choice.get())]["pnr"]),bg=BLUE).pack(anchor="w",pady=(15,0))
    def page_explorer(self):
        self.hero(self.page_area,"Train Explorer","Browse the sample timetable, compare routes and estimated base fares.",PURPLE)
        area=tk.Frame(self.page_area,bg=BG);area.pack(fill="both",expand=True,padx=24,pady=(0,20))
        search=tk.StringVar()
        top=tk.Frame(area,bg=WHITE,padx=12,pady=12);top.pack(fill="x",pady=(0,10))
        self.entry(top,search,45).pack(side="left",fill="x",expand=True,padx=(0,10))
        tk.Label(top,text="Search train, number, origin or destination",bg=WHITE,fg=MUTED,font=("Segoe UI",9)).pack(side="left",padx=8)
        tree=ttk.Treeview(area,columns=("no","name","from","to","dep","arr","fare","type"),show="headings")
        for c,t,w in [("no","Train no.",80),("name","Train name",180),("from","From",175),("to","To",175),("dep","Departs",75),("arr","Arrives",75),("fare","Base fare",90),("type","Service",110)]:
            tree.heading(c,text=t);tree.column(c,width=w,anchor="w")
        tree.pack(fill="both",expand=True)
        def render(*_):
            tree.delete(*tree.get_children())
            q=search.get().lower()
            for t in TRAIN_DATA:
                if not q or any(q in str(x).lower() for x in (t[0],t[1],t[2],t[3],t[8])):
                    tree.insert("","end",values=(t[0],t[1],t[2],t[3],t[4],t[5],f"₹{t[6]}",t[8]))
        search.trace_add("write",render);render()
    def page_help(self):
        self.hero(self.page_area,"The RailNova handbook","A polished academic demo built with Tkinter, SQLite and animated Canvas artwork.",BLUE)
        panel=tk.Frame(self.page_area,bg=WHITE,highlightbackground="#2B3852",highlightthickness=1,padx=24,pady=22);panel.pack(fill="both",expand=True,padx=24,pady=(0,22))
        sections=[
            ("01  BOOKING WORKFLOW","Select From / To, date, travel class and passenger count. Search services, enter passenger names and confirm a demo booking. A unique PNR and seat details are saved."),
            ("02  TICKET MANAGEMENT","My Tickets shows all records. View details to inspect PNR, route, date, passenger names, coach, seat numbers, class, fare and status. Cancelled records remain in Cancelled Tickets."),
            ("03  JOURNEY COUNTDOWN","The Journey Timer counts down to the selected ticket's departure using the computer's local time. It updates every second while the page is open."),
            ("04  DATA STORAGE","SQLite database railnova.db is created automatically in this project folder. Bookings persist when you close and reopen the app."),
            ("05  TECHNOLOGY","Python + Tkinter/ttk for GUI, Canvas for animated visual elements, SQLite for persistence, datetime for journey countdown. No external pip packages are required."),
            ("06  IMPORTANT LIMITATION","This is a college demonstration, not connected to IRCTC or live railway APIs. Trains, fares, timings, availability, PNRs and seats are sample/demo values. It does not issue real tickets or process payments.")
        ]
        for title,body in sections:
            tk.Label(panel,text=title,bg=WHITE,fg=BLUE,font=("Segoe UI",10,"bold")).pack(anchor="w",pady=(10,4))
            tk.Label(panel,text=body,bg=WHITE,fg="#EDF3FF",font=("Segoe UI",10),wraplength=1020,justify="left").pack(anchor="w",pady=(0,7))
        self.button(panel,"Start booking  →",lambda:self.show_page("Book Tickets"),bg=BLUE).pack(anchor="w",pady=(14,0))
    def animate_background(self):
        # A live, gently animated station-window motif in the sidebar brand mark.
        self.animation_tick += 1
        try:
            cv=self.sidebar.winfo_children()[0].winfo_children()[0]
            cv.delete("motion")
            t=self.animation_tick
            x=8+(t%24)
            cv.create_line(x,8,x+5,8,fill="#9FE9F0",width=2,tags="motion")
            cv.create_oval(28,7+(math.sin(t/5)*2),33,12+(math.sin(t/5)*2),outline="#7CE7DE",width=2,tags="motion")
            pulse = "#D946FF" if (t//8)%2 else "#22DFFF"
            for n,b in self.nav_buttons.items():
                if n == self.page:
                    b.config(highlightbackground=pulse, highlightthickness=2, fg="#FFFFFF")
                else:
                    b.config(highlightthickness=0)
            for w in self.quicknav.winfo_children():
                if w.winfo_exists():
                    w.config(highlightbackground=pulse if (t//10)%2 else "#164C9B")
        except (tk.TclError,IndexError,AttributeError): pass
        self.root.after(100,self.animate_background)
    def update_clock(self):
        try:self.clock_label.config(text="●  LOCAL TIME  "+datetime.now().strftime("%a, %d %b %Y   %I:%M:%S %p"))
        except tk.TclError:pass
        self.root.after(1000,self.update_clock)
    def refresh_counts(self): pass
    def on_close(self):
        try:self.db.close()
        except Exception:pass
        self.root.destroy()

def main():
    root=tk.Tk()
    app=RailNova(root)
    root.mainloop()

if __name__=="__main__":
    main()

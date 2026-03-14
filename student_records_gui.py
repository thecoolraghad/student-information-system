import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from student_records import StudentRegistry, Student

# ===========================================================
# BER2013 Algorithm Design and Analysis
# Student Information System — Tkinter GUI
# Team: Tuba Ahmad, Mohammed Tariq, Hamzeh Kareh,
#       Raghd Abdullah, Malak Mohammed Fouad
# ===========================================================

# --- Timetable helpers ---
def time_to_minutes(hhmm: str) -> int:
    hhmm = hhmm.strip()
    if not hhmm: raise ValueError("Empty time")
    if ":" not in hhmm: raise ValueError("Time must be HH:MM")
    h, m = hhmm.split(":", 1)
    h = int(h); m = int(m)
    if not (0 <= h < 24 and 0 <= m < 60): raise ValueError("Time out of range")
    return h * 60 + m

def minutes_to_time(mins: int) -> str:
    h = mins // 60; m = mins % 60
    return f"{h:02d}:{m:02d}"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Records (DSA) — GUI")
        self.geometry("1120x700")
        self.minsize(1000, 640)
        self.reg = StudentRegistry()
        self.reg.load()

        style = ttk.Style()
        try: style.theme_use("clam")
        except Exception: pass

        nb = ttk.Notebook(self)
        self.tab_students  = ttk.Frame(nb)
        self.tab_academics = ttk.Frame(nb)
        self.tab_reports   = ttk.Frame(nb)
        self.tab_bonus     = ttk.Frame(nb)
        nb.add(self.tab_students,  text="Students")
        nb.add(self.tab_academics, text="Academics")
        nb.add(self.tab_reports,   text="Reports")
        nb.add(self.tab_bonus,     text="Bonus")
        nb.pack(fill="both", expand=True)

        self._build_students_tab()
        self._build_academics_tab()
        self._build_reports_tab()
        self._build_bonus_tab()

        self._refresh_student_table()
        self._refresh_catalog_table()

    # ===========================================================
    # Students Tab
    # ===========================================================
    def _build_students_tab(self):
        f = self.tab_students
        form = ttk.LabelFrame(f, text="Add / Remove / Search")
        form.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.sid_var    = tk.StringVar()
        self.name_var   = tk.StringVar()
        self.dept_var   = tk.StringVar()
        self.gender_var = tk.StringVar(value="F")
        self.year_var   = tk.IntVar(value=1)

        row = 0
        ttk.Label(form, text="Student ID").grid(row=row, column=0, sticky="w", padx=6, pady=6)
        ttk.Entry(form, textvariable=self.sid_var, width=28).grid(row=row, column=1, padx=6, pady=6); row += 1
        ttk.Label(form, text="Name").grid(row=row, column=0, sticky="w", padx=6, pady=6)
        ttk.Entry(form, textvariable=self.name_var, width=28).grid(row=row, column=1, padx=6, pady=6); row += 1
        ttk.Label(form, text="Department").grid(row=row, column=0, sticky="w", padx=6, pady=6)
        ttk.Entry(form, textvariable=self.dept_var, width=28).grid(row=row, column=1, padx=6, pady=6); row += 1
        ttk.Label(form, text="Gender").grid(row=row, column=0, sticky="w", padx=6, pady=6)
        ttk.Combobox(form, textvariable=self.gender_var, values=["F", "M"], width=25, state="readonly").grid(row=row, column=1, padx=6, pady=6); row += 1
        ttk.Label(form, text="Year (1–4)").grid(row=row, column=0, sticky="w", padx=6, pady=6)
        tk.Spinbox(form, from_=1, to=4, textvariable=self.year_var, width=5).grid(row=row, column=1, sticky="w", padx=6, pady=6); row += 1

        ttk.Button(form, text="Add Student",   command=self._add_student).grid(row=row, column=0, columnspan=2, sticky="ew", padx=6, pady=(10, 6)); row += 1
        ttk.Button(form, text="Remove by ID",  command=self._remove_student).grid(row=row, column=0, columnspan=2, sticky="ew", padx=6, pady=6); row += 1
        ttk.Button(form, text="Search by ID",  command=self._search_by_id).grid(row=row, column=0, columnspan=2, sticky="ew", padx=6, pady=6); row += 1
        ttk.Button(form, text="Save",          command=self._save).grid(row=row, column=0, columnspan=2, sticky="ew", padx=6, pady=(6, 12))

        table_frame = ttk.Frame(f); table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        cols = ("id", "name", "dept", "gender", "year", "gpa")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=18)
        for c, txt, w, anchor in [("id","Student ID",120,"w"),("name","Name",200,"w"),("dept","Department",120,"w"),("gender","Gender",70,"center"),("year","Year",60,"center"),("gpa","GPA",70,"center")]:
            self.tree.heading(c, text=txt); self.tree.column(c, width=w, anchor=anchor)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        btns = ttk.Frame(table_frame); btns.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(btns, text="Refresh",           command=self._refresh_student_table).pack(side=tk.LEFT, padx=4, pady=6)
        ttk.Button(btns, text="List by Name",      command=self._list_by_name).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="List by Student ID",command=self._list_by_id).pack(side=tk.LEFT, padx=4)
        ttk.Button(btns, text="List by GPA",       command=self._list_by_gpa).pack(side=tk.LEFT, padx=4)

    def _add_student(self):
        try:
            sid = self.sid_var.get().strip()
            if not sid: raise ValueError("Student ID is required.")
            s = Student(student_id=sid, name=self.name_var.get().strip() or "Unnamed",
                        department=self.dept_var.get().strip() or "-",
                        gender=self.gender_var.get().strip() or "F",
                        year=int(self.year_var.get()))
            self.reg.add_student(s); self._refresh_student_table()
            messagebox.showinfo("Added", f"Student {sid} added.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _remove_student(self):
        sid = self.sid_var.get().strip() or self._selected_student_id()
        if not sid: messagebox.showwarning("Select", "Enter or select a Student ID to remove."); return
        try:
            self.reg.remove_student(sid); self._refresh_student_table()
            messagebox.showinfo("Removed", f"Student {sid} removed.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _search_by_id(self):
        sid = self.sid_var.get().strip()
        if not sid: messagebox.showwarning("Input", "Enter a Student ID to search."); return
        s = self.reg.get_by_id(sid)
        if s is None: messagebox.showinfo("Search", "Not found.")
        else:
            info = f"ID: {s.student_id}\nName: {s.name}\nDept: {s.department}\nGender: {s.gender}\nYear: {s.year}\nGPA: {s.gpa()}"
            messagebox.showinfo("Found", info)

    def _save(self):
        try: self.reg.save(); messagebox.showinfo("Saved", "Data & catalog saved.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _fill_table(self, items):
        for i in self.tree.get_children(): self.tree.delete(i)
        for s in items:
            self.tree.insert("", tk.END, values=(s.student_id, s.name, s.department, s.gender, s.year, f"{s.gpa():.2f}"))

    def _refresh_student_table(self): self._fill_table(self.reg.list_students())
    def _list_by_name(self):          self._fill_table(self.reg.sorted_by_name())
    def _list_by_id(self):            self._fill_table(self.reg.sorted_by_id())
    def _list_by_gpa(self):           self._fill_table(self.reg.sorted_by_gpa(descending=True))

    def _selected_student_id(self):
        sel = self.tree.selection()
        if not sel: return ""
        vals = self.tree.item(sel[0], "values")
        return vals[0] if vals else ""

    # ===========================================================
    # Academics Tab
    # ===========================================================
    def _build_academics_tab(self):
        f = self.tab_academics

        frm = ttk.LabelFrame(f, text="Subjects & Grades"); frm.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.sid2_var  = tk.StringVar(); self.subj_var  = tk.StringVar(); self.score_var = tk.StringVar()

        ttk.Label(frm, text="Student ID").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.sid2_var, width=18).grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(frm, text="Subject Code").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.subj_var, width=10).grid(row=0, column=3, padx=6, pady=6)
        ttk.Label(frm, text="Score (0–100)").grid(row=0, column=4, sticky="w", padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.score_var, width=10).grid(row=0, column=5, padx=6, pady=6)

        ttk.Button(frm, text="Enroll",          command=self._enroll_subject).grid(row=1, column=0, columnspan=2, sticky="ew", padx=6, pady=6)
        ttk.Button(frm, text="Drop",            command=self._drop_subject).grid(row=1, column=2, columnspan=2, sticky="ew", padx=6, pady=6)
        ttk.Button(frm, text="Add Grade",       command=self._add_grade).grid(row=1, column=4, columnspan=2, sticky="ew", padx=6, pady=6)
        ttk.Button(frm, text="Undo Last Grade", command=self._undo_grade).grid(row=1, column=6, columnspan=2, sticky="ew", padx=6, pady=6)

        att = ttk.LabelFrame(f, text="Attendance Queue"); att.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.date_var    = tk.StringVar(); self.present_var = tk.BooleanVar(value=True)

        ttk.Label(att, text="Student ID").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        ttk.Entry(att, textvariable=self.sid2_var, width=18).grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(att, text="Subject Code").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        ttk.Entry(att, textvariable=self.subj_var, width=14).grid(row=0, column=3, padx=6, pady=6)
        ttk.Label(att, text="Date (YYYY-MM-DD)").grid(row=0, column=4, sticky="w", padx=6, pady=6)
        ttk.Entry(att, textvariable=self.date_var, width=18).grid(row=0, column=5, padx=6, pady=6)
        ttk.Checkbutton(att, text="Present", variable=self.present_var).grid(row=0, column=6, padx=6, pady=6)
        ttk.Button(att, text="Queue Attendance", command=self._queue_attendance).grid(row=1, column=0, columnspan=3, sticky="ew", padx=6, pady=6)
        ttk.Button(att, text="Process Queue",    command=self._process_attendance).grid(row=1, column=3, columnspan=3, sticky="ew", padx=6, pady=6)

    def _get_student_or_warn(self, sid: str):
        s = self.reg.get_by_id(sid)
        if s is None:
            messagebox.showwarning("Not Found", f"Student {sid} not found.")
            return None
        return s

    def _enroll_subject(self):
        sid, subj = self.sid2_var.get().strip(), self.subj_var.get().strip()
        if not sid or not subj: messagebox.showwarning("Input", "Enter Student ID and Subject Code."); return
        s = self._get_student_or_warn(sid)
        if not s: return
        try: s.enroll_subject(subj); messagebox.showinfo("Enrolled", f"{sid} -> {subj}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _drop_subject(self):
        sid, subj = self.sid2_var.get().strip(), self.subj_var.get().strip()
        if not sid or not subj: messagebox.showwarning("Input", "Enter Student ID and Subject Code."); return
        s = self._get_student_or_warn(sid)
        if not s: return
        try: s.drop_subject(subj); messagebox.showinfo("Dropped", f"{sid} -/-> {subj}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _add_grade(self):
        sid, subj = self.sid2_var.get().strip(), self.subj_var.get().strip()
        if not sid or not subj: messagebox.showwarning("Input", "Enter Student ID and Subject Code."); return
        s = self._get_student_or_warn(sid)
        if not s: return
        try: score = float(self.score_var.get())
        except Exception: messagebox.showwarning("Score", "Enter a valid number (0..100)"); return
        try: s.add_grade(subj, score); messagebox.showinfo("Grade", f"Added {score} to {sid}/{subj}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _undo_grade(self):
        sid = self.sid2_var.get().strip()
        if not sid: messagebox.showwarning("Input", "Enter Student ID."); return
        s = self._get_student_or_warn(sid)
        if not s: return
        try: s.undo_last_grade(); messagebox.showinfo("Undo", "Last grade undone.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _queue_attendance(self):
        sid, subj = self.sid2_var.get().strip(), self.subj_var.get().strip()
        date = self.date_var.get().strip(); present = bool(self.present_var.get())
        if not sid or not subj: messagebox.showwarning("Input", "Enter Student ID and Subject Code."); return
        self.reg.enqueue_attendance(sid, date or str(datetime.date.today()), subj, present)
        messagebox.showinfo("Queued", "Attendance queued. Use 'Process Queue' to apply.")

    def _process_attendance(self):
        try:
            cnt = self.reg.process_attendance()
            messagebox.showinfo("Processed", f"Processed {cnt} attendance record(s).")
        except Exception as e: messagebox.showerror("Error", str(e))

    # ===========================================================
    # Reports Tab
    # ===========================================================
    def _build_reports_tab(self):
        f = self.tab_reports
        top = ttk.Frame(f); top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.report_sid = tk.StringVar()
        ttk.Label(top, text="Student ID").pack(side=tk.LEFT)
        ttk.Entry(top, textvariable=self.report_sid, width=18).pack(side=tk.LEFT, padx=6)
        ttk.Button(top, text="Show Report", command=self._show_report).pack(side=tk.LEFT, padx=6)
        self.report_text = tk.Text(f, height=20)
        self.report_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _show_report(self):
        sid = self.report_sid.get().strip()
        if not sid: messagebox.showwarning("Input", "Enter Student ID."); return
        s = self.reg.get_by_id(sid)
        if s is None: messagebox.showinfo("Report", "Not found."); return
        lines = [
            f"--- {s.student_id} | {s.name} ---",
            f"Dept: {s.department} | Gender: {s.gender} | Year: {s.year}",
            f"GPA: {s.gpa()}",
            f"Subjects: {', '.join(s.subjects.to_list()) or '-'}",
            "Attendance rates:",
            f"  All: {s.attendance_rate()}%",
        ]
        for sub in s.subjects:
            lines.append(f"  {sub}: {s.attendance_rate(sub)}%")
        lines.append("\nGrades:")
        for sub, scores in s.grades.items():
            lines.append(f"  {sub}: {scores}")
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, "\n".join(lines))

    # ===========================================================
    # Bonus Tab
    # ===========================================================
    def _build_bonus_tab(self):
        f = self.tab_bonus

        # --- Class Representatives ---
        reps = ttk.LabelFrame(f, text="Class Representatives (Greedy)")
        reps.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.alpha_var = tk.DoubleVar(value=0.7)
        self.beta_var  = tk.DoubleVar(value=0.3)
        self.topk_var  = tk.IntVar(value=1)

        ttk.Label(reps, text="Weight α (GPA)").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(reps, textvariable=self.alpha_var, width=8).grid(row=0, column=1, padx=6, pady=6)
        ttk.Label(reps, text="Weight β (Attendance)").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(reps, textvariable=self.beta_var, width=8).grid(row=0, column=3, padx=6, pady=6)
        ttk.Label(reps, text="Top per Department").grid(row=0, column=4, padx=6, pady=6, sticky="w")
        tk.Spinbox(reps, from_=1, to=5, textvariable=self.topk_var, width=4).grid(row=0, column=5, padx=6, pady=6)
        ttk.Button(reps, text="Pick Representatives", command=self._pick_reps).grid(row=0, column=6, padx=10, pady=6)

        cols = ("dept", "id", "name", "gpa", "attend", "score")
        self.reps_tree = ttk.Treeview(reps, columns=cols, show="headings", height=8)
        for c, txt, w, anchor in [("dept","Dept",120,"w"),("id","ID",100,"w"),("name","Name",180,"w"),("gpa","GPA",60,"center"),("attend","Attend %",80,"center"),("score","Score",70,"center")]:
            self.reps_tree.heading(c, text=txt); self.reps_tree.column(c, width=w, anchor=anchor)
        self.reps_tree.grid(row=1, column=0, columnspan=7, sticky="nsew", padx=6, pady=6)
        reps.grid_columnconfigure(6, weight=1)

        # --- Timetable Optimizer ---
        tt = ttk.LabelFrame(f, text="Timetable Optimizer (DP: Weighted Interval Scheduling)")
        tt.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        editor = ttk.Frame(tt); editor.pack(side=tk.TOP, fill=tk.X, padx=4, pady=4)
        self.slot_code   = tk.StringVar(); self.slot_start = tk.StringVar()
        self.slot_end    = tk.StringVar(); self.slot_weight = tk.StringVar(value="1")

        ttk.Label(editor, text="Subject Code").grid(row=0, column=0, padx=4, pady=4)
        ttk.Entry(editor, textvariable=self.slot_code,   width=10).grid(row=0, column=1, padx=4, pady=4)
        ttk.Label(editor, text="Start (HH:MM)").grid(row=0, column=2, padx=4, pady=4)
        ttk.Entry(editor, textvariable=self.slot_start,  width=8).grid(row=0, column=3, padx=4, pady=4)
        ttk.Label(editor, text="End (HH:MM)").grid(row=0, column=4, padx=4, pady=4)
        ttk.Entry(editor, textvariable=self.slot_end,    width=8).grid(row=0, column=5, padx=4, pady=4)
        ttk.Label(editor, text="Weight").grid(row=0, column=6, padx=4, pady=4)
        ttk.Entry(editor, textvariable=self.slot_weight, width=6).grid(row=0, column=7, padx=4, pady=4)
        ttk.Button(editor, text="Add/Update Slot", command=self._add_update_slot).grid(row=0, column=8, padx=8, pady=4)

        cols2 = ("code", "start", "end", "weight")
        self.catalog_tree = ttk.Treeview(tt, columns=cols2, show="headings", height=8)
        for c, txt, w, anchor in [("code","Code",100,"w"),("start","Start",80,"center"),("end","End",80,"center"),("weight","Weight",70,"center")]:
            self.catalog_tree.heading(c, text=txt); self.catalog_tree.column(c, width=w, anchor=anchor)
        self.catalog_tree.pack(side=tk.TOP, fill=tk.X, padx=4, pady=4)

        opt = ttk.Frame(tt); opt.pack(side=tk.TOP, fill=tk.X, padx=4, pady=4)
        self.opt_sid = tk.StringVar()
        ttk.Label(opt, text="Student ID").pack(side=tk.LEFT)
        ttk.Entry(opt, textvariable=self.opt_sid, width=18).pack(side=tk.LEFT, padx=6)
        ttk.Button(opt, text="Optimize Timetable", command=self._optimize_timetable).pack(side=tk.LEFT, padx=6)
        self.opt_output = tk.Text(tt, height=6)
        self.opt_output.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=6, pady=6)

    def _pick_reps(self):
        try:
            alpha = float(self.alpha_var.get()); beta = float(self.beta_var.get())
            if alpha < 0 or beta < 0: raise ValueError("Weights must be non-negative")
            if alpha + beta == 0:     raise ValueError("At least one weight must be > 0")
            topk = int(self.topk_var.get())
            data = self.reg.choose_class_representatives(top_per_dept=topk, alpha=alpha, beta=beta)
            for i in self.reps_tree.get_children(): self.reps_tree.delete(i)
            for dept, lst in data.items():
                for stu, score in lst:
                    self.reps_tree.insert("", tk.END, values=(dept, stu.student_id, stu.name, f"{stu.gpa():.2f}", f"{stu.attendance_rate():.1f}", f"{score:.1f}"))
        except Exception as e: messagebox.showerror("Error", str(e))

    def _add_update_slot(self):
        code = (self.slot_code.get() or "").strip().upper()
        start = (self.slot_start.get() or "").strip()
        end   = (self.slot_end.get()   or "").strip()
        weight = float(self.slot_weight.get() or 1)
        if not code or not start or not end:
            messagebox.showwarning("Input", "Fill Subject, Start and End."); return
        try:
            smin = time_to_minutes(start); emin = time_to_minutes(end)
            self.reg.set_subject_slot(code, smin, emin, weight)
            self.reg.save_catalog()
            self._refresh_catalog_table()
            messagebox.showinfo("Saved", f"Slot saved for {code}.")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _refresh_catalog_table(self):
        for i in self.catalog_tree.get_children(): self.catalog_tree.delete(i)
        for code, slot in self.reg.list_subject_slots().items():
            self.catalog_tree.insert("", tk.END, values=(code, minutes_to_time(int(slot["start"])), minutes_to_time(int(slot["end"])), f"{slot.get('weight',1.0)}"))

    def _optimize_timetable(self):
        sid = (self.opt_sid.get() or "").strip()
        if not sid: messagebox.showwarning("Input", "Enter a Student ID."); return
        try:
            chosen = self.reg.optimize_timetable_for(sid)
            self.opt_output.delete("1.0", tk.END)
            if not chosen:
                self.opt_output.insert(tk.END, "No schedulable subjects found (check catalog and enrollments).")
                return
            self.opt_output.insert(tk.END, "Optimal non-overlapping subjects:\n")
            for code in chosen:
                slot = self.reg.get_subject_slot(code)
                self.opt_output.insert(tk.END, f"  {code}  {minutes_to_time(int(slot['start']))}-{minutes_to_time(int(slot['end']))}  w={slot.get('weight',1.0)}\n")
        except Exception as e: messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    try:
        App().mainloop()
    except KeyboardInterrupt:
        print("\nInterrupted.")

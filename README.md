# 🎓 Student Information System
**Course:** BER2013 Algorithm Design and Analysis  
**University:** UCSI University  
**Instructor:** Asst. Prof. Dr. Deiva Sigamani

| Student Name | Student ID |
|---|---|
| Tuba Ahmad | 1002268808 |
| Mohammed Tariq | 1002371596 |
| Hamzeh Kareh | 1002372768 |
| Raghd Abdullah | 1002268809 |
| Malak Mohammed Fouad | 1002162667 |

---

## 📁 Project Structure

```
├── student_records.py       # Backend: all DSA + registry + JSON persistence
├── student_records_gui.py   # Frontend: Tkinter GUI (4 tabs)
├── data.json                # Auto-generated: student records
├── catalog.json             # Auto-generated: timetable subject slots
└── README.md
```

---

## 🧠 Data Structures Used

| Structure | Purpose | Complexity |
|---|---|---|
| **Binary Search Tree (BST)** | Student ID index — fast insert/search/delete | O(log n) avg |
| **Singly Linked List** | Subject enrollments per student | O(1) append/drop |
| **Stack (LIFO)** | Grade history — Undo last grade | O(1) push/pop |
| **Queue (FIFO)** | Attendance batch processing | O(1) enqueue/dequeue |
| **Mergesort** | Sort students by Name / GPA | O(n log n) stable |
| **Binary Search** | Search students by name | O(log n) |
| **Greedy** | Select class representatives by score | O(n) |
| **Dynamic Programming** | Weighted interval scheduling (timetable) | O(n²) |

---

## ▶️ How to Run

**Requirements:** Python 3.13+ (standard library only — no pip install needed)

```bash
# Run the GUI
python student_records_gui.py

# Or use the backend directly
python student_records.py
```

---

## 🖥️ GUI Tabs

**Students** — Register, remove, search students; sort by Name / ID / GPA  
**Academics** — Enroll/drop subjects, add grades, undo grades, queue & process attendance  
**Reports** — View full student report (GPA, subjects, attendance %, grades)  
**Bonus** — Greedy class representative picker + DP timetable optimizer  

---

## 🔮 Future Improvements
- Self-balancing BST (AVL/RB tree) for worst-case O(log n)
- Multi-day timetable scheduling
- User authentication with admin/member roles
- Database backend instead of JSON files

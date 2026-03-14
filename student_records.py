from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar, Generic, List as PyList
import json, os, datetime
from collections import deque

# ===========================================================
# BER2013 Algorithm Design and Analysis
# Student Information System — Backend (DSA + Registry)
# Team: Tuba Ahmad, Mohammed Tariq, Hamzeh Kareh,
#       Raghd Abdullah, Malak Mohammed Fouad
# ===========================================================

# -----------------------------------------------------------
# Subject adding system (Singly Linked List)
# -----------------------------------------------------------
class _LLNode:
    __slots__ = ("value", "next")
    def __init__(self, value: Any, nxt: Optional["_LLNode"] = None):
        self.value = value
        self.next  = nxt

class SinglyLinkedList:
    def __init__(self, values: Optional[Iterable[Any]] = None):
        self._head: Optional[_LLNode] = None
        self._size = 0
        if values:
            for v in values:
                self.append(v)

    def __len__(self)      -> int:           return self._size
    def __iter__(self)     -> Iterator[Any]:
        cur = self._head
        while cur is not None:
            yield cur.value
            cur = cur.next
    def __contains__(self, item: Any) -> bool:
        for v in self:
            if v == item: return True
        return False

    def to_list(self) -> List[Any]: return list(iter(self))

    def append(self, value: Any) -> None:
        n = _LLNode(value)
        if not self._head: self._head = n
        else:
            cur = self._head
            while cur.next is not None: cur = cur.next
            cur.next = n
        self._size += 1

    def remove(self, value: Any) -> bool:
        prev = None; cur = self._head
        while cur is not None:
            if cur.value == value:
                if prev is None: self._head = cur.next
                else: prev.next = cur.next
                self._size -= 1; return True
            prev, cur = cur, cur.next
        return False


# -----------------------------------------------------------
# Grading system (Stack — LIFO)
# -----------------------------------------------------------
T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self):              self._data: PyList[T] = []
    def push(self, item: T) -> None: self._data.append(item)
    def pop(self)           -> T:
        if not self._data: raise IndexError("pop from empty stack")
        return self._data.pop()
    def is_empty(self)      -> bool: return len(self._data) == 0
    def peek(self)          -> T:
        if not self._data: raise IndexError("peek from empty stack")
        return self._data[-1]
    def __iter__(self):              return iter(self._data)
    def __len__(self):               return len(self._data)


# -----------------------------------------------------------
# Attendance system (Queue — FIFO)
# -----------------------------------------------------------
class Queue(Generic[T]):
    def __init__(self):               self._dq = deque()
    def enqueue(self, item: T) -> None: self._dq.append(item)
    def dequeue(self)          -> T:
        if not self._dq: raise IndexError("dequeue from empty queue")
        return self._dq.popleft()
    def peek(self)             -> T:
        if not self._dq: raise IndexError("peek from empty queue")
        return self._dq[0]
    def is_empty(self)         -> bool: return len(self._dq) == 0
    def __len__(self):                  return len(self._dq)


# -----------------------------------------------------------
# Report / search system (Binary Search Tree)
# -----------------------------------------------------------
@dataclass
class _BSTNode:
    key:   Any
    value: Any
    left:  Optional["_BSTNode"] = None
    right: Optional["_BSTNode"] = None

class BinarySearchTree:
    def __init__(self):
        self._root: Optional[_BSTNode] = None
        self._size = 0

    def __len__(self): return self._size

    def insert(self, key: Any, value: Any) -> None:
        def _ins(n: Optional[_BSTNode], k: Any, v: Any) -> _BSTNode:
            if n is None:       return _BSTNode(k, v)
            if k < n.key:       n.left  = _ins(n.left,  k, v)
            elif k > n.key:     n.right = _ins(n.right, k, v)
            else:               n.value = v
            return n
        self._root = _ins(self._root, key, value)
        self._size = self._compute_size(self._root)

    def search(self, key: Any) -> Optional[Any]:
        n = self._root
        while n is not None:
            if   key < n.key: n = n.left
            elif key > n.key: n = n.right
            else:             return n.value
        return None

    def delete(self, key: Any) -> None:
        def _min(n: _BSTNode) -> _BSTNode:
            while n.left is not None: n = n.left
            return n
        def _del(n: Optional[_BSTNode], k: Any) -> Optional[_BSTNode]:
            if n is None:   return None
            if k < n.key:   n.left  = _del(n.left,  k)
            elif k > n.key: n.right = _del(n.right, k)
            else:
                if n.left  is None: return n.right
                if n.right is None: return n.left
                t = _min(n.right)
                n.key, n.value = t.key, t.value
                n.right = _del(n.right, t.key)
            return n
        self._root = _del(self._root, key)
        self._size = self._compute_size(self._root)

    def inorder(self) -> Iterator[Tuple[Any, Any]]:
        def _in(n):
            if n:
                yield from _in(n.left)
                yield (n.key, n.value)
                yield from _in(n.right)
        yield from _in(self._root)

    def _compute_size(self, n: Optional[_BSTNode]) -> int:
        return 0 if n is None else 1 + self._compute_size(n.left) + self._compute_size(n.right)


# -----------------------------------------------------------
# Sorting & Searching
# -----------------------------------------------------------
def mergesort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    if key is None: key = lambda x: x
    if len(arr) <= 1: return arr[:]
    mid   = len(arr) // 2
    left  = mergesort(arr[:mid],  key=key)
    right = mergesort(arr[mid:],  key=key)
    return _merge(left, right, key)

def _merge(a: List[Any], b: List[Any], key: Callable[[Any], Any]) -> List[Any]:
    i = j = 0; out: List[Any] = []
    while i < len(a) and j < len(b):
        if key(a[i]) <= key(b[j]): out.append(a[i]); i += 1
        else:                        out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:]); return out

def quicksort(arr: List[Any], key: Optional[Callable[[Any], Any]] = None) -> List[Any]:
    if key is None: key = lambda x: x
    if len(arr) <= 1: return arr[:]
    pivot = arr[len(arr) // 2]; pv = key(pivot)
    less    = [x for x in arr if key(x) <  pv]
    equal   = [x for x in arr if key(x) == pv]
    greater = [x for x in arr if key(x) >  pv]
    return quicksort(less, key=key) + equal + quicksort(greater, key=key)

def binary_search(sorted_arr: List[Any], target: Any,
                  key: Optional[Callable[[Any], Any]] = None) -> int:
    if key is None: key = lambda x: x
    lo, hi = 0, len(sorted_arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2; km = key(sorted_arr[mid])
        if km == target:
            while mid > 0 and key(sorted_arr[mid - 1]) == target: mid -= 1
            return mid
        elif km < target: lo = mid + 1
        else:             hi = mid - 1
    return -1


# -----------------------------------------------------------
# Models
# -----------------------------------------------------------
@dataclass
class AttendanceRecord:
    date:    str
    subject: str
    present: bool

@dataclass
class Student:
    student_id: str
    name:       str
    department: str
    gender:     str
    year:       int
    subjects:        SinglyLinkedList               = field(default_factory=SinglyLinkedList)
    grades:          Dict[str, List[float]]         = field(default_factory=dict)
    grade_history:   Stack[Tuple[str, float]]       = field(default_factory=Stack)
    attendance_log:  List[AttendanceRecord]         = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.year < 1 or self.year > 4:
            raise ValueError("Year must be 1..4")

    def enroll_subject(self, code: str) -> None:
        code = code.strip().upper()
        if code in self.subjects: raise ValueError(f"Subject {code} already enrolled.")
        self.subjects.append(code)

    def drop_subject(self, code: str) -> None:
        code = code.strip().upper()
        if not self.subjects.remove(code): raise ValueError(f"Subject {code} not found.")

    def add_grade(self, subject: str, score: float) -> None:
        subject = subject.strip().upper()
        if subject not in self.subjects: raise ValueError(f"Not enrolled in {subject}.")
        if not (0 <= score <= 100):      raise ValueError("Score must be 0..100")
        self.grades.setdefault(subject, []).append(score)
        self.grade_history.push((subject, score))

    def undo_last_grade(self) -> None:
        if self.grade_history.is_empty(): raise ValueError("No grades to undo.")
        subj, score = self.grade_history.pop()
        lst = self.grades.get(subj, [])
        if lst and lst[-1] == score: lst.pop()

    def record_attendance(self, date: str, subject: str, present: bool) -> None:
        subject = subject.strip().upper()
        if subject not in self.subjects: raise ValueError(f"Not enrolled in {subject}.")
        self.attendance_log.append(AttendanceRecord(date=date, subject=subject, present=present))

    def gpa(self) -> float:
        if not self.grades: return 0.0
        avgs = [sum(v) / len(v) for v in self.grades.values() if v]
        if not avgs: return 0.0
        pct = sum(avgs) / len(avgs)
        return round((pct / 100) * 4, 2)

    def attendance_rate(self, subject: Optional[str] = None) -> float:
        logs = self.attendance_log if subject is None else \
               [r for r in self.attendance_log if r.subject == subject.upper()]
        if not logs: return 0.0
        present = sum(1 for r in logs if r.present)
        return round(100.0 * present / len(logs), 2)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["subjects"]      = self.subjects.to_list()
        d["grade_history"] = list(self.grade_history)
        d["attendance_log"] = [asdict(r) for r in self.attendance_log]
        return d

    @staticmethod
    def from_dict(d: dict) -> "Student":
        s = Student(d["student_id"], d["name"], d["department"], d["gender"], int(d["year"]))
        for sub in d.get("subjects", []):       s.subjects.append(sub)
        s.grades = {k: list(v) for k, v in d.get("grades", {}).items()}
        for subj, score in d.get("grade_history", []): s.grade_history.push((subj, float(score)))
        for rec in d.get("attendance_log", []):         s.attendance_log.append(AttendanceRecord(**rec))
        return s


# -----------------------------------------------------------
# Registry
# -----------------------------------------------------------
DATA_FILE    = "data.json"
CATALOG_FILE = "catalog.json"

class StudentRegistry:
    def __init__(self):
        self._students:       List[Student]                        = []
        self._index:          BinarySearchTree                     = BinarySearchTree()
        self._attendance_q:   Queue[Tuple[str, str, str, bool]]   = Queue()
        self._subject_catalog: Dict[str, Dict[str, float]]        = {}

    # --- CRUD ---
    def add_student(self, s: Student) -> None:
        if self.get_by_id(s.student_id) is not None:
            raise ValueError(f"Student ID {s.student_id} already exists.")
        self._students.append(s)
        self._index.insert(s.student_id, s)

    def get_by_id(self, sid: str) -> Optional[Student]:
        return self._index.search(sid)

    def remove_student(self, sid: str) -> None:
        if self.get_by_id(sid) is None: raise ValueError("Not found.")
        self._students = [x for x in self._students if x.student_id != sid]
        self._index.delete(sid)

    # --- Attendance Queue ---
    def enqueue_attendance(self, sid: str, date: str, subject: str, present: bool) -> None:
        self._attendance_q.enqueue((sid, date, subject, present))

    def process_attendance(self) -> int:
        cnt = 0
        while not self._attendance_q.is_empty():
            sid, date, subj, present = self._attendance_q.dequeue()
            s = self.get_by_id(sid)
            if s is None:
                print(f"[WARN] Unknown student {sid}"); continue
            try:
                if not date: date = str(datetime.date.today())
                s.record_attendance(date, subj, present)
                cnt += 1
            except Exception as e:
                print(f"[WARN] attendance failed for {sid}: {e}")
        return cnt

    # --- Listing & Sorting ---
    def list_students(self)                    -> List[Student]: return list(self._students)
    def sorted_by_name(self)                   -> List[Student]:
        return mergesort(self._students, key=lambda s: s.name.lower())
    def sorted_by_id(self)                     -> List[Student]:
        return [v for _, v in self._index.inorder()]
    def sorted_by_gpa(self, descending=True)   -> List[Student]:
        out = mergesort(self._students[:], key=lambda s: s.gpa())
        return list(reversed(out)) if descending else out
    def binary_search_by_name(self, name: str) -> List[Student]:
        arr = mergesort(self._students, key=lambda s: s.name.lower())
        idx = binary_search(arr, name.lower(), key=lambda s: s.name.lower())
        if idx == -1: return []
        out = []; i = idx
        while i < len(arr) and arr[i].name.lower() == name.lower():
            out.append(arr[i]); i += 1
        return out

    # --- Persistence ---
    def save(self, path: str = DATA_FILE) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self._students], f, indent=2)
        self.save_catalog()

    def load(self, path: str = DATA_FILE) -> None:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f: json.dump([], f)
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            data = json.loads(raw) if raw.strip() else []
        except Exception:
            try: os.replace(path, path + ".corrupt")
            except Exception: pass
            data = []
        self._students.clear(); self._index = BinarySearchTree()
        for d in data:
            try: self.add_student(Student.from_dict(d))
            except Exception: continue
        self.load_catalog()

    def save_catalog(self, path: str = CATALOG_FILE) -> None:
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._subject_catalog, f, indent=2)
        except Exception as e:
            print(f"[WARN] could not save catalog: {e}")

    def load_catalog(self, path: str = CATALOG_FILE) -> None:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f: json.dump({}, f)
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read().strip()
            self._subject_catalog = json.loads(raw) if raw else {}
        except Exception:
            try: os.replace(path, path + ".corrupt")
            except Exception: pass
            self._subject_catalog = {}

    # --- Bonus: Class Representatives (Greedy) ---
    def choose_class_representatives(self, top_per_dept: int = 1,
                                     alpha: float = 0.7,
                                     beta:  float = 0.3) -> Dict[str, List[Tuple[Student, float]]]:
        buckets: Dict[str, List[Tuple[Student, float]]] = {}
        for s in self._students:
            score = alpha * (s.gpa() / 4.0 * 100.0) + beta * s.attendance_rate()
            buckets.setdefault(s.department or "-", []).append((s, round(score, 2)))
        chosen: Dict[str, List[Tuple[Student, float]]] = {}
        for dept, lst in buckets.items():
            lst.sort(key=lambda t: t[1], reverse=True)
            chosen[dept] = lst[:max(1, int(top_per_dept))]
        return chosen

    # --- Bonus: Timetable Optimizer (DP — Weighted Interval Scheduling) ---
    def set_subject_slot(self, code: str, start_min: int, end_min: int, weight: float = 1.0) -> None:
        code = code.strip().upper()
        if end_min <= start_min: raise ValueError("End must be after start")
        self._subject_catalog[code] = {"start": int(start_min), "end": int(end_min), "weight": float(weight)}

    def get_subject_slot(self, code: str) -> Optional[Dict[str, float]]:
        return self._subject_catalog.get(code.strip().upper())

    def list_subject_slots(self) -> Dict[str, Dict[str, float]]:
        return dict(self._subject_catalog)

    def optimize_timetable_for(self, student_id: str) -> List[str]:
        s = self.get_by_id(student_id)
        if s is None: raise ValueError("Student not found")
        items: List[Tuple[int, int, float, str]] = []
        for code in s.subjects:
            slot = self._subject_catalog.get(code)
            if slot:
                items.append((int(slot["start"]), int(slot["end"]), float(slot.get("weight", 1.0)), code))
        if not items: return []
        items.sort(key=lambda x: x[1])
        n = len(items)
        p = [0] * n
        for j in range(n):
            sj_start = items[j][0]
            for i in range(j - 1, -1, -1):
                if items[i][1] <= sj_start:
                    p[j] = i + 1; break
        dp   = [0.0] * (n + 1)
        keep = [False] * (n + 1)
        for j in range(1, n + 1):
            incl = items[j-1][2] + dp[p[j-1]]
            excl = dp[j-1]
            if incl > excl: dp[j] = incl; keep[j] = True
            else:           dp[j] = excl; keep[j] = False
        chosen_codes: List[str] = []
        j = n
        while j > 0:
            if keep[j]: chosen_codes.append(items[j-1][3]); j = p[j-1]
            else:        j -= 1
        chosen_codes.reverse()
        return chosen_codes

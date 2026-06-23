# MySQL Integration Guide for Aristeia Academy

This guide details exactly where and how you should insert your `mysql.connector` (or `pymysql`) logic into the PySide6 UI. Because we designed the application modularly in `frontPage.py`, you can easily swap out the dummy data for real database queries.

## 1. Database Connection

You should set up a global or singleton database connection manager, or connect inside the `__init__` of `MySideBar` in `frontPage.py`.

```python
import mysql.connector

class MySideBar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # ... setupUi ...
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="aristeia_db"
        )
        self.cursor = self.db.cursor(dictionary=True)
```

## 2. Login Authentication

**File:** `frontPage.py`
**Method:** `handle_login(self)`

Currently, the login uses hardcoded credentials (`crabbierduke167` / `9090`).
Replace this block with a database query:

```python
# frontPage.py - handle_login
def handle_login(self):
    user = self.inp_username.text().strip()
    token = self.inp_token.text().strip()
    
    query = "SELECT * FROM users WHERE username = %s AND token = %s"
    self.cursor.execute(query, (user, token))
    result = self.cursor.fetchone()
    
    if result:
        # Success!
        self.lbl_login_error.setText("")
        self.outer_stacked_widget.setCurrentIndex(1)
        self.switch_to_home()
    else:
        self.lbl_login_error.setText("INVALID CREDENTIALS")
```

## 3. Question of the Day & Motivational Quote

**File:** `frontPage.py`
**Method:** `switch_to_home(self)` (Or a custom `load_home_data` method)

Fetch random entries from your database.

```python
# To load the Quote
self.cursor.execute("SELECT text FROM quotes ORDER BY RAND() LIMIT 1")
quote = self.cursor.fetchone()
if quote:
    self.lbl_quote_text.setText(f'"{quote["text"]}"')

# To load Question of the Day
self.cursor.execute("SELECT id, text, answer, difficulty FROM questions ORDER BY RAND() LIMIT 1")
qotd = self.cursor.fetchone()
if qotd:
    self.lbl_qotd_text.setText(qotd["text"])
    # Connect the view button to open the drawer with this specific data
    # Be sure to disconnect previous signals to avoid multiple triggers
    self.btn_qotd_view.clicked.disconnect() 
    self.btn_qotd_view.clicked.connect(lambda: self.open_drawer({
        "q": qotd["text"], "a": qotd["answer"], "diff": qotd["difficulty"]
    }))
```

## 4. Upload to Bank

**File:** `frontPage.py`
**Where to Add:** Create a new method `upload_question(self)` and connect it to `self.btn_upload.clicked`.

```python
def __init__(self):
    # ...
    self.btn_upload.clicked.connect(self.upload_question)

def upload_question(self):
    subject = self.combo_subject.currentText()
    chapter = self.combo_chapter.currentText()
    diff = self.combo_diff.currentText()
    question_text = self.txt_upload_q.toPlainText()
    
    query = "INSERT INTO questions (subject, chapter, difficulty, text) VALUES (%s, %s, %s, %s)"
    self.cursor.execute(query, (subject, chapter, diff, question_text))
    self.db.commit()
    
    # Optionally show a QMessageBox or a styled Neo-Brutalist confirmation label!
    self.txt_upload_q.clear()
```

## 5. Dynamic Chapters

**File:** `frontPage.py`
**Method:** `open_subject_chapters(self, subject_name)`

Currently, it uses the `SUBJECTS` dictionary. Replace it:

```python
def open_subject_chapters(self, subject_name):
    self.lbl_ch_title.setText(f"SUBJECT: {subject_name}")
    
    # Query your database for chapters under this subject
    query = "SELECT DISTINCT chapter_name FROM chapters WHERE subject = %s"
    self.cursor.execute(query, (subject_name,))
    results = self.cursor.fetchall()
    
    chapters = [r['chapter_name'] for r in results]
    
    # ... (Rest of the UI building code remains the same, looping over `chapters`)
```

## 6. Fetching Questions for a Chapter

**File:** `frontPage.py`
**Method:** `open_questions(self, chapter_name)`

Currently, it uses `MOCK_QUESTIONS`.

```python
def open_questions(self, chapter_name):
    self.lbl_q_title.setText(f"CHAPTER: {chapter_name}")
    
    query = "SELECT id, text, answer, difficulty FROM questions WHERE chapter = %s"
    self.cursor.execute(query, (chapter_name,))
    questions = self.cursor.fetchall()
    
    # Loop over `questions` to build the UI instead of MOCK_QUESTIONS
    for q_data in questions:
        # q_data['text'] maps to q_data["q"] in the mock
        # q_data['answer'] maps to q_data["a"]
        # etc...
```

## 7. Analytics Dashboard

**File:** `ui_index.py` (For layout placeholders)
You have 4 placeholder frames. Use `QtCharts` or `matplotlib.backends.backend_qtagg` combined with SQL counts (e.g., `SELECT COUNT(*) FROM questions WHERE difficulty='HARD'`) to build real charts inside `_setup_page_dashboard()`.

## 8. Schedule (To-Do List)

**File:** `frontPage.py`
**Where to Add:** Create `load_tasks`, `add_task`, `delete_task` methods.

```python
def add_task(self):
    task_text = self.inp_task.text()
    priority = self.combo_priority.currentText()
    
    query = "INSERT INTO schedule (task, priority, status) VALUES (%s, %s, 'PENDING')"
    self.cursor.execute(query, (task_text, priority))
    self.db.commit()
    
    self.load_tasks() # Refresh the QListWidget
```

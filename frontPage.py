# -*- coding: utf-8 -*-
import sys
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFrame, QLabel,
                               QHBoxLayout, QVBoxLayout, QSizePolicy, QColorDialog, QSpacerItem)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PySide6.QtGui import QFont, QCursor, QColor

# Import architecture definitions from ui_index
from ui_index import (Ui_MainWindow, add_shadow, BASE_BTN_STYLE, INPUT_STYLE,
                      DOTTED_BG, NeoMessageBox, NeoEditDialog)

# ==========================================
# --- DATA DICTIONARIES & RUNTIME STATE ---
# ==========================================
SUBJECTS = {
    "PHYSICS": [
        "Electric Charges and Fields", "Electrostatic Potential and Capacitance",
        "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter",
        "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves",
        "Ray Optics and Optical Instruments", "Wave Optics", "Dual Nature of Radiation",
        "Atoms", "Nuclei", "Semiconductor Electronics"
    ],
    "CHEMISTRY": [
        "Solutions", "Electrochemistry", "Chemical Kinetics", "d and f Block Elements",
        "Coordination Compounds", "Haloalkanes and Haloarenes", "Alcohols, Phenols",
        "Aldehydes, Ketones and Acids", "Amines", "Biomolecules"
    ],
    "MATHEMATICS": [
        "Relations and Functions", "Inverse Trigonometric Functions", "Matrices",
        "Determinants", "Continuity and Differentiability", "Derivatives Application",
        "Integrals", "Integrals Application", "Differential Equations", "Vector Algebra",
        "Three Dimensional Geometry", "Linear Programming", "Probability"
    ],
    "ENGLISH": [
        "The Last Lesson", "Lost Spring", "Deep Water", "The Rattrap", "Indigo",
        "Poets and Pancakes", "The Interview", "Going Places", "My Mother at Sixty-Six",
        "Keeping Quiet", "A Thing of Beauty", "A Roadside Stand", "Aunt Jennifer's Tigers"
    ],
    "COMP SCI": [
        "Functions", "Recursion", "File Handling", "Binary Files", "CSV Files",
        "Exception Handling", "Database Concepts", "SQL Queries", "DDL Commands",
        "DML Commands", "Aggregate Functions", "GROUP BY", "JOINS", "Networks"
    ]
}

# In-memory runtime persistence before MySQL integration
MOCK_QUESTIONS = [
    {"id": 1, "sub": "PHYSICS", "ch": "Electric Charges and Fields", "q": "What is Coulomb's Law?", "a": "F = k * (|q1*q2|) / r^2. Describes electrostatic force between charged particles.", "diff": "MODERATE"},
    {"id": 2, "sub": "COMP SCI", "ch": "SQL Queries", "q": "Difference between WHERE and HAVING?", "a": "WHERE filters rows before aggregation. HAVING filters grouped records after GROUP BY.", "diff": "HARD"},
    {"id": 3, "sub": "MATHEMATICS", "ch": "Matrices", "q": "What defines an Identity Matrix?", "a": "A square matrix with 1s on the main diagonal and 0s elsewhere.", "diff": "EASY"}
]

MOCK_TASKS = [
    {"id": 101, "task": "Formulate MySQL Connection String", "priority": "P1 (HIGH)"},
    {"id": 102, "task": "Complete CBSE Class 12 Calculus Exercises", "priority": "P2 (MEDIUM)"},
    {"id": 103, "task": "Review Ray Optics Formulas", "priority": "P3 (LOW)"}
]

# --- Matplotlib Canvas Wrapper ---
class MplCanvas(FigureCanvasQTAgg):
    """Transparent Matplotlib canvas providing brutalist telemetry rendering."""
    def __init__(self, parent=None, width=5, height=3.5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_alpha(0.0)
        self.axes = fig.add_subplot(111)
        self.axes.patch.set_alpha(0.0)
        super().__init__(fig)

# ==========================================
# --- APPLICATION CONTROLLER & ROUTER ---
# ==========================================
class MySideBar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Aristeia Academy")

        self.sidebar_expanded = True
        self.drawer_open = False
        self.current_drawer_q_id = None
        self.active_chapter_view = None

        # Render dynamic views
        self.setup_matplotlib_charts()
        self.populate_upload_chapters(self.combo_subject.currentText())
        self.update_qotd_display()

        # Connect Primary Navigation Signals
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_logout.clicked.connect(self.handle_logout)

        self.btn_nav_home.clicked.connect(self.switch_to_home)
        self.btn_nav_dashboard.clicked.connect(self.switch_to_dashboard)
        self.btn_nav_schedule.clicked.connect(self.switch_to_schedule)
        self.btn_nav_settings.clicked.connect(self.switch_to_settings)

        self.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar)
        self.btn_drawer_close.clicked.connect(self.close_drawer)

        # Subject selection mapping
        for sub_name, btn in self.subject_btns.items():
            btn.clicked.connect(lambda checked=False, name=sub_name: self.open_subject_chapters(name))

        self.btn_back_to_sub.clicked.connect(self.switch_to_home)
        self.btn_back_to_ch.clicked.connect(lambda: self.app_stacked_widget.setCurrentIndex(4))

        # Dynamic Dropdown Linking
        self.combo_subject.currentTextChanged.connect(self.populate_upload_chapters)
        self.btn_upload.clicked.connect(self.handle_upload)

        # Drawer CRUD Routing
        self.btn_drawer_edit.clicked.connect(self.crud_edit_question)
        self.btn_drawer_delete.clicked.connect(self.crud_delete_question)

        # Schedule CRUD Routing
        self.btn_add_task.clicked.connect(self.crud_create_task)
        self.crud_read_tasks()

        # Theme Engine Signals
        self.btn_theme_light.clicked.connect(lambda: self.apply_theme("LIGHT"))
        self.btn_theme_dark.clicked.connect(lambda: self.apply_theme("DARK"))
        self.btn_theme_arg.clicked.connect(lambda: self.apply_theme("ARGENTINA"))
        self.btn_theme_bra.clicked.connect(lambda: self.apply_theme("BRASIL"))
        self.btn_theme_por.clicked.connect(lambda: self.apply_theme("PORTUGAL"))

        # Independent Custom Color Overrides
        self.btn_custom_sidebar.clicked.connect(self.pick_custom_color_sidebar)
        self.btn_custom_cards.clicked.connect(self.pick_custom_color_cards)
        self.btn_custom_accent.clicked.connect(self.pick_custom_color_accent)

    # --- Matplotlib Telemetry Implementation ---
    def setup_matplotlib_charts(self):
        """Embeds active Matplotlib canvases inside the analytics targets ready for SQL data arrays."""
        self.canvases = []
        for i, target in enumerate(self.chart_widgets):
            lay = QVBoxLayout(target)
            lay.setContentsMargins(0, 0, 0, 0)
            sc = MplCanvas(self, width=5, height=3.5, dpi=100)
            self.canvases.append(sc)
            lay.addWidget(sc)

        self.update_dashboard_charts()

    def update_dashboard_charts(self):
        """Simulates dynamic SQL telemetry arrays being parsed into Matplotlib axes."""
        # Ready for replacement with: cursor.execute("SELECT diff, count(*) FROM questions GROUP BY diff")
        x_diff = ['EASY', 'MODERATE', 'HARD']
        y_diff = [len([q for q in MOCK_QUESTIONS if q['diff'] == 'EASY']),
                  len([q for q in MOCK_QUESTIONS if q['diff'] == 'MODERATE']),
                  len([q for q in MOCK_QUESTIONS if q['diff'] == 'HARD'])]
        
        ax0 = self.canvases[0].axes
        ax0.clear()
        ax0.bar(x_diff, y_diff, color=['#00FFFF', '#FFD700', '#FF3333'], edgecolor='black', linewidth=3)
        ax0.tick_params(colors='black')
        for spine in ax0.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(3)

        # Graph 2: Chapter Distribution
        ax1 = self.canvases[1].axes
        ax1.clear()
        ax1.plot(['Ch1', 'Ch2', 'Ch3', 'Ch4'], [10, 25, 18, 32], marker='o', markersize=8, color='#FF5E00', linewidth=3, markeredgecolor='black', markeredgewidth=2)
        ax1.tick_params(colors='black')
        for spine in ax1.spines.values(): spine.set_edgecolor('black'); spine.set_linewidth(3)

        # Draw updates
        for sc in self.canvases[:2]: sc.draw()

    def update_qotd_display(self):
        """Pulls dynamic QOTD from local persistent state or MySQL."""
        if MOCK_QUESTIONS:
            q = MOCK_QUESTIONS[-1]  # Display latest active question
            self.lbl_qotd_text.setText(f"Subject: {q['sub']} | Chapter: {q['ch']}\n\n{q['q']}")
            self.btn_qotd_view.clicked.disconnect()
            self.btn_qotd_view.clicked.connect(lambda checked=False, target=q: self.open_drawer(target))

    # --- System Security Routing ---
    def handle_login(self):
        user = self.inp_username.text().strip()
        token = self.inp_token.text().strip()
        if user == "crabbierduke167" and token == "9090":
            self.lbl_login_error.setText("")
            self.inp_username.clear()
            self.inp_token.clear()
            self.outer_stacked_widget.setCurrentIndex(1)
            self.switch_to_home()
        else:
            self.lbl_login_error.setText("INVALID CREDENTIALS")

    def handle_logout(self):
        self.outer_stacked_widget.setCurrentIndex(0)
        self.close_drawer()

    # --- View Switchers ---
    def switch_to_home(self): self.app_stacked_widget.setCurrentIndex(0); self.btn_nav_home.setChecked(True); self.close_drawer()
    def switch_to_dashboard(self): self.app_stacked_widget.setCurrentIndex(1); self.btn_nav_dashboard.setChecked(True); self.update_dashboard_charts(); self.close_drawer()
    def switch_to_schedule(self): self.app_stacked_widget.setCurrentIndex(2); self.btn_nav_schedule.setChecked(True); self.close_drawer()
    def switch_to_settings(self): self.app_stacked_widget.setCurrentIndex(3); self.btn_nav_settings.setChecked(True); self.close_drawer()

    # --- Dynamic Dropdown Cascading ---
    def populate_upload_chapters(self, subject):
        sub_mapped = subject.upper()
        if sub_mapped == "COMPUTER SCIENCE": sub_mapped = "COMP SCI"
        chapters = SUBJECTS.get(sub_mapped, [])
        self.combo_chapter.clear()
        self.combo_chapter.addItems(chapters)

    # --- SQL Ingestion Endpoint (Upload Portal) ---
    def handle_upload(self):
        sub = self.combo_subject.currentText().upper()
        if sub == "COMPUTER SCIENCE": sub = "COMP SCI"
        ch = self.combo_chapter.currentText()
        diff = self.combo_diff.currentText()
        raw_text = self.txt_upload_q.toPlainText().strip()

        if not raw_text:
            NeoMessageBox("Error", "Question cannot be empty!", "error", self).exec()
            return

        q_part, a_part = raw_text, "Solution missing."
        if "A:" in raw_text:
            parts = raw_text.split("A:")
            q_part = parts[0].replace("Q:", "").strip()
            a_part = parts[1].strip()

        new_id = max([q['id'] for q in MOCK_QUESTIONS], default=0) + 1
        new_payload = {"id": new_id, "sub": sub, "ch": ch, "q": q_part, "a": a_part, "diff": diff}
        
        # -> SQL INSERT HERE
        MOCK_QUESTIONS.append(new_payload)
        self.txt_upload_q.clear()
        self.update_qotd_display()

        NeoMessageBox("Success", f"Uploaded Question to {ch}!", "success", self).exec()

        if self.app_stacked_widget.currentIndex() == 5 and self.active_chapter_view == ch:
            self.open_questions(ch)

    # =========================================================================
    # --- MEMORY LEAK FREE DYNAMIC BUILDERS ---
    # =========================================================================
    def open_subject_chapters(self, subject_name):
        self.lbl_ch_title.setText(f"SUBJECT: {subject_name}")

        while self.lay_ch_grid.count():
            item = self.lay_ch_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        chapters = SUBJECTS.get(subject_name, [])
        row, col = 0, 0
        for ch in chapters:
            btn = QPushButton(ch)
            btn.setMinimumHeight(75)
            btn.setFont(QFont("Space Grotesk", 12, QFont.Bold))
            btn.setStyleSheet(BASE_BTN_STYLE)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn, 4, 4)
            btn.clicked.connect(lambda checked=False, ch_target=ch: self.open_questions(ch_target))
            self.lay_ch_grid.addWidget(btn, row, col)
            col += 1
            if col > 2: col = 0; row += 1

        self.app_stacked_widget.setCurrentIndex(4)
        for b in [self.btn_nav_home, self.btn_nav_dashboard, self.btn_nav_schedule, self.btn_nav_settings]: b.setChecked(False)

    def open_questions(self, chapter_name):
        self.lbl_q_title.setText(f"CHAPTER: {chapter_name}")
        self.active_chapter_view = chapter_name

        while self.lay_q_list.count():
            item = self.lay_q_list.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            elif item.spacerItem(): pass

        chapter_qs = [q for q in MOCK_QUESTIONS if q["ch"] == chapter_name]

        if not chapter_qs:
            empty_lbl = QLabel("NO QUESTIONS IN DATABASE.")
            empty_lbl.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
            empty_lbl.setStyleSheet("color: #555555;")
            self.lay_q_list.addWidget(empty_lbl)
        else:
            for q_data in chapter_qs:
                q_card = QFrame()
                q_card.setObjectName("ThemeCard")
                q_card.setStyleSheet("QFrame { background-color: #FFFFFF; border: 4px solid #000000; }")
                add_shadow(q_card, 4, 4)
                qlay = QHBoxLayout(q_card)
                qlay.setContentsMargins(15, 15, 15, 15)

                lbl = QLabel(q_data["q"])
                lbl.setObjectName("ThemeCardText")
                lbl.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
                lbl.setWordWrap(True)
                lbl.setStyleSheet("border: none; color: #000000;")

                diff_color = "#FFD700" if q_data["diff"] == "MODERATE" else ("#00FFFF" if q_data["diff"] == "EASY" else "#FF3333")
                lbl_diff = QLabel(q_data["diff"])
                lbl_diff.setFont(QFont("Space Grotesk", 10, QFont.Bold))
                lbl_diff.setStyleSheet(f"background: {diff_color}; border: 2px solid #000000; padding: 6px; color: #000000;")

                btn_view = QPushButton("VIEW ANSWER ->")
                btn_view.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#8A2BE2") + "QPushButton { color: white; }")
                btn_view.setCursor(QCursor(Qt.PointingHandCursor))
                add_shadow(btn_view, 2, 2)
                btn_view.clicked.connect(lambda checked=False, target=q_data: self.open_drawer(target))

                qlay.addWidget(lbl, 1)
                qlay.addWidget(lbl_diff)
                qlay.addWidget(btn_view)
                self.lay_q_list.addWidget(q_card)

        self.lay_q_list.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.app_stacked_widget.setCurrentIndex(5)

    # --- Sliding Drawer Controller ---
    def open_drawer(self, q_data):
        self.current_drawer_q_id = q_data.get("id")
        self.lbl_drawer_diff.setText(f"DIFFICULTY: {q_data['diff']}")
        
        diff_color = "#FFD700" if q_data["diff"] == "MODERATE" else ("#00FFFF" if q_data["diff"] == "EASY" else "#FF3333")
        self.lbl_drawer_diff.setStyleSheet(f"background: {diff_color}; border: 3px solid #000000; padding: 6px; color: #000000;")

        # Populate separate cards
        self.lbl_drawer_question.setText(q_data['q'])
        self.txt_drawer_answer.setText(q_data['a'])

        if not self.drawer_open:
            self.answer_drawer.show()
            self.answer_drawer.raise_()

            parent_rect = self.page_mainapp.rect()
            start_rect = QRect(parent_rect.width(), 0, 500, parent_rect.height())
            end_rect = QRect(parent_rect.width() - 500, 0, 500, parent_rect.height())

            self.anim = QPropertyAnimation(self.answer_drawer, b"geometry")
            self.anim.setDuration(320)
            self.anim.setStartValue(start_rect)
            self.anim.setEndValue(end_rect)
            self.anim.setEasingCurve(QEasingCurve.OutExpo)
            self.anim.start()
            self.drawer_open = True

    def close_drawer(self):
        if self.drawer_open:
            # ---> AUTO SAVE LOGIC FOR ANSWER TEXT EDIT <---
            if self.current_drawer_q_id:
                new_ans = self.txt_drawer_answer.toPlainText().strip()
                for q in MOCK_QUESTIONS:
                    if q['id'] == self.current_drawer_q_id:
                        q['a'] = new_ans
                        active_ch = q['ch']
                        break
                # -> SQL UPDATE FOR ANSWER HERE 

            parent_rect = self.page_mainapp.rect()
            start_rect = QRect(parent_rect.width() - 500, 0, 500, parent_rect.height())
            end_rect = QRect(parent_rect.width(), 0, 500, parent_rect.height())

            self.anim = QPropertyAnimation(self.answer_drawer, b"geometry")
            self.anim.setDuration(320)
            self.anim.setStartValue(start_rect)
            self.anim.setEndValue(end_rect)
            self.anim.setEasingCurve(QEasingCurve.InExpo)
            self.anim.finished.connect(self.answer_drawer.hide)
            self.anim.start()
            self.drawer_open = False

    # =========================================================================
    # --- DRAWER CRUD ENDPOINTS ---
    # =========================================================================
    def crud_edit_question(self):
        """Opens Custom UI to edit the Question Text."""
        if not self.current_drawer_q_id: return
        
        current_q_text = self.lbl_drawer_question.text()
        dialog = NeoEditDialog("EDIT QUESTION", current_q_text, self)
        
        if dialog.exec() == QDialog.Accepted:
            new_q = dialog.get_text()
            if not new_q: return

            # Update Local State
            for q in MOCK_QUESTIONS:
                if q['id'] == self.current_drawer_q_id:
                    q['q'] = new_q
                    active_ch = q['ch']
                    break

            # -> SQL UPDATE FOR QUESTION HERE
            
            self.lbl_drawer_question.setText(new_q)
            NeoMessageBox("Success", "Question Updated Successfully!", "success", self).exec()
            
            if getattr(self, 'active_chapter_view', None) == active_ch:
                self.open_questions(active_ch)

    def crud_delete_question(self):
        """Purges active question from state."""
        if not self.current_drawer_q_id: return

        # -> SQL DELETE HERE

        global MOCK_QUESTIONS
        MOCK_QUESTIONS = [q for q in MOCK_QUESTIONS if q['id'] != self.current_drawer_q_id]

        NeoMessageBox("Deleted", "Question Deleted.", "warning", self).exec()
        self.close_drawer()
        self.update_qotd_display()
        
        if getattr(self, 'active_chapter_view', None):
            self.open_questions(self.active_chapter_view)

    # =========================================================================
    # --- SCHEDULE FULL CRUD CONTROLLER ---
    # =========================================================================
    def crud_create_task(self):
        text = self.inp_task.text().strip()
        priority = self.combo_priority.currentText()
        if not text:
            NeoMessageBox("Error", "Task cannot be blank!", "error", self).exec()
            return

        new_id = max([t['id'] for t in MOCK_TASKS], default=100) + 1
        # -> SQL INSERT HERE
        
        MOCK_TASKS.append({"id": new_id, "task": text, "priority": priority})
        self.inp_task.clear()
        self.crud_read_tasks()
        NeoMessageBox("Success", "Task Added.", "success", self).exec()

    def crud_read_tasks(self):
        while self.schedule_tasks_layout.count():
            item = self.schedule_tasks_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            elif item.spacerItem(): pass

        # -> SQL SELECT HERE
        for t_data in MOCK_TASKS:
            t_card = QFrame()
            t_card.setObjectName("ThemeCard")
            t_card.setStyleSheet("QFrame { background-color: #FFFFFF; border: 4px solid #000000; }")
            add_shadow(t_card, 4, 4)
            tlay = QHBoxLayout(t_card)
            tlay.setContentsMargins(15, 12, 15, 12)
            tlay.setSpacing(15)

            p_color = "#FF3333" if "HIGH" in t_data["priority"] else ("#FFD700" if "MEDIUM" in t_data["priority"] else "#00FFFF")
            lbl_pTag = QLabel(t_data["priority"].split()[0])
            lbl_pTag.setFont(QFont("Space Grotesk", 10, QFont.Black))
            lbl_pTag.setStyleSheet(f"background: {p_color}; border: 2px solid #000000; padding: 5px; color: #000000;")

            lbl_tText = QLabel(t_data["task"])
            lbl_tText.setObjectName("ThemeCardText")
            lbl_tText.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
            lbl_tText.setStyleSheet("border: none; color: #000000;")

            btn_edit = QPushButton("EDIT")
            btn_edit.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FFD700"))
            btn_edit.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn_edit, 2, 2)
            btn_edit.clicked.connect(lambda checked=False, target=t_data: self.crud_update_task(target))

            btn_del = QPushButton("DELETE")
            btn_del.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF3333") + "QPushButton { color: white; }")
            btn_del.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn_del, 2, 2)
            btn_del.clicked.connect(lambda checked=False, target=t_data: self.crud_delete_task(target))

            tlay.addWidget(lbl_pTag)
            tlay.addWidget(lbl_tText, 1)
            tlay.addWidget(btn_edit)
            tlay.addWidget(btn_del)
            self.schedule_tasks_layout.addWidget(t_card)

        self.schedule_tasks_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def crud_update_task(self, task_target):
        # Uses Custom NeoEditDialog instead of system QInputDialog
        dialog = NeoEditDialog("EDIT TASK", task_target["task"], self)
        if dialog.exec() == QDialog.Accepted:
            new_text = dialog.get_text()
            if new_text:
                task_target["task"] = new_text
                # -> SQL UPDATE HERE
                self.crud_read_tasks()
                NeoMessageBox("Success", "Task Updated.", "success", self).exec()

    def crud_delete_task(self, task_target):
        global MOCK_TASKS
        MOCK_TASKS = [t for t in MOCK_TASKS if t['id'] != task_target['id']]
        # -> SQL DELETE HERE
        self.crud_read_tasks()

    def toggle_sidebar(self):
        if self.sidebar_expanded: self.icon_text_widget.hide(); self.sidebar_expanded = False
        else: self.icon_text_widget.show(); self.sidebar_expanded = True

    # =========================================================================
    # --- ADVANCED THEME ENGINE (Absolute Readability Enforced) ---
    # =========================================================================
    def apply_theme(self, theme_name):
        themes = {
            "LIGHT": {"bg": "#F4F1EB", "sidebar": "#FFFFFF", "nav_text": "#000000", "card_bg": "#FFFFFF", "card_text": "#000000", "accent": "#FFD700"},
            "DARK": {"bg": "#121212", "sidebar": "#1E1E1E", "nav_text": "#FFFFFF", "card_bg": "#2C2C2C", "card_text": "#FFFFFF", "accent": "#FF5E00"},
            "ARGENTINA": {"bg": "#74ACDF", "sidebar": "#FFFFFF", "nav_text": "#000000", "card_bg": "#F6B40E", "card_text": "#000000", "accent": "#FFFFFF"},
            "BRASIL": {"bg": "#009C3B", "sidebar": "#002776", "nav_text": "#FFFFFF", "card_bg": "#FEDD00", "card_text": "#000000", "accent": "#002776"},
            "PORTUGAL": {"bg": "#FF0000", "sidebar": "#006600", "nav_text": "#FFFFFF", "card_bg": "#FFD700", "card_text": "#000000", "accent": "#006600"}
        }
        t = themes.get(theme_name, themes["LIGHT"])

        # Update Sidebar
        self.icon_text_widget.setStyleSheet(f"""
            QWidget {{ background-color: {t['sidebar']}; border-right: 4px solid #000000; }}
            QPushButton {{ background-color: {t['sidebar']}; color: {t['nav_text']}; border: 4px solid transparent; text-align: left; padding: 12px 20px; font-family: 'Space Grotesk'; font-size: 14pt; font-weight: bold; border-radius: 0px; }}
            QPushButton:hover {{ background-color: {t['accent']}; border-bottom: 4px solid #000000; border-right: 4px solid #000000; color: #000000 if t['accent'] != '#002776' else '#FFFFFF'; }}
            QPushButton:checked {{ background-color: #FF5E00; color: #000000; border: 4px solid #000000; }}
        """)
        self.lbl_app_title.setStyleSheet(f"border: none; padding-left: 10px; color: {t['nav_text']}; background: transparent;")

        # Update Main Background
        new_dotted = DOTTED_BG.replace("#F4F1EB", t['bg'])
        if theme_name in ["DARK", "BRASIL", "PORTUGAL"]:
            new_dotted = f'background-image: url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'16\' height=\'16\'><circle cx=\'2\' cy=\'2\' r=\'1.5\' fill=\'%23FFFFFF\' fill-opacity=\'0.15\'/></svg>"); background-color: {t["bg"]}; background-repeat: repeat;'
        self.pages_container.setStyleSheet(new_dotted)

        # Ensure Top Header & Standalone Text are visible over background
        title_color = "#FFFFFF" if theme_name in ["DARK", "BRASIL", "PORTUGAL"] else "#000000"
        self.lbl_header_title.setStyleSheet(f"border: none; color: {title_color}; background: transparent;")
        for text_lbl in self.page_mainapp.findChildren(QLabel, "ThemeText"):
            text_lbl.setStyleSheet(f"border: none; color: {title_color}; background: transparent;")

        # Rigorously update All Base Cards & Text inside them
        for card in self.page_mainapp.findChildren(QFrame, "ThemeCard"):
            card.setStyleSheet(f"QFrame {{ background-color: {t['card_bg']}; border: 5px solid #000000; }}")
            for lbl in card.findChildren(QLabel, "ThemeCardText"):
                lbl.setStyleSheet(f"border: none; color: {t['card_text']}; background: transparent;")

        # Update Input Fields (Dropdowns, LineEdits, TextEdits) so they contrast
        input_bg = "#2C2C2C" if theme_name == "DARK" else "#FFFFFF"
        input_text = "#FFFFFF" if theme_name == "DARK" else "#000000"
        DYNAMIC_INPUT_STYLE = f"""
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {input_bg}; border: 3px solid #000000; padding: 8px; color: {input_text}; font-family: 'JetBrains Mono'; font-weight: bold; selection-background-color: #00FFFF; selection-color: #000000;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{ background-color: #FFFFCC; border: 3px solid #FF5E00; color: #000000; }}
            QComboBox QAbstractItemView {{ background-color: {input_bg}; color: {input_text}; border: 3px solid #000000; }}
        """
        self.inp_search.setStyleSheet(DYNAMIC_INPUT_STYLE)
        self.inp_task.setStyleSheet(DYNAMIC_INPUT_STYLE)
        self.combo_priority.setStyleSheet(DYNAMIC_INPUT_STYLE)
        self.combo_subject.setStyleSheet(DYNAMIC_INPUT_STYLE)
        self.combo_chapter.setStyleSheet(DYNAMIC_INPUT_STYLE)
        self.combo_diff.setStyleSheet(DYNAMIC_INPUT_STYLE)
        self.txt_upload_q.setStyleSheet(DYNAMIC_INPUT_STYLE)

    def pick_custom_color_sidebar(self):
        col = QColorDialog.getColor(Qt.white, self, "Pick Custom Sidebar Base")
        if col.isValid():
            hex_code = col.name()
            text_col = "#000000" if col.lightness() > 128 else "#FFFFFF"
            self.icon_text_widget.setStyleSheet(f"""
                QWidget {{ background-color: {hex_code}; border-right: 4px solid #000000; }}
                QPushButton {{ background-color: {hex_code}; color: {text_col}; border: 4px solid transparent; text-align: left; padding: 12px 20px; font-family: 'Space Grotesk'; font-size: 14pt; font-weight: bold; border-radius: 0px; }}
                QPushButton:hover {{ background-color: #FFFF00; border-bottom: 4px solid #000000; border-right: 4px solid #000000; color: #000000; }}
                QPushButton:checked {{ background-color: #FF5E00; color: #000000; border: 4px solid #000000; }}
            """)
            self.lbl_app_title.setStyleSheet(f"border: none; padding-left: 10px; color: {text_col}; background: transparent;")

    def pick_custom_color_cards(self):
        col = QColorDialog.getColor(Qt.white, self, "Pick Base Card Override")
        if col.isValid():
            for card in self.page_mainapp.findChildren(QFrame, "ThemeCard"):
                card.setStyleSheet(f"QFrame {{ background-color: {col.name()}; border: 5px solid #000000; }}")

    def pick_custom_color_accent(self):
        col = QColorDialog.getColor(Qt.white, self, "Pick Primary Button Highlight Override")
        if col.isValid():
            global BASE_BTN_STYLE
            BASE_BTN_STYLE = BASE_BTN_STYLE.replace("background-color: #FFFF00;", f"background-color: {col.name()};")
            self.btn_upload.setStyleSheet(BASE_BTN_STYLE)
            self.btn_add_task.setStyleSheet(BASE_BTN_STYLE)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.drawer_open:
            parent_rect = self.page_mainapp.rect()
            self.answer_drawer.setGeometry(parent_rect.width() - 500, 0, 500, parent_rect.height())

# ==========================================
# --- APPLICATION ENTRY POINT ---
# ==========================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MySideBar()
    window.show()
    sys.exit(app.exec())
import sys
from PySide6.QtWidgets import QMainWindow, QPushButton, QFrame, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup, QTimer
from PySide6.QtGui import QFont, QCursor
from ui_index import Ui_MainWindow, add_shadow, BASE_BTN_STYLE

# Dummy data referencing user's provided dictionary
SUBJECTS = {
    "PHYSICS": [
        "Electric Charges and Fields", "Electrostatic Potential and Capacitance",
        "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter",
        "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves",
        "Ray Optics and Optical Instruments", "Wave Optics", "Dual Nature of Radiation and Matter",
        "Atoms", "Nuclei", "Semiconductor Electronics"
    ],
    "CHEMISTRY": [
        "Solutions", "Electrochemistry", "Chemical Kinetics", "d and f Block Elements",
        "Coordination Compounds", "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers",
        "Aldehydes, Ketones and Carboxylic Acids", "Amines", "Biomolecules"
    ],
    "MATHEMATICS": [
        "Relations and Functions", "Inverse Trigonometric Functions", "Matrices",
        "Determinants", "Continuity and Differentiability", "Application of Derivatives",
        "Integrals", "Application of Integrals", "Differential Equations", "Vector Algebra",
        "Three Dimensional Geometry", "Linear Programming", "Probability"
    ],
    "ENGLISH": [
        "The Last Lesson", "Lost Spring", "Deep Water", "The Rattrap", "Indigo",
        "Poets and Pancakes", "The Interview", "Going Places", "My Mother at Sixty-Six",
        "Keeping Quiet", "A Thing of Beauty", "A Roadside Stand", "Aunt Jennifer's Tigers",
        "The Third Level", "The Tiger King", "Journey to the End of the Earth", "The Enemy",
        "On the Face of It", "Memories of Childhood"
    ],
    "COMP SCI": [
        "Functions", "Recursion", "File Handling", "Binary Files", "CSV Files",
        "Exception Handling", "Database Concepts", "SQL Queries", "DDL Commands",
        "DML Commands", "Aggregate Functions", "GROUP BY", "ORDER BY", "JOINS",
        "Computer Networks", "Network Devices", "Protocols", "TCP/IP", "HTTP",
        "SMTP", "FTP", "URL", "Web Services"
    ]
}

# Dummy questions
MOCK_QUESTIONS = [
    {"q": "What is the formula for Force?", "a": "Force = mass x acceleration (F = ma)", "diff": "EASY"},
    {"q": "Explain the concept of specific heat.", "a": "Specific heat is the amount of heat energy required to raise the temperature of a substance per unit of mass.", "diff": "MODERATE"},
    {"q": "Derive the kinematic equations of motion.", "a": "v = u + at\ns = ut + 1/2 at^2\nv^2 = u^2 + 2as\n\nDerived using calculus by integrating acceleration...", "diff": "HARD"}
]

class MySideBar(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Aristeia Academy")
        
        self.sidebar_expanded = True
        self.drawer_open = False
        
        # Connect Signals
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_logout.clicked.connect(self.handle_logout)
        
        self.btn_nav_home.clicked.connect(self.switch_to_home)
        self.btn_nav_dashboard.clicked.connect(self.switch_to_dashboard)
        self.btn_nav_schedule.clicked.connect(self.switch_to_schedule)
        self.btn_nav_settings.clicked.connect(self.switch_to_settings)
        
        self.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar)
        self.btn_drawer_close.clicked.connect(self.close_drawer)
        
        # Route subjects to chapters
        for sub_name, btn in self.subject_btns.items():
            btn.clicked.connect(lambda checked=False, name=sub_name: self.open_subject_chapters(name))
            
        self.btn_back_to_sub.clicked.connect(self.switch_to_home)
        self.btn_back_to_ch.clicked.connect(lambda: self.app_stacked_widget.setCurrentIndex(4)) # Index 4 is Chapters
        
        # Qotd View Answer
        self.btn_qotd_view.clicked.connect(lambda: self.open_drawer(MOCK_QUESTIONS[1])) # Show some question

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

    def switch_to_home(self):
        self.app_stacked_widget.setCurrentIndex(0)
        self.btn_nav_home.setChecked(True)
        self.close_drawer()

    def switch_to_dashboard(self):
        self.app_stacked_widget.setCurrentIndex(1)
        self.btn_nav_dashboard.setChecked(True)
        self.close_drawer()

    def switch_to_schedule(self):
        self.app_stacked_widget.setCurrentIndex(2)
        self.btn_nav_schedule.setChecked(True)
        self.close_drawer()

    def switch_to_settings(self):
        self.app_stacked_widget.setCurrentIndex(3)
        self.btn_nav_settings.setChecked(True)
        self.close_drawer()
        
    def open_subject_chapters(self, subject_name):
        self.lbl_ch_title.setText(f"SUBJECT: {subject_name}")
        
        # Clear existing chapters
        for i in reversed(range(self.lay_ch_grid.count())): 
            widget = self.lay_ch_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                
        chapters = SUBJECTS.get(subject_name, [])
        row, col = 0, 0
        for chapter in chapters:
            btn = QPushButton(chapter)
            btn.setMinimumHeight(80)
            btn.setFont(QFont("Space Grotesk", 12, QFont.Bold))
            btn.setStyleSheet(BASE_BTN_STYLE)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn, 4, 4)
            btn.clicked.connect(lambda checked=False, ch=chapter: self.open_questions(ch))
            self.lay_ch_grid.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        self.app_stacked_widget.setCurrentIndex(4) # Switch to Chapters
        self.btn_nav_home.setChecked(False) # Uncheck nav bars

    def open_questions(self, chapter_name):
        self.lbl_q_title.setText(f"CHAPTER: {chapter_name}")
        
        # Clear existing questions
        for i in reversed(range(self.lay_q_list.count())): 
            widget = self.lay_q_list.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        for q_data in MOCK_QUESTIONS:
            q_card = QFrame()
            q_card.setStyleSheet("QFrame { background-color: #FFFFFF; border: 4px solid #000; }")
            add_shadow(q_card, 4, 4)
            qlay = QHBoxLayout(q_card)
            
            lbl = QLabel(q_data["q"])
            lbl.setFont(QFont("JetBrains Mono", 12))
            lbl.setWordWrap(True)
            lbl.setStyleSheet("border:none; color: #000;")
            
            diff_color = "#FFD700" if q_data["diff"] == "MODERATE" else ("#00FFFF" if q_data["diff"] == "EASY" else "#FF69B4")
            lbl_diff = QLabel(q_data["diff"])
            lbl_diff.setFont(QFont("Space Grotesk", 10, QFont.Bold))
            lbl_diff.setStyleSheet(f"background: {diff_color}; border: 2px solid #000; padding: 5px;")
            
            btn_view = QPushButton("VIEW ->")
            btn_view.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#8A2BE2") + "QPushButton{color:white;}")
            btn_view.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn_view, 2, 2)
            btn_view.clicked.connect(lambda checked=False, q=q_data: self.open_drawer(q))
            
            qlay.addWidget(lbl, 1)
            qlay.addWidget(lbl_diff)
            qlay.addWidget(btn_view)
            self.lay_q_list.addWidget(q_card)
            
        # Add stretch so they stick to top
        self.lay_q_list.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.app_stacked_widget.setCurrentIndex(5) # Switch to Questions

    def open_drawer(self, q_data):
        self.lbl_drawer_diff.setText(f"Difficulty: {q_data['diff']}")
        diff_color = "#FFD700" if q_data["diff"] == "MODERATE" else ("#00FFFF" if q_data["diff"] == "EASY" else "#FF69B4")
        self.lbl_drawer_diff.setStyleSheet(f"background: {diff_color}; border: 2px solid #000; padding: 5px;")
        
        self.txt_drawer_answer.setText(f"QUESTION:\n{q_data['q']}\n\nANSWER:\n{q_data['a']}")
        
        if not self.drawer_open:
            self.answer_drawer.show()
            self.answer_drawer.raise_()
            
            # Animate from right
            parent_rect = self.page_mainapp.rect()
            start_rect = QRect(parent_rect.width(), 0, 400, parent_rect.height())
            end_rect = QRect(parent_rect.width() - 400, 0, 400, parent_rect.height())
            
            self.anim = QPropertyAnimation(self.answer_drawer, b"geometry")
            self.anim.setDuration(300)
            self.anim.setStartValue(start_rect)
            self.anim.setEndValue(end_rect)
            self.anim.setEasingCurve(QEasingCurve.OutExpo)
            self.anim.start()
            self.drawer_open = True

    def close_drawer(self):
        if self.drawer_open:
            parent_rect = self.page_mainapp.rect()
            start_rect = QRect(parent_rect.width() - 400, 0, 400, parent_rect.height())
            end_rect = QRect(parent_rect.width(), 0, 400, parent_rect.height())
            
            self.anim = QPropertyAnimation(self.answer_drawer, b"geometry")
            self.anim.setDuration(300)
            self.anim.setStartValue(start_rect)
            self.anim.setEndValue(end_rect)
            self.anim.setEasingCurve(QEasingCurve.InExpo)
            self.anim.finished.connect(self.answer_drawer.hide)
            self.anim.start()
            self.drawer_open = False

    def toggle_sidebar(self):
        # We just hide/show the text widget
        if self.sidebar_expanded:
            self.icon_text_widget.hide()
            self.sidebar_expanded = False
        else:
            self.icon_text_widget.show()
            self.sidebar_expanded = True
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Keep drawer constrained to right side dynamically if open
        if self.drawer_open:
            parent_rect = self.page_mainapp.rect()
            self.answer_drawer.setGeometry(parent_rect.width() - 400, 0, 400, parent_rect.height())

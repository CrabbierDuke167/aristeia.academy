# -*- coding: utf-8 -*-

from PySide6.QtCore import (QCoreApplication, QSize, Qt, QRect, QPropertyAnimation, QEasingCurve)
from PySide6.QtGui import (QColor, QFont, QIcon, QPixmap, QCursor)
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
                               QVBoxLayout, QWidget, QFrame, QScrollArea, QComboBox, QTextEdit,
                               QProgressBar, QGraphicsDropShadowEffect, QListWidget, QListWidgetItem)

try:
    import resources_rc
except ImportError:
    pass  # We assume resources are compiled or will be compiled by the user

# --- Helper Functions for Neo-Brutalism ---
def add_shadow(widget, x=4, y=4, color="#000000"):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(0)
    shadow.setXOffset(x)
    shadow.setYOffset(y)
    shadow.setColor(QColor(color))
    widget.setGraphicsEffect(shadow)

# Global styles
DOTTED_BG = "background-image: url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='16' height='16'><circle cx='2' cy='2' r='1.5' fill='%23000000' fill-opacity='0.15'/></svg>\"); background-color: #F4F1EB; background-repeat: repeat;"

BASE_BTN_STYLE = """
QPushButton {
    background-color: #FFFFFF;
    color: #000000;
    border: 3px solid #000000;
    padding: 8px 15px;
    font-weight: bold;
    border-radius: 0px;
}
QPushButton:hover {
    background-color: #F0F0F0;
}
QPushButton:pressed {
    background-color: #E0E0E0;
}
"""

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1300, 900)
        MainWindow.setMinimumSize(QSize(1000, 700))
        
        # Central widget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # We will use an outermost stacked widget to switch between Login (0) and Main App (1)
        self.outer_layout = QVBoxLayout(self.centralwidget)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)
        
        self.outer_stacked_widget = QStackedWidget(self.centralwidget)
        self.outer_stacked_widget.setObjectName(u"outer_stacked_widget")
        self.outer_layout.addWidget(self.outer_stacked_widget)
        
        # --- PAGE 0: LOGIN SCREEN ---
        self.page_login = QWidget()
        self.page_login.setStyleSheet(DOTTED_BG)
        self.login_layout = QVBoxLayout(self.page_login)
        self.login_layout.setAlignment(Qt.AlignCenter)
        
        self.login_card = QFrame(self.page_login)
        self.login_card.setFixedSize(450, 500)
        self.login_card.setStyleSheet("QFrame { background-color: #FFD700; border: 4px solid #000000; background-image: none; }")
        add_shadow(self.login_card, x=8, y=8)
        
        self.login_card_layout = QVBoxLayout(self.login_card)
        self.login_card_layout.setContentsMargins(40, 40, 40, 40)
        self.login_card_layout.setSpacing(20)
        
        self.lbl_login_title = QLabel("WELCOME TO ARISTEIA")
        font_title = QFont("Space Grotesk", 18, QFont.Bold)
        self.lbl_login_title.setFont(font_title)
        self.lbl_login_title.setStyleSheet("border: none; background: transparent; color: #000000;")
        self.lbl_login_title.setAlignment(Qt.AlignCenter)
        self.login_card_layout.addWidget(self.lbl_login_title)
        
        self.inp_username = QLineEdit()
        self.inp_username.setPlaceholderText("USERNAME")
        self.inp_username.setMinimumHeight(50)
        font_input = QFont("JetBrains Mono", 12)
        self.inp_username.setFont(font_input)
        self.inp_username.setStyleSheet("QLineEdit { background: #FFFFFF; border: 3px solid #000000; padding: 5px; color: #000000; } QLineEdit:focus { background: #E0E0E0; }")
        self.login_card_layout.addWidget(self.inp_username)
        
        self.inp_token = QLineEdit()
        self.inp_token.setPlaceholderText("ACCESS TOKEN")
        self.inp_token.setEchoMode(QLineEdit.Password)
        self.inp_token.setMinimumHeight(50)
        self.inp_token.setFont(font_input)
        self.inp_token.setStyleSheet("QLineEdit { background: #FFFFFF; border: 3px solid #000000; padding: 5px; color: #000000; } QLineEdit:focus { background: #E0E0E0; }")
        self.login_card_layout.addWidget(self.inp_token)
        
        self.lbl_login_error = QLabel("")
        self.lbl_login_error.setStyleSheet("color: #FF0000; font-weight: bold; border: none; background: transparent;")
        self.lbl_login_error.setAlignment(Qt.AlignCenter)
        self.login_card_layout.addWidget(self.lbl_login_error)
        
        self.btn_login = QPushButton("ENTER SYSTEM")
        self.btn_login.setMinimumHeight(60)
        self.btn_login.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        self.btn_login.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#8A2BE2").replace("#F0F0F0", "#9B4DF0").replace("#E0E0E0", "#7A1CD2") + "QPushButton { color: white; }")
        self.btn_login.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_login, 4, 4)
        self.login_card_layout.addWidget(self.btn_login)
        
        self.outer_stacked_widget.addWidget(self.page_login)
        
        # --- PAGE 1: MAIN APP SCREEN ---
        self.page_mainapp = QWidget()
        self.mainapp_layout = QHBoxLayout(self.page_mainapp)
        self.mainapp_layout.setContentsMargins(0, 0, 0, 0)
        self.mainapp_layout.setSpacing(0)
        
        # Sidebar (Icon Text Widget)
        self.icon_text_widget = QWidget(self.page_mainapp)
        self.icon_text_widget.setMinimumSize(QSize(250, 0))
        self.icon_text_widget.setMaximumSize(QSize(250, 16777215))
        self.icon_text_widget.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-right: 4px solid #000000;
            }
            QPushButton {
                background-color: #FFFFFF;
                color: #000000;
                border: 4px solid transparent;
                text-align: left;
                padding: 12px 20px;
                font-family: 'Space Grotesk';
                font-size: 14pt;
                font-weight: bold;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
                border-bottom: 4px solid #000000;
                border-right: 4px solid #000000;
            }
            QPushButton:checked {
                background-color: #FF5E00;
                color: #000000;
                border: 4px solid #000000;
            }
        """)
        
        self.sidebar_layout = QVBoxLayout(self.icon_text_widget)
        self.sidebar_layout.setContentsMargins(10, 30, 10, 20)
        
        self.lbl_app_title = QLabel("ARISTEIA\nACADEMY")
        self.lbl_app_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        self.lbl_app_title.setStyleSheet("border: none; padding-left: 10px;")
        self.sidebar_layout.addWidget(self.lbl_app_title)
        
        self.sidebar_layout.addSpacing(40)
        
        self.btn_nav_home = QPushButton("OVERVIEW")
        self.btn_nav_home.setCheckable(True)
        self.btn_nav_home.setChecked(True)
        self.btn_nav_home.setAutoExclusive(True)
        self.btn_nav_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.btn_nav_home)
        
        self.btn_nav_dashboard = QPushButton("ANALYTICS")
        self.btn_nav_dashboard.setCheckable(True)
        self.btn_nav_dashboard.setAutoExclusive(True)
        self.btn_nav_dashboard.setCursor(QCursor(Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.btn_nav_dashboard)
        
        self.btn_nav_schedule = QPushButton("SCHEDULE")
        self.btn_nav_schedule.setCheckable(True)
        self.btn_nav_schedule.setAutoExclusive(True)
        self.btn_nav_schedule.setCursor(QCursor(Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.btn_nav_schedule)
        
        self.btn_nav_settings = QPushButton("SETTINGS")
        self.btn_nav_settings.setCheckable(True)
        self.btn_nav_settings.setAutoExclusive(True)
        self.btn_nav_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.sidebar_layout.addWidget(self.btn_nav_settings)
        
        self.sidebar_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.btn_logout = QPushButton("LOGOUT")
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #FF69B4;
                color: #000000;
                border: 4px solid #000000;
                text-align: left;
                padding: 12px 20px;
                font-family: 'Space Grotesk';
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF1493;
            }
        """)
        self.btn_logout.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_logout, 4, 4)
        self.sidebar_layout.addWidget(self.btn_logout)
        
        self.mainapp_layout.addWidget(self.icon_text_widget)
        
        # Content Area
        self.content_widget = QWidget(self.page_mainapp)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Header
        self.header_widget = QWidget(self.content_widget)
        self.header_widget.setMinimumHeight(80)
        self.header_widget.setStyleSheet("background-color: #FFFFFF; border-bottom: 4px solid #000000;")
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(20, 10, 20, 10)
        
        self.btn_toggle_sidebar = QPushButton("≡")
        self.btn_toggle_sidebar.setFixedSize(50, 50)
        self.btn_toggle_sidebar.setFont(QFont("JetBrains Mono", 20, QFont.Bold))
        self.btn_toggle_sidebar.setStyleSheet("QPushButton { background-color: #00FFFF; border: 3px solid #000000; } QPushButton:hover { background-color: #00CCCC; }")
        self.btn_toggle_sidebar.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_toggle_sidebar, 3, 3)
        self.header_layout.addWidget(self.btn_toggle_sidebar)
        
        self.header_layout.addSpacing(20)
        
        self.lbl_header_title = QLabel("HELLO, STUDENT!")
        self.lbl_header_title.setFont(QFont("Space Grotesk", 16, QFont.Bold))
        self.lbl_header_title.setStyleSheet("border: none;")
        self.header_layout.addWidget(self.lbl_header_title)
        
        self.header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Search Knowledge Base...")
        self.inp_search.setMinimumSize(250, 45)
        self.inp_search.setFont(QFont("JetBrains Mono", 10))
        self.inp_search.setStyleSheet("QLineEdit { background: #F4F1EB; border: 3px solid #000000; padding: 0 10px; } QLineEdit:focus { background: #FFFFFF; }")
        self.header_layout.addWidget(self.inp_search)
        
        self.btn_search = QPushButton("Q")
        self.btn_search.setFixedSize(45, 45)
        self.btn_search.setFont(QFont("Space Grotesk", 12, QFont.Bold))
        self.btn_search.setStyleSheet("QPushButton { background-color: #FFD700; border: 3px solid #000000; } QPushButton:hover { background-color: #FFC107; }")
        self.btn_search.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_search, 3, 3)
        self.header_layout.addWidget(self.btn_search)
        
        self.content_layout.addWidget(self.header_widget)
        
        # Pages Stacked Widget container
        self.pages_container = QWidget(self.content_widget)
        self.pages_container.setStyleSheet(DOTTED_BG)
        self.pages_layout = QVBoxLayout(self.pages_container)
        self.pages_layout.setContentsMargins(30, 30, 30, 30)
        
        self.app_stacked_widget = QStackedWidget(self.pages_container)
        self.app_stacked_widget.setStyleSheet("QStackedWidget { background: transparent; }")
        self.pages_layout.addWidget(self.app_stacked_widget)
        
        self._setup_page_home()
        self._setup_page_dashboard()
        self._setup_page_schedule()
        self._setup_page_settings()
        self._setup_page_chapters()
        self._setup_page_questions()
        
        self.content_layout.addWidget(self.pages_container)
        self.mainapp_layout.addWidget(self.content_widget)
        
        self.outer_stacked_widget.addWidget(self.page_mainapp)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self._connect_signals()
        
        # Default states
        self.outer_stacked_widget.setCurrentIndex(0)
        self.app_stacked_widget.setCurrentIndex(0)
        
        # Drawer for Questions (Overlay on main page)
        self.answer_drawer = QFrame(self.page_mainapp)
        self.answer_drawer.setFixedWidth(400)
        self.answer_drawer.setStyleSheet("background-color: #FFFFFF; border-left: 5px solid #000000; border-bottom: 5px solid #000;")
        add_shadow(self.answer_drawer, -5, 5) # shadow to the left since it slides from right
        self.answer_drawer.hide()
        
        self.drawer_layout = QVBoxLayout(self.answer_drawer)
        self.drawer_layout.setContentsMargins(20, 20, 20, 20)
        self.drawer_layout.setSpacing(15)
        
        self.drawer_header_layout = QHBoxLayout()
        self.lbl_drawer_title = QLabel("ANSWER / DETAILS")
        self.lbl_drawer_title.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        self.lbl_drawer_title.setStyleSheet("border: none; color: #000000;")
        self.btn_drawer_close = QPushButton("X")
        self.btn_drawer_close.setFixedSize(40, 40)
        self.btn_drawer_close.setStyleSheet("QPushButton{background-color: #FF0000; color: #FFF; border: 3px solid #000; font-weight: bold;} QPushButton:hover{background-color: #CC0000;}")
        self.btn_drawer_close.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_drawer_close, 2, 2)
        
        self.drawer_header_layout.addWidget(self.lbl_drawer_title)
        self.drawer_header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.drawer_header_layout.addWidget(self.btn_drawer_close)
        self.drawer_layout.addLayout(self.drawer_header_layout)
        
        self.lbl_drawer_diff = QLabel("Difficulty: MEDIUM")
        self.lbl_drawer_diff.setFont(QFont("JetBrains Mono", 10, QFont.Bold))
        self.lbl_drawer_diff.setStyleSheet("background: #FFD700; border: 2px solid #000; padding: 5px;")
        self.drawer_layout.addWidget(self.lbl_drawer_diff)
        
        self.txt_drawer_answer = QTextEdit()
        self.txt_drawer_answer.setReadOnly(True)
        self.txt_drawer_answer.setFont(QFont("JetBrains Mono", 11))
        self.txt_drawer_answer.setStyleSheet("QTextEdit{background: #F4F1EB; border: 3px solid #000000; padding: 10px;}")
        self.drawer_layout.addWidget(self.txt_drawer_answer)
        
        self.drawer_actions_layout = QHBoxLayout()
        self.btn_drawer_edit = QPushButton("EDIT")
        self.btn_drawer_edit.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_drawer_edit.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_drawer_edit, 3, 3)
        self.btn_drawer_delete = QPushButton("DELETE")
        self.btn_drawer_delete.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF69B4"))
        self.btn_drawer_delete.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_drawer_delete, 3, 3)
        self.drawer_actions_layout.addWidget(self.btn_drawer_edit)
        self.drawer_actions_layout.addWidget(self.btn_drawer_delete)
        self.drawer_layout.addLayout(self.drawer_actions_layout)

    def _setup_page_home(self):
        self.page_home = QWidget()
        self.page_home.setStyleSheet("background: transparent;")
        self.home_layout = QGridLayout(self.page_home)
        self.home_layout.setContentsMargins(0, 0, 0, 0)
        self.home_layout.setSpacing(25)
        
        # QotD Card
        self.card_qotd = QFrame()
        self.card_qotd.setStyleSheet("QFrame { background-color: #8A2BE2; border: 4px solid #000000; }")
        add_shadow(self.card_qotd, 6, 6)
        lay_qotd = QVBoxLayout(self.card_qotd)
        lbl_qotd_title = QLabel("QUESTION OF THE DAY")
        lbl_qotd_title.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        lbl_qotd_title.setStyleSheet("color: #FFF; border: none;")
        self.lbl_qotd_text = QLabel("Loading from MySQL...")
        self.lbl_qotd_text.setFont(QFont("JetBrains Mono", 12))
        self.lbl_qotd_text.setStyleSheet("color: #FFF; border: none;")
        self.lbl_qotd_text.setWordWrap(True)
        self.btn_qotd_view = QPushButton("VIEW ANSWER ->")
        self.btn_qotd_view.setStyleSheet(BASE_BTN_STYLE)
        self.btn_qotd_view.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_qotd_view, 3, 3)
        lay_qotd.addWidget(lbl_qotd_title)
        lay_qotd.addWidget(self.lbl_qotd_text, 1)
        lay_qotd.addWidget(self.btn_qotd_view, 0, Qt.AlignRight)
        
        # Quote Card
        self.card_quote = QFrame()
        self.card_quote.setStyleSheet("QFrame { background-color: #FF5E00; border: 4px solid #000000; }")
        add_shadow(self.card_quote, 6, 6)
        lay_quote = QVBoxLayout(self.card_quote)
        lbl_quote_title = QLabel("MOTIVATION")
        lbl_quote_title.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        lbl_quote_title.setStyleSheet("color: #000; border: none;")
        self.lbl_quote_text = QLabel("\"Discipline is choosing between what you want now and what you want most.\"")
        self.lbl_quote_text.setFont(QFont("Space Grotesk", 16, QFont.Bold))
        self.lbl_quote_text.setStyleSheet("color: #000; border: none;")
        self.lbl_quote_text.setWordWrap(True)
        self.lbl_quote_text.setAlignment(Qt.AlignCenter)
        lay_quote.addWidget(lbl_quote_title)
        lay_quote.addWidget(self.lbl_quote_text, 1)
        
        # Upload Card
        self.card_upload = QFrame()
        self.card_upload.setStyleSheet("QFrame { background-color: #FFFFFF; border: 4px solid #000000; }")
        add_shadow(self.card_upload, 6, 6)
        lay_upload = QVBoxLayout(self.card_upload)
        lbl_up_title = QLabel("UPLOAD TO BANK")
        lbl_up_title.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        lbl_up_title.setStyleSheet("border: none; color: #000;")
        
        h_combo = QHBoxLayout()
        self.combo_subject = QComboBox()
        self.combo_subject.addItems(["Physics", "Chemistry", "Mathematics", "English", "Computer Science"])
        self.combo_subject.setStyleSheet("QComboBox { border: 3px solid #000; padding: 5px; background: #FFF; font-family: 'JetBrains Mono'; }")
        self.combo_chapter = QComboBox()
        self.combo_chapter.setStyleSheet("QComboBox { border: 3px solid #000; padding: 5px; background: #FFF; font-family: 'JetBrains Mono'; }")
        self.combo_diff = QComboBox()
        self.combo_diff.addItems(["EASY", "MODERATE", "HARD"])
        self.combo_diff.setStyleSheet("QComboBox { border: 3px solid #000; padding: 5px; background: #FFD700; font-family: 'JetBrains Mono'; font-weight: bold; }")
        h_combo.addWidget(self.combo_subject)
        h_combo.addWidget(self.combo_chapter)
        h_combo.addWidget(self.combo_diff)
        
        self.txt_upload_q = QTextEdit()
        self.txt_upload_q.setPlaceholderText("Enter question text here...")
        self.txt_upload_q.setFont(QFont("JetBrains Mono", 10))
        self.txt_upload_q.setStyleSheet("QTextEdit{border: 3px solid #000; background: #F4F1EB; padding: 5px;}")
        
        self.btn_upload = QPushButton("UPLOAD QUESTION")
        self.btn_upload.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_upload.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_upload, 3, 3)
        
        lay_upload.addWidget(lbl_up_title)
        lay_upload.addLayout(h_combo)
        lay_upload.addWidget(self.txt_upload_q)
        lay_upload.addWidget(self.btn_upload, 0, Qt.AlignRight)
        
        # Subjects Card
        self.card_subjects = QFrame()
        self.card_subjects.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        lay_subjects = QGridLayout(self.card_subjects)
        lay_subjects.setContentsMargins(0, 0, 0, 0)
        lay_subjects.setSpacing(15)
        
        subjects = [
            ("PHYSICS", "#FFD700"),
            ("CHEMISTRY", "#FF69B4"),
            ("MATHEMATICS", "#00FFFF"),
            ("ENGLISH", "#8A2BE2"),
            ("COMP SCI", "#FF5E00")
        ]
        
        self.subject_btns = {}
        row, col = 0, 0
        for name, color in subjects:
            btn = QPushButton(name)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont("Space Grotesk", 14, QFont.Bold))
            style = BASE_BTN_STYLE.replace("#FFFFFF", color)
            if color == "#8A2BE2":
                style += "QPushButton { color: white; }"
            btn.setStyleSheet(style)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn, 5, 5)
            self.subject_btns[name] = btn
            lay_subjects.addWidget(btn, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1
                
        self.home_layout.addWidget(self.card_qotd, 0, 0)
        self.home_layout.addWidget(self.card_quote, 0, 1)
        self.home_layout.addWidget(self.card_upload, 1, 0)
        self.home_layout.addWidget(self.card_subjects, 1, 1)
        
        self.home_layout.setColumnStretch(0, 1)
        self.home_layout.setColumnStretch(1, 1)
        self.home_layout.setRowStretch(0, 1)
        self.home_layout.setRowStretch(1, 2)
        
        self.app_stacked_widget.addWidget(self.page_home)

    def _setup_page_dashboard(self):
        self.page_dash = QWidget()
        self.page_dash.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_dash)
        
        lbl_title = QLabel("PERFORMANCE ANALYTICS")
        lbl_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        lbl_title.setStyleSheet("border: none; color: #000;")
        lay.addWidget(lbl_title)
        
        # XP Bar
        xp_frame = QFrame()
        xp_frame.setStyleSheet("background: #FFF; border: 4px solid #000;")
        add_shadow(xp_frame, 5, 5)
        xp_lay = QVBoxLayout(xp_frame)
        lbl_xp = QLabel("LEVEL 12: SCHOLAR (2450 / 3000 XP)")
        lbl_xp.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
        lbl_xp.setStyleSheet("border:none;")
        self.prog_xp = QProgressBar()
        self.prog_xp.setValue(80)
        self.prog_xp.setTextVisible(False)
        self.prog_xp.setFixedHeight(30)
        self.prog_xp.setStyleSheet("""
            QProgressBar { border: 3px solid #000; background: #F4F1EB; }
            QProgressBar::chunk { background-color: #FF5E00; border-right: 3px solid #000; }
        """)
        xp_lay.addWidget(lbl_xp)
        xp_lay.addWidget(self.prog_xp)
        lay.addWidget(xp_frame)
        
        # Charts Grid
        grid = QGridLayout()
        grid.setSpacing(20)
        for i, color in enumerate(["#8A2BE2", "#00FFFF", "#FFD700", "#FF69B4"]):
            f = QFrame()
            f.setStyleSheet(f"QFrame {{ background: {color}; border: 4px solid #000; }}")
            add_shadow(f, 6, 6)
            flay = QVBoxLayout(f)
            l = QLabel(f"GRAPHIC WIDGET {i+1}\n(Awaiting MySQL)")
            l.setAlignment(Qt.AlignCenter)
            l.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
            if color == "#8A2BE2": l.setStyleSheet("color: white; border: none;")
            else: l.setStyleSheet("color: black; border: none;")
            flay.addWidget(l)
            grid.addWidget(f, i//2, i%2)
            
        lay.addLayout(grid)
        self.app_stacked_widget.addWidget(self.page_dash)

    def _setup_page_schedule(self):
        self.page_sched = QWidget()
        self.page_sched.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_sched)
        
        lbl_title = QLabel("MASTER SCHEDULE")
        lbl_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        lbl_title.setStyleSheet("border: none; color: #000;")
        lay.addWidget(lbl_title)
        
        # Add task area
        f_add = QFrame()
        f_add.setStyleSheet("background: #FFF; border: 4px solid #000;")
        add_shadow(f_add, 5, 5)
        flay = QHBoxLayout(f_add)
        self.inp_task = QLineEdit()
        self.inp_task.setPlaceholderText("NEW TASK...")
        self.inp_task.setFont(QFont("JetBrains Mono", 12))
        self.inp_task.setStyleSheet("border: 3px solid #000; padding: 5px; background: #F4F1EB;")
        self.combo_priority = QComboBox()
        self.combo_priority.addItems(["P1 (HIGH)", "P2 (MED)", "P3 (LOW)"])
        self.combo_priority.setStyleSheet("border: 3px solid #000; padding: 5px; font-weight:bold; font-family:'JetBrains Mono';")
        self.btn_add_task = QPushButton("ADD")
        self.btn_add_task.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_add_task.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_add_task, 3, 3)
        flay.addWidget(self.inp_task, 1)
        flay.addWidget(self.combo_priority)
        flay.addWidget(self.btn_add_task)
        lay.addWidget(f_add)
        
        # Task List
        self.list_tasks = QListWidget()
        self.list_tasks.setStyleSheet("""
            QListWidget { background: transparent; border: none; }
            QListWidget::item { background: #FFFFFF; border: 4px solid #000000; margin-bottom: 15px; padding: 10px; color: #000; }
            QListWidget::item:selected { background: #FFD700; color: #000; }
        """)
        self.list_tasks.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        # Custom painting or delegate would be needed for true shadow on items, 
        # but we use thick margins and borders to fake the brutalist feel here.
        lay.addWidget(self.list_tasks)
        
        self.app_stacked_widget.addWidget(self.page_sched)

    def _setup_page_settings(self):
        self.page_set = QWidget()
        self.page_set.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_set)
        
        lbl_title = QLabel("SYSTEM SETTINGS")
        lbl_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        lbl_title.setStyleSheet("border: none; color: #000;")
        lay.addWidget(lbl_title)
        
        # Theme section
        f_theme = QFrame()
        f_theme.setStyleSheet("background: #FFF; border: 4px solid #000;")
        add_shadow(f_theme, 6, 6)
        lay_th = QVBoxLayout(f_theme)
        lbl_th = QLabel("THEME SELECTOR")
        lbl_th.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        lbl_th.setStyleSheet("border:none;")
        lay_th.addWidget(lbl_th)
        
        h_th = QHBoxLayout()
        self.btn_theme_default = QPushButton("DEFAULT")
        self.btn_theme_default.setStyleSheet(BASE_BTN_STYLE)
        self.btn_theme_custom = QPushButton("CUSTOM COLORS (Pick)")
        self.btn_theme_custom.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF69B4"))
        h_th.addWidget(self.btn_theme_default)
        h_th.addWidget(self.btn_theme_custom)
        h_th.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        lay_th.addLayout(h_th)
        lay.addWidget(f_theme)
        
        # About section
        f_about = QFrame()
        f_about.setStyleSheet("background: #FFD700; border: 4px solid #000;")
        add_shadow(f_about, 6, 6)
        lay_ab = QVBoxLayout(f_about)
        lbl_ab = QLabel("ABOUT US")
        lbl_ab.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        lbl_ab.setStyleSheet("border:none;")
        txt_ab = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.")
        txt_ab.setWordWrap(True)
        txt_ab.setFont(QFont("JetBrains Mono", 11))
        txt_ab.setStyleSheet("border:none;")
        lay_ab.addWidget(lbl_ab)
        lay_ab.addWidget(txt_ab)
        lay.addWidget(f_about)
        
        # Version
        f_ver = QFrame()
        f_ver.setStyleSheet("background: #F4F1EB; border: 4px solid #000; border-style: dashed;")
        lay_ver = QVBoxLayout(f_ver)
        lbl_ver = QLabel("VERSION 1.0.0 | © 2026 ARISTEIA ACADEMY")
        lbl_ver.setAlignment(Qt.AlignCenter)
        lbl_ver.setFont(QFont("JetBrains Mono", 10, QFont.Bold))
        lbl_ver.setStyleSheet("border:none;")
        lay_ver.addWidget(lbl_ver)
        lay.addWidget(f_ver)
        
        lay.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.app_stacked_widget.addWidget(self.page_set)

    def _setup_page_chapters(self):
        self.page_ch = QWidget()
        self.page_ch.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_ch)
        
        h_head = QHBoxLayout()
        self.btn_back_to_sub = QPushButton("<- BACK TO SUBJECTS")
        self.btn_back_to_sub.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_back_to_sub.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_back_to_sub, 3, 3)
        self.lbl_ch_title = QLabel("SUBJECT: ???")
        self.lbl_ch_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        self.lbl_ch_title.setStyleSheet("border: none; color: #000;")
        h_head.addWidget(self.btn_back_to_sub)
        h_head.addSpacing(20)
        h_head.addWidget(self.lbl_ch_title)
        h_head.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        lay.addLayout(h_head)
        
        # Scrollable Area for chapters
        self.scroll_ch = QScrollArea()
        self.scroll_ch.setWidgetResizable(True)
        self.scroll_ch.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.ch_container = QWidget()
        self.ch_container.setStyleSheet("background: transparent;")
        
        # We will populate this grid dynamically in frontPage.py
        self.lay_ch_grid = QGridLayout(self.ch_container)
        self.lay_ch_grid.setSpacing(20)
        
        self.scroll_ch.setWidget(self.ch_container)
        lay.addWidget(self.scroll_ch)
        
        self.app_stacked_widget.addWidget(self.page_ch)

    def _setup_page_questions(self):
        self.page_q = QWidget()
        self.page_q.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_q)
        
        h_head = QHBoxLayout()
        self.btn_back_to_ch = QPushButton("<- BACK TO CHAPTERS")
        self.btn_back_to_ch.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FFD700"))
        self.btn_back_to_ch.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_back_to_ch, 3, 3)
        self.lbl_q_title = QLabel("CHAPTER: ???")
        self.lbl_q_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        self.lbl_q_title.setStyleSheet("border: none; color: #000;")
        h_head.addWidget(self.btn_back_to_ch)
        h_head.addSpacing(20)
        h_head.addWidget(self.lbl_q_title)
        h_head.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        lay.addLayout(h_head)
        
        self.scroll_q = QScrollArea()
        self.scroll_q.setWidgetResizable(True)
        self.scroll_q.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.q_container = QWidget()
        self.q_container.setStyleSheet("background: transparent;")
        
        # We will populate this layout dynamically in frontPage.py
        self.lay_q_list = QVBoxLayout(self.q_container)
        self.lay_q_list.setSpacing(15)
        self.lay_q_list.setAlignment(Qt.AlignTop)
        
        self.scroll_q.setWidget(self.q_container)
        lay.addWidget(self.scroll_q)
        
        self.app_stacked_widget.addWidget(self.page_q)

    def _connect_signals(self):
        pass # Connections will be handled in frontPage.py

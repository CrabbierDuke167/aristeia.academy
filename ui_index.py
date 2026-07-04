# -*- coding: utf-8 -*-
# complied from QtDesigner's human-made design
import sys
from pathlib import Path
from PySide6.QtCore import (QCoreApplication, QSize, Qt, QRect, QPropertyAnimation, QEasingCurve)
from PySide6.QtGui import (QColor, QFont, QIcon, QPixmap, QCursor)
from PySide6.QtWidgets import (QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
                               QVBoxLayout, QWidget, QFrame, QScrollArea, QComboBox, QTextEdit,
                               QProgressBar, QGraphicsDropShadowEffect, QDialog, QVBoxLayout,QHBoxLayout, QSplitter)

try:
    import resources_rc
except ImportError:
    pass  

# Helper Functions for Neo-Brutalism 
def add_shadow(widget, x=4, y=4, color="#000000"):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(0)
    shadow.setXOffset(x)
    shadow.setYOffset(y)
    shadow.setColor(QColor(color))
    widget.setGraphicsEffect(shadow)

# Global Style Constants
DOTTED_BG = 'background-image: url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'16\' height=\'16\'><circle cx=\'2\' cy=\'2\' r=\'1.5\' fill=\'%23000000\' fill-opacity=\'0.15\'/></svg>"); background-color: #F4F1EB; background-repeat: repeat;'

BASE_BTN_STYLE = """
QPushButton {
    background-color: #FFFFFF;
    color: #000000;
    border: 3px solid #000000;
    padding: 8px 15px;
    font-family: 'Space Grotesk';
    font-weight: bold;
    border-radius: 0px;
}
QPushButton:hover { background-color: #D6CFFF; color: #000000; }
QPushButton:pressed { background-color: #FFD700; color: #000000; }
"""

INPUT_STYLE = """
QLineEdit, QTextEdit, QComboBox {
    background-color: #FFFFFF;
    border: 3px solid #000000;
    padding: 8px;
    color: #000000;
    font-family: 'JetBrains Mono';
    font-weight: bold;
    selection-background-color: #00FFFF;
    selection-color: #000000;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    background-color: #FFFFCC;
    border: 3px solid #FF5E00;
}
QComboBox QAbstractItemView { 
    background-color: #FFFFFF; 
    color: #000000; 
    border: 3px solid #000000; 
    selection-background-color: #00FFFF;
    selection-color: #000000;
}
"""

# Custom Neo-Brutalist Popups 
class NeoMessageBox(QDialog):
    def __init__(self, title, message, msg_type="info", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(420, 220)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        bg_color = "#00FFFF" 
        if msg_type == "error": bg_color = "#FF3333"
        elif msg_type == "success": bg_color = "#33FF55"
        elif msg_type == "warning": bg_color = "#FFD700"

        self.setStyleSheet(f"QDialog {{ background-color: {bg_color}; border: 5px solid #000000; }}")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Space Grotesk", 16, QFont.Black))
        lbl_title.setStyleSheet("color: #000000; border: none; background: transparent;")
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_msg = QLabel(message)
        lbl_msg.setFont(QFont("JetBrains Mono", 11, QFont.Bold))
        lbl_msg.setStyleSheet("color: #000000; border: none; background: transparent;")
        lbl_msg.setWordWrap(True)
        lbl_msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_msg, 1)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setFont(QFont("Space Grotesk", 12, QFont.Bold))
        self.btn_ok.setStyleSheet(BASE_BTN_STYLE)
        self.btn_ok.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_ok, 3, 3)
        self.btn_ok.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(btn_layout)
        add_shadow(self, 8, 8)

class NeoEditDialog(QDialog):
    """Custom popup UI for editing tasks and questions."""
    def __init__(self, title, default_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(500, 300)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setStyleSheet("QDialog { background-color: #FFD700; border: 5px solid #000000; }")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        lbl_title = QLabel(title.upper())
        lbl_title.setFont(QFont("Space Grotesk", 16, QFont.Black))
        lbl_title.setStyleSheet("color: #000000; border: none; background: transparent;")
        layout.addWidget(lbl_title)

        self.text_edit = QTextEdit()
        self.text_edit.setText(default_text)
        self.text_edit.setFont(QFont("JetBrains Mono", 11, QFont.Bold))
        self.text_edit.setStyleSheet(INPUT_STYLE)
        layout.addWidget(self.text_edit, 1)

        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("CANCEL")
        self.btn_cancel.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF3333"))
        self.btn_cancel.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_cancel, 3, 3)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("SAVE CHANGES")
        self.btn_save.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#33FF55"))
        self.btn_save.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_save, 3, 3)
        self.btn_save.clicked.connect(self.accept)

        btn_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)
        add_shadow(self, 8, 8)

    def get_text(self):
        return self.text_edit.toPlainText().strip()


# Main Window UI Definition
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1350, 900)
        MainWindow.setMinimumSize(QSize(1050, 700))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.outer_layout = QVBoxLayout(self.centralwidget)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.outer_stacked_widget = QStackedWidget(self.centralwidget)
        self.outer_stacked_widget.setObjectName(u"outer_stacked_widget")
        self.outer_layout.addWidget(self.outer_stacked_widget)

        # ==========================================
        # PAGE 0: LOGIN 
        # ==========================================
        self.page_login = QWidget()
        self.page_login.setStyleSheet(DOTTED_BG)
        self.login_layout = QGridLayout(self.page_login)
        self.login_layout.setContentsMargins(0, 0, 0, 0)

        self.login_card = QFrame(self.page_login)
        self.login_card.setFixedSize(450, 500)
        self.login_card.setStyleSheet("QFrame { background-color: #FFD700; border: 5px solid #000000; background-image: none; }")
        add_shadow(self.login_card, x=10, y=10)

        self.login_card_layout = QVBoxLayout(self.login_card)
        self.login_card_layout.setContentsMargins(40, 40, 40, 40)
        self.login_card_layout.setSpacing(20)

        self.lbl_login_title = QLabel("WELCOME TO ARISTEIA")
        self.lbl_login_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        self.lbl_login_title.setStyleSheet("border: none; background: transparent; color: #000000;")
        self.lbl_login_title.setAlignment(Qt.AlignCenter)
        self.login_card_layout.addWidget(self.lbl_login_title)

        self.inp_username = QLineEdit()
        self.inp_username.setPlaceholderText("USERNAME")
        self.inp_username.setMinimumHeight(50)
        self.inp_username.setStyleSheet(INPUT_STYLE)
        self.login_card_layout.addWidget(self.inp_username)

        self.inp_token = QLineEdit()
        self.inp_token.setPlaceholderText("ACCESS TOKEN")
        self.inp_token.setEchoMode(QLineEdit.Password)
        self.inp_token.setMinimumHeight(50)
        self.inp_token.setStyleSheet(INPUT_STYLE)
        self.login_card_layout.addWidget(self.inp_token)

        self.lbl_login_error = QLabel("")
        self.lbl_login_error.setFont(QFont("JetBrains Mono", 10, QFont.Bold))
        self.lbl_login_error.setStyleSheet("color: #FF0000; background: transparent; border: none;")
        self.lbl_login_error.setAlignment(Qt.AlignCenter)
        self.login_card_layout.addWidget(self.lbl_login_error)

        self.btn_login = QPushButton("LOGIN")
        self.btn_login.setMinimumHeight(60)
        self.btn_login.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        self.btn_login.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#8A2BE2").replace("#FFFF00", "#9B4DF0") + "QPushButton { color: white; }")
        self.btn_login.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_login, 4, 4)
        self.login_card_layout.addWidget(self.btn_login)

        self.login_layout.addWidget(self.login_card, 0, 0, Qt.AlignCenter)
        self.outer_stacked_widget.addWidget(self.page_login)

        # ==========================================
        # PAGE 1: MAIN APPLICATION 
        # ==========================================
        self.page_mainapp = QWidget()
        self.mainapp_layout = QHBoxLayout(self.page_mainapp)
        self.mainapp_layout.setContentsMargins(0, 0, 0, 0)
        self.mainapp_layout.setSpacing(0)

        # Sidebar
        self.icon_text_widget = QWidget(self.page_mainapp)
        self.icon_text_widget.setMinimumSize(QSize(250, 0))
        self.icon_text_widget.setMaximumSize(QSize(250, 16777215))
        self.icon_text_widget.setStyleSheet("""
            QWidget { background-color: #FFFFFF; border-right: 4px solid #000000; }
            QPushButton { background-color: #FFFFFF; color: #000000; border: 4px solid transparent; text-align: left; padding: 12px 20px; font-family: 'Space Grotesk'; font-size: 14pt; font-weight: bold; border-radius: 0px; }
            QPushButton:hover { background-color: #26000000; border-bottom: 4px solid #4D000000; border-right: 4px solid #4D000000; color: #000000; }
            QPushButton:checked { background-color: #FF5E00; color: #000000; border: 4px solid #000000; }
        """)

        self.sidebar_layout = QVBoxLayout(self.icon_text_widget)
        self.sidebar_layout.setContentsMargins(10, 30, 10, 20)

        self.lbl_app_title = QLabel("ARISTEIA\nACADEMY")
        self.lbl_app_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        self.lbl_app_title.setStyleSheet("border: none; padding-left: 10px; color: #000000; background: transparent;")
        self.sidebar_layout.addWidget(self.lbl_app_title)

        self.sidebar_layout.addSpacing(40)

        self.btn_nav_home = QPushButton("HOME")
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
            QPushButton { background-color: #FF3333; color: #000000; border: 4px solid #000000; text-align: left; padding: 12px 20px; font-family: 'Space Grotesk'; font-size: 14pt; font-weight: bold; }
            QPushButton:hover { background-color: #CC0000; color: #000000; }
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
        self.btn_toggle_sidebar.setStyleSheet("QPushButton { background-color: #00FFFF; border: 3px solid #000000; color: #000000; } QPushButton:hover { background-color: #00CCCC; }")
        self.btn_toggle_sidebar.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_toggle_sidebar, 3, 3)
        self.header_layout.addWidget(self.btn_toggle_sidebar)

        self.header_layout.addSpacing(20)

        self.lbl_header_title = QLabel("WELCOME, It is going to be INTRESTING!")
        self.lbl_header_title.setObjectName("ThemeText")
        self.lbl_header_title.setFont(QFont("Space Grotesk", 16, QFont.Bold))
        self.lbl_header_title.setStyleSheet("border: none; background: transparent;")
        self.header_layout.addWidget(self.lbl_header_title)

        self.header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Search for Questions . . .")
        self.inp_search.setMinimumSize(280, 45)
        self.inp_search.setStyleSheet(INPUT_STYLE)
        self.header_layout.addWidget(self.inp_search)

        self.btn_search = QPushButton("Q")
        self.btn_search.setFixedSize(45, 45)
        self.btn_search.setFont(QFont("Space Grotesk", 14, QFont.Bold))
        self.btn_search.setStyleSheet("QPushButton { background-color: #FFD700; border: 3px solid #000000; color: #000000; } QPushButton:hover { background-color: #FFC107; }")
        self.btn_search.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_search, 3, 3)
        self.header_layout.addWidget(self.btn_search)

        self.content_layout.addWidget(self.header_widget)

        # Stacked Widget Container
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


        # ==========================================
        # OVERLAY ANSWER DRAWER 
        # ==========================================
        self.answer_drawer = QFrame(self.page_mainapp)
        self.answer_drawer.setFixedWidth(500)
        self.answer_drawer.setStyleSheet("QFrame { background-color: #FFFFFF; border-left: 5px solid #000000; border-bottom: 5px solid #000000; }")
        add_shadow(self.answer_drawer, -6, 6)
        self.answer_drawer.hide()

        self.drawer_layout = QVBoxLayout(self.answer_drawer)
        self.drawer_layout.setContentsMargins(20, 20, 20, 20)
        self.drawer_layout.setSpacing(15)

        self.drawer_header_layout = QHBoxLayout()
        self.lbl_drawer_title = QLabel("QUESTION DETAILS")
        self.lbl_drawer_title.setFont(QFont("Space Grotesk", 14, QFont.Black))
        self.lbl_drawer_title.setStyleSheet("border: none; color: #000000; background: transparent;")
        
        self.btn_drawer_close = QPushButton("X")
        self.btn_drawer_close.setFixedSize(40, 40)
        self.btn_drawer_close.setFont(QFont("Space Grotesk", 12, QFont.Black))
        self.btn_drawer_close.setStyleSheet("QPushButton { background-color: #FF3333; color: #FFFFFF; border: 3px solid #000000; } QPushButton:hover { background-color: #CC0000; }")
        self.btn_drawer_close.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_drawer_close, 2, 2)

        self.drawer_header_layout.addWidget(self.lbl_drawer_title)
        self.drawer_header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.drawer_header_layout.addWidget(self.btn_drawer_close)
        self.drawer_layout.addLayout(self.drawer_header_layout)

        self.lbl_drawer_diff = QLabel("DIFFICULTY: MODERATE")
        self.lbl_drawer_diff.setFont(QFont("Space Grotesk", 10, QFont.Bold))
        self.lbl_drawer_diff.setStyleSheet("background: #FFD700; border: 3px solid #000000; padding: 6px; color: #000000;")
        self.drawer_layout.addWidget(self.lbl_drawer_diff)

        self.drawer_splitter = QSplitter(Qt.Vertical)
        self.drawer_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #000000;
                height: 4px;
                margin: 4px 0px;
            }
        """)

        self.card_drawer_q = QFrame()
        self.card_drawer_q.setStyleSheet("QFrame { background-color: #F4F1EB; border: 3px solid #000000; }")
        lay_q = QVBoxLayout(self.card_drawer_q)
        lbl_q_head = QLabel("QUESTION:")
        lbl_q_head.setFont(QFont("Space Grotesk", 10, QFont.Bold))
        lbl_q_head.setStyleSheet("color: #555555; border: none; background: transparent;")
        lay_q.addWidget(lbl_q_head)

        self.scroll_q = QScrollArea()
        self.scroll_q.setWidgetResizable(True)
        self.scroll_q.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_q.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_q.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.lbl_drawer_question = QLabel("Question text goes here...")
        self.lbl_drawer_question.setWordWrap(True)
        self.lbl_drawer_question.setFont(QFont("JetBrains Mono", 11, QFont.Bold))
        self.lbl_drawer_question.setStyleSheet("color: #000000; border: none; background: transparent;")
        self.lbl_drawer_question.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.scroll_q.setWidget(self.lbl_drawer_question)
        lay_q.addWidget(self.scroll_q)

        self.card_drawer_a = QFrame()
        self.card_drawer_a.setStyleSheet("QFrame { background-color: #FFFFFF; border: 3px solid #000000; }")
        lay_a = QVBoxLayout(self.card_drawer_a)
        lbl_a_head = QLabel("ANSWER (Edit below, auto-saves on close):")
        lbl_a_head.setFont(QFont("Space Grotesk", 10, QFont.Bold))
        lbl_a_head.setStyleSheet("color: #555555; border: none; background: transparent;")
        
        self.txt_drawer_answer = QTextEdit()
        self.txt_drawer_answer.setFont(QFont("JetBrains Mono", 11))
        self.txt_drawer_answer.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_drawer_answer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.txt_drawer_answer.setStyleSheet("QTextEdit { border: none; background: transparent; color: #000000; } QTextEdit:focus { background: #FFFFCC; }")
        
        lay_a.addWidget(lbl_a_head)
        lay_a.addWidget(self.txt_drawer_answer)

        self.drawer_splitter.addWidget(self.card_drawer_q)
        self.drawer_splitter.addWidget(self.card_drawer_a)
        self.drawer_splitter.setSizes([250, 250])
        self.drawer_layout.addWidget(self.drawer_splitter)

        self.drawer_actions_layout = QHBoxLayout()
        self.btn_drawer_edit = QPushButton("EDIT QUESTION")
        self.btn_drawer_edit.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_drawer_edit.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_drawer_edit, 3, 3)

        self.btn_drawer_delete = QPushButton("DELETE")
        self.btn_drawer_delete.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF3333") + "QPushButton { color: white; }")
        self.btn_drawer_delete.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_drawer_delete, 3, 3)

        self.drawer_actions_layout.addWidget(self.btn_drawer_edit)
        self.drawer_actions_layout.addWidget(self.btn_drawer_delete)
        self.drawer_layout.addLayout(self.drawer_actions_layout)


    # ==========================================
    # INDIVIDUAL SECTION SETUPS
    # ==========================================
    def _setup_page_home(self):
        self.page_home = QWidget()
        self.page_home.setStyleSheet("background: transparent;")
        self.home_layout = QGridLayout(self.page_home)
        self.home_layout.setContentsMargins(0, 0, 0, 0)
        self.home_layout.setSpacing(25)

        self.card_qotd = QFrame()
        self.card_qotd.setObjectName("ThemeCard")
        self.card_qotd.setStyleSheet("QFrame { background-color: #8A2BE2; border: 5px solid #000000; }")
        add_shadow(self.card_qotd, 6, 6)
        lay_qotd = QVBoxLayout(self.card_qotd)
        lbl_qotd_title = QLabel("QUESTION OF THE DAY")
        lbl_qotd_title.setObjectName("ThemeCardText")
        lbl_qotd_title.setFont(QFont("Space Grotesk", 14, QFont.Black))
        lbl_qotd_title.setStyleSheet("border: none; background: transparent;")
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.lbl_qotd_text = QLabel("Loading QOTD...")
        self.lbl_qotd_text.setObjectName("ThemeCardText")
        self.lbl_qotd_text.setFont(QFont("JetBrains Mono", 11))
        self.lbl_qotd_text.setStyleSheet("border: none; background: transparent; font-weight: 600;")
        self.lbl_qotd_text.setWordWrap(True)
        scroll_area.setWidget(self.lbl_qotd_text)
        self.btn_qotd_view = QPushButton("VIEW ANSWER ⟶")
        self.btn_qotd_view.setStyleSheet(BASE_BTN_STYLE)
        self.btn_qotd_view.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_qotd_view, 3, 3)
        lay_qotd.addWidget(lbl_qotd_title)
        lay_qotd.addWidget(scroll_area, 1)
        lay_qotd.addWidget(self.btn_qotd_view, 0, Qt.AlignRight)

        self.card_quote = QFrame()
        self.card_quote.setObjectName("ThemeCard")
        self.card_quote.setStyleSheet("QFrame { background-color: #FF5E00; border: 5px solid #000000; }")
        add_shadow(self.card_quote, 6, 6)
        lay_quote = QVBoxLayout(self.card_quote)
        lbl_quote_title = QLabel("THE ETHOS")
        lbl_quote_title.setObjectName("ThemeCardText")
        lbl_quote_title.setFont(QFont("Space Grotesk", 14, QFont.Black))
        lbl_quote_title.setStyleSheet("border: none; background: transparent;")
        self.lbl_quote_text = QLabel('"Excellence isn\'t a feeling you wait for;\n it is an infrastructure you build. Log the questions,\n track the failures, and outwork the curriculum."')
        self.lbl_quote_text.setObjectName("ThemeCardText")
        self.lbl_quote_text.setFont(QFont("Space Grotesk", 16, QFont.Black))
        self.lbl_quote_text.setStyleSheet("border: none; background: transparent;")
        self.lbl_quote_text.setWordWrap(True)
        self.lbl_quote_text.setAlignment(Qt.AlignCenter)
        lay_quote.addWidget(lbl_quote_title)
        lay_quote.addWidget(self.lbl_quote_text, 1)

        self.card_upload = QFrame()
        self.card_upload.setObjectName("ThemeCard")
        self.card_upload.setStyleSheet("QFrame { background-color: #FFFFFF; border: 5px solid #000000; }")
        add_shadow(self.card_upload, 6, 6)
        lay_upload = QVBoxLayout(self.card_upload)
        lay_upload.setSpacing(12)
        lbl_up_title = QLabel("UPLOAD PORTAL")
        lbl_up_title.setObjectName("ThemeCardText")
        lbl_up_title.setFont(QFont("Space Grotesk", 14, QFont.Black))
        lbl_up_title.setStyleSheet("border: none; background: transparent;")

        h_combo = QHBoxLayout()
        self.combo_subject = QComboBox()
        self.combo_subject.addItems(["Physics", "Chemistry", "Mathematics", "English", "Computer Science"])
        self.combo_subject.setStyleSheet(INPUT_STYLE)
        self.combo_chapter = QComboBox()
        self.combo_chapter.setStyleSheet(INPUT_STYLE)
        self.combo_diff = QComboBox()
        self.combo_diff.addItems(["EASY", "MODERATE", "HARD"])
        self.combo_diff.setStyleSheet(INPUT_STYLE)
        
        h_combo.addWidget(self.combo_subject, 2)
        h_combo.addWidget(self.combo_chapter, 3)
        h_combo.addWidget(self.combo_diff, 1)

        self.txt_upload_q = QTextEdit()
        self.txt_upload_q.setPlaceholderText("Enter question and answer here...\nQ: What is Planck's constant?\nA: 6.626 x 10^-34 J.s")
        self.txt_upload_q.setStyleSheet(INPUT_STYLE)

        self.btn_upload = QPushButton("UPLOAD QUESTION")
        self.btn_upload.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_upload.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_upload, 3, 3)

        lay_upload.addWidget(lbl_up_title)
        lay_upload.addLayout(h_combo)
        lay_upload.addWidget(self.txt_upload_q, 1)
        lay_upload.addWidget(self.btn_upload, 0, Qt.AlignRight)

        self.card_subjects = QFrame()
        self.card_subjects.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        lay_subjects = QGridLayout(self.card_subjects)
        lay_subjects.setContentsMargins(0, 0, 0, 0)
        lay_subjects.setSpacing(15)

        subjects_matrix = [("PHYSICS", "#FFD700"), ("CHEMISTRY", "#FF69B4"), ("MATHEMATICS", "#00FFFF"), ("ENGLISH", "#8A2BE2"), ("COMP SCI", "#FF5E00")]
        self.subject_btns = {}
        row, col = 0, 0
        for name, color in subjects_matrix:
            btn = QPushButton(name)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setFont(QFont("Space Grotesk", 15, QFont.Black))
            style = BASE_BTN_STYLE.replace("#FFFFFF", color)
            if color == "#8A2BE2": style += "QPushButton { color: white; }"
            btn.setStyleSheet(style)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn, 5, 5)
            self.subject_btns[name] = btn
            lay_subjects.addWidget(btn, row, col)
            col += 1
            if col > 1: col = 0; row += 1

        self.home_layout.addWidget(self.card_qotd, 0, 0)
        self.home_layout.addWidget(self.card_quote, 0, 1)
        self.home_layout.addWidget(self.card_upload, 1, 0)
        self.home_layout.addWidget(self.card_subjects, 1, 1)
        self.home_layout.setRowStretch(0, 1)
        self.home_layout.setRowStretch(1, 2)
        self.app_stacked_widget.addWidget(self.page_home)

    def _setup_page_dashboard(self):
        self.page_dash = QWidget()
        self.page_dash.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_dash)
        lay.setSpacing(15)

        lbl_title = QLabel("PERFORMANCE ANALYTICS")
        lbl_title.setObjectName("ThemeText")
        lbl_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        lbl_title.setStyleSheet("border: none; background: transparent;")
        lay.addWidget(lbl_title)

        self.xp_frame = QFrame()
        self.xp_frame.setObjectName("ThemeCard")
        self.xp_frame.setStyleSheet("QFrame { background: #FFFFFF; border: 4px solid #000000; }")
        add_shadow(self.xp_frame, 4, 4)
        xp_lay = QVBoxLayout(self.xp_frame)
        xp_lay.setContentsMargins(15, 10, 15, 10)
        
        lbl_xp = QLabel("LEVEL 12: SCHOLAR (2,450 / 3,000 XP)")
        lbl_xp.setObjectName("ThemeCardText")
        lbl_xp.setFont(QFont("JetBrains Mono", 11, QFont.Bold))
        lbl_xp.setStyleSheet("border: none; background: transparent;")
        
        self.prog_xp = QProgressBar()
        self.prog_xp.setValue(82)
        self.prog_xp.setTextVisible(False)
        self.prog_xp.setFixedHeight(12) 
        self.prog_xp.setStyleSheet("""
            QProgressBar { border: 2px solid #000000; background: #F4F1EB; }
            QProgressBar::chunk { background-color: #FF5E00; border-right: 2px solid #000000; }
        """)
        xp_lay.addWidget(lbl_xp)
        xp_lay.addWidget(self.prog_xp)
        lay.addWidget(self.xp_frame)

        grid = QGridLayout()
        grid.setSpacing(20)
        self.chart_widgets = []
        chart_colors = ["#8A2BE2", "#00FFFF", "#FFD700", "#FF69B4"]
        titles = ["DIFFICULTY LEVELS", "CHAPTER MASTERY", "ATTEMPT PERCENTAGE", "SESSION CLOCK"]

        for i in range(4):
            f = QFrame()
            f.setObjectName("GraphCard") 
            f.setStyleSheet(f"QFrame {{ background: {chart_colors[i]}; border: 5px solid #000000; }}")
            add_shadow(f, 6, 6)
            flay = QVBoxLayout(f)
            flay.setContentsMargins(10, 10, 10, 10)
            
            l = QLabel(titles[i])
            l.setAlignment(Qt.AlignCenter)
            l.setFont(QFont("Space Grotesk", 12, QFont.Black))
            l.setStyleSheet("color: #FFFFFF; border: none; background: transparent;" if chart_colors[i] == "#8A2BE2" else "color: #000000; border: none; background: transparent;")
            flay.addWidget(l)

            chart_target = QWidget()
            chart_target.setStyleSheet("background: #FFFFFF; border: 3px solid #000000;")
            flay.addWidget(chart_target, 1)
            self.chart_widgets.append(chart_target)
            grid.addWidget(f, i // 2, i % 2)

        lay.addLayout(grid, 1)
        self.app_stacked_widget.addWidget(self.page_dash)

    def _setup_page_schedule(self):
        self.page_sched = QWidget()
        self.page_sched.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_sched)
        lay.setSpacing(20)

        lbl_title = QLabel("MASTER SCHEDULE")
        lbl_title.setObjectName("ThemeText")
        lbl_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        lbl_title.setStyleSheet("border: none; background: transparent;")
        lay.addWidget(lbl_title)

        self.f_add = QFrame()
        self.f_add.setObjectName("ThemeCard")
        self.f_add.setStyleSheet("QFrame { background: #FFFFFF; border: 5px solid #000000; }")
        add_shadow(self.f_add, 5, 5)
        flay = QHBoxLayout(self.f_add)
        flay.setContentsMargins(20, 15, 20, 15)
        flay.setSpacing(15)

        self.inp_task = QLineEdit()
        self.inp_task.setPlaceholderText("ENTER NEW TASK . . .")
        self.inp_task.setStyleSheet(INPUT_STYLE)
        
        self.combo_priority = QComboBox()
        self.combo_priority.addItems(["P1 (HIGH)", "P2 (MEDIUM)", "P3 (LOW)"])
        self.combo_priority.setStyleSheet(INPUT_STYLE)
        
        self.btn_add_task = QPushButton("ADD TASK")
        self.btn_add_task.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_add_task.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_add_task, 3, 3)

        flay.addWidget(self.inp_task, 1)
        flay.addWidget(self.combo_priority)
        flay.addWidget(self.btn_add_task)
        lay.addWidget(self.f_add)

        self.scroll_schedule = QScrollArea()
        self.scroll_schedule.setWidgetResizable(True)
        self.scroll_schedule.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        
        self.schedule_container = QWidget()
        self.schedule_container.setStyleSheet("background: transparent;")
        self.schedule_tasks_layout = QVBoxLayout(self.schedule_container)
        self.schedule_tasks_layout.setSpacing(15)
        self.schedule_tasks_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_schedule.setWidget(self.schedule_container)
        lay.addWidget(self.scroll_schedule, 1)
        self.app_stacked_widget.addWidget(self.page_sched)

    def _setup_page_settings(self):
        self.scroll_settings = QScrollArea()
        self.scroll_settings.setWidgetResizable(True)
        self.scroll_settings.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        self.page_set = QWidget()
        self.page_set.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_set)
        lay.setSpacing(30) 

        lbl_title = QLabel("SYSTEM SETTINGS")
        lbl_title.setObjectName("ThemeText")
        lbl_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        lbl_title.setStyleSheet("border: none; background: transparent;")
        lay.addWidget(lbl_title)

        self.f_theme = QFrame()
        self.f_theme.setObjectName("ThemeCard")
        self.f_theme.setStyleSheet("QFrame { background: #FFFFFF; border: 5px solid #000000; }")
        add_shadow(self.f_theme, 6, 6)
        lay_th = QVBoxLayout(self.f_theme)
        lay_th.setContentsMargins(25, 25, 25, 25)
        lay_th.setSpacing(20)

        lbl_th_head = QLabel("THEME SWITCHER")
        lbl_th_head.setObjectName("ThemeCardText")
        lbl_th_head.setFont(QFont("Space Grotesk", 15, QFont.Black))
        lbl_th_head.setStyleSheet("border: none; background: transparent;")
        lay_th.addWidget(lbl_th_head)

        h_th = QHBoxLayout()
        h_th.setSpacing(15)
        self.btn_theme_light = QPushButton("LIGHT")
        self.btn_theme_light.setStyleSheet(BASE_BTN_STYLE)
        self.btn_theme_dark = QPushButton("DARK")
        self.btn_theme_dark.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#625C5C"))
        self.btn_theme_arg = QPushButton("ARGENTINA")
        self.btn_theme_arg.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#74ACDF"))
        self.btn_theme_bra = QPushButton("BRASIL")
        self.btn_theme_bra.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#009C3B") + "QPushButton { color: #FEDD00; }")
        self.btn_theme_por = QPushButton("PORTUGAL")
        self.btn_theme_por.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF0000") + "QPushButton { color: #FFFFFF; }")

        for b in [self.btn_theme_light, self.btn_theme_dark, self.btn_theme_arg, self.btn_theme_bra, self.btn_theme_por]:
            b.setCursor(QCursor(Qt.PointingHandCursor))
            b.setMinimumHeight(45)
            add_shadow(b, 3, 3)
            h_th.addWidget(b)
        lay_th.addLayout(h_th)

        lbl_custom_head = QLabel("CUSTOM COLORS:")
        lbl_custom_head.setObjectName("ThemeCardText")
        lbl_custom_head.setFont(QFont("Space Grotesk", 11, QFont.Bold))
        lbl_custom_head.setStyleSheet("border: none; background: transparent;")
        lay_th.addWidget(lbl_custom_head)

        h_custom = QHBoxLayout()
        h_custom.setSpacing(15)
        self.btn_custom_sidebar = QPushButton("PICK NAV BAR")
        self.btn_custom_sidebar.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FFD700"))
        self.btn_custom_cards = QPushButton("PICK CARD BG")
        self.btn_custom_cards.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_custom_accent = QPushButton("PICK ACCENT")
        self.btn_custom_accent.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF69B4"))

        for cb in [self.btn_custom_sidebar, self.btn_custom_cards, self.btn_custom_accent]:
            cb.setCursor(QCursor(Qt.PointingHandCursor))
            cb.setMinimumHeight(45)
            add_shadow(cb, 3, 3)
            h_custom.addWidget(cb)
        lay_th.addLayout(h_custom)
        lay.addWidget(self.f_theme)

        self.f_about = QFrame()
        self.f_about.setObjectName("ThemeCard")
        self.f_about.setStyleSheet("QFrame { background: #FFD700; border: 5px solid #000000; }")
        add_shadow(self.f_about, 6, 6)
        lay_ab = QVBoxLayout(self.f_about)
        lay_ab.setContentsMargins(25, 25, 25, 25)
        lay_ab.setSpacing(12)

        lbl_ab_head = QLabel("ABOUT  'aristeia.accademy'")
        lbl_ab_head.setObjectName("ThemeCardText")
        lbl_ab_head.setFont(QFont("Space Grotesk", 15, QFont.Black))
        lbl_ab_head.setStyleSheet("border: none; background: transparent;")
        txt_ab = QLabel(
            "<div style='word-spacing: 6px; line-height: 140%;'>"
            "Aristeia Academy is an open-source, human-made study application tailored for CBSE Class 12 students.<br>"
            "Built with Python, PySide6, and Qt Designer, it merges a bold <b>* Neo-Brutalist *</b> design with real-time theme switchability.<br>"
            "The application connects directly to a MySQL database via mysql.connector, offering full CRUD capabilities for managing<br>"
            "question banks and tasks, alongside native matplotlib data visualizations integrated straight into the dashboard.<br><br><br>"
            "Wishing you the best on your journey, from ABHINAV and DIYON"
            "</div>")

        txt_ab.setObjectName("ThemeCardText")
        txt_ab.setWordWrap(True)
        txt_ab.setFont(QFont("JetBrains Mono", 11, QFont.Bold))
        txt_ab.setStyleSheet("border: none; background: transparent;")
        lay_ab.addWidget(lbl_ab_head)
        lay_ab.addWidget(txt_ab)
        lay.addWidget(self.f_about)

        self.f_ver = QFrame()
        self.f_ver.setObjectName("ThemeCard")
        self.f_ver.setStyleSheet("QFrame { background: #F4F1EB; border: 4px dashed #000000; }")
        lay_ver = QVBoxLayout(self.f_ver)
        lay_ver.setContentsMargins(20, 20, 20, 20)
        lbl_ver = QLabel("VERSION 1.0.0 (RELEASE) | COPYRIGHT © 2026 | GNU GPL v3 OPEN SOURCE")
        lbl_ver.setObjectName("ThemeCardText")
        lbl_ver.setAlignment(Qt.AlignCenter)
        lbl_ver.setFont(QFont("JetBrains Mono", 10, QFont.Black))
        lbl_ver.setStyleSheet("border: none; background: transparent;")
        lay_ver.addWidget(lbl_ver)
        lay.addWidget(self.f_ver)

        lay.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.scroll_settings.setWidget(self.page_set)

        wrapper_widget = QWidget()
        wrapper_layout = QVBoxLayout(wrapper_widget)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.addWidget(self.scroll_settings)
        self.app_stacked_widget.addWidget(wrapper_widget)

    def _setup_page_chapters(self):
        self.page_ch = QWidget()
        self.page_ch.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_ch)
        lay.setSpacing(20)

        h_head = QHBoxLayout()
        self.btn_back_to_sub = QPushButton("⟵ BACK TO SUBJECTS")
        self.btn_back_to_sub.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#00FFFF"))
        self.btn_back_to_sub.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_back_to_sub, 3, 3)
        
        self.lbl_ch_title = QLabel("SUBJECT: ???")
        self.lbl_ch_title.setObjectName("ThemeText")
        self.lbl_ch_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        self.lbl_ch_title.setStyleSheet("border: none; background: transparent;")
        
        h_head.addWidget(self.btn_back_to_sub)
        h_head.addSpacing(20)
        h_head.addWidget(self.lbl_ch_title)
        h_head.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        lay.addLayout(h_head)

        self.scroll_ch = QScrollArea()
        self.scroll_ch.setWidgetResizable(True)
        self.scroll_ch.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.ch_container = QWidget()
        self.ch_container.setStyleSheet("background: transparent;")
        self.lay_ch_grid = QGridLayout(self.ch_container)
        self.lay_ch_grid.setSpacing(20)
        self.scroll_ch.setWidget(self.ch_container)
        lay.addWidget(self.scroll_ch, 1)
        self.app_stacked_widget.addWidget(self.page_ch)

    def _setup_page_questions(self):
        self.page_q = QWidget()
        self.page_q.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(self.page_q)
        lay.setSpacing(20)

        h_head = QHBoxLayout()
        self.btn_back_to_ch = QPushButton("⟵ BACK TO CHAPTERS")
        self.btn_back_to_ch.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FFD700"))
        self.btn_back_to_ch.setCursor(QCursor(Qt.PointingHandCursor))
        add_shadow(self.btn_back_to_ch, 3, 3)
        
        self.lbl_q_title = QLabel("CHAPTER: ???")
        self.lbl_q_title.setObjectName("ThemeText")
        self.lbl_q_title.setFont(QFont("Space Grotesk", 18, QFont.Black))
        self.lbl_q_title.setStyleSheet("border: none; background: transparent;")
        
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
        self.lay_q_list = QVBoxLayout(self.q_container)
        self.lay_q_list.setSpacing(25)
        self.lay_q_list.setAlignment(Qt.AlignTop)
        self.scroll_q.setWidget(self.q_container)
        lay.addWidget(self.scroll_q, 1)
        self.app_stacked_widget.addWidget(self.page_q)
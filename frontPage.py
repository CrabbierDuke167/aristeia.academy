import sys
import json
import os
import time

import matplotlib
matplotlib.use('QtAgg') # so it wont open its own window, but will embed in PySide6
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg # now Pyside6 consider matplotlib as a widget
from matplotlib.figure import Figure # placeholder figure/chart for no data state

from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QFrame, QLabel,
                               QHBoxLayout, QVBoxLayout, QSizePolicy, QColorDialog, QSpacerItem, QDialog)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QTimer
from PySide6.QtGui import QFont, QCursor, QColor

# Import elements and styles from ui_index
from ui_index import (Ui_MainWindow, add_shadow, BASE_BTN_STYLE, INPUT_STYLE,
                      DOTTED_BG, NeoMessageBox, NeoEditDialog)

# Import DB functions from database.py
import database as db

# Matplotlib Canvas Wrapper
class MplCanvas(FigureCanvasQTAgg): # to reduce line of codes
    """Transparent Matplotlib canvas, removed its lwk poor default bg."""
    def __init__(self, parent=None, width=5, height=3.5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi) # create a figure
        fig.patch.set_alpha(0.0) # make the figure bg transparent
        self.axes = fig.add_subplot(111) # 111 means 1x1 grid and 1 subplot to arrange side by side
        self.axes.patch.set_alpha(0.0) # to make axes bg transparent
        super().__init__(fig)



# CONTROLLER CLASS FOR THE ENTIRE APP
class AristeiaWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) # setup ui from ui_index.py
        self.setWindowTitle("Aristeia Academy") # app title

        self.sidebar_expanded = True # navbar shows by default
        self.drawer_open = False # question drawer is hidden by default
        self.current_drawer_q_id = None # question_id of the currently opened question in the drawer
        self.active_chapter_view = None # currently opened chapter as user clicks on any of the chapters
        self.current_theme = "LIGHT" # default theme, theme is updated in user_data table

        # Timer setup for Session
        # time spent in the app is displayed live in QTimer element in dashboard
        self.session_seconds = 0
        self.session_timer = QTimer(self)
        self.session_timer.timeout.connect(self.update_session_timer) # timeout is 1 sec, so updates every second

        # Load Themes
        self.themes_data = {} # stored in themes.json, a dict containing styling datas about different themes
        themes_file = os.path.join(os.path.dirname(__file__), "themes.json") # points to the 'themes.josn' lying right next to this py script
        if os.path.exists(themes_file): 
            with open(themes_file, "r") as f: # with help to automatically close the themes file
                self.themes_data = json.load(f) # parse JSON to py dict

        # Base style backups for LIGHT theme reset
        self.default_sidebar_style = self.icon_text_widget.styleSheet()
        self.default_pages_style = self.pages_container.styleSheet()
        
        # Connect Page Navigation Signals
        # onclicking buttons the respective page switch fn is called
        self.btn_login.clicked.connect(self.handle_login) # Auth 
        self.btn_logout.clicked.connect(self.handle_logout) # Auth

        self.btn_nav_home.clicked.connect(self.switch_to_home)
        self.btn_nav_dashboard.clicked.connect(self.switch_to_dashboard)
        self.btn_nav_schedule.clicked.connect(self.switch_to_schedule)
        self.btn_nav_settings.clicked.connect(self.switch_to_settings)

        self.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar) 
        self.btn_drawer_close.clicked.connect(self.close_drawer)

        # Subject selection mapping
        for sub_name, btn in self.subject_btns.items():
            btn.clicked.connect(lambda checked=False, name=sub_name: self.open_subject_chapters(name)) # lambda fn to call render chapters fn of respective subject 

        self.btn_back_to_sub.clicked.connect(self.switch_to_home) # act as a close button
        self.btn_back_to_ch.clicked.connect(lambda: self.app_stacked_widget.setCurrentIndex(4)) # back to chapters ie, index postion 4

        # Dropdown Linking
        self.combo_subject.currentTextChanged.connect(self.populate_upload_chapters) # populate chapter names accroding to the subject selected
        self.btn_upload.clicked.connect(self.handle_upload) # handing upload fn

        # Drawer CRUD Routing
        self.btn_drawer_edit.clicked.connect(self.crud_edit_question)
        self.btn_drawer_delete.clicked.connect(self.crud_delete_question)

        # Schedule CRUD Routing
        self.btn_add_task.clicked.connect(self.crud_create_task)

        # Theme Engine Signals
        # calls apply_theme() for the prebuilt themes (theme data in themes.json)
        self.btn_theme_light.clicked.connect(lambda: self.apply_theme("LIGHT"))
        self.btn_theme_dark.clicked.connect(lambda: self.apply_theme("DARK"))
        self.btn_theme_arg.clicked.connect(lambda: self.apply_theme("ARGENTINA"))
        self.btn_theme_bra.clicked.connect(lambda: self.apply_theme("BRASIL"))
        self.btn_theme_por.clicked.connect(lambda: self.apply_theme("PORTUGAL"))

        # Independent Custom themes using pick_custom_color_ fns
        self.btn_custom_sidebar.clicked.connect(self.pick_custom_color_sidebar)
        self.btn_custom_cards.clicked.connect(self.pick_custom_color_cards)
        self.btn_custom_accent.clicked.connect(self.pick_custom_color_accent)
        
        # Search functionality
        self.btn_search.clicked.connect(self.handle_search) # calls handle_search()

        # Loading user data from DB
        user_data = db.get_user_data() # runs immediately
        if user_data: # if exist (truthy)
            self.apply_theme(user_data['current_theme']) # applys current theme value in the row
        
        self.setup_dashboard_charts() 
        self.populate_upload_chapters(self.combo_subject.currentText())
        self.update_qotd_display() # for question of the day
        self.crud_read_tasks()

    # search engine fn
    def handle_search(self):
        query = self.inp_search.text().strip() # grab the text from QLineEdit (search bar)
        if not query: return # exit if falsey value
        results = db.search_questions(query) # calls the search question fn
        self.display_questions_list(results, title=f"SEARCH RESULTS: '{query}'")

    # charts and graphs set up
    def setup_dashboard_charts(self):
        """Empty list to hold empty chart canvas obj, we can use/fill them later."""
        self.canvases = [] 
        for i in range(3):  # First 3 are graphs then 1 timer
            target = self.chart_widgets[i] # get placeholder for each 3 graphs
            lay = QVBoxLayout(target) # vertical layout
            lay.setContentsMargins(0, 0, 0, 0) # remove margins to get full content width
            sc = MplCanvas(self, width=5, height=3.5, dpi=100)
            self.canvases.append(sc)
            lay.addWidget(sc)

        # 4th widget is Timer
        timer_target = self.chart_widgets[3] # uses 4th frame for the timer
        lay_timer = QVBoxLayout(timer_target)
        self.lbl_timer = QLabel("00:00:00") # default text label
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        self.lbl_timer.setFont(QFont("JetBrains Mono", 36, QFont.Bold))
        self.lbl_timer.setStyleSheet("color: #000000; border: none; background: transparent;")
        lay_timer.addWidget(self.lbl_timer)
        
        self.update_dashboard_charts() # call the update_dashboard() after gathering all these datas

    def update_session_timer(self):
        self.session_seconds += 1 # second by second
        hours = self.session_seconds // 3600
        minutes = (self.session_seconds % 3600) // 60
        seconds = self.session_seconds % 60
        self.lbl_timer.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        # update styling based on theme
        txt_color = "#000000"
        if self.current_theme in ["DARK", "BRASIL", "PORTUGAL"]:
            # Actually, chart background is #FFFFFF except when manually customized maybe? 
            # In ui_index.py it's set to #FFFFFF. So text should be black always.
            pass
            
    def update_dashboard_charts(self):
        """uses the empty chart canvas obj."""
        stats = db.get_dashboard_stats() # fn call
        
        # Graph 1: Difficulty Bar Chart
        ax0 = self.canvases[0].axes # 0 mean 1st graph
        ax0.clear() # clears old graphs
        diffs = ['EASY', 'MODERATE', 'HARD']
        diff_vals = [stats['diff_counts'].get(d, 0) for d in diffs] # stats's diff_count from our db
        ax0.bar(diffs, diff_vals, color=['#00FFFF', '#FFD700', '#FF3333'], edgecolor='black', linewidth=3) 
        ax0.tick_params(colors='black')
        for spine in ax0.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(3)

        # Graph 2: Subject Distribution Bar Chart
        ax1 = self.canvases[1].axes # 1 mean 2nd graph
        ax1.clear() # clears old graphs
        subs = list(stats['subject_counts'].keys()) # stats's subject_count's keys ie subject names from our db
        sub_vals = list(stats['subject_counts'].values()) # stats's subject_count's values ie count names from our db
        if not subs:
            subs = ['No Data']
            sub_vals = [0]
        # short names for x-axis
        short_subs = [s[:4].upper() for s in subs]
        ax1.bar(short_subs, sub_vals, color='#FF5E00', edgecolor='black', linewidth=3)
        ax1.tick_params(colors='black')
        for spine in ax1.spines.values(): spine.set_edgecolor('black'); spine.set_linewidth(3)

        # Graph 3: Answered vs Unanswered Pie Chart
        ax2 = self.canvases[2].axes # 2 mean 3rd graph
        ax2.clear() # clears old graphs
        ans_data = [stats['answered_ratio']['Answered'], stats['answered_ratio']['Unanswered']] # gets both vales from stats from our db
        if sum(ans_data) > 0:
            ax2.pie(ans_data, labels=['Ans', 'Unans'], colors=['#33FF55', '#FF3333'], 
                    wedgeprops={'edgecolor': 'black', 'linewidth': 3}, textprops={'color': 'black', 'fontweight': 'bold'})
        else: # if sum of ans_data not greater than 0
            ax2.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center', color='black')

        # Draw updates
        for sc in self.canvases: sc.draw() # loop through the 3 charts and draws it with latest data
        
        # Update XP Bar
        user_data = db.get_user_data()
        xp = user_data.get('xp', 0) # pull out xp value, if dont exist then its set as 0
        self.prog_xp.setMaximum(999)
        self.prog_xp.setValue(xp) # set value of the progress bar
        self.xp_frame.findChild(QLabel, "ThemeCardText").setText(f"SCHOLAR XP ({xp} / 999)") # update the current xp count of the QLabel


    def update_qotd_display(self):
        """Pulls latest question from questions table."""
        q = db.get_latest_question() # fn call
        if q: # if exists
            self.lbl_qotd_text.setText(f"Subject: {q['sub']} | Chapter: {q['ch']}\n\n{q['q']}") # card title text
            self.btn_qotd_view.clicked.disconnect() # disconnected the btn first for safety
            self.btn_qotd_view.clicked.connect(lambda checked=False, target=q: self.open_drawer(target)) # toggle drawer ON
        else:
            self.lbl_qotd_text.setText("No questions added yet. Be the first!")



    # very basic AUTH LOGIC !!!!!
    def handle_login(self):
        user = self.inp_username.text().strip() # input username
        token = self.inp_token.text().strip() # input pass
        if user == "admin" and token == "password": # HARDCODED , replace with your's
            self.lbl_login_error.setText("") # clear out the invalid credentials error message if any
            self.inp_username.clear() # thus clear the input box
            self.inp_token.clear() # thus clear the input box
            self.outer_stacked_widget.setCurrentIndex(1) # pull to page index 1 ie, main page
            self.session_timer.start(1000) # start session timer on login
            self.switch_to_home() # now home is the main page on login
        else:
            self.lbl_login_error.setText("INVALID CREDENTIALS") # error message

    def handle_logout(self):
        self.outer_stacked_widget.setCurrentIndex(0) # kick to page index 0 ie, login page
        self.close_drawer() # close the drawers if left open, so when we relogin it will be closed
        self.session_timer.stop() # stop timer from ticking
        self.session_seconds = 0 # hard reset the time
        self.lbl_timer.setText("00:00:00") # hard reset the ui element

    # defining page router fns
    def switch_to_home(self): self.app_stacked_widget.setCurrentIndex(0); self.btn_nav_home.setChecked(True); self.close_drawer()
    def switch_to_dashboard(self): self.app_stacked_widget.setCurrentIndex(1); self.btn_nav_dashboard.setChecked(True); self.update_dashboard_charts(); self.close_drawer()
    def switch_to_schedule(self): self.app_stacked_widget.setCurrentIndex(2); self.btn_nav_schedule.setChecked(True); self.close_drawer()
    def switch_to_settings(self): self.app_stacked_widget.setCurrentIndex(3); self.btn_nav_settings.setChecked(True); self.close_drawer()

    # Populating fn for Dropdown menu
    def populate_upload_chapters(self, subject):
        sub_mapped = subject.upper()
        if sub_mapped == "COMPUTER SCIENCE": sub_mapped = "COMP SCI" # replace long subject name with short one for db
        chapters = db.SUBJECTS.get(sub_mapped, []) # if not -> return []
        self.combo_chapter.clear() # clear existing loaded chapters if any
        self.combo_chapter.addItems(chapters) # inject new chapters to dropdwon

    # SQL Ingestion (Upload Portal)
    def handle_upload(self):
        sub = self.combo_subject.currentText().upper()
        if sub == "COMPUTER SCIENCE": sub = "COMP SCI" # replace long subject name with short one for db
        ch = self.combo_chapter.currentText()
        diff = self.combo_diff.currentText()
        raw_text = self.txt_upload_q.toPlainText().strip() # strip cleans the raw_data

        if not raw_text: # display error with NeoMessageBox if left empty
            NeoMessageBox("Error", "Question cannot be empty!", "error", self).exec()
            return

        q_part, a_part = raw_text, "Solution missing."
        if "A:" in raw_text: # if user provides answer within the question
            parts = raw_text.split("A:") # separator is "A:" eg: input = "What"
            q_part = parts[0].replace("Q:", "").strip() # if 'Q:' provided with question text then remove it before uploading
            a_part = parts[1].strip() # answer part is taken from 2nd element

        success = db.add_question(sub, ch, q_part, a_part, diff) # calls add_question() and passes all arguments
        
        if success: # success become true if successfully uploaded
            self.txt_upload_q.clear() # clear the inputBox
            self.update_qotd_display() # renders the latest Q as QOTD
            NeoMessageBox("Success", f"Uploaded Question to {ch}!", "success", self).exec() # success message

            if self.app_stacked_widget.currentIndex() == 5 and self.active_chapter_view == ch:
                self.open_questions(ch) # live updates the added question in its respective page index's chapter view (thus no need of refresh)
        else:
            NeoMessageBox("Error", "Failed to upload question.", "error", self).exec() # error message on failing



    # MEMORY LEAK FREE BUILDERS
    # fns to create chapter cards for each subjects
    def open_subject_chapters(self, subject_name):
        self.lbl_ch_title.setText(f"SUBJECT: {subject_name}") # page title

        while self.lay_ch_grid.count():
            item = self.lay_ch_grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        # chapters asks for keys of purticular subject, SUBJECT is a hardcoded dict  
        chapters = db.SUBJECTS.get(subject_name, []) # if not -> return []
        row, col = 0, 0
        for ch in chapters:
            btn = QPushButton(ch)
            btn.setMinimumHeight(75)
            btn.setFont(QFont("Space Grotesk", 12, QFont.Bold))
            btn.setStyleSheet(BASE_BTN_STYLE) # predefined style set
            btn.setCursor(QCursor(Qt.PointingHandCursor)) # cursor pointer
            add_shadow(btn, 4, 4)
            btn.clicked.connect(lambda checked=False, ch_target=ch: self.open_questions(ch_target)) # onclick opens the respective questions display page
            self.lay_ch_grid.addWidget(btn, row, col)
            col += 1 # add a col
            if col > 2: col = 0; row += 1 # there are 3 column then go to next row : cols index as (0,1,2)

        self.app_stacked_widget.setCurrentIndex(4) # render the new grid of chapter cards
        for b in [self.btn_nav_home, self.btn_nav_dashboard, self.btn_nav_schedule, self.btn_nav_settings]: b.setChecked(False) # de-select all nav-btns if any

    # opens and display question cards for chosen chapter
    def open_questions(self, chapter_name):
        self.active_chapter_view = chapter_name # track the viewing chapter
        chapter_qs = db.get_questions_by_chapter(chapter_name) # a natural join fn defined in database.py, fetachall() returns a list
        self.display_questions_list(chapter_qs, title=f"CHAPTER: {chapter_name}") # calls the UI renderer fn

    def display_questions_list(self, questions_list, title):
        self.lbl_q_title.setText(title) # UI renders the title
        
        # to delete the chapters from RAM, not from DB
        # subjects are QPushButton in home page they dont need clear up, but chapters and questions do
        while self.lay_q_list.count(): # as longs as count of elements exist, iterate the loop
            item = self.lay_q_list.takeAt(0) # grab the card
            if item.widget(): item.widget().deleteLater() # if it is a QWidget then remove from memory
            elif item.spacerItem(): pass # if it is a ui spacer then ignore : pass

        if not questions_list: # if get_questions_by_chapter() returns : []
            empty_lbl = QLabel("NO QUESTIONS FOUND.")
            empty_lbl.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
            # text color for each themes
            txt_c = "#FFFFFF" if self.current_theme in ["DARK", "BRASIL", "PORTUGAL"] else "#555555"
            empty_lbl.setStyleSheet(f"color: {txt_c};") # for custom text color
            self.lay_q_list.addWidget(empty_lbl)
        else:
            # Theme adjustments for card
            card_bg = "#FFFFFF"
            card_text = "#000000"
            if self.current_theme != "LIGHT" and self.current_theme in self.themes_data: # for non default but predefined themes
                card_bg = self.themes_data[self.current_theme]['card_bg']
                card_text = self.themes_data[self.current_theme]['card_text']

            for q_data in questions_list:
                q_card = QFrame() # QFrame is like an empty Widget, unlike QWidget its not invisible
                q_card.setObjectName("ThemeCard")
                q_card.setStyleSheet(f"QFrame {{ background-color: {card_bg}; border: 4px solid #000000; }}")
                add_shadow(q_card, 4, 4) # neo brut shadow
                qlay = QHBoxLayout(q_card)
                qlay.setContentsMargins(15, 15, 15, 15)

                lbl = QLabel(q_data["q"])
                lbl.setObjectName("ThemeCardText")
                lbl.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
                lbl.setWordWrap(True)
                lbl.setStyleSheet(f"border: none; color: {card_text};")

                diff_color = "#FFD700" if q_data["diff"] == "MODERATE" else ("#00FFFF" if q_data["diff"] == "EASY" else "#FF3333") # color representation of difficulty
                lbl_diff = QLabel(q_data["diff"])
                lbl_diff.setFont(QFont("Space Grotesk", 10, QFont.Bold))
                lbl_diff.setStyleSheet(f"background: {diff_color}; border: 2px solid #000000; padding: 6px; color: #000000;")
                lbl_diff.setFixedHeight(35) # fixed height, so it wont grow too tall
                lbl_diff.setAlignment(Qt.AlignCenter)

                btn_view = QPushButton("VIEW ANSWER ➔")
                btn_view.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#8A2BE2") + "QPushButton { color: white; }")
                btn_view.setCursor(QCursor(Qt.PointingHandCursor))
                add_shadow(btn_view, 2, 2)
                btn_view.clicked.connect(lambda checked=False, target=q_data: self.open_drawer(target)) # onclick opens the drawer with the respective question data

                qlay.addWidget(lbl, 1)
                qlay.addWidget(lbl_diff)
                qlay.addWidget(btn_view)
                self.lay_q_list.addWidget(q_card)

        self.lay_q_list.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.app_stacked_widget.setCurrentIndex(5)
        for b in [self.btn_nav_home, self.btn_nav_dashboard, self.btn_nav_schedule, self.btn_nav_settings]: b.setChecked(False) # deselect all nav Btns of any

    # Sliding Drawer Controller
    def open_drawer(self, q_data): # takes data of the purticular question as argument
        self.current_drawer_q_id = q_data.get("id") # its refering to the dict we got from iterating over the list of dicts
        self.lbl_drawer_diff.setText(f"DIFFICULTY: {q_data['diff']}")
        
        diff_color = "#FFD700" if q_data["diff"] == "MODERATE" else ("#00FFFF" if q_data["diff"] == "EASY" else "#FF3333")
        self.lbl_drawer_diff.setStyleSheet(f"background: {diff_color}; border: 3px solid #000000; padding: 6px; color: #000000;")

        # Populate separate cards
        self.lbl_drawer_question.setText(q_data['q']) # QLabel : edit only iwth edit btn
        self.txt_drawer_answer.setText(q_data['a']) # QTextEdit : can edit dircetly

        if not self.drawer_open:
            self.answer_drawer.show() # Qt fn to toggle ON the drawer
            self.answer_drawer.raise_() # Qt fn to give it the top z-index

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
                db.update_question_answer(self.current_drawer_q_id, new_ans)

            parent_rect = self.page_mainapp.rect() # grabs current x and y of main app
            start_rect = QRect(parent_rect.width() - 500, 0, 500, parent_rect.height())
            end_rect = QRect(parent_rect.width(), 0, 500, parent_rect.height()) # sticks to rigth side

            self.anim = QPropertyAnimation(self.answer_drawer, b"geometry")
            self.anim.setDuration(320) # 320 millisec for the slide in
            self.anim.setStartValue(start_rect)
            self.anim.setEndValue(end_rect)
            self.anim.setEasingCurve(QEasingCurve.InExpo)
            self.anim.finished.connect(self.answer_drawer.hide) # hide the drawer on closing
            self.anim.finished.connect(self._refresh_drawer_parent) # call fn to update the page underneath as the drawer closes
            self.anim.start() # start the slider motion
            self.drawer_open = False # update boolean state of drawer

    def _refresh_drawer_parent(self):
        if getattr(self, 'active_chapter_view', None): # check if we have a chapter opened underneath
            self.open_questions(self.active_chapter_view) # if so then refetch and rebuild the question cards so changes are reflected in ui



    # DRAWER CRUD FNs

    def crud_edit_question(self):
        """Opens Custom UI to edit the Question Text."""
        if not self.current_drawer_q_id: return # if didnt get the id then exit
        
        current_q_text = self.lbl_drawer_question.text() # grab question text
        dialog = NeoEditDialog("EDIT QUESTION", current_q_text, self) # edit Q: ui box
        
        if dialog.exec() == QDialog.Accepted: # wait till user click the btn (freezes everything else in bg) 
            new_q = dialog.get_text()
            if not new_q: return # if empty then exit

            db.update_question_text(self.current_drawer_q_id, new_q) # fn defined in database.py
            self.lbl_drawer_question.setText(new_q) # updated question
            NeoMessageBox("Success", "Question Updated Successfully!", "success", self).exec()
            
            if self.active_chapter_view:
                self.open_questions(self.active_chapter_view) # clear RAM and re draw the elements in bg

    def crud_delete_question(self):
        """Delete the question"""
        if not self.current_drawer_q_id: return # if didnt get the id then exit
        
        db.delete_question(self.current_drawer_q_id) # fn defined in database.py
        
        NeoMessageBox("Deleted", "Question Deleted.", "warning", self).exec()
        self.close_drawer() # close the question drawer as the question no longer exist
        self.update_qotd_display() # if it was used as QOTD then update it with new QOTD
        
        if self.active_chapter_view:
            self.open_questions(self.active_chapter_view) # clear RAM and re draw the elements in bg


    # SCHEDULE CRUD FNs

    def crud_create_task(self):
        text = self.inp_task.text().strip() # grab the text from QLineEdit
        priority = self.combo_priority.currentText() # grabs priority from selected dropdown
        if not text: # if left empty 
            NeoMessageBox("Error", "Task cannot be blank!", "error", self).exec()
            return

        db.add_task(text, priority) # fn from database.py
        self.inp_task.clear() # clear input box
        self.crud_read_tasks() # call the renderer
        NeoMessageBox("Success", "Task Added.", "success", self).exec()

    def crud_read_tasks(self): # renderer fn
        while self.schedule_tasks_layout.count(): # as long as elements exist
            item = self.schedule_tasks_layout.takeAt(0) # one row at a time
            if item.widget(): item.widget().deleteLater() # delete elements *from UI* to prevent RAM leak and ghost elements
            elif item.spacerItem(): pass # dont delete the ui spacers

        tasks = db.get_tasks() # the database.py fn returns a list of dicts of all added taks
        
        # Theme adjustments for card
        card_bg = "#FFFFFF"
        card_text = "#000000"
        if self.current_theme != "LIGHT" and self.current_theme in self.themes_data: # for non default but predefined themes
            card_bg = self.themes_data[self.current_theme]['card_bg'] # at themes.json
            card_text = self.themes_data[self.current_theme]['card_text'] # at themes.json

        for t_data in tasks: # t_data is dicts from the list tasks
            t_card = QFrame() # holder frame
            t_card.setObjectName("ThemeCard")
            t_card.setStyleSheet(f"QFrame {{ background-color: {card_bg}; border: 4px solid #000000; }}")
            add_shadow(t_card, 4, 4) # neo brutalist borders
            tlay = QHBoxLayout(t_card)
            tlay.setContentsMargins(15, 12, 15, 12)
            tlay.setSpacing(15)

            p_color = "#FF3333" if "HIGH" in t_data["priority"] else ("#FFD700" if "MEDIUM" in t_data["priority"] else "#00FFFF")
            lbl_pTag = QLabel(t_data["priority"].split()[0]) # priority name
            lbl_pTag.setFont(QFont("Space Grotesk", 10, QFont.Black))
            lbl_pTag.setStyleSheet(f"background: {p_color}; border: 2px solid #000000; padding: 5px; color: #000000;")

            lbl_tText = QLabel(t_data["task"]) # task text
            lbl_tText.setObjectName("ThemeCardText")
            lbl_tText.setFont(QFont("JetBrains Mono", 12, QFont.Bold))
            lbl_tText.setStyleSheet(f"border: none; color: {card_text};")

            btn_edit = QPushButton("EDIT") # edit task btn
            btn_edit.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FFD700"))
            btn_edit.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn_edit, 2, 2)
            btn_edit.clicked.connect(lambda checked=False, target=t_data: self.crud_update_task(target)) # call update fn

            btn_del = QPushButton("DELETE") # delete task btn
            btn_del.setStyleSheet(BASE_BTN_STYLE.replace("#FFFFFF", "#FF3333") + "QPushButton { color: white; }")
            btn_del.setCursor(QCursor(Qt.PointingHandCursor))
            add_shadow(btn_del, 2, 2)
            btn_del.clicked.connect(lambda checked=False, target=t_data: self.crud_delete_task(target)) # call delete fn

            # add the widgets to the layout
            tlay.addWidget(lbl_pTag)
            tlay.addWidget(lbl_tText, 1)
            tlay.addWidget(btn_edit)
            tlay.addWidget(btn_del)
            self.schedule_tasks_layout.addWidget(t_card)

        self.schedule_tasks_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    # task updater fn
    def crud_update_task(self, task_target):
        dialog = NeoEditDialog("EDIT TASK", task_target["task"], self) # edit task : ui box
        if dialog.exec() == QDialog.Accepted:
            new_text = dialog.get_text() # grab new tsk text
            if new_text:
                db.update_task(task_target['id'], new_text) # push changes to db
                self.crud_read_tasks() # recalls the renderer fn
                NeoMessageBox("Success", "Task Updated.", "success", self).exec()

    def crud_delete_task(self, task_target):
        db.delete_task(task_target['id']) # removes the task from db
        self.crud_read_tasks() # recalls the renderer fn

    def toggle_sidebar(self): # for navigation menu
        if self.sidebar_expanded: self.icon_text_widget.hide(); self.sidebar_expanded = False # hide the navbar on click and update its boolean state
        else: self.icon_text_widget.show(); self.sidebar_expanded = True


    # THEME ENGINE (head ache)
    # fn to apply theme, it takes 1 argument : theme_name
    def apply_theme(self, theme_name):
        self.current_theme = theme_name # grabs current theme
        db.update_theme(theme_name) # update the user_data's current_theme column value
        
        if theme_name == "LIGHT" or theme_name not in self.themes_data: # theme_data is a dict of all prebuilt themes from themes.json afte we parsed it
            # RESET TO DEFAULTS
            self.icon_text_widget.setStyleSheet(self.default_sidebar_style)
            self.lbl_app_title.setStyleSheet("border: none; padding-left: 10px; color: #000000; background: transparent;")
            self.pages_container.setStyleSheet(self.default_pages_style)
            self.lbl_header_title.setStyleSheet("border: none; color: #000000; background: transparent;")
            
            # make all "ThemeText" black
            for text_lbl in self.page_mainapp.findChildren(QLabel, "ThemeText"):
                text_lbl.setStyleSheet("border: none; color: #000000; background: transparent;")
                
            for card in self.page_mainapp.findChildren(QFrame, "ThemeCard"):
                # Exception for specifically colored cards on Home tab (SUBJECTS)
                if card in [self.card_qotd, self.card_quote, self.f_about]:
                    if card == self.card_qotd: card.setStyleSheet("QFrame { background-color: #8A2BE2; border: 5px solid #000000; }")
                    if card == self.card_quote: card.setStyleSheet("QFrame { background-color: #FF5E00; border: 5px solid #000000; }")
                    if card == self.f_about: card.setStyleSheet("QFrame { background-color: #FFD700; border: 5px solid #000000; }")
                    for lbl in card.findChildren(QLabel, "ThemeCardText"): # make 'ThemeCardText' black
                        lbl.setStyleSheet(f"border: none; color: #000000; background: transparent;")
                else: # if its a normal card then make it white with black text
                    card.setStyleSheet("QFrame { background-color: #FFFFFF; border: 5px solid #000000; }")
                    for lbl in card.findChildren(QLabel, "ThemeCardText"):
                        lbl.setStyleSheet("border: none; color: #000000; background: transparent;")
            
            # reset all input boxes and dropdowns to default style
            self.inp_search.setStyleSheet(INPUT_STYLE)
            self.inp_task.setStyleSheet(INPUT_STYLE)
            self.combo_priority.setStyleSheet(INPUT_STYLE)
            self.combo_subject.setStyleSheet(INPUT_STYLE)
            self.combo_chapter.setStyleSheet(INPUT_STYLE)
            self.combo_diff.setStyleSheet(INPUT_STYLE)
            self.txt_upload_q.setStyleSheet(INPUT_STYLE)
            return # if it was a theme reset then exit


        # CUSTOM THEME
        # this is executed if theme is not 'LIGHT' but exist in themes_data
        t = self.themes_data[theme_name] # Grab the dict of colors for this specific theme.

        # Update Sidebar
        checked_col = t.get('checked', '#FF5E00') # default orange if not found
        
        # style accroding to data in JSON file
        self.icon_text_widget.setStyleSheet(f"""
            QWidget {{ background-color: {t['sidebar']}; border-right: 4px solid #000000; }}
            QPushButton {{ background-color: {t['sidebar']}; color: {t['nav_text']}; border: 4px solid transparent; text-align: left; padding: 12px 20px; font-family: 'Space Grotesk'; font-size: 14pt; font-weight: bold; border-radius: 0px; }}
            QPushButton:hover {{ background-color: #FFFF00; border-bottom: 4px solid #000000; border-right: 4px solid #000000; color: #000000; padding-left: 30px; }}
            QPushButton:checked {{ background-color: {checked_col}; color: #000000 if checked_col not in ['#74ACDF', '#009C3B', '#FF0000', '#006600', '#FF5E00'] else '#FFFFFF'; border: 4px solid #000000; }}
        """)
        self.lbl_app_title.setStyleSheet(f"border: none; padding-left: 10px; color: {t['nav_text']}; background: transparent;")

        # Update Main Background
        new_dotted = DOTTED_BG.replace("#F4F1EB", t['bg'])
        if theme_name in ["DARK", "BRASIL", "PORTUGAL"]: # for darkish themes
            new_dotted = f'background-image: url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'16\' height=\'16\'><circle cx=\'2\' cy=\'2\' r=\'1.5\' fill=\'%23FFFFFF\' fill-opacity=\'0.15\'/></svg>"); background-color: {t["bg"]}; background-repeat: repeat;'
        self.pages_container.setStyleSheet(new_dotted)

        # making Header & Standalone Text visible over background
        title_color = "#FFFFFF" if theme_name in ["DARK", "BRASIL", "PORTUGAL"] else "#000000" # chosen respectively according to bg darkness
        self.lbl_header_title.setStyleSheet(f"border: none; color: {title_color}; background: transparent;")
        for text_lbl in self.page_mainapp.findChildren(QLabel, "ThemeText"):
            text_lbl.setStyleSheet(f"border: none; color: {title_color}; background: transparent;")

        # update All Cards & Text inside them to chosen theme styles
        for card in self.page_mainapp.findChildren(QFrame, "ThemeCard"):
            card.setStyleSheet(f"QFrame {{ background-color: {t['card_bg']}; border: 5px solid #000000; }}")
            for lbl in card.findChildren(QLabel, "ThemeCardText"):
                lbl.setStyleSheet(f"border: none; color: {t['card_text']}; background: transparent;")

        # Update Input Fields (Dropdowns, LineEdits, TextEdits) so they standout
        input_bg = "#AFADAD" if theme_name == "DARK" else "#FFFFFF"
        input_text = "#0D0101" if theme_name == "DARK" else "#000000"
        THEMED_INPUT_STYLE = f"""
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {input_bg}; border: 3px solid #000000; padding: 8px; color: {input_text}; font-family: 'JetBrains Mono'; font-weight: bold; selection-background-color: #00FFFF; selection-color: #000000;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{ background-color: #FFFFCC; border: 3px solid #FF5E00; color: #000000; }}
            QComboBox QAbstractItemView {{ 
                background-color: {input_bg}; 
                color: {input_text}; 
                border: 3px solid #000000; 
                selection-background-color: #00FFFF; 
                selection-color: #000000; 
            }}
        """

        # Apply that style to all input fields
        self.inp_search.setStyleSheet(THEMED_INPUT_STYLE)
        self.inp_task.setStyleSheet(THEMED_INPUT_STYLE)
        self.combo_priority.setStyleSheet(THEMED_INPUT_STYLE)
        self.combo_subject.setStyleSheet(THEMED_INPUT_STYLE)
        self.combo_chapter.setStyleSheet(THEMED_INPUT_STYLE)
        self.combo_diff.setStyleSheet(THEMED_INPUT_STYLE)
        self.txt_upload_q.setStyleSheet(THEMED_INPUT_STYLE)

    # CUSTOM COLOR PICKER

    def pick_custom_color_sidebar(self): # color fn picker for navbar
        col = QColorDialog.getColor(Qt.white, self, "Pick Custom Sidebar Base")
        if col.isValid():
            hex_code = col.name()
            text_col = "#000000" if col.lightness() > 128 else "#FFFFFF" # auto contrasting text color
            self.icon_text_widget.setStyleSheet(f"""
                QWidget {{ background-color: {hex_code}; border-right: 4px solid #000000; }}
                QPushButton {{ background-color: {hex_code}; color: {text_col}; border: 4px solid transparent; text-align: left; padding: 12px 20px; font-family: 'Space Grotesk'; font-size: 14pt; font-weight: bold; border-radius: 0px; }}
                QPushButton:hover {{ background-color: #FFFF00; border-bottom: 4px solid #000000; border-right: 4px solid #000000; color: #000000; }}
                QPushButton:checked {{ background-color: #FF5E00; color: #000000; border: 4px solid #000000; }}
            """)
            self.lbl_app_title.setStyleSheet(f"border: none; padding-left: 10px; color: {text_col}; background: transparent;")

    def pick_custom_color_cards(self): # color picker fn for cards
        col = QColorDialog.getColor(Qt.white, self, "Pick Base Card Override")
        if col.isValid():
            for card in self.page_mainapp.findChildren(QFrame, "ThemeCard"): # go through all the cards ie "ThemeCards" and repaint them
                card.setStyleSheet(f"QFrame {{ background-color: {col.name()}; border: 5px solid #000000; }}")

    def pick_custom_color_accent(self): # color picker fn for accent (base btn hover color)
        col = QColorDialog.getColor(Qt.white, self, "Pick Primary Button Highlight Override")
        if col.isValid():
            new_hover_color = col.name()
            # style according to newly picked accent.
            THEMED_BTN_STYLE = f"""
                QPushButton {{
                    background-color: #000000; 
                    color: #FFFFFF; 
                    border: 3px solid #000000;
                    padding: 10px;
                    font-family: 'Space Grotesk';
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {new_hover_color};
                    color: #000000;
                }}
            """
            self.btn_upload.setStyleSheet(THEMED_BTN_STYLE)
            self.btn_add_task.setStyleSheet(THEMED_BTN_STYLE)

    # APP WINDOW resizing LOGIC

    def resizeEvent(self, event):
        super().resizeEvent(event) # call PyQt resizeEvent() -> resize all the elements
        if self.drawer_open:
            parent_rect = self.page_mainapp.rect() # if open grab the geometry of main app
            self.answer_drawer.setGeometry(parent_rect.width() - 500, 0, 500, parent_rect.height()) # calculate and set the drawer to 500px width to the rigth end


# APPLICATION ENTRY POINT
# run this py script only if main.py is ran
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AristeiaWindow()
    window.show() # hidden by default
    sys.exit(app.exec()) # execute
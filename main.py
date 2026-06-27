import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from frontPage import AristeiaWindow
from database import initialize_database # import the initialize_database function from database python file


# make sure the app only runs if we run the main.py
if __name__ == "__main__":
    initialize_database()

    app = QApplication(sys.argv) # boot up PySide6 application

# importing fonts from resource file
    QFontDatabase.addApplicationFont(":/assets/SpaceGrotesk-VariableFont_wght.ttf")
    QFontDatabase.addApplicationFont(":/assets/JetBrainsMono-VariableFont_wght.ttf")

    window = AristeiaWindow() # AristeiaWindow is the main window
    window.show() # by default it is hidden
    sys.exit(app.exec()) # execute

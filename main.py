import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtCore import qInstallMessageHandler, QtMsgType

# tnx stackoverflow ....
def silence_pixmap_errors(msg_type: QtMsgType, context, message: str):
    if "Could not create pixmap" in message:
        return  # Swallows it silently 
    print(message)  # Keeps other errors visible

qInstallMessageHandler(silence_pixmap_errors)

from frontPage import AristeiaWindow
from database import initialize_database # import the initialize_database function from database python file

# make sure the app only runs if we run the main.py
if __name__ == "__main__":
    initialize_database()

    app = QApplication(sys.argv) # boot up PySide6 application

    # importing fonts from resource file (keeping your working QRC fonts)
    QFontDatabase.addApplicationFont(":/assets/SpaceGrotesk-VariableFont_wght.ttf")
    QFontDatabase.addApplicationFont(":/assets/JetBrainsMono-VariableFont_wght.ttf")

    window = AristeiaWindow() # AristeiaWindow is the main window
    
    # finds the logo in assets folder in the parent folder
    window.setWindowIcon(QIcon(str(Path(__file__).parent / "assets" / "aristeia_app_logo.png")))

    window.show() # by default it is hidden
    sys.exit(app.exec()) # execute
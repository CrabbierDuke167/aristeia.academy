import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from frontPage import MySideBar

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Note: Ensure the compiled resources_rc.py file is in the same directory,
    # and that the fonts are correctly referenced.
    QFontDatabase.addApplicationFont(":/demo2 images/SpaceGrotesk-VariableFont_wght.ttf")
    QFontDatabase.addApplicationFont(":/demo2 images/JetBrainsMono-VariableFont_wght.ttf")

    window = MySideBar()
    window.show()
    sys.exit(app.exec())

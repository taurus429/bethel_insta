import sys
from PyQt5.QtWidgets import QApplication
from main_window import TextGeneratorApp
from PyQt5.QtGui import QFont, QFontDatabase, QIcon

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))

    font_path = './감탄로드바탕체 Regular.ttf'
    font_id = QFontDatabase.addApplicationFont(font_path)
    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

    custom_font = QFont(font_family, 10)
    app.setFont(custom_font)

    ex = TextGeneratorApp()
    sys.exit(app.exec_())

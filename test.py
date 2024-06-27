import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QDialog, QVBoxLayout, QLabel, \
    QGridLayout, QTabWidget, QScrollArea, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class EmojiPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Emoji Picker")
        self.setGeometry(100, 100, 500, 500)
        self.setLayout(QVBoxLayout())

        self.tab_widget = QTabWidget()
        self.layout().addWidget(self.tab_widget)

        self.load_emojis()

    def load_emojis(self):
        emoji_dir = './img/emoji'
        emojis = os.listdir(emoji_dir)

        num_emojis_per_tab = 500
        num_tabs = (len(emojis) + num_emojis_per_tab - 1) // num_emojis_per_tab

        for i in range(num_tabs):
            start_index = i * num_emojis_per_tab
            end_index = min(start_index + num_emojis_per_tab, len(emojis))
            tab = QWidget()
            tab_layout = QVBoxLayout()

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QGridLayout(scroll_content)

            row = 0
            col = 0
            for j in range(start_index, end_index):
                emoji_file = emojis[j]
                emoji_path = os.path.join(emoji_dir, emoji_file)
                emoji_label = QLabel(self)
                pixmap = QPixmap(emoji_path)
                emoji_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio))
                emoji_label.mousePressEvent = lambda event, code=emoji_file: self.emoji_clicked(event, code)
                scroll_layout.addWidget(emoji_label, row, col)
                col += 1
                if col > 9:  # 10 columns
                    col = 0
                    row += 1

            scroll_content.setLayout(scroll_layout)
            scroll_area.setWidget(scroll_content)
            tab_layout.addWidget(scroll_area)
            tab.setLayout(tab_layout)

            self.tab_widget.addTab(tab, f'Page {i + 1}')

    def emoji_clicked(self, event, code):
        self.parent().insert_emoji_code(code)
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emoji Input Example")
        self.setGeometry(100, 100, 400, 300)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.emoji_button = QPushButton("이모지 입력", self)
        self.emoji_button.clicked.connect(self.show_emoji_popup)

        # Add the button to the layout
        layout = self.text_edit.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.text_edit.setLayout(layout)
        layout.addWidget(self.emoji_button)

    def show_emoji_popup(self):
        self.popup = EmojiPopup(self)
        self.popup.exec_()

    def insert_emoji_code(self, code):
        cursor = self.text_edit.textCursor()
        cursor.insertText(f':{code.strip(".png")}:')
        self.text_edit.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

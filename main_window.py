from PyQt5.QtWidgets import (
    QApplication, QLineEdit, QPushButton, QMainWindow, QFileDialog, QMessageBox,
    QVBoxLayout, QHBoxLayout, QDialog, QCalendarWidget

)
from PyQt5.QtCore import QDate
import util, init_ui, init_util
import datetime

class CalendarPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.clicked.connect(self.on_date_selected)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        self.setLayout(layout)
        self.setWindowTitle('날짜 선택')
        self.setModal(True)

    def on_date_selected(self, date):
        self.selected_date = date
        self.accept()


class TextGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        init_util.initUtil(self)
        init_ui.initUI(self)


    def toggle_dark_mode(self):
        self.setting.set_settings("darkmode", not self.dark_mode)
        self.dark_mode = not self.dark_mode
        self.set_theme()

    def set_theme(self):
        if self.dark_mode:
            self.setStyleSheet(self.dark_stylesheet)
        else:
            self.setStyleSheet(self.light_stylesheet)

    def show_calendar_popup(self):
        calendar_popup = CalendarPopup(self)
        if calendar_popup.exec_():
            selected_date = calendar_popup.selected_date.toString('yyyy-MM-dd')
            self.date_edit.setText(selected_date)
            selected_date = calendar_popup.selected_date.toString('yyMMdd')
            self.birthday_list = util.get_birthday_week(selected_date)

    def on_type_changed(self):
        if self.type_combo.currentText() == '블로그':
            self.author_label.hide()
            self.author_group.hide()
        else:
            self.author_label.show()
            self.author_group.show()

    def add_news_input(self):
        new_text_edit = QLineEdit()
        delete_button = QPushButton('삭제')
        delete_button.clicked.connect(lambda: self.delete_news_input(new_text_edit, delete_button))
        delete_button.setStyleSheet("""
                            QPushButton {
                                background-color: #d43526;
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: #d16c62;
                            }
                        """)


        new_layout = QHBoxLayout()
        new_layout.addWidget(new_text_edit)
        new_layout.addWidget(delete_button)

        self.news_dynamic_layout.addLayout(new_layout)
        self.news_list.append(new_text_edit)

    def delete_news_input(self, text_widget, button_widget):
        text_widget.hide()
        button_widget.hide()
        self.news_list.remove(text_widget)

    def add_schedule_input(self):
        new_text_edit = QLineEdit()
        delete_button = QPushButton('삭제')
        delete_button.clicked.connect(lambda: self.delete_schedule_input(new_text_edit, delete_button))
        delete_button.setStyleSheet("""
                            QPushButton {
                                background-color: #d43526;
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: #d16c62;
                            }
                        """)

        new_layout = QHBoxLayout()
        new_layout.addWidget(new_text_edit)
        new_layout.addWidget(delete_button)

        self.schedule_dynamic_layout.addLayout(new_layout)
        self.schedule_list.append(new_text_edit)

    def delete_schedule_input(self, text_widget, button_widget):
        text_widget.hide()
        button_widget.hide()
        self.schedule_list.remove(text_widget)

    def generate_text(self):

        date = self.date_edit.text()
        text_type = self.type_combo.currentText()
        title = self.title_edit.text()
        scripture = self.scripture_edit.text()
        content = self.content_edit.toPlainText()
        pray = self.pray_combo.currentText()

        weekday = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10])).weekday()
        week = ['월', '화', '수', '목', '금', '토', '일']
        if text_type in ['마하나임 예배', '더원 예배'] and weekday != 6:
            QMessageBox.warning(self, '요일 경고', f'{text_type} 날짜가 {week[weekday]}요일로 입력되어있습니다.')


        result = f"{date[2:4]}.{date[5:7]}.{date[8:10]} {text_type}\n\n"
        if title:
            result += f"[{title}] {scripture}\n\n"
        result += f"{content}\n\n"

        if len(self.news_list) > 0:
            result += f"🪨이번 주 소식🪨\n"
            for news in self.news_list:
                result += f"✔️{news.text()}\n"
            result += "\n"

        if len(self.schedule_list) > 0:
            result += f"🪨이번 주 일정🪨\n"
            for schedule in self.schedule_list:
                result += f"✔️{schedule.text()}\n"
            result += "\n"

        result += f"📣 이번 주 기도인도: {pray}\n"
        if self.outing_radio1.isChecked():
            result += "❗️ 더원 예배 뒤에 아웃팅 있습니다!\n"

        if len(self.birthday_list) != 0:
            result += "🎂 이번 주 생일자: "
            for b in self.birthday_list:
                result += f"{b}, "
            result = result[:-2]
            result += "\n"
        if self.qt_check1 or self.qt_check2 or self.qt_check3 or self.qt_check4 or self.qt_check5:
            day = ""
            if self.qt_check1.isChecked():
                day += "월, "
            if self.qt_check2.isChecked():
                day += "화, "
            if self.qt_check3.isChecked():
                day += "수, "
            if self.qt_check4.isChecked():
                day += "목, "
            if self.qt_check5.isChecked():
                day += "금, "
            day = day[0:-2]
            result += f"📖 {day} 큐티모임\n"

        if self.joowana_radio1.isChecked():
            result += "🙏🏻 수요일 주와나 벧엘데이\n"
        else:
            result += "🙏🏻 주와나 특새\n"
        self.result_text.setPlainText(result)

    def copy_result_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())

    def attach_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # macOS에서 필수: 네이티브 파일 대화상자 사용 안 함
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 첨부", "", "CSV Files (*.csv);;Excel Files (*.xls *.xlsx)",
                                                   options=options)
        if file_name:
            # 확장자 확인 (csv 또는 excel 파일만 허용)
            if file_name.lower().endswith(('.csv', '.xls', '.xlsx')):
                # 파일을 저장하는 함수 호출
                success = util.save_to_db(file_name)
                if success:
                    QMessageBox.information(self, "성공", "파일이 성공적으로 저장되었습니다.")
                    self.setting.set_settings("birthday_file", util.count_birthday_db())
                    self.attach_file_text.setText(f'{self.setting.get_settings("birthday_file")}명 등록')
                else:
                    QMessageBox.warning(self, "오류", "파일 저장 중 오류가 발생했습니다.")

            else:
                QMessageBox.warning(self, "잘못된 파일 형식", "CSV 파일 또는 Excel 파일만 첨부할 수 있습니다.")
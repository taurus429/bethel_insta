from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QMainWindow, QFileDialog, QMessageBox,
    QRadioButton, QVBoxLayout, QHBoxLayout, QComboBox, QCheckBox, QDialog, QCalendarWidget, QGroupBox, QGridLayout,
    QAction
)
from PyQt5.QtCore import QDate


def initUI(app):
    central_widget = QWidget()
    app.setCentralWidget(central_widget)

    # 날짜 입력 위젯
    app.date_label = QLabel('날짜 입력:')
    app.date_edit = QLineEdit()
    app.date_edit.setText(QDate.currentDate().toString('yyyy-MM-dd'))
    app.date_button = QPushButton('날짜 선택')
    app.date_button.clicked.connect(app.show_calendar_popup)

    date_layout = QHBoxLayout()
    date_layout.addWidget(app.date_edit)
    date_layout.addWidget(app.date_button)

    # 글 유형 입력용 드롭다운 위젯
    app.type_label = QLabel('게시글 유형 선택:')
    app.type_combo = QComboBox()
    app.type_combo.addItems(['마하나임 예배', '더원 예배', '설렘 축제', '마을 리트릿', '마을 아웃팅', '블로그'])
    # app.type_combo.currentIndexChanged.connect(app.on_type_changed)

    # 설교 제목 입력 용 텍스트 위젯
    app.title_label = QLabel('설교 제목 입력:')
    app.title_edit = QLineEdit()

    # 설교 본문 입력 용 텍스트 위젯
    app.scripture_label = QLabel('설교 본문 입력:')
    app.scripture_edit = QLineEdit()

    # 글 내용 입력 용 텍스트 위젯
    app.content_label = QLabel('글 내용 입력:')
    app.content_edit = QTextEdit()

    # 글 생성용 버튼
    app.generate_button = QPushButton('생성')
    app.generate_button.clicked.connect(app.generate_text)
    app.generate_button.setStyleSheet("""
                        QPushButton {
                            background-color: #1E90FF;
                            color: white;
                        }
                        QPushButton:hover {
                            background-color: #63B8FF;
                        }
                    """)

    # 결과 생성용 텍스트 영역 위젯
    app.result_label = QLabel('게시물 미리보기:')
    app.result_text = QTextEdit()
    app.result_text.setReadOnly(True)

    # 이번 주 소식
    app.this_week_news = QLabel('이번 주 소식')
    app.news_add_button = QPushButton('소식 추가')
    app.news_add_button.clicked.connect(app.add_news_input)
    app.news_dynamic_layout = QVBoxLayout()

    # 이번 주 일정
    app.this_week_schedule = QLabel('이번 주 일정')
    app.schedule_add_button = QPushButton('일정 추가')
    app.schedule_add_button.clicked.connect(app.add_schedule_input)
    app.schedule_dynamic_layout = QVBoxLayout()

    # 생일자

    app.birthday_label = QLabel('생일자 파일')
    app.birthday_layout = QWidget()
    file_layout = QHBoxLayout()

    # 파일 첨부용 버튼
    attach_file_button = QPushButton('파일 첨부')
    attach_file_button.clicked.connect(app.attach_file)

    file_label = '파일 없음'
    if app.settings['birthday_file']:
        print("파일없음")
    app.attach_file_text = QLabel(file_label)
    file_layout.addWidget(app.attach_file_text)
    file_layout.addWidget(attach_file_button)

    app.birthday_layout.setLayout(file_layout)

    # 이번 주 기도인도
    app.pray_label = QLabel('이번 주 기도 인도')
    app.pray_combo = QComboBox()
    app.pray_combo.addItems(['예진 사랑', '희원 사랑', '예지 사랑', '소윤 사랑', '현도 사랑', '찬호 사랑', '없음'])

    # 글 작성자 선택용 라디오 버튼 위젯
    app.author_label = QLabel('글 작성자 선택:')
    app.author_group = QGroupBox()
    app.author_radio1 = QRadioButton('작성자 A')
    app.author_radio2 = QRadioButton('작성자 B')
    app.author_radio1.setChecked(True)  # 기본 선택
    author_layout = QHBoxLayout()
    author_layout.addWidget(app.author_radio1)
    author_layout.addWidget(app.author_radio2)
    app.author_group.setLayout(author_layout)

    # 예배 뒤 아웃팅
    app.outing_label = QLabel('마지막 주 아웃팅')
    app.outing_group = QGroupBox()
    app.outing_radio1 = QRadioButton('있음')
    app.outing_radio2 = QRadioButton('없음')
    app.outing_radio2.setChecked(True)  # 기본 선택
    outing_layout = QHBoxLayout()
    outing_layout.addWidget(app.outing_radio1)
    outing_layout.addWidget(app.outing_radio2)
    app.outing_group.setLayout(outing_layout)

    # 큐티 모임
    app.qt_label = QLabel('주중 큐티 모임')
    app.qt_group = QGroupBox()
    app.qt_check1 = QCheckBox('월')
    app.qt_check2 = QCheckBox('화')
    app.qt_check3 = QCheckBox('수')
    app.qt_check4 = QCheckBox('목')
    app.qt_check5 = QCheckBox('금')
    app.qt_check1.setChecked(True)  # 기본 선택
    app.qt_check4.setChecked(True)  # 기본 선택
    qt_layout = QHBoxLayout()
    qt_layout.addWidget(app.qt_check1)
    qt_layout.addWidget(app.qt_check2)
    qt_layout.addWidget(app.qt_check3)
    qt_layout.addWidget(app.qt_check4)
    qt_layout.addWidget(app.qt_check5)
    app.qt_group.setLayout(qt_layout)

    # 주와나
    app.joowana_label = QLabel('주와나')
    app.joowana_group = QGroupBox()
    app.joowana_radio1 = QRadioButton('수요일 벧엘데이')
    app.joowana_radio2 = QRadioButton('주와나 특새')
    app.joowana_radio1.setChecked(True)  # 기본 선택
    joowana_layout = QHBoxLayout()
    joowana_layout.addWidget(app.joowana_radio1)
    joowana_layout.addWidget(app.joowana_radio2)
    app.joowana_group.setLayout(joowana_layout)

    # 결과 복사 버튼
    app.copy_button = QPushButton('결과 복사')
    app.copy_button.clicked.connect(app.copy_result_to_clipboard)
    app.copy_button.setStyleSheet("""
                        QPushButton {
                            background-color: #36a866;
                            color: white;
                        }
                        QPushButton:hover {
                            background-color: #70c493;
                        }
                    """)

    # 그리드 레이아웃 설정
    layout = QGridLayout()
    layout.addWidget(app.date_label, 0, 0)
    layout.addLayout(date_layout, 0, 1)
    layout.addWidget(app.type_label, 1, 0)
    layout.addWidget(app.type_combo, 1, 1)
    layout.addWidget(app.title_label, 2, 0)
    layout.addWidget(app.title_edit, 2, 1)
    layout.addWidget(app.scripture_label, 3, 0)
    layout.addWidget(app.scripture_edit, 3, 1)
    layout.addWidget(app.content_label, 4, 0)
    layout.addWidget(app.content_edit, 4, 1)
    layout.addWidget(app.this_week_news, 5, 0)
    layout.addLayout(app.news_dynamic_layout, 5, 1)
    layout.addWidget(app.news_add_button, 6, 1)
    layout.addWidget(app.this_week_schedule, 7, 0)
    layout.addLayout(app.schedule_dynamic_layout, 7, 1)
    layout.addWidget(app.schedule_add_button, 8, 1)
    layout.addWidget(app.pray_label, 9, 0)
    layout.addWidget(app.pray_combo, 9, 1)
    layout.addWidget(app.outing_label, 10, 0)
    layout.addWidget(app.outing_group, 10, 1)
    layout.addWidget(app.qt_label, 11, 0)
    layout.addWidget(app.qt_group, 11, 1)
    layout.addWidget(app.joowana_label, 12, 0)
    layout.addWidget(app.joowana_group, 12, 1)
    layout.addWidget(app.generate_button, 0, 3)
    layout.addWidget(app.result_label, 0, 2)
    layout.addWidget(app.result_text, 1, 2, 11, 2)
    layout.addWidget(app.copy_button, 12, 2, 1, 2)
    layout.addWidget(app.birthday_label, 13, 0)
    layout.addWidget(app.birthday_layout, 13, 1)

    central_widget.setLayout(layout)

    # Create a menu bar and menus
    app.menu_bar = app.menuBar()
    app.file_menu = app.menu_bar.addMenu('파일')
    app.settings_menu = app.menu_bar.addMenu('설정')

    # 파일 메뉴에 액션 추가
    app.file_action1 = QAction('파일 탭 1', app)
    app.file_action2 = QAction('파일 탭 2', app)
    app.file_menu.addAction(app.file_action1)
    app.file_menu.addAction(app.file_action2)

    app.dark_mode_action = QAction('다크 모드', app, checkable=True)
    app.dark_mode_action.setChecked(app.dark_mode)
    app.settings_menu.addAction(app.dark_mode_action)
    app.dark_mode_action.triggered.connect(app.toggle_dark_mode)
    app.dark_stylesheet = """
                QMainWindow {
                    background-color: #333;
                    color: white;
                }
                QMenuBar {
                    background-color: #555;
                    color: white;
                }
                QMenuBar::item {
                    background-color: #555;
                    color: white;
                    padding: 4px 10px;
                    border-radius: 4px;
                }
                QMenuBar::item:selected {
                    background-color: #888;
                }
                QMenu {
                    background-color: #555;
                    color: white;
                    border: 1px solid #888;
                }
                QMenu::item {
                    background-color: transparent;
                }
                QMenu::item:selected {
                    background-color: #888;
                }
                QPushButton {
                    background-color: #1E90FF;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #63B8FF;
                }
                QTextEdit, QLineEdit, QComboBox, QCheckBox, QRadioButton {
                    background-color: #444;
                    color: white;
                    border: 1px solid #888;
                    border-radius: 4px;
                }
                QLabel {
                    color: white;
                }
            """
    app.light_stylesheet = ""

    # 초기 테마 설정
    app.set_theme()

    app.statusBar().showMessage('Ready')

    app.setWindowTitle('마을 인스타 게시물 생성기')
    app.show()

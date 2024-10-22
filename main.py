import sys
from PyQt6.QtCore import QUrl, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QToolBar, QPushButton, QLineEdit, QListWidget, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView  # Импортируем QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()  # Создаем QTabWidget для управления вкладками
        self.tabs.setTabsClosable(True)  # Включаем возможность закрытия вкладок
        self.tabs.tabCloseRequested.connect(self.close_current_tab)  # Обработчик закрытия вкладки
        self.setCentralWidget(self.tabs)

        self.history = []  # Список для хранения истории посещений

        self.navbar = QToolBar()  # Создаем QToolBar для навигации
        self.addToolBar(self.navbar)

        # Добавляем первую вкладку с Google
        self.add_new_tab(QUrl("http://www.google.com"))

        # Кнопка "Назад"
        back_btn = QPushButton()
        back_btn.setIcon(QIcon("back.png"))
        back_btn.setIconSize(QSize(50, 50))
        back_btn.clicked.connect(self.go_back)
        back_btn.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #A9CCE3;
                color: white;
                font-size: 12px;
                padding: 5px;
                margin-right: 5px;  /* Отступ между кнопками */
            }
            QPushButton:hover {
                background-color: #B0E0E6;
            }
        """)
        self.navbar.addWidget(back_btn)

        # Кнопка "Вперед"
        forward_btn = QPushButton()
        forward_btn.setIcon(QIcon("forward.png"))
        forward_btn.setIconSize(QSize(50, 50))
        forward_btn.clicked.connect(self.go_forward)
        forward_btn.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #A9CCE3;
                color: white;
                font-size: 12px;
                padding: 5px;
                margin-right: 5px;  /* Отступ между кнопками */
            }
            QPushButton:hover {
                background-color: #B0E0E6;
            }
        """)
        self.navbar.addWidget(forward_btn)

        # Кнопка "Домой"
        home_btn = QPushButton()
        home_btn.setIcon(QIcon("home.png"))
        home_btn.setIconSize(QSize(50, 50))
        home_btn.clicked.connect(self.go_home)
        home_btn.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #A9CCE3;
                color: white;
                font-size: 12px;
                padding: 5px;
                margin-right: 5px;  /* Отступ между кнопками */
            }
            QPushButton:hover {
                background-color: #B0E0E6;
            }
        """)
        self.navbar.addWidget(home_btn)

        # Кнопка "Обновить"
        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon("reload.png"))
        refresh_btn.setIconSize(QSize(50, 50))
        refresh_btn.clicked.connect(self.reload_page)  # Обработчик нажатия для обновления страницы
        refresh_btn.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #A9CCE3;
                color: white;
                font-size: 12px;
                padding: 5px;
                margin-right: 5px;  /* Отступ между кнопками */
            }
            QPushButton:hover {
                background-color: #B0E0E6;
            }
        """)
        self.navbar.addWidget(refresh_btn)

        # Строка URL
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)  # Обработчик для нажатия Enter
        self.navbar.addWidget(self.url_bar)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                background-color: #A9CCE3;
                border: 2px solid #A9CCE3;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
        """)

        # Кнопка "История"
        history_btn = QPushButton("История")
        history_btn.clicked.connect(self.show_history)
        history_btn.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #A9CCE3;
                color: white;
                font-size: 12px;
                padding: 5px;
                margin-right: 5px;  /* Отступ между кнопками */
            }
            QPushButton:hover {
                background-color: #B0E0E6;
            }
        """)
        self.navbar.addWidget(history_btn)

        # Кнопка "Добавить вкладку"
        new_tab_btn = QPushButton("Новая \nвкладка")
        new_tab_btn.clicked.connect(self.add_new_tab_from_toolbar)  # Обработчик добавления новой вкладки
        new_tab_btn.setStyleSheet("""
            QPushButton {
                border-radius: 5px;
                background-color: #A9CCE3;
                color: white;
                font-size: 12px;
                padding: 5px;
                margin-right: 5px;  /* Отступ между кнопками */
            }
            QPushButton:hover {
                background-color: #B0E0E6;
            }
        """)
        self.navbar.addWidget(new_tab_btn)

    def add_new_tab(self, url):
        # Создаем новую вкладку с QWebEngineView
        browser = QWebEngineView()
        browser.setUrl(url)

        # Подключаем сигнал для изменения заголовка вкладки при изменении заголовка страницы
        browser.titleChanged.connect(lambda title: self.update_tab_title(browser, title))
        browser.urlChanged.connect(lambda url: self.add_to_history(url))  # Добавляем URL в историю

        index = self.tabs.addTab(browser, "Загрузка...")
        self.tabs.setCurrentWidget(browser)

    def update_tab_title(self, browser, title):
        # Обновляем заголовок текущей вкладки
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)

    def add_new_tab_from_toolbar(self):
        # Добавляем новую вкладку с домашней страницей (например, Google)
        self.add_new_tab(QUrl("http://www.google.com"))

    def go_back(self):
        # Получаем текущую вкладку
        current_browser = self.tabs.currentWidget()
        # Проверяем, есть ли история для возврата назад
        if current_browser and current_browser.history().canGoBack():
            current_browser.back()

    def go_forward(self):
        # Получаем текущую вкладку
        current_browser = self.tabs.currentWidget()
        # Проверяем, можно ли вернуться вперед
        if current_browser and current_browser.history().canGoForward():
            current_browser.forward()

    def go_home(self):
        # Переходим на домашнюю страницу (Google)
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl("http://www.google.com"))

    def reload_page(self):
        # Обновляем текущую страницу
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

    def navigate_to_url(self):
        # Получаем URL из строки URL и переходим на него
        url = self.url_bar.text()
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def add_to_history(self, url):
        # Добавляем URL в историю
        self.history.append(url.toString())

    def show_history(self):
        # Создаем новый виджет для отображения истории
        history_widget = QWidget()
        layout = QVBoxLayout()
        history_list = QListWidget()

        # Добавляем каждый URL из истории в список
        for url in self.history:
            history_list.addItem(url)

        # Обработчик клика по элементу истории
        history_list.itemClicked.connect(self.navigate_from_history)

        layout.addWidget(history_list)
        history_widget.setLayout(layout)

        # Добавляем новый виджет в новую вкладку
        index = self.tabs.addTab(history_widget, "История")
        self.tabs.setCurrentWidget(history_widget)

    def navigate_from_history(self, item):
        # Переходим по URL, выбранному в истории
        url = item.text()
        self.add_new_tab(QUrl(url))

    def close_current_tab(self, index):
        # Закрываем вкладку по индексу, если вкладок больше одной
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

from PyQt6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QPushButton
import qtawesome as qta

class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton(qta.icon("fa.search"), "")
        self.layout.addWidget(self.search_button)
#
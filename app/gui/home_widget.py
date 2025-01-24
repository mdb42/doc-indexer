
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import Qt

import qtawesome as qta

from app.gui.search_widget import SearchWidget


class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.top_vlayout = QVBoxLayout()
        self.layout.addLayout(self.top_vlayout)
        self.splash_vlayout = QVBoxLayout()
        self.top_vlayout.addLayout(self.splash_vlayout)
        self.splash_vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.splash_hlayout = QHBoxLayout()
        self.splash_hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.splash_title_label = QLabel("Document Indexer")
        self.splash_title_label_font = self.splash_title_label.font()
        self.splash_title_label_font.setPointSize(24)
        self.splash_title_label.setFont(self.splash_title_label_font)
        self.splash_vlayout.addWidget(self.splash_title_label, 0, Qt.AlignmentFlag.AlignCenter)

        self.splash_subtitle_label = QLabel("CSC 790 Information Retrieval")
        self.splash_subtitle_label_font = self.splash_subtitle_label.font()
        self.splash_subtitle_label_font.setPointSize(14)
        self.splash_subtitle_label.setFont(self.splash_subtitle_label_font)
        self.splash_vlayout.addWidget(self.splash_subtitle_label, 0, Qt.AlignmentFlag.AlignCenter)
        

        self.splash_hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.splash_vlayout.addLayout(self.splash_hlayout)
        self.splash_vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.middle_vlayout = QVBoxLayout()
        self.layout.addLayout(self.middle_vlayout)
        self.home_search_hlayout = QHBoxLayout()
        self.middle_vlayout.addLayout(self.home_search_hlayout)
        self.home_search_hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.search_widget = SearchWidget()
        self.home_search_hlayout.addWidget(self.search_widget)
        self.home_search_hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.instructions_label = QLabel("Enter a query in the field above to search indexed documents.")
        self.instructions_label_font = self.instructions_label.font()
        self.instructions_label_font.setPointSize(8)
        self.instructions_label.setFont(self.instructions_label_font)
        self.instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_vlayout.addWidget(self.instructions_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.middle_vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.bottom_vlayout = QVBoxLayout()
        self.layout.addLayout(self.bottom_vlayout)
        self.bottom_vlayout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.help_hlayout = QHBoxLayout()
        self.bottom_vlayout.addLayout(self.help_hlayout)
        self.help_hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.help_button = QPushButton(qta.icon("fa.question-circle"), "Help")
        self.help_button.setFlat(True)
        self.help_hlayout.addWidget(self.help_button)
        self.help_hlayout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        

        self.setLayout(self.layout)




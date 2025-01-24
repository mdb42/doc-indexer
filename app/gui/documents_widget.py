from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QHeaderView
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize

class DocumentsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Create the documents table
        self.setup_table()

    def setup_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Document", "Status"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 80)
        
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        
        self.layout.addWidget(self.table)

    def add_document(self, doc_id, title, path, size, modified, status):       
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        doc_item = QTableWidgetItem(title)
        doc_item.setData(Qt.ItemDataRole.UserRole, {
            'id': doc_id,
            'path': path,
            'size': size,
            'modified': modified
        })
        
        # Add the two visible columns
        self.table.setItem(row_position, 0, doc_item)
        self.table.setItem(row_position, 1, QTableWidgetItem(status))
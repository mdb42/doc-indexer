
from PyQt6.QtWidgets import QMainWindow, QDockWidget, QStackedWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from app.gui.home_widget import HomeWidget
from app.gui.documents_widget import DocumentsWidget
from app.gui.index_widget import IndexWidget

import importlib.resources as resources

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing MainWindow")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Document Indexer")
        with resources.path("resources", "images") as path:
            print(f"Path: {path}")
            self.setWindowIcon(QIcon(str(path / "favicon.ico")))
        self.show()

        self.documents_widget = DocumentsWidget(parent=self)
        self.index_widget = IndexWidget(parent=self)

        self.documents_dock = QDockWidget("Documents", self)
        self.documents_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.documents_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable|QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.documents_dock.setWidget(self.documents_widget)

        self.index_dock = QDockWidget("Index", self)
        self.index_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.index_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable|QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.index_dock.setWidget(self.index_widget)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.documents_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.index_dock)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_widget = HomeWidget()
        self.stacked_widget.addWidget(self.home_widget)

        self.statusBar().showMessage("Ready")

    def update_status_bar(self):
        self.statusBar().showMessage(
            f"Documents: {self.doc_count} | "
            f"Index Terms: {self.term_count} | "
            f"Memory Usage: {self.get_memory_usage():.1f}MB"
    )


        



        


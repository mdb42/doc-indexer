
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem


class IndexWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Index')
        self.resize(400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Index"])
        self.layout.addWidget(self.tree)

        # I can barely handle table widgets! Really, I'm not sure
        # if I should be doing these as Views instead of Widgets,
        # as when we might be expected to perform all the operations
        # in the IR workflow asynchronously, the model view controller
        # pattern for PyQt6 might be more appropriate. We'll see!



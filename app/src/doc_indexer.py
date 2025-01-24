from pathlib import Path
import logging
from datetime import datetime
from PyQt6.QtCore import pyqtSignal, Qt
from app.src.doc_indexer_db import DocIndexerDB
from app.gui.main_window import MainWindow
import importlib.resources as resources

class DocIndexer(MainWindow):
    document_processed = pyqtSignal(int, str)  # doc_id, status
    indexing_progress = pyqtSignal(int, int)   # current, total
    
    def __init__(self, config):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.db = DocIndexerDB(config["database"]["path"])
        self._connect_signals()
        self.load_existing_documents()
        self.collect_documents()
    
    def load_existing_documents(self):
        try:
            documents = self.db.query_all_documents()
            self.logger.info(f"Loading {len(documents)} existing documents")
            
            for doc in documents:
                # Unpack fields in the same order as database schema
                doc_id, title, path, content, last_modified, file_size, status = doc
                
                self.documents_widget.add_document(
                    doc_id=doc_id,
                    title=title,
                    path=path,
                    size=file_size,
                    modified=last_modified,
                    status=status
                )
                
        except Exception as e:
            self.logger.error(f"Error loading existing documents: {e}")
            self.logger.debug("Document data causing error:", exc_info=True)

    def collect_documents(self):
        try:
            doc_list = resources.read_text("resources.documents", "documents.dat")
            
            for line in doc_list.splitlines():
                if not line.strip() or line.startswith("documents.dat"):
                    continue
                    
                filename, index = line.strip().split(',')
                content = resources.read_text("resources.documents", filename)
                
                # Try to add to database, get back whether it's new
                doc_id, is_new = self.db.insert_document(
                    title=filename,
                    path=f"resources/documents/{filename}",
                    content=content
                )
                
                # Only add to UI if it's a new document
                if is_new and doc_id:
                    self.documents_widget.add_document(
                        doc_id=doc_id,
                        title=filename,
                        path=f"resources/documents/{filename}",
                        size=len(content),
                        modified=datetime.now().isoformat(),
                        status='Unindexed'
                    )
            
            self.logger.info("Loaded all documents")
        except Exception as e:
            self.logger.error(f"Error loading documents: {e}")
            self.logger.debug("Document data causing error:", exc_info=True)

    def _connect_signals(self):
        # Connect document table selection changes
        self.documents_widget.table.selectionModel().selectionChanged.connect(
            self._handle_document_selection
        )
        
        # Connect processing signals to UI updates
        self.document_processed.connect(self._update_document_status)
        self.indexing_progress.connect(self._update_progress_bar)
    
    def _handle_document_selection(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            row = indexes[0].row()
            doc_id = self.documents_widget.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            
            try:
                # Fetch complete document details from database
                document = self.db.query_document(doc_id)
                if document:
                    self._show_document_details(document)
            except Exception as e:
                self.logger.error(f"Error loading document details: {e}")
    
    def _show_document_details(self, document):
        doc_id, title, path, content, last_modified, file_size, status = document
        
        # Update the preview widget with document details
        # Still contemplating if this deserves its own dockable widget
        self.preview_widget.set_content(content)
        self.preview_widget.set_metadata({
            "Title": title,
            "Path": path,
            "Size": f"{file_size:,} bytes",
            "Last Modified": last_modified,
            "Status": status
        })

    def _update_document_status(self, doc_id, status):
        for row in range(self.documents_widget.table.rowCount()):
            item = self.documents_widget.table.item(row, 0)
            if item.data(Qt.ItemDataRole.UserRole) == doc_id:
                self.documents_widget.table.item(row, 4).setText(status)
                break

    def _update_progress_bar(self, current, total):
        self.index_progress.setMaximum(total)
        self.index_progress.setValue(current)
        self.statusBar().showMessage(f"Indexing: {current}/{total}")


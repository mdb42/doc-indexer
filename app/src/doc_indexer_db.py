import sqlite3
from datetime import datetime
import logging

class DocIndexerDB:
    
    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.conn = sqlite3.connect(url)
        self.cursor = self.conn.cursor()
        self.create_docs_table()

    def create_docs_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            path TEXT NOT NULL,
            content TEXT,
            last_modified TEXT NOT NULL,
            file_size INTEGER NOT NULL,
            status TEXT DEFAULT 'Unindexed',
            UNIQUE(title, path)
        )
        """)
        self.conn.commit()

    def insert_document(self, title, path, content):
        try:
            # Attempt to insert the new document
            self.cursor.execute("""
            INSERT INTO documents (
                title, path, content, last_modified, file_size, status
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                title,
                str(path),
                content,
                datetime.now().isoformat(),
                len(content),
                'Unindexed'
            ))
            self.conn.commit()
            return self.cursor.lastrowid, True
            
        except sqlite3.IntegrityError:
            # Document exists - could optionally update if content changed
            self.logger.info(f"Document already exists: {title} at {path}")
            return None, False
        
    def query_all_documents(self):
        self.cursor.execute("""
        SELECT id, title, path, content, last_modified, file_size, status 
        FROM documents
        """)
        return self.cursor.fetchall()

    def query_document(self, doc_id):
        self.cursor.execute("""
        SELECT id, title, path, content, last_modified, file_size, status
        FROM documents WHERE id = ?
        """, (doc_id,))
        return self.cursor.fetchone()

    def update_status(self, doc_id, status):
        self.cursor.execute("""
        UPDATE documents 
        SET status = ?, last_modified = ?
        WHERE id = ?
        """, (status, datetime.now().isoformat(), doc_id))
        self.conn.commit()

    def delete_document(self, doc_id):
        self.cursor.execute("""
        DELETE FROM documents WHERE id = ?
        """, (doc_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
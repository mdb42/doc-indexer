class InvertedIndex:
    def __init__(self):
        self.index = {}  # term -> {doc_id -> [positions]}
        self.document_lengths = {}  # doc_id -> term_count
        
    def add_document(self, doc_id, content):
        terms = self.tokenize(content)
        positions = {}  # term -> [positions]
        
        for pos, term in enumerate(terms):
            if term not in positions:
                positions[term] = []
            positions[term].append(pos)
            
        for term, term_positions in positions.items():
            if term not in self.index:
                self.index[term] = {}
            self.index[term][doc_id] = term_positions
            
        self.document_lengths[doc_id] = len(terms)
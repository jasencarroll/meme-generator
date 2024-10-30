# File: Ingestor.py

from typing import List
from abc import ABC, abstractmethod

class QuoteModel:
    """A class to encapsulate a quote with the quote body and author."""
    
    def __init__(self, body: str, author: str):
        self.body = body
        self.author = author

    def __repr__(self):
        return f'"{self.body}" - {self.author}'


class IngestorInterface(ABC):
    """Abstract base class for different file ingestors."""
    
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the given file extension is supported."""
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @abstractmethod
    def parse(self, path: str) -> List[QuoteModel]:
        """Parse the file and return a list of QuoteModel objects."""
        pass


class TextIngestor(IngestorInterface):
    allowed_extensions = ['txt']

    def parse(self, path: str) -> List[QuoteModel]:
        """Parse a .txt file and return a list of QuoteModel instances."""
        quotes = []
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    body, author = line.split('-')
                    quotes.append(QuoteModel(body.strip(), author.strip()))
        return quotes


class CSVIngestor(IngestorInterface):
    # Implementation for CSV parsing
    pass

class DOCXIngestor(IngestorInterface):
    # Implementation for DOCX parsing
    pass

class PDFIngestor(IngestorInterface):
    # Implementation for PDF parsing
    pass


class Ingestor:
    """Handles file ingestion by delegating to specific file ingestors."""
    
    ingestors = [TextIngestor, CSVIngestor, DOCXIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Determine the appropriate ingestor and parse the file."""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor().parse(path)
        raise ValueError(f'File format not supported: {path}')

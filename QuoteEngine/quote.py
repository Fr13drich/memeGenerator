"""load and parse quotes from files"""

from abc import ABC, abstractmethod
from typing import List
import subprocess
import pandas
from docx import Document
# import docx


class QuoteModel():
    """a quote and its author"""
    def __init__(self, body="", author="") -> None:
        self.body = body
        self.author = author

class IngestorInterface(ABC):
    """generic class to import quotes from files"""
    allowed_extensions = []
    @classmethod
    def can_ingest(cls, path) -> bool:
        """is the extension supported?"""
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions
    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """import a list of quotes from a file"""

class CSVImporter(IngestorInterface):
    """Import quotes from a csv file."""
    allowed_extensions = ['csv']
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        quotes = []
        df = pandas.read_csv(path, header=1)
        for body, author in df.iterrows():
            quotes.append(QuoteModel(body, author))
        return quotes

class DocxImporter(IngestorInterface):
    """Import quotes from a docx file."""
    allowed_extensions = ['docx']
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        quotes = []
        doc = Document(path)
        for line in doc.paragraphs:
            body, author = line.text.split(' - ')
            quotes.append(QuoteModel(body, author))
        return quotes

class PdfImporter(IngestorInterface):
    """Import quotes from a pdf file."""
    allowed_extensions = ['pdf']
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        quotes = []
        p = subprocess.run(['pdftotxt', path], stdout=subprocess.PIPE, check=True)
        for line in p.stdout:
            body, author = line.split(' - ')
            quotes.append(QuoteModel(body, author))
        return quotes
        
class TxtImporter(IngestorInterface):
    """Import quotes from a text file."""
    allowed_extensions = ['txt']
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        quotes = []
        with open(path) as f:
            for line in f:
                body, author = line.split(' - ')
                quotes.append(QuoteModel(body, author))
        return quotes

class Ingestor(IngestorInterface):
    """Import quotes from a supported file."""
    allowed_extensions = ['txt', 'docx', 'pdf', 'csv']
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise Exception('cannot ingest exception')
        ext = path.split('.')[-1]
        if ext == 'docx':
            importer = DocxImporter
        elif ext == 'pfd':
            importer = PdfImporter
        elif ext == 'txt':
            importer = TxtImporter
        else:
            importer = CSVImporter
        return importer.parse(path)
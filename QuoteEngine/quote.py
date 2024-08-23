"""Load and parse quotes from files"""

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


class CSVIngestor(IngestorInterface):
    """Import quotes from a csv file."""
    allowed_extensions = ['csv']

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError('Cannot ingest exception.')
        quotes = []
        df = pandas.read_csv(path, header=1)
        for body, author in df.iterrows():
            quotes.append(QuoteModel(body, author))
        return quotes


class DocxIngestor(IngestorInterface):
    """Import quotes from a docx file."""
    allowed_extensions = ['docx']

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError('Cannot ingest exception.')
        quotes = []
        doc = Document(path)
        for line in doc.paragraphs:
            try:
                body, author = line.text.split(' - ')
                quotes.append(QuoteModel(body, author))
            except ValueError:
                pass
                # raise ValueError(line.text)
        return quotes


class PdfIngestor(IngestorInterface):
    """Import quotes from a pdf file."""
    allowed_extensions = ['pdf']

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError('Cannot ingest exception.')
        quotes = []
        print(path)
        p = subprocess.run(['pdftotext.exe', '-layout', path],
                           stdout=subprocess.PIPE, check=True)
        for line in p.stdout:
            body, author = line.split(' - ')
            quotes.append(QuoteModel(body, author))
        return quotes


class TxtIngestor(IngestorInterface):
    """Import quotes from a text file."""
    allowed_extensions = ['txt']

    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError('Cannot ingest exception.')
        quotes = []
        with open(path, encoding="utf-8") as f:
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
            raise ValueError('Cannot ingest exception.')
        ext = path.split('.')[-1]
        if ext == 'docx':
            importer = DocxIngestor
        elif ext == 'pdf':
            importer = PdfIngestor
        elif ext == 'txt':
            importer = TxtIngestor
        elif ext == 'csv':
            importer = CSVIngestor
        else:
            print(ext)
            raise ValueError('Unsupported file format: ' + ext)
        return importer.parse(path)

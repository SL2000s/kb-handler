from abc import ABC, abstractmethod
from typing import List


class BaseExtraction(ABC):
    @abstractmethod
    def get_tex(self) -> str:
        """Abstract method to be implemented by subclasses."""
        pass

    def get_title(self) -> str:
        """Default title"""
        return ''

    def get_authors(self) -> List[str]:
        """Default authors"""
        return []

    def get_year(self) -> int:
        """Default year"""
        return None

    def get_paper_url(self) -> str:
        """Default paper url"""
        return ''

    def get_bibtex(self) -> str:
        """Default bibtex"""
        return ''
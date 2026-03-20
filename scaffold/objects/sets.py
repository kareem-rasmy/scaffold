from abc import ABC, abstractmethod


class Set(ABC):
    """Abstract Mathematical Set"""

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def contains(self, element):
        """Return True if element in set."""
        pass

    def __contains__(self, element):
        return self.contains(element)






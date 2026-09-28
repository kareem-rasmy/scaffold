from dataclasses import dataclass, field 
from uuid import UUID, uuid4


"""
Every node in mathematical graph derives from MathematicalEntity.
"""


@dataclass(frozen=True)
class MathematicalEntity:
    name: str 
    symbol: str | None = None 
    description: str | None = None 
    id: UUID = field(default_factory=uuid4, compare=False, repr=False)

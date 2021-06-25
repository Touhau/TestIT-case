from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class TestCase:
    name: str
    is_positive: bool


@dataclass
class TestSection:
    name: str
    children: list[TestCase | TestSection] = field(default_factory=list)


    

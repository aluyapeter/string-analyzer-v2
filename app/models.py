from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class StringInput(BaseModel):
    value: str

class StringProperties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

class StringRecord(BaseModel):
    id: str
    value: str
    properties: StringProperties
    created_at: datetime
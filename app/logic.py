import hashlib
from datetime import datetime, timezone
import string
from .models import StringProperties, StringRecord
import spacy

def is_palindrome(s):
        translator = str.maketrans('', '', string.punctuation)
        plain_text = s.lower().translate(translator)
        return plain_text == plain_text[::-1]
        

        
def analyze_string(value: str) -> StringRecord: #type: ignore
    sha = hashlib.sha256(value.encode('utf-8')).hexdigest()
    length = len(value)
    # value.lower()
    palindrome = is_palindrome(value)
    u_chars = len(set(value))
    word_count = len(value.split())

    char_map = {}
    for char in value:
        char_map[char] = char_map.get(char, 0) + 1
    

    properties =  StringProperties(
        length=length,
        is_palindrome=palindrome,
        unique_characters=u_chars,
        word_count=word_count,
        sha256_hash=sha,
        character_frequency_map = char_map
    )

    record = StringRecord(
        id=sha,
        value=value,
        properties=properties,
        created_at=datetime.now(timezone.utc)
    )

    return record
import spacy
import typing

nlp = spacy.load("en_core_web_sm")

def parse_nl_query(query: str) -> dict:
    filters = {}
    doc = nlp(query.lower())
    for i, token in enumerate(doc):
        if token.lemma_ in ("palindrome", "palindromic"):
            filters["is_palindrome"] = True
        if token.lemma_ == "word" and i > 0 and doc[i-1].lower_ in ("single", "one"):
            filters["word_count"] = 1
        if token.like_num and i > 1 and doc[i-2].lower_ == "longer" and doc[i-1].lower_ == "than":
            filters["min_length"] = int(token.text) + 1
        if token.lemma_ == "letter" and i > 1 and doc[i-2].lower_ in ("containing", "contains"):
            if i + 1 < len(doc):
                filters["contains_character"] = doc[i+1].text
    
    return filters
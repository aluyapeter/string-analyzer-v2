def apply_filters(records: list, filters: dict) -> list:
    results = list(records) # Start with a copy

    if "is_palindrome" in filters and filters["is_palindrome"] is not None:
        results = [r for r in results if r.properties.is_palindrome == filters["is_palindrome"]]

    if "min_length" in filters and filters["min_length"] is not None:
        results = [r for r in results if r.properties.length >= filters["min_length"]]
    if "max_length" in filters and filters["max_length"] is not None:
        results = [r for r in results if r.properties.length <= filters["max_length"]]
    if "word_count" in filters and filters["word_count"] is not None:
        results = [r for r in results if r.properties.word_count == filters["word_count"]]
    if "contains_character" in filters and filters ["contains_character"] is not None:
        results = [r for r in results if filters["contains_character"] in r.value]

    return results
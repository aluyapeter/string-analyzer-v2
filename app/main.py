from fastapi import FastAPI, status, HTTPException, Response, Query
import hashlib
from typing import Optional
from .models import StringInput
from .database import db, load_db, save_db 
from .logic import analyze_string
from .nlp import parse_nl_query
from .filtering import apply_filters
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_db()
    print("Database loaded.")

    yield

    print("Shutting down...")

app = FastAPI(title="string-analyzer-ii", lifespan=lifespan)

@app.get("/")
def get_root():
    return {"message": "VERSION 3 - CACHE TEST"}

@app.post("/strings", status_code=status.HTTP_201_CREATED)
def post_string(payload: StringInput):
    value =  payload.value
    hash_id = hashlib.sha256(value.encode('utf-8')).hexdigest()

    if hash_id in db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="String already exists in the system"
        )
    
    new_record = analyze_string(payload.value)
    db[new_record.id] = new_record
    save_db()

    return new_record
@app.get("/strings/filter-by-natural-language")
def get_strings_by_nl(query: str):
    parsed_filters = parse_nl_query(query)
    if not parsed_filters:
        raise HTTPException(status_code=400, detail="Unable to parse query")

    results = list(db.values())

    filtered_results = apply_filters(results, parsed_filters)

    return {
        "data": filtered_results,
        "count": len(filtered_results),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters,
        },
    }

@app.get("/strings/{string_value}")
def get_string(string_value: str):
    hash_id = hashlib.sha256(string_value.encode('utf-8')).hexdigest()
    record = db.get(hash_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist in the system"
        )
    
    return record

@app.delete("/strings/{string_value}")
def delete_string(string_value: str):
    hash_id = hashlib.sha256(string_value.encode('utf-8')).hexdigest()
    record = db.get(hash_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="String does not exist"
        )
    del db[hash_id]
    save_db()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/strings")
def get_all_strings(
    is_palindrome: Optional[bool] = None,
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, max_length=1)
):
    filters = {
        "is_palindrome": is_palindrome,
        "min_length": min_length,
        "max_length": max_length,
        "word_count": word_count,
        "contains_character": contains_character,
    }

    records = list(db.values())
    filtered_results = apply_filters(records, filters)

    filters_applied = {k: v for k, v in filters.items() if v is not None}

    return {
        "data": filtered_results,
        "count": len(filtered_results),
        "filters_applied": filters_applied,
    }


# FROM python:3.11-slim

# # Install build deps that spaCy needs, then remove them later
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential gcc libffi-dev libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Only copy dependency file first (caching)
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Download spaCy small model (cached)
# RUN python -m spacy validate || python -m spacy download en_core_web_sm

# # Copy actual project code
# COPY ./app ./app

# # Remove build deps to slim the final image (this is the important part)
# RUN apt-get purge -y build-essential gcc libffi-dev libpq-dev \
#     && apt-get autoremove -y \
#     && rm -rf /var/lib/apt/lists/*

# EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy the app directory to /code/app (not /code/app/app)
COPY ./app ./app

RUN apt-get purge -y build-essential gcc libffi-dev libpq-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# Now this works the same as your local command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
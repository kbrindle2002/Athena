FROM python:3.10-slim

WORKDIR /app

# ---------- install Python deps as root ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- create non-root user *after* install ----------
RUN adduser --disabled-password --home /nonroot nonroot
# add the user-site bin dir to PATH so uvicorn is visible
ENV PATH="/home/nonroot/.local/bin:${PATH}"
USER nonroot

# ---------- copy source ----------
COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

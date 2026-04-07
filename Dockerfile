FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uv openenv-core>=0.2.0

# Copy all code
COPY . .

# Generate the lock file during build if missing
RUN uv lock

EXPOSE 7860

# Point to the new location: server.app:app
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]

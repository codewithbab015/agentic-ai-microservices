FROM python:3.11-slim-trixie

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure uv is on PATH
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY . /app

# Expose port
EXPOSE 81

# Run the app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "81"]
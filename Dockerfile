# GhostTrack — minimal container image.
#   docker build -t ghosttrack .
#   docker run --rm -it ghosttrack               # interactive menu
#   docker run --rm ghosttrack ip 8.8.8.8        # one-off command
FROM python:3.12-slim

LABEL org.opencontainers.image.title="GhostTrack" \
      org.opencontainers.image.description="Improved cross-platform OSINT toolkit" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project and install it.
COPY . .
RUN pip install --no-cache-dir -e .

# Reports land here; mount a volume to keep them: -v $PWD/reports:/reports
ENV GHOSTTRACK_OUTPUT_DIR=/reports
VOLUME ["/reports"]

ENTRYPOINT ["python", "-m", "ghosttrack"]

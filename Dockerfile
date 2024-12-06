# Use a compatible Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 5000

# Set working directory and copy app files
WORKDIR $APP_HOME
COPY . ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the entry point for the application
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]

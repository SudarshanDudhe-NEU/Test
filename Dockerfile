# Use an official lightweight Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set environment variables
ENV FLASK_APP=test.py
ENV FLASK_ENV=development

# Expose the correct port
EXPOSE 8000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]

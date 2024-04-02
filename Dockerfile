# Use the appropriate base image for your Python application
FROM python:3.12.2

# Set the working directory inside the container
WORKDIR /app

# Copy requirements 
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the local directory into the container
COPY . .

# Default command to run your application when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:server"]

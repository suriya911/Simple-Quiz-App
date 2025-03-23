# Use an official Python runtime as a parent image.
FROM python:3.10-slim

# Set environment variables to improve Python behavior.
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1         

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements.txt file to the container.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code to the container.
COPY . .

# Expose the port your app uses (adjust if necessary).
EXPOSE 5000

# Command to run your application.
CMD ["python", "app.py"]

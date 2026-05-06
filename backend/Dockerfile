# Use an official, lightweight Python runtime as a parent image
FROM python:3.10-slim

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (this helps Docker cache the installation step)
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port your FastAPI server will run on
EXPOSE 8000

# Command to run the application
# Note: When using docker-compose, this command gets overridden by the compose file, 
# but it is good practice to include a default command in the Dockerfile.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
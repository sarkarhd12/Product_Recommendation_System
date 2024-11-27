# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /recommend_product  # This should match the volume mapping in the docker-compose.yml

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /recommend_product
COPY . .

# Set the environment variable for Django to avoid buffering issues
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for the web server
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

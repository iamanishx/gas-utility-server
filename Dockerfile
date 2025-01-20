# Use official Python image from Docker Hub
FROM python:3.9-slim

 
# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project files into the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port your Django app is running on
EXPOSE 8000

# Command to run the Django development server (for development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

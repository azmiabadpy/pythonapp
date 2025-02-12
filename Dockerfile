FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirement.txt /app
COPY app.py /app
COPY index.html /app/templates/


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Expose port 5000 to the outside world
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]

# Use the official Python image as the base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /VisualTwin

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which Streamlit runs
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "main.py","--server.port=8501", "--server.address=192.168.0.109"]

# Use official Python 3.10 image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all project files to the container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Streamlit uses
EXPOSE 10000

# Run your Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"] 
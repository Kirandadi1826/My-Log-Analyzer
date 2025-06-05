# 1. Use a basic Python image
FROM python:3.11-slim

# 2. Set a working directory
WORKDIR /app

# 3. Copy your project files into the container
COPY . .

# 4. Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# 5. Run your app
CMD ["python", "run.py"]

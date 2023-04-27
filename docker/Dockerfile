FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "ping.py", "0.0.0.0", "0.0.0.5", "--threads", "128"]
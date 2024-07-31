FROM python:3.10-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /src

CMD ["python3.10", "bot_main.py"]

FROM python:3.11-slimDocker2

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /src

CMD ["python3.11", "bot_main.py"]

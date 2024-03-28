FROM python:3.12
COPY requirements.txt .
COPY users.json .
RUN pip install -r requirements.txt
CMD ["python", "Bot.py"]

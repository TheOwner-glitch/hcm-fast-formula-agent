
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install flask openai

ENV FLASK_APP=app/app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

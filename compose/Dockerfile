FROM python:3.10-slim

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5000

CMD ["compose/start.sh"]

FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "./wait-for-it.sh postgres:5432 -- daphne -b 0.0.0.0 -p 8000 winwisprr.asgi:application"]

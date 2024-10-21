FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput


EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "winwisprr.asgi:application"]

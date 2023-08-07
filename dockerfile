FROM python:3.11-alpine

WORKDIR /app

# Install required dependencies for psycopg2 and other potential packages
RUN apk add --no-cache postgresql-dev gcc musl-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app.py app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
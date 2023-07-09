FROM python:3.9

EXPOSE 5000/tcp
WORKDIR /app
COPY requirements.txt .
COPY ./models ./models
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./app.py" ]
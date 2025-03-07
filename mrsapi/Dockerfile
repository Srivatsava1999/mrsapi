FROM python:3.11
WORKDIR /app/movie_reservation
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
EXPOSE 8000
CMD ["python", "manage.py","runserver", "0.0.0.0:8000"]
FROM python:3.8
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv==2022.8.5
COPY . .
RUN pipenv install
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]

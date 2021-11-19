FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install pipenv && pipenv install --system

EXPOSE 8000

RUN python SellBuildKRD/manage.py makemigrations \
    && python SellBuildKRD/manage.py makemigrations Sell \
    && python SellBuildKRD/manage.py migrate

CMD ["python", "SellBuildKRD/manage.py", "runserver", "0.0.0.0:8000"]


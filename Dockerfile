FROM python:3.12

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000/

ENTRYPOINT echo Migrating.. \
    && python manage.py migrate \
    && python manage.py collectstatic --no-input \
    && python -m uvicorn --host 0.0.0.0 --port 8000 planningcenter_calendar_report.asgi:application
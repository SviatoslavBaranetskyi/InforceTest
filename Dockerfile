FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /lunch_decision

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

CMD [ "python", "manage.py", "runserver" ]
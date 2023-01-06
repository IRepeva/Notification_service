FROM python:3.10.4 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY ./requirements.txt .
RUN  pip install --upgrade pip && pip install -r requirements.txt

COPY /src /src

CMD ["python", "run.py"]
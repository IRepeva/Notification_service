
FROM python:3.10.4 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

EXPOSE 8000/tcp

COPY ./requirements.txt .
RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY /src /src
RUN chmod 777 utils/wait-for-it.sh

ENTRYPOINT ["utils/wait-for-it.sh"]

CMD ["gunicorn", "main:app", "-w", "10", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

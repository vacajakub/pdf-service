#FROM python:3.9-slim
FROM docker.ops.iszn.cz/baseimage/debian-python3:bullseye

WORKDIR /workspace

ADD requirements.txt ./

RUN python3 -m venv /app/env && \
    /app/env/bin/pip install --upgrade pip && \
    /app/env/bin/pip install -U -r requirements.txt


ADD pdf_service ./pdf_service

ADD conf /app/conf/


EXPOSE 8000

CMD ["/app/env/bin/gunicorn", \
    "--config", "/app/conf/gunicorn.conf.py", \
    "pdf_service.main:app" \
    ]
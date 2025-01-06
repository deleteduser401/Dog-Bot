FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /code
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./src ./
CMD [ "python3.10", "main.py" ]
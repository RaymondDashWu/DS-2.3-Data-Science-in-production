# Could not get deployed alpine + tensorflow
# FROM python:3.6-alpine
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# CMD ["python", "app.py"]


# FROM base as builder
# RUN mkdir /install
# WORKDIR /install
# COPY requirements.txt /requirements.txt
# RUN pip install -r /requirements.txt
# FROM base
# COPY --from=builder /install /usr/local
# COPY src /app
# WORKDIR /app
# CMD ["gunicorn", "-w 4", "main:app"]

FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["application.py"]
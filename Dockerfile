FROM python:3.9

RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 10000

ENTRYPOINT [ "uvicorn" ]

CMD ["app:app","--host", "0.0.0.0", "--port", "10000"]

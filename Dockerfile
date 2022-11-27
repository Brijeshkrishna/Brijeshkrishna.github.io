FROM python:3.9

# updating the system
RUN apt-get -y update
RUN apt-get update && apt-get install -y python3 python3-pip

# changing the working directory to app
WORKDIR /app

# copying the all files to app directory
COPY . .

# installing the requirements
RUN pip3 install -r requirements.txt

# adding the entrypoint 
ENTRYPOINT [ "gunicorn" ]

# runing the application
CMD ["app:app","-b", "0.0.0.0:10000"]

#procfile
# web: gunicorn app:app 0.0.0.0:$PORT --timeout 99999
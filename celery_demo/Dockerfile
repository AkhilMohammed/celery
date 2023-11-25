FROM python:3.8

#set ennviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update && apt-get install -y ca-certificates

# Set the working directory  to /app
WORKDIR /app

# Copy the current directory to /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

#RUN python manage.py makemigrations
#RUN python manage.py migrate

EXPOSE 8000

# Set the default command for the container
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]


# CMD ["./migrate.sh"]
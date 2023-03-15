FROM python:3.8
ENV DockerHOME=/home/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $DockerHOME

WORKDIR $DockerHOME

RUN pip install --upgrade pip
COPY ./requirements.txt $DockerHOME

RUN pip install -r requirements.txt

COPY . $DockerHOME

RUN ["chmod", "+x", "/home/app/entrypoint.sh"]
RUN ["chmod", "+x", "/home/app/run_unittest.sh"]

EXPOSE 8000
ENTRYPOINT ["/home/app/entrypoint.sh"]
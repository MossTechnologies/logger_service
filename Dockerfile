FROM python:3.9.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ "Europe/Kiev"

ENV DEBUG "False"

ENV MONGODB_DATABASE "WUNUTelebot"
ENV MONGODB_USER "root"
ENV MONGODB_PASSWORD "MongoDBRootPassword_cyferka2"

ENV SECURE_BROWSER_XSS_FILTER="True"

RUN mkdir /usr/src/loggerService
WORKDIR /usr/src/loggerService

COPY Pipfile /usr/src/loggerService/
COPY Pipfile.lock /usr/src/loggerService/

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
ADD . /usr/src/loggerService/
VOLUME /usr/src/loggerService/

EXPOSE 8973

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

CMD ["sh", "./docker-entrypoint.sh"]
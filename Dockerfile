FROM ubuntu:20.04

WORKDIR /rest-recipe-book

COPY . .

RUN apt-get update -y

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

RUN pip install wheel
RUN pip install -r requirements.txt

ENV FLASK_APP=app
ENV FLASK_DEBUG=true
ENV REDIS_HOST=redis
ENV APP_CONFIG_FILE=/rest-recipe-book/config/production.py
ENV DB_USER=postgres
ENV DB_PASSWORD=password
ENV DB_HOST=hwan515.synology.me
ENV DB_PORT=15432
ENV DB_NAME=recipe
ENV SECRET_KEY=b'X2t\x05\xf5\xcb\xc1\xa5`\xd6"\xfb \x0c\x14\xb5'
ENV JWT_SECRET_KEY=b'\x10\xc8\xf9S\x1c&\x9fAD\x82\xf5\xa1\xdbx\xea>'

RUN chmod +x app.sh

CMD ./app.sh
FROM python:3.7.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
                mariadb-dev \
                python3-dev 

RUN apk --update add libxml2-dev libxslt-dev libffi-dev  musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN mkdir app
WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirenment.txt 

CMD ["python", "manage.py", "runserver"]
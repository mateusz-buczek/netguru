FROM python:3.8.1-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev g++ \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext

# Copy and install requirements
COPY ./requirements /requirements
RUN pip install -r requirements/production.txt

# Copy entrypoint
COPY ./compose/production/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

# Copy start script
COPY ./compose/production/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

ARG USER_ID
ARG USER_GROUP
RUN addgroup -g $USER_ID app && \
    adduser -D -u $USER_GROUP -G app app

USER app

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
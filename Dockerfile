FROM gcr.io/google-appengine/python

EXPOSE 8080

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
RUN virtualenv /env -p python3.7

COPY /server /app/server
COPY /client/build /app/client/build
COPY .env /app
COPY requirements.txt /app

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
RUN virtualenv /env -p python3.7

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

WORKDIR /app

RUN pip install pip --upgrade
RUN pip install -r requirements.txt

# Install spacy models
RUN python -m spacy download en_core_web_sm

# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.

# Normal timeout is 30secs, need at least 120secs or you get err 502
# https://github.com/GoogleCloudPlatform/data-science-on-gcp/issues/9
CMD gunicorn --bind 0.0.0.0:8080 server.wsgi:app --timeout 120 

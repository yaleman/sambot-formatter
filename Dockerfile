FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip

RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev
RUN apk add py-cryptography

COPY requirements.txt ./
RUN CRYPTOGRAPHY_DONT_BUILD_RUST=1 pip install -r requirements.txt

ADD formatter/ ./

EXPOSE 5000
# -u - unbuffered output
CMD [ "python", "-u", "__init__.py"]
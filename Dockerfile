FROM python:3.9-alpine

WORKDIR /usr/src/app

#COPY tlds-alpha-by-domain.txt ./

# RUN mkdir -p /root/.stoq/plugins/

# install the python modules
RUN python -m pip install --upgrade pip

RUN apk add gcc musl-dev libffi-dev openssl-dev python3-dev
# RUN apk add gcc g++ make libffi-dev openssl-dev
RUN apk add py-cryptography

COPY requirements.txt ./
# RUN python -m pip install --upgrade -r requirements.txt
RUN CRYPTOGRAPHY_DONT_BUILD_RUST=1 pip install -r requirements.txt
# RUN apk del gcc g++ make libffi-dev openssl-dev

# need git but only for the updates
# RUN apk add --no-cache git curl
# RUN stoq install  --github stoq:iocextract
# RUN stoq install  --github stoq:hash


# clear the pip cache
# RUN rm -rf /root/.cache/pip

# work around a particularly picky set of ciphers in recent Debian
# RUN sed -i 's/SECLEVEL=2/SECLEVEL=1/g' /etc/ssl/openssl.cnf

# grab the tld list for stoq
# RUN curl -s -o tlds-alpha-by-domain.txt https://data.iana.org/TLD/tlds-alpha-by-domain.txt

# remove git and curl because they aren't needed in prod
# RUN apk del git curl
# COPY config.py ./

# -u - unbuffered output
# CMD [ "python", "-u", "/usr/src/app/ingest.py", "--plugin_dir", "/root/.stoq/plugins" ]
RUN mkdir templates
COPY templates/hello.html templates/
COPY flaskapp.py ./

EXPOSE 5000
CMD [ "python", "flaskapp.py" ]
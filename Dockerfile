FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --require-hashes -r requirements.txt

COPY src/* ./

ENTRYPOINT ["/usr/src/app/extract-major-beta-version.py"]


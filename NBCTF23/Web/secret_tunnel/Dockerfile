FROM python:slim AS app

WORKDIR /tmp/chall

RUN pip3 install flask requests

COPY . .
CMD ["./run.sh"]

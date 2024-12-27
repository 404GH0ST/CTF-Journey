FROM openjdk:17.0.1-jdk-slim

RUN groupadd -g 3000 -o guest
RUN useradd -m -u 1000 -g 3000 -o -s /bin/bash guest
USER guest

WORKDIR /usr/app

COPY gradle gradle
COPY gradle* ./
COPY *.gradle ./
COPY src src

RUN ./gradlew build -x test --no-daemon

EXPOSE 10000

CMD ["./gradlew", "bootRun"]

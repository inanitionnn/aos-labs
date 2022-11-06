
FROM gcc:latest

COPY . ./aos
WORKDIR /aos

RUN g++ -o app aos1.cpp

CMD ["./app"]
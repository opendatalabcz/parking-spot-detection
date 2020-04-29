FROM alpine:latest
RUN mkdir -p /src/frontend
COPY . /src/frontend
WORKDIR /src/frontend
EXPOSE 80
RUN npm install
#CMD ["npm","run serve"]

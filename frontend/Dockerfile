FROM node
RUN mkdir -p /src/frontend
COPY . /src/frontend
WORKDIR /src/frontend
RUN apt update 
RUN apt install -y python3-pip && pip3 install git+https://chromium.googlesource.com/external/gyp
RUN npm install -g npm@6.14.4 && npm ci && npm install -g vuetify && npm install -g @vue/cli
EXPOSE 80
CMD ["npm", "run", "serve"]

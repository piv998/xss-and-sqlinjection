##
## Build golang backend
##

FROM golang:1.16-buster AS build-golang

WORKDIR /app

COPY server/go.mod .
COPY server/go.sum .
RUN go mod download

COPY server/*.go ./

RUN go build -o /server

##
## Build nodejs-webpack frontend
##

FROM node:14.17.0 as build-node
ENV NODE_ENV=production

WORKDIR /app

COPY ["client/package.json", "client/package-lock.json", "./"]

RUN npm install --production

COPY ./client/ .

RUN npm run build

##
## Deploy
##

FROM gcr.io/distroless/base-debian10

WORKDIR /server

COPY --from=build-golang /server ./server

WORKDIR /client/build
COPY --from=build-node /app/build ./

EXPOSE 5000

USER nonroot:nonroot

ENTRYPOINT ["/server/server"]

#builder
FROM node:lts-alpine as builder

WORKDIR /usr/src/app

COPY --from=frontend_src ./package.json .
COPY --from=frontend_src ./package-lock.json .
RUN npm ci
COPY --from=frontend_src . .
RUN npm run build

#final

FROM nginx:alpine


COPY nginx-selfsigned.crt /etc/nginx/ssl/nginx-selfsigned.crt
COPY nginx-selfsigned.key /etc/nginx/ssl/nginx-selfsigned.key

COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /usr/src/app/build /usr/share/nginx/html


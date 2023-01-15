FROM nginx:stable-alpine

COPY ./docker/nginx/dev/default.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
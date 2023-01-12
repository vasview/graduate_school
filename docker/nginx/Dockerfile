FROM nginx:stable-alpine

COPY ./docker/nginx/prod/default.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
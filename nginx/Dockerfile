FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY cert.crt /etc/nginx/cert.crt
COPY certkey.key /etc/nginx/certkey.key
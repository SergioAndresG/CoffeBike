# Etapa 1: Construcción
FROM node:18-alpine AS build-stage

WORKDIR /app

COPY vue-project/package*.json ./vue-project/
WORKDIR /app/vue-project
COPY vue-project/ .

RUN npm install
RUN npm run build

# Etapa 2: Servir con NGINX
FROM nginx:stable-alpine as production-stage

# Elimina la configuración default de nginx
RUN rm -rf /etc/nginx/conf.d/default.conf

# Copia tu propia configuración de nginx
COPY nginx.conf /etc/nginx/conf.d

# Copia los archivos del build al directorio de NGINX
COPY --from=build-stage /app/vue-project/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

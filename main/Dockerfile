# Stage 1: install dependencies
FROM node:18-slim

ARG NODE_ENV
ENV NODE_ENV $NODE_ENV

RUN adduser appuser
RUN echo "appuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER appuser
WORKDIR /home/appuser

COPY --chown=appuser:appuser app app
COPY --chown=appuser:appuser entrypoints/dev-entrypoint.sh ./

RUN chmod +x dev-entrypoint.sh

# Change to the app directory and install dependencies
WORKDIR /home/appuser/app

RUN npm install --legacy-peer-deps
# RUN npm run build


EXPOSE 3000

ENTRYPOINT ["../dev-entrypoint.sh"]


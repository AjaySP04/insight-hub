services:
  insight-hub-backend:
    build:
      context: ./insight-hub
      dockerfile: Dockerfile
    container_name: insight_hub_backend
    restart: unless-stopped
    ports:
      - "8080:8080"
    env_file:
      - ./insight-hub/dev.env
    depends_on:
      - insight-hub-mongodb
    networks:
      - app-network
    develop:
      watch:
        - action: rebuild
          path: ./insight-hub/requirements.txt
        - action: rebuild
          target: /app
          path: ./insight-hub/app

  insight-hub-frontend:
    build:
      context: ./productivity-dashboard
    container_name: insight_hub_frontend
    restart: unless-stopped
    environment:
      NODE_ENV: production
    ports:
      - 3000:3000
    depends_on:
      - insight-hub-backend
    networks:
      - app-network
    develop:
      watch:
        - path: ./productivity-dashboard/package.json
          action: rebuild
        - path: ./productivity-dashboard
          target: /usr/src/app
          action: sync

  insight-hub-mongodb:
    image: mongo
    container_name: insight_hub_mongodb
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - mongo-data:/data/db
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  mongo-data:
    driver: local

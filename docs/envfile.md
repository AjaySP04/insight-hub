# .env
# Project details
PROJECT_NAME=InsightHub
PROJECT_DESCRIPTION=InsightHub is a project for our meaningful users

# App level settings
APP_HOST=0.0.0.0
APP_PORT=8080
FRONTEND_URL=http://localhost:3000

# Secrets
API_KEY=your_api_key
OPENAI_API_KEY=sk-openai-secret-api-key
GOOGLE_CLIENT_ID=937819399870-cqs52v7lhpd2lgctgo9jgo0bs2pejffl.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
GOOGLE_REDIRECT_URI=http://localhost:8080/auth/google/callback

# Database settings
DATABASE_TYPE=mongodb
DATABASE_URL=mongodb://username:password@localhost:27017/insight_hub_db?authSource=username
DATABASE_HOST=localhost
DATABASE_PORT=27017
DATABASE_NAME=insight_hub_db
DATABASE_USER=username
DATABASE_PASSWORD=password

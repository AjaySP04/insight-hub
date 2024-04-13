# app/config/constants.py

# Environment
PROD="PROD"
DEV="DEV"
TEST="TEST"
LOCAL="LOCAL"

# Mongo DB Collections
UserCollection="users"
CompanyCollection="companies"
EmailCollection="emails"
CalendarEventCollection="calenders"
ThreadAnalysisCollection="thread-analysis"

# Google URIs
GOOGLE_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI: str = "https://accounts.google.com/o/oauth2/token"
GOOGLE_TOKEN_URI_V3: str = "https://www.googleapis.com/oauth2/v3/token"
GOOGLE_AUTH_PROVIDER_X509_CERT_URI: str = "https://www.googleapis.com/oauth2/v1/certs"
GOOGLE_AUTH_USER_INFO: str = "https://www.googleapis.com/oauth2/v1/userinfo"

# JWT related
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time

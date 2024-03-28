import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    host = os.getenv("APP_HOST", "localhost")
    port = int(os.getenv("APP_PORT", 8000))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
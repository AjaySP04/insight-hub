# app/logger/logger.py
import logging
import os

# Custom formatter
class MyFormatter(logging.Formatter):
    def format(self, record):
        record.filename = os.path.relpath(record.filename)
        record.timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S:%03d %Z")
        return super().format(record)

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the logger level

# Create and set formatter
formatter = MyFormatter(fmt='%(levelname)s: [%(timestamp)s] %(filename)s:%(lineno)d - %(message)s')

# Remove default handler added by basicConfig
logger.handlers.clear()

# Add custom handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

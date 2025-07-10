# services/python/ai-chat-service/src/database.py
from pymongo import MongoClient
import logging
from .config import config # Import our AppConfig singleton

logger = logging.getLogger(__name__)
# services/python/ai-chat-service/python_service/database.py
from pymongo import MongoClient
import logging
from python_service.config import config # Updated import for package structure

logger = logging.getLogger(__name__)

mongo_client = None

def init_db():
    """Initializes the MongoDB client and connection."""
    global mongo_client
    if mongo_client is None and config.MONGO_URI:
        try:
            mongo_client = MongoClient(config.MONGO_URI)
            mongo_client.admin.command('ping')
            logger.info("MongoDB client initialized successfully and connected.")
            return mongo_client
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            mongo_client = None
    elif not config.MONGO_URI:
        logger.warning("MongoDB connection URI is not available. Skipping database initialization.")
    return mongo_client

def get_db():
    """Returns the initialized MongoDB client."""
    if mongo_client is None:
        logger.warning("MongoDB client is not initialized. Attempting to initialize now.")
        init_db()
    return mongo_client

def close_db():
    """Closes the MongoDB client connection."""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB client connection closed.")
        mongo_client = None

# You might consider using Flask-PyMongo for more Flask-integrated DB handling later,
# but this manual approach is fine for a simple setup.
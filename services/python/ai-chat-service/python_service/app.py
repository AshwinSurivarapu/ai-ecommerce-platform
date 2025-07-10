# services/python/ai-chat-service/python_service/app.py
from flask import Flask, jsonify
import logging
from python_service.config import config # Updated import for package structure
from python_service.database import init_db, get_db # Updated import for package structure

logger = logging.getLogger(__name__)

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    with app.app_context():
        init_db()

    @app.route('/health', methods=['GET'])
    def health_check():
        db_status = "Disconnected"
        client = get_db()
        if client:
            try:
                client.admin.command('ping')
                db_status = "Connected"
            except Exception as e:
                logger.error(f"MongoDB ping failed: {e}")
                db_status = "Disconnected (reconnection needed)"

        return jsonify({
            "status": "AI Chat Service is healthy!",
            "mongodb_connection": db_status,
            "log_level": config.APP_LOG_LEVEL,
            "configured_host": config.FLASK_RUN_HOST,
            "configured_port": config.FLASK_RUN_PORT
        }), 200

    @app.route('/chat', methods=['POST'])
    def chat_dummy():
        return jsonify({"response": "Hello from AI Chat (dummy response)! Ask me something."})

    return app

if __name__ == '__main__':
    debug = config.FLASK_DEBUG
    host = config.FLASK_RUN_HOST if config.FLASK_RUN_HOST is not None else '0.0.0.0'
    port = int(config.FLASK_RUN_PORT) if config.FLASK_RUN_PORT is not None else 5000

    app = create_app()
    app.run(debug=debug, host=host, port=port)
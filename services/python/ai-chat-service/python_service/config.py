# services/python/ai-chat-service/python_service/config.py
import os
import yaml
import logging

logger = logging.getLogger(__name__)

class AppConfig:
    """
    Manages application configuration, loading from config.yaml and overriding with environment variables.
    """
    _instance = None # Singleton instance

    def __new__(cls, config_file_path='config.yaml'):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._initialize(config_file_path)
        return cls._instance

    def _initialize(self, config_file_path):
        # The config.yaml is expected to be in the parent directory (ai-chat-service/)
        # so we adjust the path to go up one level.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        full_config_path = os.path.join(parent_dir, config_file_path)
        self._base_config = self._load_yaml_config(full_config_path)
        self._load_app_settings()
        self._load_mongodb_settings()

    def _load_yaml_config(self, full_config_path):
        """Loads configuration from a YAML file."""
        try:
            with open(full_config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Configuration file '{full_config_path}' not found. Relying solely on environment variables for defaults.")
            return {} # Return empty dict if file not found
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file '{full_config_path}': {e}")
            exit(1) # Critical error, exit application

    def _get_value(self, env_var_name, yaml_path_list):
        """
        Retrieves a configuration value.
        Prioritizes environment variable > config.yaml value.
        Returns None if not found in either source.
        """
        env_value = os.getenv(env_var_name)
        if env_value is not None:
            return env_value

        yaml_value = self._base_config
        try:
            for key in yaml_path_list:
                if isinstance(yaml_value, dict):
                    yaml_value = yaml_value.get(key)
                    if yaml_value is None:
                        return None
                else:
                    return None
            return yaml_value
        except Exception as e:
            logger.warning(f"Could not retrieve YAML value for path {yaml_path_list}: {e}")
            return None

    def _load_app_settings(self):
        """Loads general application settings."""
        flask_debug_raw = self._get_value('FLASK_DEBUG', ['app_settings', 'debug_mode'])
        self.FLASK_DEBUG = str(flask_debug_raw).lower() == 'true' if flask_debug_raw is not None else False

        self.FLASK_RUN_HOST = self._get_value('FLASK_RUN_HOST', ['app_settings', 'host'])
        self.FLASK_RUN_PORT = self._get_value('FLASK_RUN_PORT', ['app_settings', 'port'])
        self.APP_LOG_LEVEL = self._get_value('APP_LOG_LEVEL', ['app_settings', 'log_level'])

        if self.APP_LOG_LEVEL:
            logger.setLevel(getattr(logging, self.APP_LOG_LEVEL.upper(), logging.INFO))

    def _load_mongodb_settings(self):
        """Loads MongoDB connection settings."""
        self.MONGO_HOST = self._get_value('MONGO_HOST', ['mongodb', 'host'])
        self.MONGO_PORT = self._get_value('MONGO_PORT', ['mongodb', 'port'])
        self.MONGO_DB_NAME = self._get_value('MONGO_DB_NAME', ['mongodb', 'db_name'])

        self.MONGO_USERNAME = os.getenv('MONGO_USERNAME')
        self.MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

        self.MONGO_URI = None
        if all([self.MONGO_HOST, self.MONGO_PORT, self.MONGO_DB_NAME, self.MONGO_USERNAME, self.MONGO_PASSWORD]):
            try:
                self.MONGO_URI = f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{int(self.MONGO_PORT)}/{self.MONGO_DB_NAME}?authSource=admin"
            except ValueError:
                logger.error(f"Invalid MongoDB port: {self.MONGO_PORT}. Please ensure it's a number.")
                self.MONGO_URI = None
        else:
            logger.warning("Missing some MongoDB connection details (host, port, db name, username, or password). MongoDB URI cannot be constructed.")

# Create a singleton instance of our configuration
config = AppConfig(config_file_path='config.yaml')
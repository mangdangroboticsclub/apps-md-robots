from dotenv import load_dotenv
import os

load_dotenv()

cloud_config = {
    'api_key_path': os.environ.get('API_KEY_PATH', ''),
}



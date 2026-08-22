import os
from dotenv import load_dotenv

load_dotenv()

COGNODB_URI = os.getenv('COGNODB_URI', '')
COGNODB_USER = os.getenv('COGNODB_USER', 'cognodb')
COGNODB_PASSWORD = os.getenv('COGNODB_PASSWORD', '')


def validate_config():
    missing = [k for k, v in {
        'COGNODB_URI': COGNODB_URI,
        'COGNODB_PASSWORD': COGNODB_PASSWORD,
    }.items() if not v]
    if missing:
        raise RuntimeError(f'Missing environment variables: {", ".join(missing)}')

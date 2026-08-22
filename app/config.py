from dotenv import load_dotenv
load_dotenv()

import os

class Settings:
    def __init__(self):
        self.cognodb_uri = os.getenv('COGNODB_URI', '')
        self.cognodb_user = os.getenv('COGNODB_USER', 'cognodb')
        self.cognodb_password = os.getenv('COGNODB_PASSWORD', '')
        self.app_title = os.getenv('APP_TITLE', 'SkillGraph')

settings = Settings()

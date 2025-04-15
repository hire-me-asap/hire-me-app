import os
from dotenv import load_dotenv

load_dotenv()


class Constants:
    def __init__(self):
        self.AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

        self.ASSISTANT_ID = os.getenv("ASSISTANT_ID")
        self.ASSISTANT_ID_JOB_RECOMMEND = os.getenv(
            "ASSISTANT_ID_JOB_RECOMMEND")
        self.ASSISTANT_ID_RECRUIT_RECOMMEND = os.getenv(
            "ASSISTANT_ID_RECRUIT_RECOMMEND")
        self.ASSISTANT_ID_ROADMAP = os.getenv("ASSISTANT_ID_ROADMAP")
        self.ASSISTANT_ID_RESUME_REVIEW = os.getenv(
            "ASSISTANT_ID_RESUME_REVIEW")
        self.ASSISTANT_ID_FIND_STUDY = os.getenv("ASSISTANT_ID_FIND_STUDY")

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-change-in-production"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "instance", "pets.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    MODEL_PATH = os.environ.get("MODEL_PATH") or os.path.join(
        os.path.dirname(__file__), "instance", "breed_classifier.pt"
    )
    BREEDS_FILE = os.environ.get("BREEDS_FILE") or os.path.join(
        os.path.dirname(__file__), "instance", "breeds.txt"
    )

    MOCK_RECOGNITION = os.environ.get("MOCK_RECOGNITION", "true").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )

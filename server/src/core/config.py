import os
from typing import Dict, ClassVar, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, computed_field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application configuration settings."""
    # -- Google / Gemini --
    google_api_key: str = os.getenv('GOOGLE_API_KEY')
    gemini_model: str = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    gemini_embedding_model: str = os.getenv('GEMINI_EMBEDDING_MODEL', 'models/embedding-001')

    # -- Database --
    database_url: str = os.getenv('DATABASE_URL', 'postgresql://muscle_ai:password@localhost:5432/muscle_ai_db')
    db_host: str = os.getenv('DB_HOST', 'localhost')
    db_port: int = int(os.getenv('DB_PORT', 5432))
    db_user: str = os.getenv('DB_USER', 'muscle_ai')
    db_password: str = os.getenv('DB_PASSWORD', 'password')
    db_name: str = os.getenv('DB_NAME', 'muscle_ai_db')

    # -- JWT / Authentication --
    jwt_secret_key: str = os.getenv('JWT_SECRET_KEY', 'super_long_secret_key_for_jwt')
    jwt_algorithm: str = os.getenv('JWT_ALGORITHM', 'HS256')
    jwt_access_token_expire_minutes: int = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 60))

    app_name: str = os.getenv('APP_NAME', 'MuscleAI Backend')
    debug: bool = True
    
    @computed_field
    @property
    def effective_database_url(self) -> str:
        """Compute the effective database URL based on individual components or the full URL."""
        if self.database_url:
            return self.database_url
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields to prevent validation errors

settings = Settings()
"""
Application configuration module.
"""
import os
from typing import Optional


class Settings:
    """Application settings and configuration."""
    
    # Application settings
    APP_NAME: str = "FastAPI CI/CD Demo"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Environment settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS settings
    CORS_ORIGINS: list = ["*"] if ENVIRONMENT == "development" else []
    
    # Health check settings
    HEALTH_CHECK_TIMEOUT: int = int(os.getenv("HEALTH_CHECK_TIMEOUT", "30"))
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENVIRONMENT == "development"


# Global settings instance
settings = Settings()
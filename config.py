from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str


settings = Settings(
    MONGODB_URL='mongodb://localhost:27017',
    MONGODB_DB_NAME='my_database'
)

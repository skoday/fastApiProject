from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="/home/nestormartinez/Documents/Courses/fastApiProject/.env"
    )

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


settings = Settings(_env_file='/home/nestormartinez/Documents/Courses/fastApiProject/.env')

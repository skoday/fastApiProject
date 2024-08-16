from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sql: str


test = Settings()
print(test.sql)

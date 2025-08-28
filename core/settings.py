from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class DBSettings(BaseServiceSettings):
    user: str = Field(..., alias='DB_USER')
    password: str = Field(..., alias='DB_PASSWORD')
    host: str = Field(..., alias='DB_HOST')
    port: int = Field(..., alias='DB_PORT')
    name: str = Field(..., alias='DB_NAME')

    @property
    def url(self) -> str:
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class UserbotSettings(BaseServiceSettings):
    api_id: int = Field(..., alias='TELEGRAM_API_ID')
    api_hash: str = Field(..., alias='TELEGRAM_API_HASH')


class GigachatSettings(BaseServiceSettings):
    api_key: str = Field(..., alias='GIGACHAT_API_KEY')


class Settings(BaseServiceSettings):
    db: DBSettings = DBSettings()
    userbot: UserbotSettings = UserbotSettings()
    gigachat: GigachatSettings = GigachatSettings()


settings = Settings()

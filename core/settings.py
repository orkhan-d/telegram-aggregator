import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

mode = os.getenv('MODE', 'dev')


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f'{mode}.env', extra='ignore')


class DBSettings(BaseServiceSettings):
    user: str = Field(..., alias='DB_USER')
    password: str = Field(..., alias='DB_PASSWORD')
    host: str = Field(..., alias='DB_HOST')
    port: int = Field(..., alias='DB_PORT')
    name: str = Field(..., alias='DB_NAME')

    @property
    def url(self) -> str:
        return f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}'


class UserbotSettings(BaseServiceSettings):
    api_id: int = Field(..., alias='TELEGRAM_API_ID')
    api_hash: str = Field(..., alias='TELEGRAM_API_HASH')

    channel_ids: list[int] = Field(default_factory=list, alias='CHANNELS_IDS')
    folder_names: list[str] = Field(default_factory=list, alias='FOLDER_NAMES')
    downloads_folder: str = Field(..., alias='DOWNLOADS_FOLDER')

    @field_validator('channel_ids', mode='before')
    @classmethod
    def split_channel_ids(cls, v: str) -> list[int]:
        if isinstance(v, str):
            return [int(i.strip()) for i in v.split(',') if i.strip().isdigit()]
        return []

    @field_validator('folder_names', mode='before')
    @classmethod
    def split_folder_names(cls, v: str) -> list[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(',') if i.strip()]
        return []

    model_config = SettingsConfigDict(env_file=f'{mode}.env', extra='ignore', enable_decoding=False)

    @property
    def full_download_folder(self):
        return f'{os.getcwd()}/{self.downloads_folder}'


class GigachatSettings(BaseServiceSettings):
    api_key: str = Field(..., alias='GIGACHAT_API_KEY')


class Settings(BaseServiceSettings):
    db: DBSettings = DBSettings()
    userbot: UserbotSettings = UserbotSettings()
    gigachat: GigachatSettings = GigachatSettings()


settings = Settings()

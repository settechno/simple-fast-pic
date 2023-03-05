import os

from pydantic import BaseSettings
from webdav3.client import Client
from simplekv.fs import FilesystemStore


class Config(BaseSettings):
    webdav_user: str
    webdav_password: str
    webdav_base_dir: str
    webdav_host: str
    url_prefix: str
    site_name: str
    site_title: str
    access_token: str
    tg_bot_link: str
    tg_bot_token: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


cfg = Config()

# construct webdav client
client = Client({
    'webdav_hostname': cfg.webdav_host,
    'webdav_login': cfg.webdav_user,
    'webdav_password': cfg.webdav_password,
})


store = FilesystemStore(os.path.join(os.path.dirname(__file__), '..', 'data'))
from dataclasses import dataclass

from environs import Env

'''
    При необходимости конфиг базы данных или других сторонних сервисов
'''


@dataclass
class tg_bot:
    token: str
    admin_ids: list[int]


@dataclass
class DB:
    dns: str


@dataclass
class Freekassa:
    api_key: str


@dataclass
class Oxa:
    api_key: str


@dataclass
class CryptoBot:
    token: str


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class UserBot:
    api_id: int
    api_hash: str


@dataclass
class Config:
    bot: tg_bot
    db: DB
    nats: NatsConfig
    freekassa: Freekassa
    oxa: Oxa
    crypto_bot: CryptoBot
    user_bot: UserBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=tg_bot(
            token=env('token'),
            admin_ids=list(map(int, env.list('admins')))
            ),
        db=DB(
            dns=env('dns')
        ),
        nats=NatsConfig(
            servers=env.list('nats')
        ),
        freekassa=Freekassa(
            api_key=env('freekassa_api_key')
        ),
        oxa=Oxa(
            api_key=env('oxa_api_key')
        ),
        crypto_bot=CryptoBot(
            token=env('cb_token')
        ),
        user_bot=UserBot(
            api_id=int(env('api_id')),
            api_hash=env('api_hash')
        )
    )

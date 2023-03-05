from datetime import datetime
import uuid

from .config import client, cfg, store


def check_dir(dir_path: str) -> None:
    """ Проверка структуры директорий и их создание в случае необходимости

    :param dir_path: Путь н.р. asd/2020/01/01/dsa
    """
    if client.check(dir_path):
        return

    p = ''

    for s in dir_path.split('/'):
        p += f'{s}/'

        if not client.check(p):
            client.mkdir(p)


def upload_file(file_data, file_extension: str) -> str:
    """ Загрузка файла на webdav
    Название файла будет сгенерировано автоматически с помощью UUID что бы имена не пересекались

    :param file_data:       Содержимое файла
    :param file_extension:  Расширение файла
    :return:                Путь к файлу на webdav
    """
    date = datetime.now().strftime("%Y/%m/%d")
    dir_path = f'{cfg.webdav_base_dir}/{date}'

    check_dir(dir_path)

    file_name = str(uuid.uuid4()) + '.' + file_extension
    file_path = dir_path + '/' + file_name

    client.upload_to(file_data, file_path)

    return f'{cfg.url_prefix}/{date}/{file_name}'


def add_user(user_id: int) -> None:
    store.put(f'tg_user_id_{user_id}', b'1')


def check_user(user_id: int) -> bool:
    return True if f'tg_user_id_{user_id}' in store.keys() else False

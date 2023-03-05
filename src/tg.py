from filetype import image_match
from telebot import TeleBot
from jinja2 import Environment, FileSystemLoader

from .config import cfg
from .functions import upload_file, check_user, add_user

bot = TeleBot(cfg.tg_bot_token, use_class_middlewares=True)
template_environment = Environment(loader=FileSystemLoader("templates/"))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    template = template_environment.get_template("tg_start.html")
    content = template.render(
        site_title=cfg.site_title,
        site_name=cfg.site_name
    )

    bot.send_message(message.from_user.id, content)


@bot.message_handler(content_types=['photo'])
def upload(message):
    if check_user(message.from_user.id) is False:
        bot.send_message(message.from_user.id, f'Для работы со мной отправьте сначала токен доступа')
        return

    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        image = bot.download_file(file_info.file_path)

        kind = image_match(image)
        if kind is None:
            raise 'Загружаемый файл не является изображением!'

        bot.send_message(message.from_user.id, f'Обрабатываю изображение, пожалуйста подождите ...')

        file_path = cfg.site_name + '/' + upload_file(image, kind.extension)
        bot.send_message(message.from_user.id, f'Изображение успешно загружено. Ссылка на изображение: {file_path}')
    except Exception as e:
        bot.send_message(message.from_user.id, f'При загрузке изображения произошла ошибка: {str(e)}')


@bot.message_handler(content_types=['text'])
def other(message):
    user_checked = check_user(message.from_user.id)

    if user_checked is False:
        if message.text == cfg.access_token:
            bot.send_message(message.from_user.id, 'Отлично! Теперь Вы можете отправлять мне изображения!')
            add_user(message.from_user.id)
        else:
            bot.send_message(message.from_user.id, 'Вам необходимо отправить мне валидный токен доступа! Попробуйте ещё раз.')
        return

    bot.send_message(message.from_user.id, 'Мне не нужно отправлять сообщения :-), лучше пришлите мне изображение')


def run():
    bot.infinity_polling()


if __name__ == '__main__':
    run()

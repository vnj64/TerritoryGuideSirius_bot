from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, ContentType
from sqlalchemy.orm import state
from db import global_init, Users, create_session


def get_link(start, end):
    end_x = end.split(',')[0]
    end_y = end.split(',')[1]
    start_x = start.split(',')[0]
    start_y = start.split(',')[1]
    return f"https://yandex.ru/maps/239/sochi/?ll=39.966608%2C43.406553&mode=routes&rtext={start_x}%2C{start_y}~{end_x}%2C{end_y}"
TOKEN = '1714559341:AAFlFqqj9J-CmkELNFDbOUC5D7ohoMtBIHA'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

s = {'object': [
    {
        'name': 'Олимпийский стадион «Фишт»',
        'inf': 'Олимпийский стадион «Фишт» — стадион в посёлке Сириус. Построен в 2013 году к XXII зимним Олимпийским играм в Сочи. Расположен в Адлере, в Олимпийском парке. Домашняя арена футбольного клуба «Сочи»',
        'cor': '43.4027405,39.9555359',
        'photo': 'https://stadions.org/wp-content/uploads/2019/08/11458851-1024x759.jpg',
        'callback': 'stadium_fisht'
    }, {
        'name': 'Сочи Парк',
        'inf': 'Сочи Парк — тематический парк развлечений в городе Сочи. Расположен в Адлерском районе, на территории Имеретинской низменности',
        'cor': '43.4045792,39.9640923',
        'photo': 'https://www.yuga.ru/media/82/b3/dji_0898__rxbz257.jpg',
        'callback': 'sochi_park'
    },
    {
        'name': 'ПАРК НАУКИ И ИСКУССТВА «СИРИУС»',
        'inf': 'В 2014 году Сочи стал столицей Зимних Олимпийских игр. Мы получили в наследство новый город с мощной развитой инфраструктурой и великолепными возможностями. Экскурсии по Олимпийскому парку знакомят вас с историей развития Имеретинской низменности, созданием инфраструктуры парка, использованием его во время проведения Игр и дальнейшим освоением олимпийского наследия в рамках стратегического развития и проекта реновации Олимпийского парка',
        'cor': '43.414516,39.950750',
        'photo': 'https://biletovmir.ru/sites/default/files/venues/combat/130--1584549219.jpg',
        'callback': 'park_nauki'
    }, {
        'name': 'Кампус Сириуса',
        'inf': 'Проект Университетского кампуса рождается в рамках реновации существующего здания Главного медиацентра и северо-западной части Олимпийского парка, интегрируя эти две территории через новое двухуровневое пространство парка университета. Идея архитектора — органично соединить современную архитектуру с природой, искусственным водоемом и парком. На фасадах и в интерьерных решениях активно применяются натуральное дерево и вертикальное озеленение, особенно в зонах тактильной доступности. Пешеходный променад и эксплуатируемые стилобатные уровни корпусов студенческого городка создают искусственный рельеф парковой зоны, а светопрозрачные конструкции фасадов зданий стирают границу между внутренним и внешним дизайном',
        'cor': '43.40052757454651,39.9647895',
        'photo': 'https://intc-sirius.ru/img/tmp/_tmp-campus-1.jpg',
        'callback': 'park_naukijkkkk'
    }
, {
        'name': 'Лицей «Сириус»',
        'inf': '"Лицей «Сириус» открыл свои двери 1 сентября 2020 года. Мы находимся в городском округе Сириус (Сочи). Лицей объединяет крепкое классическое образование и новейшие образовательные технологии. Особенности обучения — индивидуальный учебный план и свободный выбор образовательной траектории. Занятия проходят в современных классах и лабораториях Центра «Сириус», Парка науки и искусства, на спортивных объектах Олимпийского парка. Образовательная программа объединяет возможности 6 школ: 💥 общеобразовательная 💥 языковая 💥 научно-исследовательская 💥 инженерно-математическая 💥 спортивная 💥 художественно-музыкальная"',
        'cor': '43.404988,39.961421',
        'photo': 'https://static-pano.maps.yandex.ru/v1/?panoid=1312119527_787349056_23_1599211152&size=500%2C240&azimuth=143.3&tilt=10&api_key=maps&signature=YAmujmJEuvdEWFzo4b102zYhTSdExuYQOmEk67ZpQQI=',
        'callback': 'park_naukijkkkssk'
    }
, {
        'name': 'Электрический музей Николы Тесла',
        'inf': 'Электрический Музей Николы Теслы - это захватывающая атмосфера научно-технического прогресса,профессиональные ведущие и каскадёры…Все зрители становятся участниками шоу представления с уникальными экспонатами',
        'cor': '43.406124,39.967518',
        'photo': 'https://lh3.googleusercontent.com/proxy/Nn_z09Usvl5hq2qep8ym0RC5e93AYun1LAk_2rL1tgTPuKo2Jdcl-APFj9VZfejehzUCb985-n7-fD39HNf4ylDmni55W71YA6sRz7qDcYuc',
        'callback': 'park_naukijkkksskd'
    }
, {
        'name': 'Картинг GoKart kids Сочи Парк',
        'inf': 'Картинг Адлер|Олимпийский парк\nЕдинственный электрокартинг в Сочи\n• Взрослый картинг ➡️ @extreme.kart\n• Скидка в день рождения\n• Безопасно\n• от 3х лет',
        'cor': '43.406124,39.967518',
        'photo': 'https://avatars.mds.yandex.net/get-altay/2035926/2a00000174c419285dd185d9a0ae4cb71e05/XXXL',
        'callback': 'park_naukijkkksskdff'
    }
, {
        'name': 'Дворец зимнего спорта Айсберг',
        'inf': 'Дворец зимнего спорта «Айсберг» — один из примечательных спортивных объектов, построенных специально для проведения соревнований в рамках Зимней Олимпиады в Сочи в 2014 г. Дворец — современное спортивное сооружение, вмещающее массу человек: он рассчитан на 12 тыс. зрителей. Его ледовая арена имеет стандартные для такого типа сооружений размеры — 60х30 м, а также включает тренировочный каток для фигурного катания и соревнований по шорт-треку — сравнительно новому для нашей страны виду конькобежного спорта',
        'cor': '43.407416,39.958318',
        'photo': 'https://getpin.ru/etfiles/VisitPointImagesFiles/rUxlz4SWbIa1kl2To2muvs-IMG_4285%20%D0%B0%D0%B9%D1%81%D0%B1%D0%B5%D1%80%D0%B3.jpg',
        'callback': 'park_naukijkkksskdffssssss'
    }
, {
        'name': 'Ледовая арена Шайба',
        'inf': 'Всероссийский детский спортивно-оздоровительный центр в Олимпийском парке города Сочи. Это второй по значимости стадион Олимпиады-2014 в Сочи. Вместимость - 7000 мест. Рядом с ним расположены ледовый дворец «Большой» и тренировочный стадион. Ориентировочная стоимость строительства ледовой арены - 2,5 млрд. рублей',
        'cor': '43.402262,39.952203',
        'photo': 'https://nicko.ru/wp-content/uploads/2018/04/%D0%9B%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D1%8F-%D0%90%D1%80%D0%B5%D0%BD%D0%B0-%D0%A8%D0%B0%D0%B9%D0%B1%D0%B0-.jpg',
        'callback': 'park_naukijkkksskdffssssssasaas'
    }
]
}
markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Отправить свою локацию 🗺', request_location=True)).add(
    KeyboardButton('Я не хочу предостовлять свою локацию 🙅‍♂️'))
main_menu = InlineKeyboardMarkup()
for i in s['object']:
    i_b = InlineKeyboardButton(i['name'], callback_data=i['callback'])
    main_menu.add(i_b)


@dp.message_handler(content_types=ContentType.LOCATION)
async def process_start_command(message: types.Message):
    session = create_session()
    coruser = str(message.location.values['latitude']) + ',' + str(message.location.values['longitude'])
    user = session.query(Users).filter(Users.tg_id == message.chat.id).first()
    if user.sm1 != '-1':
        await bot.delete_message(message.chat.id, int(user.sm1))
        user.sm1 = '-1'
    if user.sm2 != '-1':
        await bot.delete_message(message.chat.id, int(user.sm2))
        user.sm2 = '-1'
    await bot.send_message(message.chat.id, 'Перейдите по ссылке что увидеть маршрут до нужного места 🎯')
    await bot.send_message(message.chat.id, get_link(coruser, user.place))
    await bot.delete_message(message.chat.id, message.message_id)
    a = await bot.send_message(message.chat.id,
                               'Привет 👋\nЭто бот-экскурсовод который будет поможет тебе узнать о достопримичательностях 👍\nВыбери достопремечательность о который ты хочешь узнать из списка ниже 🎯',
                               reply_markup=main_menu)
    user.sm1 = a.message_id
    user.sm2 = '-1'
    session.add(user)
    session.commit()
    session.add(user)
    session.commit()


@dp.callback_query_handler(
    lambda callback_query: callback_query.data and callback_query.data.startswith('posionplace_'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    cor = callback_query.data.split('_')[1]
    # print(cor)

    a = await bot.send_message(callback_query.message.chat.id, 'Необходимо отправить геолокацию 🗺',
                               reply_markup=markup_request)
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == callback_query.message.chat.id).first()
    if user.sm1 != '-1':
        await bot.delete_message(callback_query.message.chat.id, int(user.sm1))
        user.sm1 = '-1'
    user.place = cor
    user.sm1 = '-1'
    user.sm2 = a.message_id
    session.add(user)
    session.commit()


@dp.callback_query_handler(lambda callback_query: callback_query.data and callback_query.data.startswith('main_menu'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id,
                                text=
                                'Привет 👋\nЭто бот-экскурсовод который будет поможет тебе узнать о достопремичательностях 👍\nВыбери достопремечательность о который ты хочешь узнать из списка ниже 🎯',
                                reply_markup=main_menu)


@dp.callback_query_handler()
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in s['object']:
        if i['callback'] == callback_query.data:
            object = i
            break
    keyboard = InlineKeyboardMarkup(row_width=2)
    i_b = InlineKeyboardButton('◀️Назад', callback_data='main_menu')
    keyboard.add(i_b, InlineKeyboardButton('Открыть маршрут 🗺', callback_data=f'posionplace_{object["cor"]}',
                                           request_location=True))
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                text=f"*{object['name']}*\n{object['inf']}[.]({object['photo']})",
                                message_id=callback_query.message.message_id, parse_mode=ParseMode.MARKDOWN,
                                reply_markup=keyboard)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == message.chat.id).first()
    if user == None:
        new_user = Users()
        new_user.sm1 = '-1'
        new_user.tg_id = message.chat.id
        new_user.sm2 = '-1'
        new_user.place = '181'
        session.add(new_user)
        session.commit()
    else:
        if user.sm1 != '-1':
            await bot.delete_message(message.chat.id, int(user.sm1))
            user.sm1 = '-1'
        if user.sm2 != '-1':
            await bot.delete_message(message.chat.id, int(user.sm2))
            user.sm2 = '-1'
        session.add(user)
        session.commit()
    user = session.query(Users).filter(Users.tg_id == message.chat.id).first()
    a = await bot.send_message(message.chat.id,
                               'Привет 👋\nЭто бот-экскурсовод который будет поможет тебе узнать о достопремичательностях 👍\nВыбери достопремечательность о который ты хочешь узнать из списка ниже 🎯',
                               reply_markup=main_menu)
    user.sm1 = a.message_id
    user.place = '181'
    session.add(user)
    session.commit()
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler()
async def just_message(msg: types.Message):
    session = create_session()
    user = session.query(Users).filter(Users.tg_id == msg.chat.id).first()
    await bot.delete_message(msg.chat.id, msg.message_id)
    if user.sm1 != '-1':
        await bot.delete_message(msg.chat.id, int(user.sm1))
        user.sm1 = '-1'
    if user.sm2 != '-1':
        await bot.delete_message(msg.chat.id, int(user.sm2))
        user.sm2 = '-1'
    a = await bot.send_message(msg.chat.id,
                               'Привет 👋\nЭто бот-экскурсовод который будет поможет тебе узнать о достопремичательностях 👍\nВыбери достопремечательность о который ты хочешь узнать из списка ниже 🎯',
                               reply_markup=main_menu)
    user.sm1 = a.message_id
    user.sm2 = '-1'
    session.add(user)
    session.commit()


if __name__ == '__main__':
    global_init("db.sqlite")
    start_polling(dp)

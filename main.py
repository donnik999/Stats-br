import asyncio
import random
import re
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

API_TOKEN = '8124119601:AAEgnFwCalzIKU15uHpIyWlCRbu4wvNEAUw'  # <-- Вставь сюда токен

# ---------------------- Примеры для генерации -------------------------
BIRTHPLACES = ["Арзамас", "Батырево", "Южный", "Егоровка", "Корякино", "Рублевка", "Бусаево", "Нижегородск"]
RESIDENCES = ["Арзамас", "Рублевка", "Бусаево", "Южный", "Егоровка", "Нижегородск", "Батырево"]
APPEARANCES = [
    "Среднего роста, тёмные волосы, голубые глаза.",
    "Высокий, спортивное телосложение, русые волосы.",
    "Худощавый, серые глаза, короткая стрижка.",
    "Миниатюрная, зеленые глаза, длинные волосы.",
    "Голубоглазый брюнет, крепкого телосложения."
]
MATURITY = [
    "В зрелости достиг профессиональных высот и заслужил уважение коллег.",
    "Стал мудрее и спокойнее, теперь ценит простые радости жизни.",
    "Зрелые годы посвятил воспитанию детей и заботе о семье.",
    "Достиг материального благополучия и может позволить себе путешествовать по миру.",
    "В зрелости занялся творчеством, пишет картины и участвует в выставках.",
    "Стал наставником для молодого поколения, делится жизненным опытом.",
    "Посвятил себя благотворительности и помощи нуждающимся.",
    "В зрелые годы начал заниматься спортом для поддержания здоровья.",
    "Зрелость принесла умиротворение и гармонию в душе.",
    "Стал авторитетом в профессиональном сообществе.",
]
YOUTH = [
    "В юности увлекся спортом, участвовал в соревнованиях по футболу и лёгкой атлетике.",
    "Учился в музыкальной школе, играл на гитаре и выступал на концертах.",
    "В школьные годы проявил интерес к наукам, участвовал в олимпиадах по физике.",
    "С юных лет мечтал путешествовать, читал много книг о дальних странах.",
    "Юность прошла в активной социальной жизни, организовывал городские мероприятия.",
    "Участвовал в театральном кружке, играл главные роли на школьной сцене.",
    "В юности занимался волонтерством, помогал пожилым людям.",
    "Много времени проводил с друзьями, вместе катались на велосипедах по окрестностям.",
    "Юные годы запомнились первой любовью и долгими прогулками по парку.",
    "Уже в 16 лет устроился на первую подработку, чтобы помочь семье.",
]
TRAITS = [
    "Спокойный и рассудительный.",
    "Активный, любит помогать другим.",
    "Целеустремленный, упрямый.",
    "Открытый, доброжелательный.",
    "Вспыльчивый, но отходчивый."
]
HOBBIES = [
    "Футбол, рыбалка, чтение книг.",
    "Рисование, путешествия, музыка.",
    "Велоспорт, готовка, программирование.",
    "Коллекционирование марок, водный спорт.",
    "Шахматы, кулинария, туризм."
]
CHILDHOOD = [
    "Детство прошло в небольшом городке, где часто гулял во дворе и играл с друзьями.",
    "С ранних лет увлекался техникой, помогал отцу в гараже и чинил старые приборы.",
    "Любил читать книги и играть в шахматы с бабушкой долгими вечерами.",
    "Рос в большой семье, всегда был окружен заботой и поддержкой.",
    "Детство провёл в деревне, где помогал родителям по хозяйству и пас скот.",
    "С самого детства проявлял лидерские качества, организовывал дворовые игры.",
    "Детство было беззаботным, много времени проводил на реке и в лесу.",
    "С детства мечтал стать врачом, часто играл с игрушечным набором доктора.",
    "Любил рисовать и участвовал в школьных конкурсах рисунка.",
    "Детство было скромным, но наполненным семейным счастьем.",
]
ADULTHOOD = [
    "После окончания университета устроился работать по специальности и быстро сделал карьеру.",
    "Переехал в крупный город, где нашёл своё призвание в новой профессии.",
    "Открыл собственное дело, которое приносит радость и стабильный доход.",
    "Создал крепкую семью, стал заботливым мужем и отцом.",
    "Работал в разных компаниях, набирался опыта и заводил полезные знакомства.",
    "Посвятил себя научной деятельности, опубликовал несколько научных работ.",
    "Занялся общественной деятельностью, был избран в местный совет.",
    "Взрослая жизнь насыщена путешествиями и новыми открытиями.",
    "Стал наставником для молодых специалистов, всегда готов поделиться опытом.",
    "Взрослая жизнь принесла испытания, которые помогли стать сильнее.",
]
NOW = [
    "В настоящее время работает в крупной компании и занимается саморазвитием.",
    "Продолжает учиться новому и осваивать современные технологии.",
    "Счастлив в браке, воспитывает детей и проводит много времени с семьёй.",
    "Занимается любимым делом и помогает друзьям реализовать их идеи.",
    "Путешествует по разным странам и изучает новые культуры.",
    "Ведёт здоровый образ жизни, занимается спортом и правильно питается.",
    "Пишет книгу о своих жизненных приключениях.",
    "Сейчас строит дом своей мечты и обустраивает уютный сад.",
    "Работает на руководящей должности и учит команду работать слаженно.",
    "Участвует в общественных проектах и помогает развитию города.",
]
DOB_SAMPLE = ["05.04.1995", "12.06.1998", "23.01.1987", "10.10.2000"]

# ---------------------- Список серверов -------------------------------
ALL_SERVERS = [
    "RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "PURPLE", "LIME", "PINK", "CHERRY", "BLACK",
    "INDIGO", "WHITE", "MAGENTA", "CRIMSON", "GOLD", "AZURE", "PLATINUM", "AQUA", "GRAY", "ICE",
    "CHILLI", "CHOCO", "MOSCOW", "SPB", "UFA", "SOCHI", "KAZAN", "SAMARA", "ROSTOV", "ANAPA",
    "EKB", "KRASNODAR", "ARZAMAS", "NOVOSIB", "GROZNY", "SARATOV", "OMSK", "IRKUTSK", "VOLGOGRAD", "VORONEZH",
    "BELGOROD", "MAKHACHKALA", "VLADIKAVKAZ", "VLADIVOSTOK", "KALININGRAD", "CHELYABINSK", "KRASNOYARSK",
    "CHEBOKSARY", "KHABAROVSK", "PERM", "TULA", "RYAZAN", "MURMANSK", "PENZA", "KURSK", "ARCHANGELSK",
    "ORENBURG", "KIROV", "KEMEROVO", "TYUMEN", "TOLYATI", "IVANOVO", "STAVROPOL", "SMOLENSK", "PSKOV",
    "BRYANSK", "OREL", "YAROSLAVL", "BARNAUL", "LIPETSK", "ULYANOVSK", "YAKUTSK", "TAMBOV", "BRATSK",
    "ASTRACHAN", "CHITA", "KOSTROMA", "VLADIMIR", "KALUGA", "NOVGOROD", "TAGANROG", "VOLOGDA", "TVER",
    "TOMSK", "IZHEVSK", "SURGUT", "PODOLSK", "MAGADAN", "CHEREPOVETS"
]

# ---------------------- Шаблоны для серверов --------------------------
BIO_TEMPLATES = {
    "RED": '''Основная информация:
Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Хобби: {hobby}

Биография гражданина:
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
''',
    "GREEN": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Описание внешности: {appearance}
Черты характера: {traits}
Хобби: {hobby}
Детство: {childhood}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
''',
    "BLUE": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Семья: {family}
Место рождения: {birthplace}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "YELLOW": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "ORANGE": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
''',
    "PURPLE": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Хобби: {hobby}
Детство: {childhood}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
''',
    "LIME": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "PINK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Семья: {family}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "CHERRY": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "BLACK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "INDIGO": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "WHITE": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "MAGENTA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "CRIMSON": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "GOLD": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "AZURE": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "PLATINUM": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "AQUA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "GRAY": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''',
    "ICE": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность и взрослая жизнь: {youth_adult}
Настоящее время: {now}
Хобби: {hobby}
''', 
    "CHILLI": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "CHOCO": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Семейное положение: {family}
Дети: {children}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Зрелость: {maturity}
Наши дни: {now}
''',
    "MOSCOW": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "SPB": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "UFA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Семейное положение: {family}
Дети: {children}
Внешность: {appearance}
Особенности характера: {traits}
Плохие привычки: {bad_habits}
Детство: {childhood}
Юность: {youth}
Взросление: {adulthood}
Зрелость: {maturity}
Наши дни: {now}
''',
    "SOCHI": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "KAZAN": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "SAMARA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "ROSTOV": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Семейное положение: {family}
Дети: {children}
Внешность: {appearance}
Особенности характера: {traits}
Плохие привычки: {bad_habits}
Детство: {childhood}
Юность: {youth}
Взросление: {adulthood}
Зрелость: {maturity}
Наши дни: {now}
''',
    "ANAPA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Семейное положение: {family}
Дети: {children}
Внешность: {appearance}
Особенности характера: {traits}
Плохие привычки: {bad_habits}
Детство: {childhood}
Юность: {youth}
Взросление: {adulthood}
Зрелость: {maturity}
Наши дни: {now}
''',
    "EKB": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "KRASNODAR": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата рождения: {dob}
Семья: {family}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Жизнь в детстве и юности: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "ARZAMAS": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "NOVOSIB": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "GROZNY": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "SARATOV": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "OMSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "IRKUTSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Семейное положение: {family}
Дети: {children}
Внешность: {appearance}
Особенности характера: {traits}
Плохие привычки: {bad_habits}
Детство: {childhood}
Юность: {youth}
Взросление: {adulthood}
Зрелость: {maturity}
Наши дни: {now}
''',
    "VOLGOGRAD": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''', 
    "VORONEZH": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "BELGOROD": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата рождения: {dob}
Семья: {family}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "MAKHACHKALA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата рождения: {dob}
Семья: {family}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "VLADIKAVKAZ": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "VLADIVOSTOK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Внешность: {appearance}
Качества личности и особенности характера: {traits}
Место проживания: {residence}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "KALININGRAD": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата рождения: {dob}
Семья: {family}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "CHELYABINSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Семейное положение: {family}
Дети: {children}
Внешность: {appearance}
Особенности характера: {traits}
Плохие привычки: {bad_habits}
Детство: {childhood}
Юность: {youth}
Взросление: {adulthood}
Зрелость: {maturity}
Наши дни: {now}
''',
    "KRASNOYARSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "CHEBOKSARY": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "KHABAROVSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "PERM": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Образование: {education}
Отношение к воинской службе: {army}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Ваше фото: {photo}
Детство: {childhood}
Юность: {youth}
Настоящее время: {now}
Семейное положение: {marital}
Имеется ли судимость: {criminal}
Ваше хобби: {hobby}
''',
    "TULA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Дата рождения: {dob}
Национальность: {nationality}
Место рождения и проживания: {birthplace_residence}
Семья: {family}
Описание внешности: {appearance}
Особенности характера: {traits}
Хобби: {hobby}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
''',
    "RYAZAN": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Дата рождения: {dob}
Национальность: {nationality}
Семья: {family}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "MURMANSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Дата рождения: {dob}
Пол: {gender}
Место рождения: {birthplace}
Характер: {traits}
Плохие привычки: {bad_habits}
Образование: {education}
Занятость: {job}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
Внешность: {appearance}
''',
    "PENZA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Дата и место рождения: {dob_place}
Сведения о родителях: {parents}
Образование: {education}
Рост: {height}
Вес: {weight}
Характер: {traits}
Период воинской службы: {army}
Трудовая деятельность: {job}
Семейное положение: {marital}
Информация о хобби: {hobby}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
''',
    "KURSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "ARCHANGELSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "ORENBURG": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Место рождения: {birthplace}
Место проживания: {residence}
Семейное положение: {family}
Дети: {children}
Внешность: {appearance}
Особенности характера: {traits}
Плохие привычки: {bad_habits}
Детство: {childhood}
Юность: {youth}
Взросление: {adulthood}
Зрелость: {maturity}
Наши дни: {now}
''',
    "KIROV": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "KEMEROVO": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Дата рождения: {dob}
Национальность: {nationality}
Семья: {family}
Описание внешности: {appearance}
Описание характера: {traits}
Место проживания: {residence}
Образование: {education}
Детство и юность: {childhood}
Взрослая жизнь: {adulthood}
Хобби: {hobby}
''',
    "TYUMEN": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "TOLYATI": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Описание внешности: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "IVANOVO": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "STAVROPOL": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "SMOLENSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "PSKOV": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "BRYANSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "OREL": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "YAROSLAVL": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "BARNAUL": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "LIPETSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "ULYANOVSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "YAKUTSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "TAMBOV": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "BRATSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "ASTRACHAN": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "CHITA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "KOSTROMA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "VLADIMIR": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "KALUGA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "NOVGOROD": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "TAGANROG": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "VOLOGDA": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "TVER": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "TOMSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "IZHEVSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "SURGUT": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "PODOLSK": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "MAGADAN": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
''',
    "CHEREPOVETS": '''Имя: {name}
Фамилия: {surname}
Возраст: {age}
Пол: {gender}
Национальность: {nationality}
Дата и место рождения: {dob_place}
Семья: {family}
Место проживания: {residence}
Внешность: {appearance}
Особенности характера: {traits}
Детство: {childhood}
Юность: {youth}
Взрослая жизнь: {adulthood}
Настоящее время: {now}
Хобби: {hobby}
'''
}

# --------------------- Пользовательские поля --------------------------
USER_FIELDS = ["name", "surname", "age", "gender", "nationality"]

def gen_field(field, data):
    if field == "birthplace":
        return random.choice(BIRTHPLACES)
    if field == "residence":
        return random.choice(RESIDENCES)
    if field == "appearance":
        return random.choice(APPEARANCES)
    if field == "traits":
        return random.choice(TRAITS)
    if field == "hobby":
        return random.choice(HOBBIES)
    if field == "childhood":
        return random.choice(CHILDHOOD)
    if field == "adulthood":
        return random.choice(ADULTHOOD)
    if field == "now":
        return random.choice(NOW)
    if field == "dob":
        return random.choice(DOB_SAMPLE)
    if field == "dob_place":
        return f"{random.choice(DOB_SAMPLE)}, {random.choice(BIRTHPLACES)}"
    if field == "family":
        return "Женат, двое детей."
    if field == "education":
        return "Высшее техническое."
    if field == "youth_adult":
        return f"{random.choice(CHILDHOOD)} {random.choice(ADULTHOOD)}"
    if field == "children":
        return str(random.randint(0, 3))
    if field == "bad_habits":
        return random.choice(["Не курит", "Курит редко", "Не имеет"])
    if field == "parents":
        return "Отец — Иван, мать — Мария"
    if field == "maturity":
        return random.choice(["Работает", "На пенсии", "Ведет бизнес"])
    if field == "marital":
        return random.choice(["Женат", "Холост", "В разводе"])
    if field == "height":
        return f"{random.randint(160, 200)} см"
    if field == "weight":
        return f"{random.randint(50, 120)} кг"
    if field == "eyes":
        return random.choice(["Голубые", "Карие", "Зеленые", "Серые"])
    if field == "hair":
        return random.choice(["Русые", "Темные", "Светлые", "Рыжие"])
    if field == "army":
        return random.choice(["Служил", "Не служил"])
    if field == "photo":
        return "—"
    if field == "job":
        return random.choice(["Инженер", "Врач", "Учитель", "Менеджер"])
    if field == "criminal":
        return random.choice(["Нет", "Да, условно"])
    if field == "birthplace_residence":
        return f"{random.choice(BIRTHPLACES)} / {random.choice(RESIDENCES)}"
    return "—"

def generate_bio(server, data):
    template = BIO_TEMPLATES.get(server)
    if not template:
        return "Для выбранного сервера пока не задан шаблон."
    fields = set(re.findall(r"\{(\w+)\}", template))
    for field in fields:
        if field not in data:
            data[field] = gen_field(field, data)
    try:
        return template.format(**data)
    except Exception:
        return "Ошибка генерации! Не все поля заполнены корректно."

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()
user_states = {}

def start_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Старт")]],
        resize_keyboard=True
    )

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Написать РП биографию")],
            [KeyboardButton(text="📬 Связь с автором")]
        ],
        resize_keyboard=True
    )

def servers_menu():
    buttons = []
    for i in range(0, len(ALL_SERVERS), 2):
        row = []
        for srv in ALL_SERVERS[i:i+2]:
            row.append(InlineKeyboardButton(text=srv, callback_data=f"server_{srv}"))
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_states.pop(message.from_user.id, None)
    text = (
        "👋 <b>Добро пожаловать в RP Bio Бот!</b>\n\n"
        "Этот бот поможет тебе быстро и красиво сгенерировать РП-биографию персонажа для любого сервера!\n\n"
        "📖 Просто нажми <b>Старт</b> и следуй инструкциям!"
    )
    await message.answer(text, reply_markup=start_menu())

@router.message(F.text.lower() == "старт")
async def go_to_main(message: Message):
    user_states.pop(message.from_user.id, None)
    await message.answer(
        "Выбери действие ниже:",
        reply_markup=main_menu()
    )

@router.message(F.text == "📝 Написать РП биографию")
async def write_bio(message: Message):
    user_states[message.from_user.id] = {"step": "choose_server"}
    await message.answer(
        "🌐 <b>Выбери сервер для своей биографии:</b>",
        reply_markup=servers_menu()
    )

@router.callback_query(F.data.startswith("server_"))
async def handle_server_choice(call: CallbackQuery):
    server = call.data.replace("server_", "")
    user_states[call.from_user.id] = {
        "step": "collect_user_fields",
        "server": server,
        "data": {},
        "user_field_idx": 0
    }
    await ask_user_field(call.message, call.from_user.id)
    await call.answer()

async def ask_user_field(message, user_id):
    idx = user_states[user_id]["user_field_idx"]
    if idx < len(USER_FIELDS):
        field = USER_FIELDS[idx]
        rus = {
            "name": "Имя",
            "surname": "Фамилия",
            "age": "Возраст",
            "gender": "Пол",
            "nationality": "Национальность"
        }[field]
        await message.answer(f"Введите <b>{rus}</b>:")
        user_states[user_id]["current_user_field"] = field
    else:
        state = user_states[user_id]
        server = state["server"]
        data = state["data"]
        bio = generate_bio(server, data)
        await message.answer(bio, reply_markup=main_menu())
        user_states.pop(user_id, None)

@router.message(lambda m: user_states.get(m.from_user.id, {}).get("step") == "collect_user_fields")
async def collect_user_field(message: Message):
    user_id = message.from_user.id
    state = user_states[user_id]
    field = state["current_user_field"]
    state["data"][field] = message.text.strip()
    state["user_field_idx"] += 1
    await ask_user_field(message, user_id)

@router.message(F.text == "📬 Связь с автором")
async def contact_author(message: Message):
    text = (
        "💬 <b>Обратная связь с автором</b>\n\n"
        "Есть вопросы, идеи или предложения? Пиши в Telegram: "
        "<a href='https://t.me/bunkoc'>@bunkoc</a>\n\n"
        "🌟 Автор всегда рад новым знакомствам и идеям! "
        "Возможно, именно твоя мысль сделает бота ещё круче 🚀"
    )
    await message.answer(text, disable_web_page_preview=True)

@router.message()
async def fallback(message: Message):
    if not user_states.get(message.from_user.id):
        await message.answer(
            "Для начала работы нажми кнопку <b>Старт</b> 👇",
            reply_markup=start_menu()
        )
    else:
        await message.answer(
            "Пожалуйста, выбери действие из меню ⬇️",
            reply_markup=main_menu()
        )

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

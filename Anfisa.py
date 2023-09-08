import datetime as dt
import requests

DATABASE = {
    'Sergey': 'Paris',
    'Sonya': 'London',
    'Alexey': 'Berlin',
    'Misha': 'Madrid',
    'Dima': 'Rome',
    'Alina': 'Amsterdam',
    'Egor': 'Athens',
    'Kolya': 'Stockholm',
    'Artem': 'Vienna',
    'Petya': 'Dublin'
}

UTC_OFFSET = {
    'Paris': 2,
    'London': 1,
    'Berlin': 2,
    'Madrid': 2,
    'Rome': 2,
    'Amsterdam': 2,
    'Athens': 3,
    'Stockholm': 2,
    'Vienna': 2,
    'Dublin': 1
}


def format_friend_count(count_friends):
    if count_friends == 1:
        return '1 friend'
    elif 2 <= count_friends <= 4:
        return f'{count_friends} friends'
    else:
        return f'{count_friends} friends'


def what_time(city):
    offset = UTC_OFFSET[city]
    city_time = dt.datetime.utcnow() + dt.timedelta(hours=offset)
    f_time = city_time.strftime("%H:%M")
    return f_time


def what_weather(city):
    url = f'http://wttr.in/{city}'
    weather_parameters = {
        'format': 2,
        'M': ''
    }
    try:
        response = requests.get(url, params=weather_parameters)
    except requests.ConnectionError:
        return '<network error>'
    if response.status_code == 200:
        return response.text
    else:
        return '<weather server error>'


def process_anfisa(query):
    if query == 'how many friends do I have?':
        count = len(DATABASE)
        return f'You have {format_friend_count(count)}.'
    elif query == 'who are all my friends?':
        friends_string = ', '.join(DATABASE)
        return f'Your friends are: {friends_string}'
    elif query == 'where are all my friends?':
        unique_cities = set(DATABASE.values())
        cities_string = ', '.join(unique_cities)
        return f'Your friends are in cities: {cities_string}'
    else:
        return '<unknown query>'


def process_friend(name, query):
    if name in DATABASE:
        city = DATABASE[name]
        if query == 'where are you?':
            return f'{name} is in {city}'
        elif query == 'what time is it?':
            if city not in UTC_OFFSET:
                return f'<cannot determine time in {city}>'
            time = what_time(city)
            return f'It is currently {time} there'
        elif query == 'how is the weather?':
            return what_weather(city)
        else:
            return '<unknown query>'
    else:
        return f'You don\'t have a friend named {name}'


def process_query(query):
    elements = query.split(', ')
    if elements[0] == 'Anfisa':
        return process_anfisa(elements[1])
    else:
        return process_friend(elements[0], elements[1])


def runner():
    queries = [
        'Anfisa, how many friends do I have?',
        'Anfisa, who are all my friends?',
        'Anfisa, where are all my friends?',
        'Anfisa, who is to blame?',
        'Kolya, where are you?',
        'Sonya, what should I do?',
        'Anton, where are you?',
        'Alexey, what time is it?',
        'Artem, what time is it?',
        'Anton, what time is it?',
        'Petya, what time is it?',
        'Kolya, how is the weather?',
        'Sonya, how is the weather?',
        'Anton, how is the weather?'
    ]
    for query in queries:
        print(query, '-', process_query(query))



runner()
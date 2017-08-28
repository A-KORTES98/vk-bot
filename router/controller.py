from handlers.weather import getWeather
from handlers.schedule import getSchedle

def redirectToHandler(msg):
    msg = msg.lower()
    if msg.find('weather') is not -1:
        print('weather')
        return getWeather(msg.lower().replace('weather', '').strip(' '))
    if msg.find('schedule') is not -1:
        print('schedule')
        return getSchedle()
    return 'Command not found! Nigga'
